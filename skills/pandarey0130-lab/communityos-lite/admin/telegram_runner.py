#!/usr/bin/env python3
"""
CommunityOS Lite - Telegram Bot Runner
轮询接收 Telegram 消息并分发给 Bot 引擎
"""
import os
import json
import time
import requests
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

DATA_DIR = BASE_DIR / "admin" / "data"


def load_json(name, default=dict):
    path = DATA_DIR / f"{name}.json"
    if not path.exists():
        return default()
    with open(path) as f:
        return json.load(f)


class TelegramRunner:
    def __init__(self):
        # 每个 bot token 独立 offset（Telegram 要求）
        self.offset_by_token: dict[str, int] = {}
        self.running = True

    def _resolve_token(self, bot: dict) -> str:
        token = bot.get("bot_token", "") or ""
        if not token or token.startswith("TELEGRAM_BOT_TOKEN"):
            env_key = f"{bot.get('bot_id', 'BOT').upper()}_TOKEN"
            token = os.environ.get(env_key, "") or os.environ.get("TELEGRAM_BOT_TOKEN", "")
        return (token or "").strip()

    def get_updates(self, token: str, offset: int, timeout: int = 30):
        """获取 Telegram 更新"""
        url = f"https://api.telegram.org/bot{token}/getUpdates"
        params = {"offset": offset, "timeout": timeout}
        try:
            resp = requests.get(url, params=params, timeout=timeout + 5)
            data = resp.json()
            if data.get("ok"):
                return data.get("result", [])
            print(f"getUpdates not ok: {data.get('description', data)}")
        except Exception as e:
            print(f"Error getting updates: {e}")
        return []

    def process_update(self, update: dict, bot: dict, token: str):
        """处理单条更新（update 必须来自该 token 对应 bot 的长轮询）"""
        if "message" not in update:
            return

        msg = update["message"]
        chat = msg.get("chat", {})
        chat_type = chat.get("type", "")
        chat_id = chat.get("id")
        text = (msg.get("text") or "").strip()
        from_user = msg.get("from") or {}
        user_id = from_user.get("id")
        message_id = msg.get("message_id")

        if from_user.get("is_bot"):
            return

        if not bot.get("enabled", True):
            return

        if chat_type == "private":
            if not bot.get("allow_pm", True):
                return
            if not text:
                return
            context = {
                "is_private_chat": True,
                "user_id": user_id,
                "chat_id": chat_id,
                "message_id": message_id,
            }
            response = self.generate_response(bot, text, context)
            if response:
                self.send_message(token, chat_id, response)
            return

        if chat_type in ("group", "supergroup"):
            if not bot.get("modes", {}).get("passive_qa", True):
                return
            if not text:
                return
            context = {
                "is_private_chat": False,
                "user_id": user_id,
                "chat_id": chat_id,
                "message_id": message_id,
            }
            response = self.generate_response(bot, text, context)
            if response:
                self.send_message(token, chat_id, response)

    def generate_response(self, bot, text, context):
        """生成回复"""
        from bot_engine.llm import LLMFactory

        soul = bot.get("soul", "You are a helpful AI assistant.")
        knowledge_text = bot.get("knowledge", {}).get("text", "")

        prompt = text
        if knowledge_text:
            prompt = (
                f"【知识库】\n{knowledge_text}\n\n【问题】\n{text}\n\n请根据知识库回答问题。"
            )

        messages = []
        if soul:
            messages.append({"role": "system", "content": soul})
        messages.append({"role": "user", "content": prompt})

        try:
            llm_config = load_json("llm_config", {})
            minimax_key = os.environ.get("MINIMAX_API_KEY", "")
            if minimax_key and len(minimax_key) > 10:
                llm_config["api_key"] = minimax_key
            if not llm_config.get("api_key"):
                return "⚠️ LLM API Key 未配置，请在 Lite 后台「LLM 配置」中填写。"

            llm = LLMFactory.create(llm_config)
            response = llm.chat(messages)
            return (response or "").strip() or None
        except Exception as e:
            print(f"LLM error: {e}")
            return "抱歉，我现在无法回答这个问题。"

    def send_message(self, token, chat_id, text):
        """发送消息（不使用 Markdown，避免特殊字符导致发送失败）"""
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        body = {"chat_id": chat_id, "text": text[:4096]}
        try:
            resp = requests.post(url, json=body, timeout=10)
            data = resp.json()
            if not data.get("ok"):
                print(f"sendMessage failed: {data}")
        except Exception as e:
            print(f"Error sending message: {e}")

    def run(self):
        """主循环"""
        print("🤖 CommunityOS Telegram Runner started")

        while self.running:
            bots = load_json("bots", {"bots": []}).get("bots", [])
            enabled_bots = [b for b in bots if b.get("enabled")]
            if not enabled_bots:
                time.sleep(5)
                continue

            valid = [(b, self._resolve_token(b)) for b in enabled_bots]
            valid = [(b, t) for b, t in valid if t]
            if not valid:
                print("No bot token configured; waiting...")
                time.sleep(5)
                continue

            got_any = False
            for idx, (bot, token) in enumerate(valid):
                off = self.offset_by_token.get(token, 0)
                timeout = 25 if idx == 0 else 0
                updates = self.get_updates(token, off, timeout=timeout)
                for update in updates:
                    got_any = True
                    self.offset_by_token[token] = update.get("update_id", 0) + 1
                    self.process_update(update, bot, token)

            if not got_any:
                time.sleep(1)


if __name__ == "__main__":
    runner = TelegramRunner()
    runner.run()
