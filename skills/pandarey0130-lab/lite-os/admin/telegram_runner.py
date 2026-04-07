#!/usr/bin/env python3
"""
CommunityOS Lite - Telegram Bot Runner
轮询接收 Telegram 消息并分发给 Bot 引擎
"""
import os
import json
import time
import asyncio
import requests
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "admin" / "data"

def load_json(name, default=dict):
    path = DATA_DIR / f"{name}.json"
    if not path.exists():
        return default()
    with open(path) as f:
        return json.load(f)

class TelegramRunner:
    def __init__(self):
        self.offset = 0
        self.running = True
    
    def get_updates(self, token, timeout=30):
        """获取 Telegram 更新"""
        url = f"https://api.telegram.org/bot{token}/getUpdates"
        params = {"offset": self.offset, "timeout": timeout}
        try:
            resp = requests.get(url, params=params, timeout=timeout + 5)
            data = resp.json()
            if data.get("ok"):
                return data.get("result", [])
        except Exception as e:
            print(f"Error getting updates: {e}")
        return []
    
    def process_update(self, update, bots):
        """处理单条更新"""
        # 私聊消息
        if "message" in update:
            msg = update["message"]
            chat = msg.get("chat", {})
            chat_type = chat.get("type", "")
            chat_id = chat.get("id")
            text = msg.get("text", "")
            from_user = msg.get("from", {})
            user_id = from_user.get("id")
            message_id = msg.get("message_id")
            
            # 私聊
            if chat_type == "private":
                for bot in bots:
                    if not bot.get("enabled", True):
                        continue
                    allow_pm = bot.get("allow_pm", True)
                    if not allow_pm:
                        continue
                    
                    token = bot.get("bot_token", "")
                    if not token or token.startswith("TELEGRAM_BOT_TOKEN"):
                        # 尝试从环境变量获取
                        env_key = f"{bot['bot_id'].upper()}_TOKEN"
                        token = os.environ.get(env_key, "")
                        if not token:
                            token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
                    
                    if not token:
                        continue
                    
                    # 获取 bot 名称
                    try:
                        me_resp = requests.get(f"https://api.telegram.org/bot{token}/getMe", timeout=10)
                        bot_username = me_resp.json().get("result", {}).get("username", "")
                    except:
                        bot_username = bot.get("bot_id", "")
                    
                    # 只处理发送给该 bot 的消息
                    entities = msg.get("entities", [])
                    is_bot_command = any(e.get("type") == "bot_command" for e in entities)
                    
                    # 构建上下文
                    context = {
                        "is_private_chat": True,
                        "user_id": user_id,
                        "chat_id": chat_id,
                        "message_id": message_id,
                    }
                    
                    # 调用 bot 处理
                    response = self.generate_response(bot, text, context)
                    if response:
                        self.send_message(token, chat_id, response)
                    return  # 只处理第一个匹配的 bot
    
    def generate_response(self, bot, text, context):
        """生成回复"""
        from bot_engine.llm import LLMFactory
        
        soul = bot.get("soul", "You are a helpful AI assistant.")
        knowledge_text = bot.get("knowledge", {}).get("text", "")
        
        # 构建 prompt
        prompt = text
        if knowledge_text:
            prompt = f"【知识库】\n{knowledge_text}\n\n【问题】\n{text}\n\n请根据知识库回答问题。"
        
        try:
            # 加载全局 LLM 配置
            llm_config = load_json("llm_config", {})
            llm_config["api_key"] = os.environ.get("MINIMAX_API_KEY", "")
            
            llm = LLMFactory.create(llm_config)
            response = llm.chat(prompt, system=soul)
            return response
        except Exception as e:
            print(f"LLM error: {e}")
            return "抱歉，我现在无法回答这个问题。"
    
    def send_message(self, token, chat_id, text):
        """发送消息"""
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }
        try:
            requests.post(url, json=data, timeout=10)
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
            
            updates = self.get_updates(enabled_bots[0].get("bot_token", ""))
            
            for update in updates:
                self.offset = update.get("update_id", 0) + 1
                self.process_update(update, enabled_bots)
            
            if not updates:
                time.sleep(1)

if __name__ == "__main__":
    runner = TelegramRunner()
    runner.run()
