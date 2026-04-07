"""
Bot Instance - 单个Bot实例
"""
import os
import re
import time
from typing import Dict, Any, Optional, List
from pathlib import Path


class BotConfig:
    """Bot配置"""
    def __init__(self, config: dict):
        self.config = config
        self.bot_id = config.get("bot_id", "")
        self.name = config.get("name", self.bot_id)
        self.avatar = config.get("avatar", "🤖")
        self.soul = config.get("soul", "")
        self.modes = config.get("modes", {})
        self.knowledge = config.get("knowledge", {})
        self.allow_pm = config.get("allow_pm", True)
        self.enabled = config.get("enabled", True)


class BotInstance:
    """单个Bot实例"""

    def __init__(self, config: dict):
        self.config = BotConfig(config)
        self.active_modes = self.config.modes
        self._llm_client = None

    def should_respond(self, message: str, is_new_member: bool = False) -> bool:
        """判断是否应该响应"""
        if not self.config.enabled:
            return False
        
        if is_new_member:
            return self.config.modes.get("welcome", False)
        
        if self.config.modes.get("passive_qa"):
            return bool(message.strip())
        
        return False

    def generate_response(self, message: str, context: Dict[str, Any] = None) -> str:
        """生成响应"""
        context = context or {}

        # 检查私聊权限
        if context.get("is_private_chat") and not self.config.allow_pm:
            return ""

        # 欢迎新成员
        if context.get("is_new_member"):
            return self._generate_welcome(context.get("member_name", ""))

        # 被动问答
        if self.config.modes.get("passive_qa") and message.strip():
            return self._answer_with_knowledge(message)

        return ""

    def _answer_with_knowledge(self, query: str) -> str:
        """基于知识库回答"""
        knowledge_text = self.config.knowledge.get("text", "")
        
        if knowledge_text:
            prompt = f"【知识库】\n{knowledge_text}\n\n【问题】\n{query}\n\n请根据知识库回答问题。"
        else:
            prompt = query
        
        return self._llm_generate(query, knowledge_text)

    def _llm_generate(self, query: str, context: str = "") -> str:
        """调用LLM生成回答"""
        from bot_engine.llm import LLMFactory
        
        soul = self.config.soul or "你是一个有用的助手。"
        
        if context:
            prompt = f"【知识库】\n{context}\n\n【问题】\n{query}\n\n请根据知识库回答问题。"
        else:
            prompt = query
        
        try:
            # 加载全局LLM配置
            from pathlib import Path
            data_dir = Path(__file__).parent.parent / "admin" / "data"
            import json
            
            llm_config_path = data_dir / "llm_config.json"
            if llm_config_path.exists():
                with open(llm_config_path) as f:
                    llm_config = json.load(f)
            else:
                llm_config = {"provider": "minimax", "model": "MiniMax-2.7"}
            
            # API Key
            api_key = os.environ.get("MINIMAX_API_KEY", "")
            if not api_key:
                api_key = os.environ.get("OPENAI_API_KEY", "")
            llm_config["api_key"] = api_key
            
            if not api_key:
                return "⚠️ LLM API Key 未配置，请在 LLM 配置页面设置"
            
            llm = LLMFactory.create(llm_config)
            response = llm.chat(prompt, system=soul)
            return response
        except Exception as e:
            return f"抱歉，我现在无法回答这个问题。"

    def _generate_welcome(self, member_name: str) -> str:
        """生成欢迎消息"""
        template = self.config.knowledge.get("welcome_template", "欢迎 {name} 加入群聊！")
        return template.replace("{name}", member_name)
