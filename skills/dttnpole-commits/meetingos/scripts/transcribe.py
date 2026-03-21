"""
MeetingOS — 转录引擎
支持：本地 Whisper（privacy-first）| OpenAI Whisper API | AssemblyAI
"""
import os
import tempfile
import subprocess
from pathlib import Path

PRIVACY_MODE = os.getenv("MEETINGOS_PRIVACY_MODE", "local")
WHISPER_MODEL = os.getenv("WHISPER_LOCAL_MODEL", "large-v3")

def extract_audio(video_path: str) -> str:
    """使用 ffmpeg 从视频提取音频（WAV 16kHz mono）"""
    out_path = tempfile.mktemp(prefix="meetingos_", suffix=".wav")
    cmd = [
        "ffmpeg", "-i", video_path,
        "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le",
        out_path, "-y", "-loglevel", "error"
    ]
    subprocess.run(cmd, check=True)
    return out_path

def transcribe_local(audio_path: str) -> dict:
    """本地 Whisper 转录（完全隐私）"""
    import whisper
    model = whisper.load_model(WHISPER_MODEL)
    result = model.transcribe(
        audio_path,
        language=None,           # 自动检测
        word_timestamps=True,
        verbose=False
    )
    return result

def transcribe_cloud(audio_path: str) -> dict:
    """OpenAI Whisper API 转录（需网络）"""
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    with open(audio_path, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            response_format="verbose_json",
            timestamp_granularities=["word"]
        )
    return transcript

def transcribe(input_path: str) -> str:
    """主转录入口"""
    suffix = Path(input_path).suffix.lower()
    if suffix in [".mp4", ".mov", ".avi", ".mkv", ".webm"]:
        audio_path = extract_audio(input_path)
        cleanup_needed = True
    else:
        audio_path = input_path
        cleanup_needed = False
    
    try:
        if PRIVACY_MODE == "local":
            result = transcribe_local(audio_path)
        else:
            result = transcribe_cloud(audio_path)
        return result.get("text", "") if isinstance(result, dict) else result.text
    finally:
        if cleanup_needed and os.path.exists(audio_path):
            os.remove(audio_path)

if __name__ == "__main__":
    import sys
    print(transcribe(sys.argv[1]))

from scripts.wecom_helper import send_wecom_message
send_wecom_message(os.getenv("WECom_WEBHOOK_URL"), action_items_markdown)