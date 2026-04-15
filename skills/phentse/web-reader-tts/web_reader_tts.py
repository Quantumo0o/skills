#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web Reader TTS - 网页内容朗读工具（混合提取方案）

将网页内容转换为语音，支持多种 TTS 引擎和 Whisper 语音识别。
使用混合提取方案（Trafilatura + Readability + newspaper3k）提升正文识别准确率。

Usage:
    # 完整流程
    python web_reader_tts.py --url "https://example.com"
    
    # 仅生成语音
    python web_reader_tts.py --url "https://example.com" --tts-only
    
    # 仅语音识别
    python web_reader_tts.py --audio "audio.mp3" --stt-only
    
    # 自然语言调用
    # 直接说："朗读网址 https://example.com"
"""

import argparse
import asyncio
import os
import re
import sys
from pathlib import Path
from typing import Optional, Tuple, Dict, Any
from datetime import datetime

# 确保 UTF-8 输出
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')


# 语言到声音的映射
LANGUAGE_VOICE_MAP = {
    'zh': 'zh-CN-XiaoxiaoNeural',  # 中文女声
    'zh-cn': 'zh-CN-XiaoxiaoNeural',
    'zh-tw': 'zh-TW-HsiaoChenNeural',
    'en': 'en-US-JennyNeural',  # 英文女声
    'ja': 'ja-JP-NanamiNeural',  # 日文女声
    'ko': 'ko-KR-SunHiNeural',  # 韩文女声
    'fr': 'fr-FR-DeniseNeural',  # 法文女声
    'de': 'de-DE-KatjaNeural',  # 德文女声
    'es': 'es-ES-ElviraNeural',  # 西班牙文女声
    'ru': 'ru-RU-SvetlanaNeural',  # 俄文女声
}

# 默认声音
DEFAULT_VOICE = 'zh-CN-XiaoxiaoNeural'


def check_dependencies():
    """检查依赖是否安装"""
    missing = []
    
    try:
        import playwright
    except ImportError:
        missing.append('playwright')
    
    try:
        import edge_tts
    except ImportError:
        missing.append('edge-tts')
    
    try:
        import whisper
    except ImportError:
        missing.append('openai-whisper')
    
    try:
        import langdetect
    except ImportError:
        missing.append('langdetect')
    
    try:
        import trafilatura
    except ImportError:
        missing.append('trafilatura')
    
    try:
        from newspaper import Article
    except ImportError:
        missing.append('newspaper3k')
    
    if missing:
        print("❌ 缺少依赖，请安装：")
        print(f"   pip install {' '.join(missing)}")
        if 'playwright' in missing:
            print("   python -m playwright install chromium")
        sys.exit(1)


def detect_language(text: str) -> str:
    """检测文本的主要语言"""
    # 统计中文字符比例
    chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    total_chars = len([c for c in text if c.isalpha() or '\u4e00' <= c <= '\u9fff'])
    
    # 如果中文字符占比超过 20%，则认为是中文
    if total_chars > 0 and chinese_chars / total_chars > 0.2:
        return 'zh'
    
    try:
        from langdetect import detect
        sample = text[:500]
        lang = detect(sample)
        return lang
    except Exception:
        return 'zh'


def get_voice_for_language(language: str) -> str:
    """根据语言获取合适的 TTS 声音"""
    return LANGUAGE_VOICE_MAP.get(language.lower(), DEFAULT_VOICE)


# ============================================================================
# 混合提取方案
# ============================================================================

def extract_with_trafilatura(url: str) -> Optional[Dict[str, Any]]:
    """使用 Trafilatura 提取正文"""
    try:
        import trafilatura
        
        print("  🔍 Trafilatura 提取中...")
        
        # 下载网页
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            return None
        
        # 提取正文
        text = trafilatura.extract(
            downloaded,
            include_comments=False,
            include_tables=True,
            favor_precision=True,  # 偏向精确
            favor_recall=False     # 不偏向召回
        )
        
        if not text:
            return None
        
        # 提取元数据
        metadata = trafilatura.extract_metadata(downloaded)
        
        result = {
            'engine': 'trafilatura',
            'text': text,
            'title': metadata.title if metadata else None,
            'author': metadata.author if metadata else None,
            'date': metadata.date if metadata else None,
            'categories': metadata.categories if metadata else None,
            'tags': metadata.tags if metadata else None,
        }
        
        print(f"    ✅ 提取成功: {len(text)} 字符")
        return result
        
    except Exception as e:
        print(f"    ❌ 失败: {e}")
        return None


def extract_with_readability(url: str) -> Optional[Dict[str, Any]]:
    """使用 Readability.js 提取正文"""
    try:
        from playwright.sync_api import sync_playwright
        
        print("  🔍 Readability.js 提取中...")
        
        # Readability.js 路径
        script_path = Path(__file__).parent / 'Readability.js'
        if not script_path.exists():
            print("    ❌ Readability.js 不存在")
            return None
        
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url, wait_until='domcontentloaded', timeout=60000)
            
            # 注入 Readability.js
            page.add_script_tag(path=str(script_path))
            
            # 提取正文
            result = page.evaluate('''() => {
                try {
                    const article = new Readability(document.cloneNode(true)).parse();
                    if (!article) return null;
                    return {
                        title: article.title,
                        text: article.textContent,
                        excerpt: article.excerpt,
                        byline: article.byline
                    };
                } catch (e) {
                    return null;
                }
            }''')
            
            browser.close()
        
        if not result or not result.get('text'):
            return None
        
        result['engine'] = 'readability'
        result['author'] = result.get('byline')
        
        print(f"    ✅ 提取成功: {len(result['text'])} 字符")
        return result
        
    except Exception as e:
        print(f"    ❌ 失败: {e}")
        return None


def extract_with_newspaper(url: str) -> Optional[Dict[str, Any]]:
    """使用 newspaper3k 提取正文"""
    try:
        from newspaper import Article
        
        print("  🔍 newspaper3k 提取中...")
        
        article = Article(url, language='zh')
        article.download()
        article.parse()
        
        if not article.text:
            return None
        
        # NLP 分析（可选）
        try:
            article.nlp()
        except:
            pass
        
        result = {
            'engine': 'newspaper',
            'text': article.text,
            'title': article.title,
            'authors': article.authors,
            'date': article.publish_date,
            'top_image': article.top_image,
            'keywords': getattr(article, 'keywords', None),
            'summary': getattr(article, 'summary', None),
        }
        
        print(f"    ✅ 提取成功: {len(article.text)} 字符")
        return result
        
    except Exception as e:
        print(f"    ❌ 失败: {e}")
        return None


def score_result(result: Dict[str, Any]) -> float:
    """评估提取结果质量"""
    if not result or not result.get('text'):
        return 0.0
    
    score = 0.0
    text = result['text']
    
    # 1. 长度得分（最多 10 分）
    length_score = min(len(text) / 1000, 10)
    score += length_score
    
    # 2. 标题得分（5 分）
    if result.get('title'):
        score += 5
    
    # 3. 作者得分（3 分）
    if result.get('author') or result.get('authors'):
        score += 3
    
    # 4. 日期得分（2 分）
    if result.get('date'):
        score += 2
    
    # 5. 中文内容得分（最多 5 分）
    chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    if len(text) > 0:
        chinese_ratio = chinese_chars / len(text)
        score += chinese_ratio * 5
    
    # 6. 段落数量得分（最多 3 分）
    paragraphs = [p for p in text.split('\n') if len(p.strip()) > 50]
    score += min(len(paragraphs) / 5, 3)
    
    # 7. 引擎加权（不同引擎有不同权重）
    engine_weights = {
        'trafilatura': 1.1,  # Trafilatura 权重最高
        'readability': 1.0,
        'newspaper': 0.9
    }
    engine = result.get('engine', 'unknown')
    score *= engine_weights.get(engine, 1.0)
    
    return score


def extract_webpage_content(url: str, verbose: bool = True) -> Tuple[str, str, Dict[str, Any]]:
    """
    使用混合方案提取网页内容
    
    Args:
        url: 网页 URL
        verbose: 是否显示详细信息
        
    Returns:
        (title, content, metadata): 标题、内容和元数据
    """
    if verbose:
        print(f"📖 正在获取网页: {url}")
    
    results = {}
    
    # 尝试 Trafilatura（最快，准确率高）
    results['trafilatura'] = extract_with_trafilatura(url)
    
    # 尝试 Readability.js（准确率最高）
    results['readability'] = extract_with_readability(url)
    
    # 尝试 newspaper3k（功能最全）
    results['newspaper'] = extract_with_newspaper(url)
    
    # 评估并选择最佳结果
    scored = []
    for engine, data in results.items():
        if data and data.get('text'):
            score = score_result(data)
            scored.append((engine, data, score))
            if verbose:
                print(f"  📊 {engine} 得分: {score:.1f}")
    
    if not scored:
        print("❌ 所有提取引擎都失败了")
        return "", "", {}
    
    # 选择得分最高的
    best_engine, best_data, best_score = max(scored, key=lambda x: x[2])
    
    if verbose:
        print(f"\n✅ 选择 {best_engine} 引擎（得分: {best_score:.1f}）")
        print(f"   标题: {best_data.get('title', '未知')}")
        print(f"   作者: {best_data.get('author') or best_data.get('authors', '未知')}")
        print(f"   长度: {len(best_data['text'])} 字符")
    
    title = best_data.get('title', '')
    content = best_data['text']
    
    return title, content, best_data


def clean_content(content: str, max_length: int = 10000) -> str:
    """清理内容（混合方案已提取高质量内容，只需简单清理）"""
    
    # 移除多余的空行
    lines = content.split('\n')
    cleaned = []
    
    for line in lines:
        line = line.strip()
        if line:
            cleaned.append(line)
    
    result = '\n\n'.join(cleaned)
    
    # 限制长度
    if len(result) > max_length:
        result = result[:max_length]
        last_period = result.rfind('。')
        if last_period > max_length * 0.8:
            result = result[:last_period + 1]
    
    return result


async def generate_audio_edge_tts(
    text: str,
    voice: Optional[str] = None,
    output: str = 'audio.mp3',
    rate: str = '+0%',
    volume: str = '+0%',
    auto_language: bool = True
) -> Tuple[str, str]:
    """使用 Edge TTS 生成语音"""
    import edge_tts
    
    # 自动检测语言并选择声音
    if auto_language and voice is None:
        language = detect_language(text)
        voice = get_voice_for_language(language)
        print(f"🌐 检测到语言: {language}")
    elif voice is None:
        voice = DEFAULT_VOICE
    
    print(f"\n🎤 正在生成语音...")
    print(f"   声音: {voice}")
    print(f"   语速: {rate}, 音量: {volume}")
    print(f"   文本长度: {len(text)} 字符")
    
    communicate = edge_tts.Communicate(
        text,
        voice,
        rate=rate,
        volume=volume
    )
    await communicate.save(output)
    
    size = os.path.getsize(output)
    print(f"✅ 语音已生成: {output}")
    print(f"   大小: {size / 1024:.2f} KB")
    
    return output, voice


def transcribe_audio_whisper(
    audio_path: str,
    model_name: str = 'medium',
    language: Optional[str] = None
) -> str:
    """使用 Whisper 识别语音"""
    import whisper
    
    print(f"\n🔊 正在加载 Whisper 模型: {model_name}")
    model = whisper.load_model(model_name)
    print(f"✅ 模型加载完成")
    
    print(f"🔊 正在识别语音...")
    
    transcribe_params = {}
    if language:
        transcribe_params['language'] = language
    
    result = model.transcribe(audio_path, **transcribe_params)
    
    text = result['text']
    print(f"✅ 识别完成")
    
    return text


def main():
    parser = argparse.ArgumentParser(
        description='网页内容朗读工具（混合提取方案）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 完整流程
  python web_reader_tts.py --url "https://example.com"
  
  # 仅生成语音
  python web_reader_tts.py --url "https://example.com" --tts-only
  
  # 仅语音识别
  python web_reader_tts.py --audio "audio.mp3" --stt-only

混合提取方案:
  - Trafilatura: 快速准确，适合新闻/博客
  - Readability.js: Mozilla 开源，准确率最高
  - newspaper3k: 功能全面，支持 NLP 分析
  - 自动选择最佳结果（基于质量评分）

可用声音:
  中文女声: zh-CN-XiaoxiaoNeural (推荐), zh-CN-XiaoyiNeural
  中文男声: zh-CN-YunxiNeural, zh-CN-YunyangNeural
  英文女声: en-US-JennyNeural (推荐), en-US-AriaNeural
  日文女声: ja-JP-NanamiNeural

Whisper 模型:
  tiny (39 MB), base (74 MB), small (244 MB), medium (769 MB, 默认), large-v3 (1.55 GB)
        """
    )
    
    # URL 或音频文件
    parser.add_argument('--url', help='网页 URL')
    parser.add_argument('--audio', help='音频文件路径（仅用于 --stt-only）')
    
    # TTS 参数
    parser.add_argument('--voice', default=None, help='TTS 声音（None 则自动检测）')
    parser.add_argument('--rate', default='+0%', help='语速 (如 +20%%)')
    parser.add_argument('--volume', default='+0%', help='音量 (如 +50%%)')
    parser.add_argument('--output', default='audio.mp3', help='输出音频文件')
    parser.add_argument('--auto-language', action='store_true', default=True, help='自动检测语言')
    
    # Whisper 参数
    parser.add_argument('--whisper-model', default='medium', help='Whisper 模型（默认 medium）')
    parser.add_argument('--language', default=None, help='语言（None 则自动检测）')
    
    # 模式
    parser.add_argument('--tts-only', action='store_true', help='仅生成语音')
    parser.add_argument('--stt-only', action='store_true', help='仅语音识别')
    
    # 内容处理
    parser.add_argument('--max-length', type=int, default=10000, help='最大文本长度（默认 10000）')
    
    args = parser.parse_args()
    
    # 检查依赖
    check_dependencies()
    
    # 模式 1: 仅语音识别
    if args.stt_only:
        if not args.audio:
            print("❌ 请指定音频文件: --audio <path>")
            sys.exit(1)
        
        transcript = transcribe_audio_whisper(
            args.audio,
            args.whisper_model,
            args.language
        )
        
        print("\n识别结果:")
        print(transcript)
        
        with open('transcript.txt', 'w', encoding='utf-8') as f:
            f.write(transcript)
        print(f"\n✅ 结果已保存: transcript.txt")
        
        return
    
    # 模式 2: 完整流程或仅生成语音
    if not args.url:
        print("❌ 请指定网页 URL: --url <url>")
        sys.exit(1)
    
    # 提取网页内容（混合方案）
    title, content, metadata = extract_webpage_content(args.url)
    
    if not content:
        print("❌ 无法提取网页内容")
        sys.exit(1)
    
    cleaned = clean_content(content, args.max_length)
    
    print(f"\n📝 内容预览 ({len(cleaned)} 字符):")
    print(cleaned[:500] + "..." if len(cleaned) > 500 else cleaned)
    
    # 生成语音
    output_path, used_voice = asyncio.run(generate_audio_edge_tts(
        cleaned,
        args.voice,
        args.output,
        args.rate,
        args.volume,
        args.auto_language
    ))
    
    # 如果不是仅生成语音，则进行语音识别
    if not args.tts_only:
        print()
        transcript = transcribe_audio_whisper(
            output_path,
            args.whisper_model,
            args.language
        )
        
        print("\n识别结果:")
        print(transcript)
        
        with open('transcript.txt', 'w', encoding='utf-8') as f:
            f.write(transcript)
        print(f"\n✅ 结果已保存: transcript.txt")


if __name__ == '__main__':
    main()
