---
name: imou-device-operate
description: >
  Imou/乐橙设备操控。支持云台转动（上下左右等）、设备画面抓图及下载。
  Control account devices: PTZ movement, device snapshot capture and download.
  Use when: 乐橙云台控制、设备抓图、下载设备图片、PTZ control、snapshot、capture image、download device picture、Imou device operate.
metadata:
  {
    "openclaw":
      {
        "emoji": "🎮",
        "requires": { "env": ["IMOU_APP_ID", "IMOU_APP_SECRET"], "pip": ["requests"] },
        "primaryEnv": "IMOU_APP_ID",
        "install":
          [
            { "id": "python-requests", "kind": "pip", "package": "requests", "label": "Install requests" }
          ]
      }
  }
---

# Imou Device Operate

Control Imou cloud devices: PTZ (pan-tilt-zoom) movement, device snapshot capture, and download snapshot image by URL.

## Quick Start

Install dependency:
```bash
pip install requests
```

Set environment variables (required):
```bash
export IMOU_APP_ID="your_app_id"
export IMOU_APP_SECRET="your_app_secret"
export IMOU_BASE_URL="your_base_url"
```

**API Base URL (IMOU_BASE_URL)** (required; no default—must be set explicitly):
- **Mainland China**: Register a developer account at [open.imou.com](https://open.imou.com) and use the base URL below. Get `appId` and `appSecret` from [App Information](https://open.imou.com/consoleNew/myApp/appInfo).
- **Overseas**: Register a developer account at [open.imoulife.com](https://open.imoulife.com) and use the base URL for your data center (view in [Console - Basic Information - My Information](https://open.imoulife.com/consoleNew/basicInfo/myInfo)). Get `appId` and `appSecret` from [App Information](https://open.imoulife.com/consoleNew/myApp/appInfo). See [Development Specification](https://open.imoulife.com/book/http/develop.html).

| Region         | Data Center     | Base URL |
|----------------|-----------------|----------|
| Mainland China | —               | `https://openapi.lechange.cn` |
| Overseas       | East Asia       | `https://openapi-sg.easy4ip.com:443` |
| Overseas       | Central Europe  | `https://openapi-fk.easy4ip.com:443` |
| Overseas       | Western America | `https://openapi-or.easy4ip.com:443` |

Run:
```bash
# Device snapshot (returns downloadable URL; optional save to file)
python3 {baseDir}/scripts/device_operate.py snapshot DEVICE_SERIAL CHANNEL_ID [--save PATH]

# PTZ move (operation: 0-10, duration in ms)
python3 {baseDir}/scripts/device_operate.py ptz DEVICE_SERIAL CHANNEL_ID OPERATION DURATION_MS
```

## Capabilities

1. **Device snapshot**: Call setDeviceSnapEnhanced to get a snapshot URL (valid 2 hours). Optionally download to a local file with `--save`.
2. **PTZ control**: controlMovePTZ with operation (0=up, 1=down, 2=left, 3=right, 4=up-left, 5=down-left, 6=up-right, 7=down-right, 8=zoom in, 9=zoom out, 10=stop) and duration in milliseconds. Device must support PT/PTZ.

## Request Header

All requests to Imou Open API include the header `Client-Type: OpenClaw` for platform identification.

## API References

| API | Doc |
|-----|-----|
| Dev spec | https://open.imou.com/document/pages/c20750/ |
| Get accessToken | https://open.imou.com/document/pages/fef620/ |
| Device snapshot (enhanced) | https://open.imou.com/document/pages/09fe83/ |
| PTZ move control | https://open.imou.com/document/pages/66c489/ |

See `references/imou-operate-api.md` for request/response formats.

## Tips

- **Token**: Fetched automatically per run; valid 3 days.
- **Snapshot**: Request interval should be ≥1s per device; snapshot URL expires in 2 hours.
- **PTZ**: Use operation 10 (stop) to stop movement; duration is in milliseconds.

## Data Outflow

| Data | Sent to | Purpose |
|------|---------|--------|
| appId, appSecret | Imou Open API | Obtain accessToken |
| accessToken, deviceId, channelId, etc. | Imou Open API | Snapshot, PTZ control |

All requests go to the configured `IMOU_BASE_URL`. No other third parties.
