#!/usr/bin/env python3
"""
QWeather China - 基于中国气象局数据的完整天气服务
和风天气API封装，提供实时天气、预报、生活指数等功能
跨平台兼容版本，自动处理编码问题
"""

import os
import json
import time
import jwt
import requests
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

# 导入编码处理工具
from encoding_utils import safe_print, setup_encoding

def load_config():
    """从config.json加载配置"""
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        
        qweather_config = config_data.get("qweather", {})
        jwt_config = qweather_config.get("jwt", {})
        cache_config = qweather_config.get("cache", {})
        
        return {
            "kid": jwt_config.get("kid", "YOUR_CREDENTIALS_ID_HERE"),
            "sub": jwt_config.get("sub", "YOUR_PROJECT_ID_HERE"),
            "api_host": qweather_config.get("api_host", "YOUR_API_HOST_HERE.re.qweatherapi.com"),
            "private_key_path": jwt_config.get("private_key_path", "PATH_TO_YOUR_PRIVATE_KEY.pem"),
            "cache_dir": cache_config.get("directory", "~/.cache/qweather"),
            "cache_ttl": cache_config.get("ttl", {
                "now": 600,
                "forecast": 3600,
                "indices": 10800,
                "air": 1800,
            })
        }
    except Exception as e:
        safe_print(f"⚠️ 加载配置文件失败: {e}")
        safe_print("使用默认配置，请确保config.json文件存在且格式正确")
        return {
            "kid": "YOUR_CREDENTIALS_ID_HERE",
            "sub": "YOUR_PROJECT_ID_HERE",
            "api_host": "YOUR_API_HOST_HERE.re.qweatherapi.com",
            "private_key_path": "PATH_TO_YOUR_PRIVATE_KEY.pem",
            "cache_dir": "~/.cache/qweather",
            "cache_ttl": {
                "now": 600,
                "forecast": 3600,
                "indices": 10800,
                "air": 1800,
            }
        }

def load_city_codes():
    """从config.json加载城市代码"""
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        
        qweather_config = config_data.get("qweather", {})
        cities = qweather_config.get("cities", {})
        
        if cities:
            return cities
        else:
            # 默认城市代码
            return {
                "beijing": "101010100",
                "shanghai": "101020100",
                "guangzhou": "101280101",
                "shenzhen": "101280601",
                "hangzhou": "101210101",
                "chengdu": "101270101",
                "wuhan": "101200101",
                "nanjing": "101190101",
                "xian": "101110101",
                "chongqing": "101040100",
            }
    except Exception as e:
        safe_print(f"⚠️ 加载城市代码失败: {e}")
        # 返回默认城市代码
        return {
            "beijing": "101010100",
            "shanghai": "101020100",
            "guangzhou": "101280101",
            "shenzhen": "101280601",
            "hangzhou": "101210101",
            "chengdu": "101270101",
            "wuhan": "101200101",
            "nanjing": "101190101",
            "xian": "101110101",
            "chongqing": "101040100",
        }

# 加载配置
CONFIG = load_config()
CITY_CODES = load_city_codes()

@dataclass
class WeatherNow:
    """实时天气数据"""
    obs_time: str
    temp: int
    feels_like: int
    text: str
    icon: str
    wind_speed: int
    wind_scale: str
    wind_dir: str
    humidity: int
    precip: float
    pressure: int
    vis: int
    cloud: int
    dew: int
    
    def format(self) -> str:
        """格式化显示"""
        return f"""
🌤️ 实时天气 ({self.obs_time})
🌡️ 温度: {self.temp}°C (体感: {self.feels_like}°C)
🌬️ 风力: {self.wind_scale}级 ({self.wind_speed}km/h) {self.wind_dir}
💧 湿度: {self.humidity}%
🌧️ 降水: {self.precip}mm
📊 气压: {self.pressure}hPa
👁️ 能见度: {self.vis}公里
☁️ 云量: {self.cloud}%
🌡️ 露点: {self.dew}°C
"""

@dataclass
class DailyForecast:
    """每日预报"""
    fx_date: str
    sunrise: str
    sunset: str
    temp_max: int
    temp_min: int
    text_day: str
    text_night: str
    icon_day: str
    icon_night: str
    wind_scale_day: str
    wind_dir_day: str
    precip: float
    humidity: int
    uv_index: str
    
    def format(self) -> str:
        """格式化显示"""
        return f"""
📅 {self.fx_date}
🌅 日出: {self.sunrise} | 🌇 日落: {self.sunset}
🌡️ 温度: {self.temp_min}°C ~ {self.temp_max}°C
☀️ 白天: {self.text_day}
🌙 夜间: {self.text_night}
🌬️ 风力: {self.wind_scale_day}级 {self.wind_dir_day}
🌧️ 降水: {self.precip}mm
💧 湿度: {self.humidity}%
☀️ 紫外线: {self.uv_index}
"""

@dataclass
class LifeIndex:
    """生活指数"""
    name: str
    category: str
    level: str
    text: str
    
    def format(self) -> str:
        """格式化显示"""
        level_emoji = {
            "1": "👍",  # 很适宜
            "2": "✅",  # 适宜
            "3": "⚠️",  # 较适宜
            "4": "❌",  # 不适宜
            "5": "🚫",  # 极不适宜
        }
        emoji = level_emoji.get(self.level, "📊")
        return f"{emoji} {self.name}: {self.text}"

class QWeatherClient:
    """和风天气API客户端"""
    
    def __init__(self):
        self.config = CONFIG
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "QWeather-OpenClaw/1.2.0"
        })
        
    def _get_jwt_token(self) -> str:
        """生成JWT token"""
        try:
            # 读取私钥
            with open(self.config["private_key_path"], "r") as f:
                private_key_pem = f.read()
            
            private_key = serialization.load_pem_private_key(
                private_key_pem.encode(),
                password=None,
                backend=default_backend()
            )
            
            # 生成JWT
            payload = {
                "iss": "qweather",
                "sub": self.config["sub"],
                "exp": int(time.time()) + 1800,  # 30分钟过期
                "iat": int(time.time()),
            }
            
            token = jwt.encode(
                payload,
                private_key,
                algorithm="EdDSA",
                headers={"kid": self.config["kid"]}
            )
            
            return token
            
        except Exception as e:
            safe_print(f"❌ 生成JWT token失败: {e}")
            raise
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """发送API请求"""
        try:
            token = self._get_jwt_token()
            
            url = f"https://{self.config['api_host']}{endpoint}"
            headers = {
                "Authorization": f"Bearer {token}"
            }
            
            response = self.session.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            safe_print(f"❌ API请求失败: {e}")
            raise
        except json.JSONDecodeError as e:
            safe_print(f"❌ JSON解析失败: {e}")
            raise
    
    def get_weather_now(self, city: str) -> WeatherNow:
        """获取实时天气"""
        city_code = CITY_CODES.get(city.lower(), city)
        
        data = self._make_request("/v7/weather/now", {
            "location": city_code
        })
        
        now = data["now"]
        return WeatherNow(
            obs_time=now["obsTime"],
            temp=int(now["temp"]),
            feels_like=int(now["feelsLike"]),
            text=now["text"],
            icon=now["icon"],
            wind_speed=int(now["windSpeed"]),
            wind_scale=now["windScale"],
            wind_dir=now["windDir"],
            humidity=int(now["humidity"]),
            precip=float(now["precip"]),
            pressure=int(now["pressure"]),
            vis=int(now["vis"]),
            cloud=int(now["cloud"]),
            dew=int(now["dew"])
        )
    
    def get_weather_forecast(self, city: str, days: int = 3) -> List[DailyForecast]:
        """获取天气预报"""
        city_code = CITY_CODES.get(city.lower(), city)
        
        endpoint = "/v7/weather/7d" if days > 3 else "/v7/weather/3d"
        data = self._make_request(endpoint, {
            "location": city_code
        })
        
        forecasts = []
        for item in data["daily"][:days]:
            forecasts.append(DailyForecast(
                fx_date=item["fxDate"],
                sunrise=item["sunrise"],
                sunset=item["sunset"],
                temp_max=int(item["tempMax"]),
                temp_min=int(item["tempMin"]),
                text_day=item["textDay"],
                text_night=item["textNight"],
                icon_day=item["iconDay"],
                icon_night=item["iconNight"],
                wind_scale_day=item["windScaleDay"],
                wind_dir_day=item["windDirDay"],
                precip=float(item["precip"]),
                humidity=int(item["humidity"]),
                uv_index=item["uvIndex"]
            ))
        
        return forecasts
    
    def get_life_indices(self, city: str) -> List[LifeIndex]:
        """获取生活指数"""
        city_code = CITY_CODES.get(city.lower(), city)
        
        data = self._make_request("/v7/indices/1d", {
            "location": city_code,
            "type": "0"  # 全部类型
        })
        
        indices = []
        for item in data["daily"]:
            indices.append(LifeIndex(
                name=item["name"],
                category=item["category"],
                level=item["level"],
                text=item["text"]
            ))
        
        return indices
    
    def get_air_quality(self, city: str) -> Dict:
        """获取空气质量"""
        city_code = CITY_CODES.get(city.lower(), city)
        
        data = self._make_request("/v7/air/now", {
            "location": city_code
        })
        
        return data
    
    def get_umbrella_advice(self, precip: float, weather_text: str) -> str:
        """获取雨伞建议"""
        if precip > 0.5 or "雨" in weather_text:
            return "建议带伞 🌂"
        elif precip > 0.1:
            return "可能下雨，建议带伞 ⚠️"
        else:
            return "不需要带伞 ☀️"
    
    def get_dressing_advice(self, temperature: int) -> str:
        """获取穿衣建议"""
        if temperature >= 28:
            return "天气炎热，建议穿短袖、短裤 🩳"
        elif temperature >= 23:
            return "天气温暖，建议穿长袖T恤、薄外套 👕"
        elif temperature >= 18:
            return "天气舒适，建议穿长袖、薄外套 🧥"
        elif temperature >= 10:
            return "天气凉爽，建议穿毛衣、外套 🧶"
        else:
            return "天气寒冷，建议穿羽绒服、厚外套 🧣"

def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description="和风天气查询工具")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # now 命令
    now_parser = subparsers.add_parser("now", help="查询实时天气")
    now_parser.add_argument("--city", required=True, help="城市名称或代码")
    
    # forecast 命令
    forecast_parser = subparsers.add_parser("forecast", help="查询天气预报")
    forecast_parser.add_argument("--city", required=True, help="城市名称或代码")
    forecast_parser.add_argument("--days", type=int, default=3, help="预报天数 (1-7)")
    
    # indices 命令
    indices_parser = subparsers.add_parser("indices", help="查询生活指数")
    indices_parser.add_argument("--city", required=True, help="城市名称或代码")
    
    # air 命令
    air_parser = subparsers.add_parser("air", help="查询空气质量")
    air_parser.add_argument("--city", required=True, help="城市名称或代码")
    
    args = parser.parse_args()
    
    # 初始化编码
    setup_encoding()
    
    client = QWeatherClient()
    
    try:
        if args.command == "now":
            weather = client.get_weather_now(args.city)
            safe_print(weather.format())
            
        elif args.command == "forecast":
            if args.days < 1 or args.days > 7:
                safe_print("❌ 预报天数必须在1-7之间")
                return
            
            forecasts = client.get_weather_forecast(args.city, args.days)
            for forecast in forecasts:
                safe_print(forecast.format())
                
        elif args.command == "indices":
            indices = client.get_life_indices(args.city)
            
            # 按类别分组
            categories = {}
            for index in indices:
                if index.category not in categories:
                    categories[index.category] = []
                categories[index.category].append(index)
            
            for category, cat_indices in categories.items():
                safe_print(f"\n{category}:")
                for index in cat_indices[:5]:  # 每个类别显示前5个
                    safe_print(f"  {index.format()}")
                    
        elif args.command == "air":
            air_data = client.get_air_quality(args.city)
            now = air_data["now"]
            
            safe_print(f"""
🌫️ 空气质量
更新时间: {air_data['updateTime']}
AQI指数: {now['aqi']} ({now['category']})
主要污染物: {now['primary']}
PM2.5: {now['pm2p5']} μg/m³
PM10: {now['pm10']} μg/m³
二氧化硫: {now['so2']} μg/m³
二氧化氮: {now['no2']} μg/m³
臭氧: {now['o3']} μg/m³
一氧化碳: {now['co']} mg/m³
""")
            
        else:
            parser.print_help()
            
    except Exception as e:
        safe_print(f"❌ 查询失败: {e}")
        safe_print("请检查:")
        safe_print("1. config.json 配置文件是否正确")
        safe_print("2. 网络连接是否正常")
        safe_print("3. API认证信息是否有效")

if __name__ == "__main__":
    main()