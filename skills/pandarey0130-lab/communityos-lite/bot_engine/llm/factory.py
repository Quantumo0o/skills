"""
LLM Factory - Create LLM instances based on config
"""
import os
import requests


class LLMBase:
    """Base LLM class"""
    
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
    
    def chat(self, messages: list, **kwargs) -> str:
        """Generate chat response"""
        raise NotImplementedError


class MiniMaxLLM(LLMBase):
    """MiniMax LLM Provider"""
    
    API_URL = "https://api.minimaxi.com/v1/text/chatcompletion_v2"
    
    def chat(self, messages: list, **kwargs) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": messages,
            **kwargs
        }
        try:
            resp = requests.post(self.API_URL, headers=headers, json=data, timeout=30)
            resp.raise_for_status()
            result = resp.json()
            return result.get("choices", [{}])[0].get("message", {}).get("content", "")
        except Exception as e:
            print(f"MiniMax API error: {e}")
            return "抱歉，AI服务暂时不可用。"


class OpenAILLM(LLMBase):
    """OpenAI LLM Provider"""
    
    API_URL = "https://api.openai.com/v1/chat/completions"
    
    def chat(self, messages: list, **kwargs) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": messages,
            **kwargs
        }
        try:
            resp = requests.post(self.API_URL, headers=headers, json=data, timeout=30)
            resp.raise_for_status()
            result = resp.json()
            return result.get("choices", [{}])[0].get("message", {}).get("content", "")
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return "抱歉，AI服务暂时不可用。"


class ClaudeLLM(LLMBase):
    """Anthropic Claude LLM Provider"""
    
    API_URL = "https://api.anthropic.com/v1/messages"
    
    def chat(self, messages: list, **kwargs) -> str:
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        # Convert messages format for Claude
        claude_messages = []
        for msg in messages:
            role = "user" if msg.get("role") == "user" else "assistant"
            claude_messages.append({"role": role, "content": msg.get("content", "")})
        
        data = {
            "model": self.model,
            "messages": claude_messages,
            "max_tokens": kwargs.get("max_tokens", 1024)
        }
        try:
            resp = requests.post(self.API_URL, headers=headers, json=data, timeout=30)
            resp.raise_for_status()
            result = resp.json()
            return result.get("content", [{}])[0].get("text", "")
        except Exception as e:
            print(f"Claude API error: {e}")
            return "抱歉，AI服务暂时不可用。"


class DeepSeekLLM(LLMBase):
    """DeepSeek LLM Provider"""
    
    API_URL = "https://api.deepseek.com/v1/chat/completions"
    
    def chat(self, messages: list, **kwargs) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": messages,
            **kwargs
        }
        try:
            resp = requests.post(self.API_URL, headers=headers, json=data, timeout=30)
            resp.raise_for_status()
            result = resp.json()
            return result.get("choices", [{}])[0].get("message", {}).get("content", "")
        except Exception as e:
            print(f"DeepSeek API error: {e}")
            return "抱歉，AI服务暂时不可用。"


class LLMFactory:
    """Factory to create LLM instances"""
    
    PROVIDERS = {
        "minimax": MiniMaxLLM,
        "openai": OpenAILLM,
        "anthropic": ClaudeLLM,
        "claude": ClaudeLLM,
        "deepseek": DeepSeekLLM,
    }
    
    @classmethod
    def create(cls, config: dict) -> LLMBase:
        """Create LLM instance from config"""
        provider = config.get("provider", "minimax").lower()
        model = config.get("model", "MiniMax-M2.7")
        api_key = config.get("api_key_env", "") or config.get("api_key", "") or os.environ.get(f"{provider.upper()}_API_KEY", "")
        
        llm_class = cls.PROVIDERS.get(provider, MiniMaxLLM)
        return llm_class(api_key=api_key, model=model)
