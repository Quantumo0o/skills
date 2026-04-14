#!/usr/bin/env node
/**
 * PPT to Video Generator
 * 
 * 将演示文稿 + 背景材料 → 播报/汇报视频
 * 
 * 支持输入模式：
 * 1. 已匹配讲稿：script_matched.md 或 讲稿.md
 * 2. 背景材料 + 智能匹配：background.md + README.md
 * 3. 降级模式：仅 PPT 文件
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const OUTPUT_BASE = '/home/Vincent/.openclaw/workspace/wechat_articles/Video';

// ========== 文件类型定义 ==========
const FILE_TYPES = {
  PPT: 'ppt',
  README: 'readme',
  SCRIPT: 'script',
  MATERIAL: 'material',
  OTHER: 'other'
};

const VOICE_PROFILES = {
  news: { voice: 'zh-CN-XiaoxiaoNeural', rate: '+25%', style: '新闻播报' },
  tech: { voice: 'zh-CN-YunxiNeural', rate: '+25%', style: '技术讲解' },
  politics: { voice: 'zh-CN-YunjianNeural', rate: '+25%', style: '时事政治' },
  casual: { voice: 'zh-CN-XiaoyiNeural', rate: '+25%', style: '轻松讲解' }
};

// 统一语速配置（用户可覆盖）
const DEFAULT_RATE = '+25%';

// ========== 文件类型检测 ==========
function detectFileType(filePath, fileName) {
  const ext = path.extname(fileName).toLowerCase();
  const nameLower = fileName.toLowerCase();
  
  // PPT 文件
  if (['.pptx', '.ppt', '.pdf'].includes(ext)) {
    return FILE_TYPES.PPT;
  }
  
  // README 文件（关键词匹配）
  const readmeKeywords = ['readme', '说明', 'ppt 说明', '页面说明', '关键词'];
  if (ext === '.md' && readmeKeywords.some(k => nameLower.includes(k))) {
    return FILE_TYPES.README;
  }
  
  // 已匹配讲稿（关键词匹配 或 notes 目录）
  const scriptKeywords = ['讲稿', '脚本', '配音稿', '播报稿', 'script', 'narration'];
  if (ext === '.md' && scriptKeywords.some(k => nameLower.includes(k))) {
    return FILE_TYPES.SCRIPT;
  }
  
  // 检查是否在 note 文件夹内（支持多种路径格式）- 优先级高于背景材料
  const pathLower = filePath.toLowerCase().replace(/\\/g, '/');
  if ((pathLower.includes('/note/') || pathLower.includes('/notes/')) && ext === '.md') {
    return FILE_TYPES.SCRIPT;
  }
  
  // 背景材料（其他 MD 文件）
  if (ext === '.md') {
    return FILE_TYPES.MATERIAL;
  }
  
  return FILE_TYPES.OTHER;
}

// ========== 文件收集 ==========
function collectInputFiles(args) {
  const inputFiles = [];
  
  // 方式 1: 指定输入文件夹
  if (args.input && fs.existsSync(args.input)) {
    console.log('📂 扫描输入文件夹：' + args.input);
    const files = scanDirectory(args.input);
    inputFiles.push(...files);
  }
  
  // 方式 2: 直接指定文件
  if (args.slides && fs.existsSync(args.slides)) {
    inputFiles.push({
      path: args.slides,
      name: path.basename(args.slides)
    });
  }
  
  if (args.script && fs.existsSync(args.script)) {
    inputFiles.push({
      path: args.script,
      name: path.basename(args.script)
    });
  }
  
  if (args.readme && fs.existsSync(args.readme)) {
    inputFiles.push({
      path: args.readme,
      name: path.basename(args.readme)
    });
  }
  
  // 方式 3: 搜索 note 文件夹
  if (args.searchNotes) {
    const noteDirs = findNoteDirectories(args.searchNotes);
    for (const noteDir of noteDirs) {
      const files = scanDirectory(noteDir);
      inputFiles.push(...files);
    }
  }
  
  // 去重
  const uniqueFiles = inputFiles.filter((f, i, arr) => 
    arr.findIndex(x => x.path === f.path) === i
  );
  
  console.log('✅ 共收集 ' + uniqueFiles.length + ' 个文件');
  return uniqueFiles;
}

function scanDirectory(dir) {
  const files = [];
  
  function scan(currentDir) {
    const entries = fs.readdirSync(currentDir, { withFileTypes: true });
    
    for (const entry of entries) {
      const fullPath = path.join(currentDir, entry.name);
      
      if (entry.isDirectory()) {
        // 跳过隐藏目录和临时目录
        if (!entry.name.startsWith('.') && entry.name !== 'node_modules') {
          scan(fullPath);
        }
      } else if (entry.isFile()) {
        // 只收集支持的格式
        const ext = path.extname(entry.name).toLowerCase();
        if (['.pptx', '.ppt', '.pdf', '.md', '.txt'].includes(ext)) {
          files.push({
            path: fullPath,
            name: entry.name,
            dir: currentDir
          });
        }
      }
    }
  }
  
  scan(dir);
  return files;
}

function findNoteDirectories(baseDir) {
  const noteDirs = [];
  const noteNames = ['note', 'notes', '讲稿', '脚本', 'narration', 'script'];
  
  function search(currentDir) {
    const entries = fs.readdirSync(currentDir, { withFileTypes: true });
    
    for (const entry of entries) {
      if (entry.isDirectory()) {
        const nameLower = entry.name.toLowerCase();
        if (noteNames.some(n => nameLower.includes(n))) {
          noteDirs.push(path.join(currentDir, entry.name));
        }
        search(path.join(currentDir, entry.name));
      }
    }
  }
  
  search(baseDir);
  return noteDirs;
}

// ========== 创建临时项目文件夹 ==========
function createTempProject(inputFiles, outputDir) {
  const timestamp = Date.now();
  const tempProjectDir = path.join(outputDir, '.temp_project_' + timestamp);
  
  // 标准化目录结构
  const structure = {
    root: tempProjectDir,
    ppt: path.join(tempProjectDir, 'ppt'),
    readme: path.join(tempProjectDir, 'readme'),
    scripts: path.join(tempProjectDir, 'scripts'),
    materials: path.join(tempProjectDir, 'materials'),
    other: path.join(tempProjectDir, 'other')
  };
  
  // 创建目录
  Object.values(structure).forEach(dir => {
    fs.mkdirSync(dir, { recursive: true });
  });
  
  // 分类复制文件
  const classifiedFiles = {
    ppt: [],
    readme: [],
    script: [],
    material: [],
    other: []
  };
  
  for (const file of inputFiles) {
    const fileType = detectFileType(file.path, file.name) || 'other';
    const targetDir = structure[fileType] || structure.other;
    const targetPath = path.join(targetDir, file.name);
    
    fs.copyFileSync(file.path, targetPath);
    
    const fileInfo = {
      original: file.path,
      copied: targetPath,
      name: file.name
    };
    
    if (classifiedFiles[fileType]) {
      classifiedFiles[fileType].push(fileInfo);
    } else {
      classifiedFiles.other.push(fileInfo);
    }
  }
  
  // 生成文件清单
  const manifest = {
    createdAt: new Date().toISOString(),
    inputFiles: inputFiles.length,
    classifiedFiles: classifiedFiles,
    structure: structure
  };
  
  fs.writeFileSync(
    path.join(tempProjectDir, 'manifest.json'),
    JSON.stringify(manifest, null, 2)
  );
  
  console.log('📁 临时项目文件夹：' + tempProjectDir);
  console.log('   PPT 文件：' + classifiedFiles.ppt.length);
  console.log('   README 文件：' + classifiedFiles.readme.length);
  console.log('   讲稿文件：' + classifiedFiles.script.length);
  console.log('   背景材料：' + classifiedFiles.material.length);
  
  return { structure, classifiedFiles, manifest };
}

// ========== 处理流程选择 ==========
function selectWorkflow(classifiedFiles) {
  const hasPPT = classifiedFiles.ppt.length > 0;
  const hasReadme = classifiedFiles.readme.length > 0;
  const hasScript = classifiedFiles.script.length > 0;
  const hasMaterial = classifiedFiles.material.length > 0;
  
  console.log('\n=== 处理流程选择 ===');
  
  if (!hasPPT) {
    console.error('❌ 错误：未找到 PPT 文件（.pptx/.ppt/.pdf）');
    return null;
  }
  
  // 流程 1: 已匹配讲稿模式（最高优先级）
  if (hasScript) {
    console.log('📋 流程：已匹配讲稿模式');
    console.log('   讲稿文件：' + classifiedFiles.script.length);
    console.log('   README 文件：' + (hasReadme ? classifiedFiles.readme.length : 0) + ' (用于验证)');
    return {
      type: 'SCRIPT_MATCHED',
      ppt: classifiedFiles.ppt[0].copied,
      scripts: classifiedFiles.script.map(f => f.copied),
      readme: hasReadme ? classifiedFiles.readme[0].copied : null
    };
  }
  
  // 流程 2: 背景材料 + 智能匹配
  if (hasMaterial) {
    console.log('📋 流程：背景材料 + 智能匹配');
    console.log('   背景材料：' + classifiedFiles.material.length);
    console.log('   README 文件：' + (hasReadme ? classifiedFiles.readme.length : 0));
    return {
      type: 'MATERIAL_SMART',
      ppt: classifiedFiles.ppt[0].copied,
      material: classifiedFiles.material[0].copied,
      readme: hasReadme ? classifiedFiles.readme[0].copied : null
    };
  }
  
  // 流程 3: 降级模式（仅 PPT）
  console.log('⚠️  流程：降级模式（仅 PPT，自动生成分段）');
  return {
    type: 'FALLBACK',
    ppt: classifiedFiles.ppt[0].copied
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const date = args.date || new Date().toISOString().split('T')[0];
  const outputDir = args.output || path.join(OUTPUT_BASE, 'ppt-' + date);
  const globalRate = args.rate || DEFAULT_RATE;
  
  console.log('\n🎬 PPT to Video Generator (v1.3 - 灵活输入版)');
  console.log('日期：' + date);
  console.log('输出：' + outputDir + '\n');
  
  fs.mkdirSync(outputDir, { recursive: true });
  
  // ========== 阶段 1: 文件收集 ==========
  console.log('=== 阶段 1: 文件收集 ===');
  const inputFiles = collectInputFiles(args);
  
  if (inputFiles.length === 0) {
    console.error('❌ 错误：未找到任何输入文件');
    console.error('\n支持的输入方式:');
    console.error('  1. --input <文件夹>  扫描文件夹');
    console.error('  2. --slides <文件>   指定 PPT 文件');
    console.error('  3. --script <文件>   指定讲稿文件');
    console.error('  4. --searchNotes <目录>  搜索 note 文件夹');
    process.exit(1);
  }
  
  // ========== 阶段 2: 创建临时项目 ==========
  console.log('\n=== 阶段 2: 创建临时项目 ===');
  const project = createTempProject(inputFiles, outputDir);
  
  // ========== 阶段 3: 选择处理流程 ==========
  console.log('\n=== 阶段 3: 选择处理流程 ===');
  const workflow = selectWorkflow(project.classifiedFiles);
  
  if (!workflow) {
    process.exit(1);
  }
  
  // ========== 阶段 4: 执行视频生成 ==========
  console.log('\n=== 阶段 4: 执行视频生成 ===');
  
  const slidesPath = workflow.ppt;
  const materialPath = workflow.type === 'MATERIAL_SMART' ? workflow.material : null;
  const readmePath = workflow.readme;
  const scriptsPath = workflow.type === 'SCRIPT_MATCHED' ? workflow.scripts[0] : null;
  
  // 步骤 1: 解析输入（已由工作流提供）
  console.log('\n=== 步骤 1: 解析输入 ===');
  console.log('📁 演示文件：' + slidesPath);
  if (materialPath) {
    console.log('📝 背景材料：' + materialPath);
  }
  if (scriptsPath) {
    console.log('📜 已匹配讲稿：' + scriptsPath);
  }
  if (readmePath) {
    console.log('📖 README 文件：' + readmePath);
  }
  
  // 步骤 2: 分析内容风格
  console.log('\n=== 步骤 2: 分析内容风格 ===');
  
  let style, voiceConfig;
  
  if (materialPath) {
    const materialContent = fs.readFileSync(materialPath, 'utf-8');
    style = detectContentStyle(materialContent);
    voiceConfig = VOICE_PROFILES[style];
  } else if (scriptsPath) {
    const scriptContent = fs.readFileSync(scriptsPath, 'utf-8');
    style = detectContentStyle(scriptContent);
    voiceConfig = VOICE_PROFILES[style];
  } else {
    style = 'tech';
    voiceConfig = VOICE_PROFILES[style];
  }
  
  console.log('🎯 内容风格：' + voiceConfig.style);
  console.log('🎤 TTS 音色：' + voiceConfig.voice);
  console.log('⚡ 语速：' + globalRate);
  
  // 步骤 3: 演示胶片截图
  console.log('\n=== 步骤 3: 演示胶片截图 ===');
  
  const screenshotsDir = path.join(outputDir, 'screenshots');
  const screenshots = await screenshotSlides(slidesPath, screenshotsDir);
  
  console.log('✅ 共 ' + screenshots.length + ' 页截图');
  
  if (screenshots.length === 0) {
    console.error('❌ 截图失败');
    process.exit(1);
  }
  
  // 步骤 4: 生成讲稿
  console.log('\n=== 步骤 4: 生成讲稿 ===');
  
  let scripts = [];
  
  if (scriptsPath) {
    // 已匹配讲稿模式 - 支持单个文件或多个独立文件
    let scriptContent = '';
    
    // 检查是否是目录（多个独立文件）
    const scriptsDir = path.dirname(scriptsPath);
    const scriptFiles = fs.readdirSync(scriptsDir).filter(f => f.endsWith('.md') && /^\d+\.md$/.test(f)).sort();
    
    if (scriptFiles.length > 1) {
      // 多个独立文件：按顺序合并
      console.log('📄 检测到 ' + scriptFiles.length + ' 个独立讲稿文件');
      for (const f of scriptFiles) {
        const filePath = path.join(scriptsDir, f);
        const content = fs.readFileSync(filePath, 'utf-8');
        scriptContent += content + '\n\n';
      }
    } else {
      // 单个文件
      scriptContent = fs.readFileSync(scriptsPath, 'utf-8');
    }
    
    const validation = validateMatchedScript(scriptContent, screenshots.length);
    
    if (validation.warnings.length > 0) {
      validation.warnings.forEach(w => console.warn(w));
    }
    
    scripts = validation.scripts;
    console.log('✅ 已匹配讲稿：' + scripts.length + ' 页');
  } else if (materialPath) {
    // 背景材料模式
    const materialContent = fs.readFileSync(materialPath, 'utf-8');
    scripts = generateScripts(materialContent, screenshots.length, style, readmePath);
    console.log('✅ 生成讲稿：' + scripts.length + ' 页');
  } else {
    // 降级模式
    console.warn('⚠️  无讲稿文件，使用占位文本');
    for (let i = 0; i < screenshots.length; i++) {
      scripts.push('第 ' + (i + 1) + ' 页内容');
    }
  }
  
  console.log('✅ 共 ' + scripts.length + ' 页讲稿');
  
  // 步骤 5: TTS 语音合成
  console.log('\n=== 步骤 5: TTS 语音合成 ===');
  
  const audioDir = path.join(outputDir, 'audio');
  fs.mkdirSync(audioDir, { recursive: true });
  
  const audioFiles = [];
  
  for (let i = 0; i < scripts.length; i++) {
    const audioFile = path.join(audioDir, 'audio_' + String(i + 1).padStart(2, '0') + '.mp3');
    let script = scripts[i];
    
    // 删除封面/结尾特殊加速逻辑，统一使用固定速率
    const pageRate = globalRate;
    
    if (!script || script.trim() === '') {
      audioFiles.push(null);
      continue;
    }
    
    // 口语化重写（新增）
    script = rewriteScriptForSpeech(script, i + 1, style);
    
    const cleanText = cleanScriptForTTS(script);
    const escapedText = cleanText.replace(/"/g, '\\"');
    
    try {
      execSync(
        'edge-tts --text "' + escapedText + '" --voice ' + voiceConfig.voice + ' --rate ' + pageRate + ' --write-media "' + audioFile + '"',
        { stdio: 'pipe', timeout: 120000 }
      );
      
      if (fs.existsSync(audioFile) && fs.statSync(audioFile).size > 0) {
        audioFiles.push(audioFile);
        const sizeKB = Math.round(fs.statSync(audioFile).size / 1024);
        const duration = getAudioDuration(audioFile).toFixed(1);
        console.log('  ✓ 第 ' + (i + 1) + ' 页 ' + sizeKB + 'KB ' + duration + 's');
      } else {
        audioFiles.push(null);
      }
    } catch (e) {
      audioFiles.push(null);
      console.warn('  ⚠️  第 ' + (i + 1) + ' 页 TTS 失败：' + e.message);
      console.warn('     文本前 50 字：' + cleanText.substring(0, 50));
    }
  }
  
  // 步骤 6: 视频合成
  console.log('\n=== 步骤 6: 视频合成 ===');
  
  const clipsDir = path.join(outputDir, 'clips');
  fs.mkdirSync(clipsDir, { recursive: true });
  
  const clipFiles = [];
  
  for (let i = 0; i < screenshots.length; i++) {
    const screenshot = screenshots[i];
    const audioFile = audioFiles[i];
    const clipFile = path.join(clipsDir, 'clip_' + String(i + 1).padStart(2, '0') + '.mp4');
    
    if (!audioFile) {
      continue;
    }
    
    try {
      execSync(
        'ffmpeg -y -loop 1 -i "' + screenshot + '" -i "' + audioFile + '" ' +
        '-c:v libx264 -tune stillimage -c:a aac -b:a 128k -pix_fmt yuv420p ' +
        '-vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2" ' +
        '-shortest -movflags +faststart "' + clipFile + '"',
        { stdio: 'pipe' }
      );
      
      if (fs.existsSync(clipFile) && fs.statSync(clipFile).size > 0) {
        clipFiles.push(clipFile);
        const sizeKB = Math.round(fs.statSync(clipFile).size / 1024);
        console.log('  ✓ 第 ' + (i + 1) + ' 页 ' + sizeKB + 'KB');
      }
    } catch (e) {
      console.warn('  ⚠️  第 ' + (i + 1) + ' 页视频合成失败');
    }
  }
  
  if (clipFiles.length === 0) {
    console.error('❌ 视频合成失败');
    process.exit(1);
  }
  
  // 音画对齐验证（新增）
  console.log('\n📊 音画对齐检查:');
  let allAligned = true;
  for (let i = 0; i < clipFiles.length; i++) {
    const clipDuration = getVideoDuration(clipFiles[i]);
    const audioDuration = getAudioDuration(audioFiles[i]);
    const match = Math.abs(clipDuration - audioDuration) < 0.1;
    if (!match) allAligned = false;
    const status = match ? '✅' : '❌';
    console.log(`  第${i+1}页：视频${clipDuration.toFixed(1)}s = 音频${audioDuration.toFixed(1)}s ${status}`);
  }
  if (!allAligned) {
    console.warn('\n⚠️  检测到音画不同步，请检查分段脚本');
  }
  
  // 合并所有片段
  console.log('\n🔗 合并视频片段...');
  
  const finalVideo = path.join(outputDir, 'video_' + date + '.mp4');
  const fileList = path.join(clipsDir, 'files.txt');
  
  fs.writeFileSync(fileList, clipFiles.map(function(c) { return 'file \'' + c + '\''; }).join('\n'));
  
  execSync('ffmpeg -y -f concat -safe 0 -i "' + fileList + '" -c copy -movflags +faststart "' + finalVideo + '"', { stdio: 'pipe' });
  
  const videoSize = (fs.statSync(finalVideo).size / 1024 / 1024).toFixed(1);
  const videoDuration = getVideoDuration(finalVideo).toFixed(1);
  
  console.log('✅ 视频已生成：' + finalVideo);
  console.log('   大小：' + videoSize + ' MB');
  console.log('   时长：' + videoDuration + ' 秒');
  
  // 步骤 7: 生成完成报告
  generateReport(outputDir, date, screenshots.length, finalVideo);
  
  console.log('\n🎉 全部完成！\n');
}

function parseArgs(args) {
  const result = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].slice(2);
      const value = args[i + 1] && !args[i + 1].startsWith('--') ? args[i + 1] : true;
      result[key] = value;
      if (value !== true) i++;
    }
  }
  return result;
}

function findSlidesFile(slidesArg, inputDir) {
  if (slidesArg) return slidesArg;
  if (!inputDir) return null;
  const files = fs.readdirSync(inputDir);
  const slide = files.find(function(f) { return f.endsWith('.pptx') || f.endsWith('.pdf') || f.endsWith('.html'); });
  return slide ? path.join(inputDir, slide) : null;
}

function findMaterialFile(materialArg, inputDir) {
  if (materialArg) return materialArg;
  if (!inputDir) return null;
  const files = fs.readdirSync(inputDir);
  const material = files.find(function(f) { return f.endsWith('.md') || f.endsWith('.txt'); });
  return material ? path.join(inputDir, material) : null;
}

function detectContentStyle(content) {
  const lower = content.toLowerCase();
  const politicsKeywords = ['政策', '政府', '国家', '政治', '外交', '国际形势', '两会'];
  const techKeywords = ['技术', '代码', 'api', '算法', '模型', 'ai', '人工智能', '架构', '系统'];
  const newsKeywords = ['新闻', '报道', '今日', '快讯', '动态', '发布'];
  
  let scores = { politics: 0, tech: 0, news: 0 };
  politicsKeywords.forEach(function(k) { if (lower.includes(k)) scores.politics++; });
  techKeywords.forEach(function(k) { if (lower.includes(k)) scores.tech++; });
  newsKeywords.forEach(function(k) { if (lower.includes(k)) scores.news++; });
  
  const maxScore = Math.max(scores.politics, scores.tech, scores.news);
  if (maxScore === 0) return 'casual';
  if (scores.politics === maxScore) return 'politics';
  if (scores.tech === maxScore) return 'tech';
  if (scores.news === maxScore) return 'news';
  return 'casual';
}

async function screenshotSlides(slidesPath, outputDir) {
  fs.mkdirSync(outputDir, { recursive: true });
  const screenshots = [];
  
  if (slidesPath.endsWith('.pptx')) {
    try {
      const pdfPath = path.join(outputDir, 'temp_slides.pdf');
      execSync('libreoffice --headless --convert-to pdf --outdir \'' + outputDir + '\' \'' + slidesPath + '\'', { timeout: 120000 });
      
      const generatedPdf = fs.readdirSync(outputDir).find(function(f) { return f.endsWith('.pdf') && f !== 'temp_slides.pdf'; });
      if (generatedPdf) {
        fs.renameSync(path.join(outputDir, generatedPdf), pdfPath);
      }
      
      const slidePrefix = path.join(outputDir, 'slide');
      execSync('pdftoppm -png -r 150 \'' + pdfPath + '\' \'' + slidePrefix + '\'', { timeout: 120000 });
      fs.unlinkSync(pdfPath);
      
      const pngFiles = fs.readdirSync(outputDir).filter(function(f) { return f.startsWith('slide-') && f.endsWith('.png'); }).sort();
      pngFiles.forEach(function(png, i) {
        const oldPath = path.join(outputDir, png);
        const newPath = path.join(outputDir, String(i + 1).padStart(2, '0') + '-page.png');
        fs.renameSync(oldPath, newPath);
        screenshots.push(newPath);
      });
    } catch (e) {
      console.warn('PPTX 截图失败：' + e.message);
    }
  } else if (slidesPath.endsWith('.pdf')) {
    try {
      const slidePrefix = path.join(outputDir, 'slide');
      execSync('pdftoppm -png -r 150 \'' + slidesPath + '\' \'' + slidePrefix + '\'', { timeout: 120000 });
      
      const pngFiles = fs.readdirSync(outputDir).filter(function(f) { return f.startsWith('slide-') && f.endsWith('.png'); }).sort();
      pngFiles.forEach(function(png, i) {
        const oldPath = path.join(outputDir, png);
        const newPath = path.join(outputDir, String(i + 1).padStart(2, '0') + '-page.png');
        fs.renameSync(oldPath, newPath);
        screenshots.push(newPath);
      });
    } catch (e) {
      console.warn('PDF 截图失败：' + e.message);
    }
  } else if (slidesPath.endsWith('.html')) {
    const placeholder = path.join(outputDir, '01-page.png');
    try {
      execSync('convert -size 1024x720 xc:white -gravity center -pointsize 24 -annotate 0 "HTML Slide" \'' + placeholder + '\'', { stdio: 'pipe' });
      screenshots.push(placeholder);
    } catch (e) {
      console.warn('HTML 截图失败');
    }
  }
  
  return screenshots;
}

function generateScripts(materialContent, pageCount, style, readmePath) {
  // 优先级 1: 检查背景材料是否有明确的页面对齐标记
  const lines = materialContent.split('\n');
  const scripts = [];
  let currentScript = [];
  let explicitPageMarkers = false;
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (line.match(/^[#]+\s+(第\s*\d+\s* 页|\d+\s* 页|Page\s*\d+|封面 | 结尾 | 摘要 | 动态 | 趋势 | 来源)/i)) {
      explicitPageMarkers = true;
      if (currentScript.length > 0) {
        scripts.push(currentScript.join('\n').trim());
        currentScript = [];
      }
    } else if (line.startsWith('## ') || line.startsWith('### ') || line.startsWith('---')) {
      if (currentScript.length > 0) {
        scripts.push(currentScript.join('\n').trim());
        currentScript = [];
      }
    } else {
      currentScript.push(line);
    }
  }
  
  if (currentScript.length > 0) {
    scripts.push(currentScript.join('\n').trim());
  }
  
  // 优先级 1: 如果有明确页面对齐标记，直接使用分段结果
  if (explicitPageMarkers) {
    console.log('\n✅ 检测到明确页面对齐标记，直接使用分段讲稿');
    if (scripts.length !== pageCount) {
      console.warn(`\n⚠️  警告：讲稿分段数 (${scripts.length}) 与 PPT 页数 (${pageCount}) 不匹配`);
      while (scripts.length < pageCount) {
        scripts.push('// 自动补充：无对应讲稿');
      }
      if (scripts.length > pageCount) {
        console.warn(`   将截断多余讲稿（保留前${pageCount}段）`);
        return scripts.slice(0, pageCount);
      }
    }
    return scripts;
  }
  
  // 优先级 2: 使用 README.md 进行智能匹配（新增）
  if (readmePath && fs.existsSync(readmePath)) {
    console.log('\n📖 检测到 README.md，使用智能匹配...');
    const readmeContent = fs.readFileSync(readmePath, 'utf-8');
    const pptPages = parsePPTReadme(readmeContent);
    
    if (pptPages.length === pageCount) {
      const matches = smartMatch(pptPages, scripts);
      
      // 输出匹配报告
      console.log('\n📊 智能匹配报告:');
      let lowQualityCount = 0;
      for (let i = 0; i < matches.length; i++) {
        const match = matches[i];
        const status = match.score >= 0.5 ? '✅' : (match.score >= 0.3 ? '⚠️' : '❌');
        if (match.score < 0.3) lowQualityCount++;
        console.log(`  第${i+1}页：匹配度 ${match.score.toFixed(2)} ${status}`);
      }
      
      if (lowQualityCount > pageCount * 0.3) {
        console.warn(`\n⚠️  ${lowQualityCount}/${pageCount} 页面匹配度低，建议检查 README.md 关键词`);
      }
      
      const result = matches.map(m => scripts[m.scriptIndex] || '');
      // 调试输出
      for (let i = 0; i < result.length; i++) {
        const text = result[i] ? result[i].substring(0, 50) : '(空)';
        console.log('  讲稿第' + (i+1) + '页：' + text + '...');
      }
      return result;
    } else {
      console.warn(`\n⚠️  README.md 页数 (${pptPages.length}) 与 PPT 页数 (${pageCount}) 不匹配，跳过智能匹配`);
    }
  }
  
  // 优先级 3: 降级方案 - 机械分割
  if (scripts.length === 1 && pageCount > 1) {
    console.warn('\n⚠️  未检测到页面对齐标记且无 README.md，将按句子机械分割（不推荐）');
    const sentences = scripts[0].split(/[.!??.!?]/).filter(function(s) { return s.trim().length > 10; });
    const perPage = Math.ceil(sentences.length / pageCount);
    const newScripts = [];
    for (let i = 0; i < pageCount; i++) {
      const start = i * perPage;
      const end = Math.min(start + perPage, sentences.length);
      newScripts.push(sentences.slice(start, end).join('.') + '.');
    }
    return newScripts;
  }
  
  // 默认：直接返回（可能不匹配）
  while (scripts.length < pageCount) {
    scripts.push('// 自动补充：无对应讲稿');
  }
  if (scripts.length > pageCount) {
    return scripts.slice(0, pageCount);
  }
  return scripts;
}

// 新增：解析 PPT README 文件
function parsePPTReadme(readmeContent) {
  const pages = [];
  const sections = readmeContent.split(/^##\s+/m);
  
  // 调试输出
  console.log('  README 分割为 ' + sections.length + ' 个部分');
  
  for (const section of sections) {
    const lines = section.split('\n');
    const firstLine = lines[0].trim();
    
    // 更宽松的正则：匹配 "第 X 页" 或 "X 页"
    const pageMatch = firstLine.match(/(第\d+ 页|\d+ 页)/i);
    
    if (pageMatch) {
      const keywords = [];
      for (const line of lines) {
        const kwMatch = line.match(/关键词：\s*(.+)/i);
        if (kwMatch) {
          const kwText = kwMatch[1];
          // 支持中文逗号和英文逗号分隔
          keywords.push(...kwText.split(/,|,/).map(k => k.trim()).filter(k => k.length > 0));
          break;
        }
      }
      if (keywords.length > 0) {
        pages.push({ keywords, title: firstLine });
        console.log('    ✓ ' + firstLine + ': ' + keywords.length + ' 个关键词');
      } else {
        console.log('    ⚠ ' + firstLine + ': 无关键词');
      }
    }
  }
  
  console.log('  解析到 ' + pages.length + ' 页关键词');
  return pages;
}

// ========== 已匹配讲稿验证 ==========
function validateMatchedScript(scriptContent, pageCount) {
  const lines = scriptContent.split('\n');
  const scripts = [];
  let currentScript = [];
  
  for (const line of lines) {
    if (line.match(/^[#]+\s*(第\s*\d+\s* 页|\d+ 页|Page\s*\d+|封面 | 结尾 | 摘要 | 动态 | 趋势 | 来源)/i)) {
      if (currentScript.length > 0) {
        scripts.push(currentScript.join('\n').trim());
        currentScript = [];
      }
    } else {
      currentScript.push(line);
    }
  }
  
  if (currentScript.length > 0) {
    scripts.push(currentScript.join('\n').trim());
  }
  
  // 验证结果
  const result = {
    valid: scripts.length === pageCount,
    scriptCount: scripts.length,
    pageCount: pageCount,
    scripts: scripts,
    warnings: []
  };
  
  if (scripts.length !== pageCount) {
    result.warnings.push(
      '\n⚠️  警告：讲稿段数 (' + scripts.length + ') 与 PPT 页数 (' + pageCount + ') 不匹配'
    );
    
    if (scripts.length < pageCount) {
      result.warnings.push('   缺少 ' + (pageCount - scripts.length) + ' 页讲稿');
      // 补充空讲稿
      while (scripts.length < pageCount) {
        scripts.push('// 自动补充：无对应讲稿');
      }
    } else {
      result.warnings.push('   将截断多余讲稿（保留前' + pageCount + '段）');
      return { ...result, scripts: scripts.slice(0, pageCount) };
    }
  }
  
  result.scripts = scripts;
  return result;
}

// 新增：智能匹配算法
function smartMatch(pptPages, paragraphs) {
  const matches = [];
  
  for (let i = 0; i < pptPages.length; i++) {
    const pageKeywords = pptPages[i].keywords;
    let bestScore = 0;
    let bestIndex = 0;
    
    for (let j = 0; j < paragraphs.length; j++) {
      const score = calculateKeywordScore(pageKeywords, paragraphs[j]);
      if (score > bestScore) {
        bestScore = score;
        bestIndex = j;
      }
    }
    
    matches.push({ pageIndex: i, scriptIndex: bestIndex, score: bestScore });
  }
  
  return matches;
}

// 新增：计算关键词匹配分数
function calculateKeywordScore(keywords, paragraph) {
  if (keywords.length === 0) return 0;
  
  let matchCount = 0;
  for (const kw of keywords) {
    if (paragraph.toLowerCase().includes(kw.toLowerCase())) {
      matchCount++;
    }
  }
  
  return matchCount / keywords.length;
}

function cleanScriptForTTS(text) {
  return text
    .replace(/#{1,6}\s+/g, '')
    .replace(/\*\*/g, '')
    .replace(/\*/g, '')
    .replace(/`/g, '')
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
    .replace(/\n+/g, '，')
    .replace(/\s+/g, ' ')
    .trim();
}

// ========== 讲稿口语化重写 ==========
function rewriteScriptForSpeech(script, pageNum, style) {
  // 1. 清理 Markdown 格式
  let clean = script
    .replace(/#{1,6}\s+/g, '')
    .replace(/\*\*/g, '')
    .replace(/\*/g, '')
    .replace(/`/g, '')
    .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
    .trim();
  
  // 2. 提取关键信息（数字、百分比、金额等）
  const numbers = clean.match(/\d+[,.]?\d*\s*(亿 | 万 | %|美元 | 人民币 | 倍)/g) || [];
  
  // 3. 按场景风格重写
  if (style === 'news' || pageNum === 1) {
    // 新闻播报风格：客观陈述，先结论后事实
    clean = rewriteForNewsStyle(clean, numbers);
  } else if (style === 'tech') {
    // 技术汇报风格：先重点后细节，口语化
    clean = rewriteForPresentationStyle(clean, numbers, pageNum);
  } else {
    // 通用风格：简洁明了
    clean = rewriteForGeneralStyle(clean, numbers);
  }
  
  // 4. 优化句子长度（每句 15-25 字，适合 TTS 呼吸）
  clean = optimizeSentenceLength(clean);
  
  return clean;
}

function rewriteForNewsStyle(text, numbers) {
  // 新闻播报：客观、简洁、事实导向
  let result = text;
  
  // 将长句拆分为短句
  result = result.replace(/。/g, '。\n').split('\n').filter(s => s.trim()).join('');
  
  // 添加新闻播报连接词
  if (numbers.length > 0) {
    result = '本数据显示，' + result;
  }
  
  return result;
}

function rewriteForPresentationStyle(text, numbers, pageNum) {
  // 技术汇报：先重点后事实，口语化
  let result = text;
  
  // 封面页特殊处理
  if (pageNum === 1) {
    result = '各位领导好，今天我来汇报本次财报分析的核心内容。' + result;
  }
  
  // 数据页：先说结论
  if (numbers.length >= 2) {
    const keyData = numbers.slice(0, 2).join('、');
    result = '核心数据是' + keyData + '。' + result;
  }
  
  // 添加口语化连接词
  result = result
    .replace(/增长/g, '实现了增长')
    .replace(/下降/g, '出现下滑')
    .replace(/占比/g, '占到')
    .replace(/同比/g, '和去年同期相比');
  
  return result;
}

function rewriteForGeneralStyle(text, numbers) {
  // 通用风格：简洁明了
  let result = text;
  
  // 简化复杂表达
  result = result
    .replace(/ approximately/g, '约')
    .replace(/ 分别/g, '')
    .replace(/ 其中/g, '这里面');
  
  return result;
}

function optimizeSentenceLength(text) {
  // 优化句子长度，确保每句 15-25 字左右
  let sentences = text.split(/[。！？.!?]/).filter(s => s.trim().length > 0);
  
  const optimized = [];
  for (let sentence of sentences) {
    sentence = sentence.trim();
    if (sentence.length > 30) {
      // 长句拆分
      const parts = splitLongSentence(sentence);
      optimized.push(...parts);
    } else {
      optimized.push(sentence);
    }
  }
  
  return optimized.join('。') + '。';
}

function splitLongSentence(sentence) {
  // 在逗号、连接词处拆分长句
  const splitPoints = ['，', '；', '而', '且', '并', '同时'];
  let parts = [sentence];
  
  for (const point of splitPoints) {
    const newParts = [];
    for (const part of parts) {
      if (part.includes(point) && part.length > 25) {
        newParts.push(...part.split(point).filter(p => p.trim()));
      } else {
        newParts.push(part);
      }
    }
    parts = newParts;
  }
  
  return parts.filter(p => p.trim().length > 0);
}

function getAudioDuration(audioFile) {
  try {
    const output = execSync('ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 "' + audioFile + '"', { encoding: 'utf-8' });
    return parseFloat(output.trim());
  } catch (e) {
    return 5.0;
  }
}

function getVideoDuration(videoFile) {
  try {
    const output = execSync('ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 "' + videoFile + '"', { encoding: 'utf-8' });
    return parseFloat(output.trim());
  } catch (e) {
    return 0;
  }
}

function generateReport(outputDir, date, pageCount, videoPath) {
  const videoSize = (fs.statSync(videoPath).size / 1024 / 1024).toFixed(1);
  const duration = getVideoDuration(videoPath);
  
  const report = '# PPT to Video 完成报告\n\n' +
    '**生成时间**: ' + new Date().toISOString() + '\n' +
    '**日期**: ' + date + '\n\n' +
    '## ✅ 视频规格\n\n' +
    '| 维度 | 值 |\n' +
    '|------|-----|\n' +
    '| **文件路径** | `' + videoPath + '` |\n' +
    '| **文件大小** | ' + videoSize + ' MB |\n' +
    '| **分辨率** | 1024×720 (720p) |\n' +
    '| **总页数** | ' + pageCount + ' 页 |\n' +
    '| **总时长** | ' + duration.toFixed(1) + ' 秒 |\n' +
    '| **视频编码** | H.264 |\n' +
    '| **音频编码** | AAC |\n\n' +
    '**状态**: ✅ 完成\n';
  
  fs.writeFileSync(path.join(outputDir, 'VIDEO_COMPLETE.md'), report);
}

main().catch(function(err) {
  console.error('\n❌ 执行失败:', err.message);
  process.exit(1);
});
