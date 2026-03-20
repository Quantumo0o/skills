---
name: weather
description: "Get current weather and forecasts via wttr.in, Open-Meteo, or WeatherAPI. Use when: user asks about weather, temperature, forecasts, air quality, or UV index for any location. NOT for: historical weather data, severe weather alerts, or detailed meteorological analysis."
homepage: https://wttr.in/:help
metadata: { "openclaw": { "emoji": "☔", "requires": { "bins": ["curl", "jq"] } } }
---

# Weather Skill

Get current weather conditions, forecasts, air quality, and UV index.

## When to Use

✅ **USE this skill when:**

- "What's the weather?"
- "Will it rain today/tomorrow?"
- "Temperature in [city]"
- "Weather forecast for the week"
- "Air quality in [city]"
- "UV index"
- Travel planning weather checks

## When NOT to Use

❌ **DON'T use this skill when:**

- Historical weather data → use weather archives/APIs
- Climate analysis or trends → use specialized data sources
- Hyper-local microclimate data → use local sensors
- Severe weather alerts → check official NWS sources
- Aviation/marine weather → use specialized services (METAR, etc.)

## API Keys

WeatherAPI key is stored in `TOOLS.md` under "WeatherAPI" section.

## Location

Always include a city, region, or airport code in weather queries.

---

## WeatherAPI (推荐 - 功能最全)

API Key 从环境变量 `WEATHERAPI_KEY` 或 TOOLS.md 获取。

### Current Weather + Air Quality

```bash
# 完整实况 + 空气质量
curl -s "https://api.weatherapi.com/v1/current.json?key=${WEATHERAPI_KEY}&q=Shanghai&aqi=yes" | jq '{
  location: .location.name,
  temp: .current.temp_c,
  feels_like: .current.feelslike_c,
  condition: .current.condition.text,
  humidity: .current.humidity,
  wind: "\(.current.wind_kph) km/h \(.current.wind_dir)",
  pm25: .current.air_quality.pm2_5,
  pm10: .current.air_quality.pm10,
  uv: .current.uv
}'
```

### 3-Day Forecast

```bash
curl -s "https://api.weatherapi.com/v1/forecast.json?key=${WEATHERAPI_KEY}&q=Shanghai&days=3&aqi=yes" | jq '.forecast.forecastday[] | {date: .date, max: .day.maxtemp_c, min: .day.mintemp_c, condition: .day.condition.text, rain_chance: .day.daily_chance_of_rain}'
```

### Astronomy (日出日落)

```bash
curl -s "https://api.weatherapi.com/v1/astronomy.json?key=${WEATHERAPI_KEY}&q=Shanghai" | jq '.astronomy.astro | {sunrise, sunset, moon_phase}'
```

### Quick One-Liner

```bash
# 简洁输出
curl -s "https://api.weatherapi.com/v1/current.json?key=${WEATHERAPI_KEY}&q=Shanghai" | jq '"\(.location.name): \(.current.temp_c)°C, \(.current.condition.text), feels like \(.current.feelslike_c)°C"'
```

---

## wttr.in (无需 API Key)

### Current Weather

```bash
# One-line summary
curl "wttr.in/London?format=3"

# Detailed current conditions
curl "wttr.in/London?0"

# Specific city
curl "wttr.in/New+York?format=3"
```

### Forecasts

```bash
# 3-day forecast
curl "wttr.in/London"

# Week forecast
curl "wttr.in/London?format=v2"

# Specific day (0=today, 1=tomorrow, 2=day after)
curl "wttr.in/London?1"
```

### Format Options

```bash
# One-liner
curl "wttr.in/London?format=%l:+%c+%t+%w"

# JSON output
curl "wttr.in/London?format=j1"

# PNG image
curl "wttr.in/London.png"
```

### Format Codes

- `%c` — Weather condition emoji
- `%t` — Temperature
- `%f` — "Feels like"
- `%w` — Wind
- `%h` — Humidity
- `%p` — Precipitation
- `%l` — Location

---

## Quick Responses

**"What's the weather?" (用 WeatherAPI)**

```bash
curl -s "https://api.weatherapi.com/v1/current.json?key=${WEATHERAPI_KEY}&q=Shanghai&aqi=yes" | jq '"\(.location.name): \(.current.temp_c)°C \(.current.condition.text) (体感 \(.current.feelslike_c)°C), 湿度 \(.current.humidity)%, \(.current.wind_kph)km/h \(.current.wind_dir)风, PM2.5: \(.current.air_quality.pm2_5 | floor)"'
```

**"Air quality?"**

```bash
curl -s "https://api.weatherapi.com/v1/current.json?key=${WEATHERAPI_KEY}&q=Shanghai&aqi=yes" | jq '.current.air_quality | {pm25: .pm2_5, pm10: .pm10, o3: .o3, us_epa_index: ."us-epa-index"}'
```

**"Will it rain?"**

```bash
curl -s "wttr.in/Shanghai?format=%l:+%c+%p"
```

**"Weekend forecast"**

```bash
curl "wttr.in/Shanghai?format=v2"
```

---

## Output Format (严格遵守)

```
[城市]天气 [日期]

🌡️ 温度：最低 ~ 最高
🌬️ 风力：风向 风级
☁️ 天况：晴/多云/雨
💧 湿度：百分比
🌫️ 空气质量：PM2.5 数值 (等级)

🌅 日出：HH:MM
🌇 日落：HH:MM
✨ 早晨 Golden Hour：HH:MM - HH:MM
✨ 傍晚 Golden Hour：HH:MM - HH:MM
💙 早晨 Blue Hour：HH:MM - HH:MM
💙 傍晚 Blue Hour：HH:MM - HH:MM

📊 对比昨日：（可选）
• 变化点

⚠️ 提醒：（可选）
• 注意事项
```

---

## Sunrise-Sunset API (天文数据)

免费、无需 API key：https://sunrise-sunset.org

```bash
# 获取天文数据（含 golden/blue hour）
curl -s "https://api.sunrise-sunset.org/json?lat=39.9289&lng=116.3883&date=2026-03-20&formatted=0" | jq -r '.results |
  "🌅 日出: " + (.sunrise | split("+")[0] + "Z" | fromdateiso8601 + 28800 | strftime("%H:%M")) +
  "\n🌇 日落: " + (.sunset | split("+")[0] + "Z" | fromdateiso8601 + 28800 | strftime("%H:%M")) +
  "\n✨ 早晨 Golden Hour: " + (.civil_twilight_begin | split("+")[0] + "Z" | fromdateiso8601 + 28800 | strftime("%H:%M")) + " - " + (.sunrise | split("+")[0] + "Z" | fromdateiso8601 + 28800 | strftime("%H:%M")) +
  "\n✨ 傍晚 Golden Hour: " + (.sunset | split("+")[0] + "Z" | fromdateiso8601 + 28800 | strftime("%H:%M")) + " - " + (.civil_twilight_end | split("+")[0] + "Z" | fromdateiso8601 + 28800 | strftime("%H:%M")) +
  "\n💙 早晨 Blue Hour: " + (.nautical_twilight_begin | split("+")[0] + "Z" | fromdateiso8601 + 28800 | strftime("%H:%M")) + " - " + (.civil_twilight_begin | split("+")[0] + "Z" | fromdateiso8601 + 28800 | strftime("%H:%M")) +
  "\n💙 傍晚 Blue Hour: " + (.civil_twilight_end | split("+")[0] + "Z" | fromdateiso8601 + 28800 | strftime("%H:%M")) + " - " + (.nautical_twilight_end | split("+")[0] + "Z" | fromdateiso8601 + 28800 | strftime("%H:%M"))'
```

**北京坐标**：lat=39.9289, lng=116.3883
**时区偏移**：+28800 秒 (UTC+8)

---

## Notes

- **WeatherAPI**: 1,000,000 次/月额度，支持空气质量、UV、天文数据
- **wttr.in**: 无需 API key，适合快速查询
- Rate limited; don't spam requests
- Works for most global cities
- Supports airport codes: `curl wttr.in/ORD`
