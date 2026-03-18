/**
 * 视频下载模块
 */

const { spawnSync } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');
const { 
  handleError, 
  ErrorTypes,
  checkConfirmRequired,
  showConfirm,
  formatDownloadProgress,
  formatCompletion,
  isValidUrl
} = require('./interaction');

// 默认下载目录（用户主目录的 Downloads/videodown）
const DEFAULT_OUTPUT = path.join(os.homedir(), 'Downloads', 'videodown');

// 历史记录文件
const HISTORY_FILE = path.join(DEFAULT_OUTPUT, 'history.json');

/**
 * 保存下载历史
 */
function saveHistory(video) {
  // 确保目录存在
  if (!fs.existsSync(DEFAULT_OUTPUT)) {
    fs.mkdirSync(DEFAULT_OUTPUT, { recursive: true });
  }

  // 读取历史
  let history = [];
  if (fs.existsSync(HISTORY_FILE)) {
    try {
      history = JSON.parse(fs.readFileSync(HISTORY_FILE, 'utf-8'));
    } catch (e) {
      history = [];
    }
  }

  // 添加新记录
  history.unshift({
    ...video,
    downloadedAt: new Date().toISOString()
  });

  // 只保留最近 50 条
  history = history.slice(0, 50);

  // 保存
  fs.writeFileSync(HISTORY_FILE, JSON.stringify(history, null, 2));
}

/**
 * 查看下载历史
 */
function showHistory(limit = 10) {
  if (!fs.existsSync(HISTORY_FILE)) {
    console.log('📭 暂无下载历史');
    return;
  }

  try {
    const history = JSON.parse(fs.readFileSync(HISTORY_FILE, 'utf-8'));
    
    if (history.length === 0) {
      console.log('📭 暂无下载历史');
      return;
    }

    console.log('\n📋 下载历史：\n');
    console.log('| 序号 | 标题 | 平台 | 时间 | 路径 |');
    console.log('|------|------|------|------|------|');

    history.slice(0, limit).forEach((item, index) => {
      const title = item.title.length > 30 ? item.title.substring(0, 27) + '...' : item.title;
      const platform = item.platform === 'youtube' ? '🔴 YT' : '🔵 Bili';
      const time = new Date(item.downloadedAt).toLocaleString('zh-CN', { 
        month: '2-digit', 
        day: '2-digit', 
        hour: '2-digit', 
        minute: '2-digit' 
      });
      const filename = path.basename(item.filepath);
      
      console.log(`| ${index + 1} | ${title} | ${platform} | ${time} | ${filename} |`);
    });

    console.log(`\n💡 共 ${history.length} 条记录，保存位置：${DEFAULT_OUTPUT}`);
    console.log(`💡 打开目录：open "${DEFAULT_OUTPUT}"`);
  } catch (error) {
    console.error('❌ 读取历史失败:', error.message);
  }
}

/**
 * 转码为 H.264 兼容格式
 */
function convertToH264(inputPath, outputPath) {
  console.log('\n🔄 正在转码为兼容格式 (H.264)...');
  console.log('💡 转码后可在 QuickTime 播放\n');
  
  const result = spawnSync('ffmpeg', [
    '-i', inputPath,
    '-c:v', 'libx264',
    '-c:a', 'aac',
    '-y', // 覆盖输出文件
    outputPath
  ], {
    stdio: 'inherit'
  });
  
  return result.status === 0;
}

/**
 * 下载视频
 * @param {string} url - 视频 URL
 * @param {Object} options - 下载选项
 */
async function download(url, options = {}) {
  const {
    quality = 'best',
    output = DEFAULT_OUTPUT,
    format = 'mp4',
    audioOnly = false,
    title = '',
    platform = '',
    convert = false,  // 是否转码为兼容格式
    skipConfirm = false  // 跳过确认（用于批量下载等场景）
  } = options;

  // 验证 URL
  if (!isValidUrl(url)) {
    handleError(ErrorTypes.ERR_INVALID_URL, { url });
    return;
  }

  // 确保输出目录存在
  if (!fs.existsSync(output)) {
    fs.mkdirSync(output, { recursive: true });
  }

  console.log(`📥 开始下载：${url}`);
  console.log(`💾 保存位置：${output}`);
  console.log(`质量：${quality} | 格式：${format}`);
  if (convert) {
    console.log('🔄 转码：启用 (H.264 兼容格式)');
  }

  try {
    // 先获取视频信息（用于确认）
    const videoInfo = await getVideoInfo(url);
    
    if (videoInfo) {
      // 检查是否需要确认
      const confirmType = checkConfirmRequired(videoInfo, { audioOnly });
      
      if (!skipConfirm && confirmType) {
        const confirmed = await showConfirm(confirmType, {
          ...videoInfo,
          format: format.toUpperCase(),
          audioSize: audioOnly ? '约 ' + Math.round((videoInfo.size || 50) / 5) + ' MB' : undefined
        });
        
        if (confirmed === 'audio') {
          // 用户选择提取音频
          return await download(url, { ...options, audioOnly: true, skipConfirm: true });
        } else if (!confirmed) {
          console.log('🚫 已取消下载');
          return;
        }
      }
      
      // 更新标题和平台
      if (!title) title = videoInfo.title;
      if (!platform) platform = videoInfo.platform;
    }

    // 构建 yt-dlp 参数数组
    const args = [];

    // 质量选择
    if (quality !== 'best') {
      args.push('-f', `best[height<=${quality.replace('p', '')}]`);
    }

    // 输出路径（使用简单格式，避免特殊字符）
    const outputPath = path.join(output, '%(id)s.%(ext)s');
    args.push('-o', outputPath);

    // 格式
    if (audioOnly) {
      args.push('-x', '--audio-format', 'mp3');
    } else if (format === 'mp4') {
      args.push('--merge-output-format', 'mp4');
    }

    // URL
    args.push(url);

    // 执行命令
    console.log(`执行：yt-dlp ${args.join(' ')}`);
    
    const result = spawnSync('yt-dlp', args, {
      stdio: 'inherit',
      cwd: process.cwd()
    });

    if (result.status === 0) {
      // 获取下载的文件路径（从 URL 提取 ID）
      const videoId = url.match(/video\/([a-zA-Z0-9_-]+)/)?.[1] || url.match(/(?:v=|\/)([a-zA-Z0-9_-]+)/)?.[1] || 'unknown';
      const ext = audioOnly ? 'mp3' : 'mp4';
      const filepath = path.join(output, `${videoId}.${ext}`);
      
      let finalPath = filepath;

      // 如果需要转码
      if (convert && !audioOnly && fs.existsSync(filepath)) {
        const compatPath = path.join(output, `${videoId}_compatible.mp4`);
        const success = convertToH264(filepath, compatPath);
        if (success) {
          console.log('\n✅ 转码完成！');
          finalPath = compatPath;
        } else {
          console.warn('\n⚠️ 转码失败，使用原始文件');
        }
      }

      // 保存历史
      saveHistory({
        title: title || videoId,
        url: url,
        platform: platform || 'unknown',
        filepath: finalPath,
        filename: path.basename(finalPath),
        size: videoInfo?.size || '未知',
        duration: videoInfo?.duration || 'N/A'
      });

      // 使用新的完成消息格式
      console.log(formatCompletion({
        title: title || videoId,
        size: videoInfo?.size || '未知',
        duration: videoInfo?.duration || 'N/A',
        platform: platform || 'unknown'
      }, finalPath));
    } else {
      // 分析错误类型
      const errorMsg = result.stderr?.toString() || '';
      if (errorMsg.includes('Copyright') || errorMsg.includes('copyright')) {
        handleError(ErrorTypes.ERR_COPYRIGHT);
      } else if (errorMsg.includes('Network') || errorMsg.includes('network')) {
        handleError(ErrorTypes.ERR_NETWORK, { percent: 0 });
      } else {
        handleError(ErrorTypes.ERR_DOWNLOAD);
      }
      return;
    }
  } catch (error) {
    if (error.code === 'ENOENT' || (error.status === 127)) {
      console.error('❌ 未找到 yt-dlp，请先安装：brew install yt-dlp');
    } else {
      // 更智能的错误处理
      const errorMsg = error.message || '';
      if (errorMsg.includes('No space left')) {
        handleError(ErrorTypes.ERR_STORAGE, { required: '未知', available: '0 MB' });
      } else if (errorMsg.includes('Unsupported')) {
        handleError(ErrorTypes.ERR_FORMAT, { format: format });
      } else {
        handleError(ErrorTypes.ERR_DOWNLOAD);
      }
    }
    process.exit(1);
  }
}

/**
 * 获取视频信息（标题、大小、时长等）
 * @param {string} url - 视频 URL
 * @returns {Promise<Object|null>} 视频信息
 */
async function getVideoInfo(url) {
  try {
    const { execSync } = require('child_process');
    
    // 使用 yt-dlp 获取信息
    const command = `yt-dlp --dump-json --no-download "${url}"`;
    const output = execSync(command, {
      encoding: 'utf-8',
      maxBuffer: 10 * 1024 * 1024,
      stdio: ['pipe', 'pipe', 'ignore']  // 忽略错误输出
    });

    const data = JSON.parse(output.trim());
    
    // 估算大小（根据格式和时长）
    let estimatedSize = '未知';
    if (data.duration && data.format_note) {
      // 粗略估算：时长 (秒) * 比特率 / 8
      const bitrate = data.format_note.includes('4K') ? 20000000 : 
                      data.format_note.includes('1080') ? 5000000 :
                      data.format_note.includes('720') ? 2500000 : 1000000;
      const sizeBytes = data.duration * bitrate / 8;
      const sizeMB = Math.round(sizeBytes / 1024 / 1024);
      estimatedSize = sizeMB + ' MB';
    }

    // 判断平台
    let platform = 'unknown';
    if (url.includes('youtube.com') || url.includes('youtu.be')) {
      platform = 'youtube';
    } else if (url.includes('bilibili.com')) {
      platform = 'bilibili';
    }

    return {
      title: data.title || '未知标题',
      duration: data.duration ? formatDuration(data.duration) : 'N/A',
      size: estimatedSize,
      platform: platform,
      thumbnail: data.thumbnail
    };
  } catch (error) {
    // 获取信息失败不影响下载，返回 null
    return null;
  }
}

/**
 * 格式化时长（秒 -> MM:SS）
 */
function formatDuration(seconds) {
  if (!seconds) return 'N/A';
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${mins}:${secs.toString().padStart(2, '0')}`;
}

module.exports = { download, showHistory, DEFAULT_OUTPUT };
