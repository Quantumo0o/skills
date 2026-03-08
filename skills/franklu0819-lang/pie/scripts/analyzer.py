import os
import re
import httpx
import json

class InsightAnalyzer:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={self.api_key}"

    def clean_content(self, text):
        text = re.sub(r'```json.*?```', '', text, flags=re.DOTALL)
        text = re.sub(r'# (Session|PRD|Identity|USER|AGENTS|SOUL).*?\n', '', text)
        return text.strip()

    def get_insights(self, aggregated_text):
        prompt = f"Analyze these startup session logs and provide EXACTLY 3 strategic insights (decision patterns, pain points, pivots). Format as Markdown.\n\nLOGS:\n{aggregated_text[:60000]}"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        try:
            response = httpx.post(self.url, json=payload, timeout=60.0)
            data = response.json()
            if "candidates" in data:
                return data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                return f"Error: {json.dumps(data)}"
        except Exception as e:
            return f"Exception: {str(e)}"
