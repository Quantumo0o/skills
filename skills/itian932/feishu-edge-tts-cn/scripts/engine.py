#!/usr/bin/env python3
"""
Edge-TTS 语音合成引擎 — 工程级
集成于 feishu-edge-tts skill，供 Agent 直接调用

用法:
    python3 scripts/engine.py --text "你好" --voice xiaoxiao --output /tmp/output.ogg
    python3 scripts/engine.py --text "你好"                       # 默认音色 xiaoxiao, 默认 .ogg

支持的输出格式:
    .ogg  .opus  (libopus, 48kHz, 64kbps, voip)  ← 默认/推荐
    .mp3   (libmp3lame, 64kbps)
    .wav   (pcm_s16le, 48kHz mono)
    .flac  (无损)
    .aac   (aac, 64kbps)

音色 ID 见 config/voices.json
"""

import argparse
import asyncio
import json
import os
import subprocess
import sys
import time
import tempfile
from pathlib import Path
from typing import List, Optional, Tuple

# ===== 路径解析 =====
SKILL_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = SKILL_DIR / "config" / "voices.json"
DEFAULT_OUTPUT_DIR = "/tmp/openclaw"

# ===== 速率控制 =====
# 每 3 秒一个桶，避免超过 Edge-TTS 的 20次/分钟限制
MAX_RPS = 3                    # 每秒最大请求数
_rate_lock_time = 0.0          # 上次请求时间戳

def _acquire_rate_slot():
    """获取速率许可，如果超了就等待"""
    global _rate_lock_time
    now = time.time()
    wait = 1.0 / MAX_RPS - (now - _rate_lock_time)
    if wait > 0:
        time.sleep(wait)
    _rate_lock_time = time.time()

# ===== 加载音色配置 =====
def load_voices():
    """加载 config/voices.json，返回 dict {voice_id: voice_config}
    自动过滤元数据 key（以 _ 或 === 开头）"""
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return {
        k: v for k, v in raw.items()
        if not k.startswith("_") and not k.startswith("=") and isinstance(v, dict)
    }

# ===== 核心引擎 =====
async def synthesize_one(text: str, voice_name: str, rate: str, pitch: str, volume: str, output_path: str, max_retries: int = 3) -> Optional[str]:
    """
    合成单段文本为 MP3，带 429 重试
    
    Returns: output_path 或 None（失败）
    """
    import edge_tts

    for attempt in range(max_retries):
        try:
            _acquire_rate_slot()
            t0 = time.time()

            comm = edge_tts.Communicate(text, voice_name, rate=rate, pitch=pitch, volume=volume)
            comm.save_sync(output_path)

            elapsed = time.time() - t0
            size = os.path.getsize(output_path)
            print(f"  Edge-TTS: {size/1024:.0f}KB, {elapsed:.1f}s", file=sys.stderr)
            return output_path

        except Exception as e:
            err_str = str(e)
            # 429 / Too Many Requests → 指数退避
            if "429" in err_str or "Too Many" in err_str:
                backoff = (2 ** attempt) * 1.0   # 1s → 2s → 4s
                print(f"  ⏳ 429 限速，{backoff:.1f}s 后重试 ({attempt+1}/{max_retries})", file=sys.stderr)
                time.sleep(backoff)
                continue
            else:
                print(f"  ❌ Edge-TTS 错误: {err_str}", file=sys.stderr)
                return None

    print(f"  ❌ 超过最大重试次数 {max_retries}", file=sys.stderr)
    return None

def convert_format(mp3_path: str, output_path: str) -> Optional[str]:
    """MP3 → 目标格式转换（根据扩展名自动选择编码器）"""
    ext = Path(output_path).suffix.lower()

    format_map = {
        ".ogg":  ["-c:a", "libopus", "-b:a", "64k", "-application", "voip"],
        ".mp3":  ["-c:a", "libmp3lame", "-b:a", "64k"],
        ".wav":  ["-c:a", "pcm_s16le"],
        ".flac": ["-c:a", "flac"],
        ".aac":  ["-c:a", "aac", "-b:a", "64k"],
        ".opus": ["-c:a", "libopus", "-b:a", "64k", "-application", "voip"],
    }

    if ext not in format_map:
        # 默认 OGG/Opus
        ext = ".ogg"
        if not output_path.endswith(ext):
            output_path = output_path + ext
        codec_args = format_map[".ogg"]
        print(f"  ⚠️ 不支持的格式 '{Path(output_path).suffix}'，使用默认 OGG/Opus", file=sys.stderr)
    else:
        codec_args = format_map[ext]

    os.makedirs(os.path.dirname(os.path.abspath(output_path)) if os.path.dirname(output_path) else ".", exist_ok=True)

    result = subprocess.run(
        [
            "ffmpeg", "-y", "-i", mp3_path,
            "-ar", "48000", "-ac", "1",
            *codec_args,
            "-loglevel", "error",
            output_path,
        ],
        capture_output=True, text=True
    )

    if result.returncode != 0:
        print(f"  ❌ ffmpeg 错误: {result.stderr}", file=sys.stderr)
        return None

    sz = os.path.getsize(output_path)
    print(f"  ffmpeg: {sz/1024:.0f}KB {ext.upper()}", file=sys.stderr)
    return output_path

def generate(text: str, voice_id: str = "xiaoxiao", output_path: str = None) -> Tuple[int, str]:
    """
    同步入口（Agent 调用的主函数）

    Args:
        text: 要合成的文本内容
        voice_id: 音色 ID（见 config/voices.json）
        output_path: 输出 OGG 路径（默认自动生成在 tmp 目录）

    Returns:
        tuple: (exit_code, output_path)
               exit_code == 0 成功，!= 0 失败
    """
    voices = load_voices()

    if voice_id not in voices:
        print(f"错误: 未知音色 '{voice_id}'", file=sys.stderr)
        print(f"可用音色: {', '.join(voices.keys())}", file=sys.stderr)
        return 1, ""

    voice_config = voices[voice_id]
    engine_voice = voice_config["name"]
    # 官方音色无 rate/pitch/volume，使用默认值
    rate = voice_config.get("rate", "+0%")
    pitch = voice_config.get("pitch", "+0Hz")
    volume = voice_config.get("volume", "+0%")

    if output_path is None:
        ts = int(time.time())
        safe_voice = voice_id.replace(" ", "_")
        output_path = os.path.join(DEFAULT_OUTPUT_DIR, f"edge_{safe_voice}_{ts}.ogg")

    # 直接整段合成（不分段）
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        mp3_path = tmp.name
    try:
        result = asyncio.run(
            synthesize_one(text, engine_voice, rate, pitch, volume, mp3_path)
        )
        if result is None:
            return 1, ""
        ogg = convert_format(mp3_path, output_path)
        if ogg is None:
            return 1, ""
        total_sz = os.path.getsize(ogg)
        print(f"✅ 生成成功: {output_path} ({total_sz/1024:.0f}KB)", file=sys.stderr)
        return 0, output_path
    finally:
        if os.path.exists(mp3_path):
            os.remove(mp3_path)

# ===== CLI =====
def main():
    parser = argparse.ArgumentParser(description="Edge-TTS 语音合成")
    parser.add_argument("--text", "-t", default=None, help="要合成的文本")
    parser.add_argument("--voice", "-v", default="xiaoxiao", help="音色 ID（默认 xiaoxiao）")
    parser.add_argument("--output", "-o", default=None, help="输出路径（默认自动生成）")
    parser.add_argument("--list-voices", action="store_true", help="列出所有可用音色")
    args = parser.parse_args()

    if args.list_voices:
        voices = load_voices()
        print(f"{'音色 ID':<20} {'引擎音色':<30} {'描述'}")
        print("-" * 80)
        for vid, cfg in voices.items():
            print(f"{vid:<20} {cfg['name']:<30} {cfg.get('description', '')}")
        return 0

    text = args.text
    voice_id = args.voice
    output_path = args.output

    code, path = generate(text, voice_id, output_path)
    if code == 0 and path:
        print(path)  # stdout 输出路径供 Agent 捕获
    return code

if __name__ == "__main__":
    sys.exit(main())
