---
name: PureVocals-UVR-Automator
description: |-
  批量从音频文件（.mp3/.wav/.flac 等）中提取超干净干声（Vocals Only）。
  支持 VR Architecture、Window Size 320、Aggression 10、WAV 输出。
  自动检测 GPU（有则 CUDA 加速，无则 CPU），自动管理虚拟环境，完美保持原文件夹结构。
metadata:
  openclaw:
    requires:
      bins:
        - python
---

# PureVocals-UVR-Automator

**功能**：一键把带背景音的音频文件提取为纯净干声，专为翻唱、卡拉OK、素材清洗设计。

## 支持的模型（推荐顺序）
1. **Kim_Vocal_2.onnx** → 默认推荐（速度最快 + 干净度最高）
2. **6_HP_Karaoke-UVR.pth** → 高质量卡拉OK模式（你原来的设置）
3. **UVR-MDX-NET-Karaoke_2.onnx** → 极致速度批量模式

## 执行步骤
1. **解析目录**：识别用户的源路径（支持单个音频文件或整个文件夹）。
2. **默认目标**：若未指定输出路径，默认在输入同级创建 `[输入文件夹]_vocals` 文件夹。
3. **调用命令**：使用以下兼容性命令启动脚本（优先 python3，失败则 python）。脚本会自动创建虚拟环境、检测 GPU 并安装对应版本。

   ```bash
   (python3 ./skills/purevocals-uvr-automator/scripts/purevocals.py "<输入路径>" ["<输出目录>"] [--model <模型名>] [--window_size <数值>] [--aggression <数值>] [--chunk_duration <秒数>] [--sample_mode]) || (python ./skills/purevocals-uvr-automator/scripts/purevocals.py "<输入路径>" ["<输出目录>"] [--model <模型名>] [--window_size <数值>] [--aggression <数值>] [--chunk_duration <秒数>] [--sample_mode])