/**
 * 交互策略模块 - 错误处理、确认机制、结果展示、快捷命令
 * 
 * 实现产品文档定义的交互策略：
 * - Phase 1: 错误处理优化（P0）
 * - Phase 2: 确认机制（P1）
 * - Phase 3: 结果展示优化（P1）
 * - Phase 4: 快捷命令（P2）
 */

const readline = require('readline');
const fs = require('fs');
const path = require('path');

// ============================================================================
// Phase 1: 错误处理优化
// ============================================================================

/**
 * 错误类型定义
 */
const ErrorTypes = {
  ERR_DOWNLOAD: 'ERR_DOWNLOAD',         // 下载失败
  ERR_SEARCH: 'ERR_SEARCH',             // 搜索无结果
  ERR_NETWORK: 'ERR_NETWORK',           // 网络错误
  ERR_COPYRIGHT: 'ERR_COPYRIGHT',       // 版权限制
  ERR_INVALID_URL: 'ERR_INVALID_URL',   // 链接无效
  ERR_FORMAT: 'ERR_FORMAT',             // 格式不支持
  ERR_STORAGE: 'ERR_STORAGE'            // 存储不足
};

/**
 * 错误话术模板
 */
const ErrorMessages = {
  [ErrorTypes.ERR_DOWNLOAD]: {
    title: '❌ 下载失败',
    message: '抱歉，这个视频暂时无法下载。',
    causes: [
      '视频已被删除或设为私有',
      '网络连接不稳定',
      '平台临时限制'
    ],
    suggestions: [
      '检查链接是否有效',
      '稍后重试',
      '尝试其他视频'
    ],
    actions: [
      { label: '重试', command: 'retry' },
      { label: '搜索类似', command: 'search_similar' }
    ]
  },
  [ErrorTypes.ERR_SEARCH]: {
    title: '🔍 未找到相关视频',
    message: '抱歉，没找到匹配「{keyword}」的视频。',
    suggestions: [
      '检查关键词拼写',
      '尝试更简短的关键词',
      '指定平台（如「B 站的 xxx」）'
    ],
    examples: [
      '「找个 lol 视频」',
      '「B 站 游戏集锦」'
    ],
    actions: [
      { label: '重新搜索', command: 'retry' }
    ]
  },
  [ErrorTypes.ERR_NETWORK]: {
    title: '🌐 网络连接问题',
    message: '下载过程中遇到网络错误。',
    status: '已下载 {percent}%，连接中断',
    suggestions: [
      '检查网络连接',
      '稍后重试（支持断点续传）'
    ],
    actions: [
      { label: '重试', command: 'retry' }
    ]
  },
  [ErrorTypes.ERR_COPYRIGHT]: {
    title: '⚠️ 版权保护内容',
    message: '抱歉，这个视频受版权保护，无法下载。',
    explanation: '部分付费/会员内容无法下载，版权方限制了下载权限',
    suggestions: [
      '在平台官方 App 内观看',
      '搜索其他类似视频'
    ],
    actions: [
      { label: '找类似的', command: 'search_similar' }
    ]
  },
  [ErrorTypes.ERR_INVALID_URL]: {
    title: '🔗 链接无法识别',
    message: '这个链接看起来不太对。',
    currentUrl: '{url}',
    supported: [
      'YouTube: youtube.com/watch?v=... 或 youtu.be/...',
      'B 站：bilibili.com/video/BV...'
    ],
    suggestions: [
      '检查链接是否完整',
      '从浏览器地址栏复制完整链接'
    ],
    actions: [
      { label: '重新输入', command: 'retry' }
    ]
  },
  [ErrorTypes.ERR_FORMAT]: {
    title: '📼 格式不支持',
    message: '抱歉，暂不支持「{format}」格式。',
    supported: [
      '视频：MP4, MKV, WEBM',
      '音频：MP3, M4A, FLAC'
    ],
    actions: [
      { label: 'MP4', command: 'mp4' },
      { label: 'MP3', command: 'mp3' }
    ]
  },
  [ErrorTypes.ERR_STORAGE]: {
    title: '💾 存储空间不足',
    message: '设备剩余空间不足以下载此视频。',
    required: '需要：{required}',
    available: '剩余：{available}',
    suggestions: [
      '清理存储空间',
      '选择更低画质',
      '只提取音频'
    ],
    actions: [
      { label: '720p', command: '720p' },
      { label: '音频', command: 'audio' }
    ]
  }
};

/**
 * 格式化错误消息
 * @param {string} errorType - 错误类型
 * @param {Object} params - 参数替换
 * @returns {string} 格式化的错误消息
 */
function formatError(errorType, params = {}) {
  const template = ErrorMessages[errorType];
  if (!template) {
    return `❌ 未知错误：${errorType}`;
  }

  let output = `\n**${template.title}**\n\n`;
  output += template.message + '\n\n';

  // 替换参数
  if (params.keyword) {
    output = output.replace(/{keyword}/g, params.keyword);
  }
  if (params.url) {
    output = output.replace(/{url}/g, params.url);
  }
  if (params.format) {
    output = output.replace(/{format}/g, params.format);
  }
  if (params.percent) {
    output = output.replace(/{percent}/g, params.percent);
  }
  if (params.required) {
    output = output.replace(/{required}/g, params.required);
  }
  if (params.available) {
    output = output.replace(/{available}/g, params.available);
  }

  // 添加额外信息
  if (template.causes) {
    output += '**可能原因**:\n';
    template.causes.forEach(cause => {
      output += `- ${cause}\n`;
    });
    output += '\n';
  }

  if (template.explanation) {
    output += '**说明**: ' + template.explanation + '\n\n';
  }

  if (template.status && params.percent !== undefined) {
    output += template.status.replace(/{percent}/g, params.percent) + '\n\n';
  }

  if (template.currentUrl && params.url) {
    output += '**当前链接**: `' + params.url + '`\n\n';
  }

  if (template.supported) {
    output += '**支持的链接**:\n';
    template.supported.forEach(item => {
      output += `- ${item}\n`;
    });
    output += '\n';
  }

  // 添加建议
  if (template.suggestions) {
    output += '**建议**:\n';
    template.suggestions.forEach((suggestion, index) => {
      output += `${index + 1}. ${suggestion}\n`;
    });
    output += '\n';
  }

  // 添加快捷操作
  if (template.actions && template.actions.length > 0) {
    output += '**快捷操作**:\n';
    template.actions.forEach((action, index) => {
      output += `${index + 1}️⃣ ${action.label} (回复「${action.command}」)\n`;
    });
    output += '\n';
  }

  return output;
}

/**
 * 处理错误并显示用户友好的消息
 * @param {string} errorType - 错误类型
 * @param {Object} params - 参数
 * @param {Function} onAction - 快捷操作回调
 */
function handleError(errorType, params = {}, onAction = null) {
  const message = formatError(errorType, params);
  console.log(message);

  if (onAction) {
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });

    rl.question('💡 请输入操作编号或命令：', (answer) => {
      rl.close();
      onAction(answer.trim());
    });
  }
}

// ============================================================================
// Phase 2: 确认机制
// ============================================================================

/**
 * 确认类型
 */
const ConfirmTypes = {
  CONFIRM_DOWNLOAD: 'CONFIRM_DOWNLOAD',     // 标准下载确认
  CONFIRM_LARGE_FILE: 'CONFIRM_LARGE_FILE', // 大文件确认
  CONFIRM_BATCH: 'CONFIRM_BATCH',           // 批量下载确认
  CONFIRM_AUDIO: 'CONFIRM_AUDIO'            // 音频提取确认
};

/**
 * 确认消息模板
 */
const ConfirmMessages = {
  [ConfirmTypes.CONFIRM_DOWNLOAD]: (video) => `
📺 **确认下载**

**标题**: ${video.title}
**平台**: ${video.platform === 'youtube' ? 'YouTube 🔴' : '哔哩哔哩 🔵'}
**时长**: ${video.duration || 'N/A'}
**大小**: 约 ${video.size || '未知'}
**格式**: ${video.format || 'MP4'}

回复「**确认**」开始下载
回复「**音频**」只提取音频
回复「**取消**」放弃
`,

  [ConfirmTypes.CONFIRM_LARGE_FILE]: (video) => `
⚠️ **大文件提醒**

这个视频较大，请确认：

**大小**: ${video.size}
**预计时间**: ${video.estimatedTime || '约 5-10 分钟'}
**格式**: ${video.format || 'MP4'}

确定要下载吗？回复「**确认**」继续
`,

  [ConfirmTypes.CONFIRM_BATCH]: (videos) => {
    const totalSize = videos.reduce((sum, v) => sum + (parseInt(v.size) || 0), 0);
    let list = '';
    videos.forEach((v, i) => {
      list += `${i + 1}️⃣ ${v.title} (${v.size || '未知'})\n`;
    });

    return `
📦 **批量下载确认**

您选择了 **${videos.length}** 个视频：

${list}
**总计**: 约 ${totalSize} MB

回复「**确认**」开始批量下载
回复「**取消**」重新选择
`;
  },

  [ConfirmTypes.CONFIRM_AUDIO]: (video) => `
🎵 **准备提取音频**

**来源**: ${video.title}
**格式**: MP3 (320kbps)
**预计大小**: 约 ${video.audioSize || '未知'}

回复「**确认**」开始提取
`
};

/**
 * 检查是否需要确认
 * @param {Object} video - 视频信息
 * @param {Object} options - 选项
 * @returns {string|null} 确认类型，不需要确认返回 null
 */
function checkConfirmRequired(video, options = {}) {
  const sizeMB = parseInt(video.size) || 0;
  
  // 大文件确认（>500MB）
  if (sizeMB > 500) {
    return ConfirmTypes.CONFIRM_LARGE_FILE;
  }
  
  // 音频提取确认
  if (options.audioOnly) {
    return ConfirmTypes.CONFIRM_AUDIO;
  }
  
  // 标准确认
  return ConfirmTypes.CONFIRM_DOWNLOAD;
}

/**
 * 显示确认消息并等待用户响应
 * @param {string} confirmType - 确认类型
 * @param {Object|Array} data - 视频信息或视频列表
 * @returns {Promise<boolean>} 用户是否确认
 */
async function showConfirm(confirmType, data) {
  const template = ConfirmMessages[confirmType];
  if (!template) {
    console.error('❌ 未知的确认类型');
    return false;
  }

  const message = typeof template === 'function' ? template(data) : template;
  console.log(message);

  return new Promise((resolve) => {
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });

    rl.question('⬇️  请回复（确认/取消）：', (answer) => {
      rl.close();
      const normalized = answer.trim().toLowerCase();
      
      if (normalized === '确认' || normalized === 'confirm' || normalized === '1') {
        resolve(true);
      } else if (normalized === '音频' || normalized === 'audio') {
        resolve('audio'); // 特殊处理：用户想提取音频
      } else {
        resolve(false);
      }
    });
  });
}

// ============================================================================
// Phase 3: 结果展示优化
// ============================================================================

/**
 * 格式化搜索结果表格（纯文本版本）
 * @param {Array} results - 搜索结果
 * @param {boolean} showCover - 是否显示封面提示
 * @returns {string} 格式化的表格
 */
function formatSearchResults(results, showCover = true) {
  if (!results || results.length === 0) {
    return '🔍 未找到结果';
  }

  let output = `\n🔍 找到 **${results.length}** 个相关视频\n\n`;
  
  // 打印表头
  output += '┌────┬─────────────────────┬────────┬───────┐\n';
  output += '│ 序号 │       标题        │  平台  │ 时长  │\n';
  output += '├────┼─────────────────────┼────────┼───────┤\n';
  
  // 打印每一行
  results.forEach((video, index) => {
    const platformIcon = video.platform === 'youtube' ? 'YouTube' : 'B 站';
    let title = video.title || '未知标题';
    if (title.length > 20) {
      title = title.substring(0, 17) + '...';
    }
    const duration = video.duration || 'N/A';
    
    output += `│ ${String(index + 1).padStart(4)} │ ${title.padEnd(19)} │ ${platformIcon.padEnd(6)} │ ${duration.padStart(5)} │\n`;
  });
  
  output += '└────┴─────────────────────┴────────┴───────┘\n\n';

  // 封面提示
  if (showCover && results[0]?.thumbnail) {
    output += '📷 封面：' + results[0].thumbnail + '\n';
  }

  output += '\n📌 回复序号下载（如「1」或「下载 2」）\n';
  output += '💡 说「查看更多」获取下一页结果\n';

  return output;
}

/**
 * 格式化下载进度
 * @param {number} percent - 进度百分比 (0-100)
 * @param {number} speed - 下载速度 (MB/s)
 * @param {number} eta - 剩余时间 (秒)
 * @returns {string} 格式化的进度条
 */
function formatDownloadProgress(percent, speed = 0, eta = 0) {
  const barLength = 35;
  const filledLength = Math.floor((percent / 100) * barLength);
  const bar = '█'.repeat(filledLength) + '━'.repeat(barLength - filledLength);
  
  let output = `\n⬇️ 下载中... \`${percent}%\`\n`;
  output += `${bar}\n`;
  
  if (speed > 0) {
    output += `📊 速度：${speed.toFixed(1)} MB/s\n`;
  }
  
  if (eta > 0) {
    const mins = Math.floor(eta / 60);
    const secs = eta % 60;
    output += `⏱️  剩余：${mins > 0 ? mins + '分' : ''}${secs}秒\n`;
  }
  
  return output;
}

/**
 * 格式化完成通知
 * @param {Object} video - 视频信息
 * @param {string} filepath - 文件路径
 * @returns {string} 格式化的完成消息
 */
function formatCompletion(video, filepath) {
  let output = `\n✅ **下载完成！**\n\n`;
  output += `📁 **文件名**: ${path.basename(filepath)}\n`;
  output += `📊 **大小**: ${video.size || '未知'}\n`;
  output += `🎬 **时长**: ${video.duration || 'N/A'}\n`;
  output += `💾 **位置**: ${filepath}\n`;
  output += `🔗 **来源**: ${video.platform === 'youtube' ? 'YouTube' : '哔哩哔哩'}\n`;
  output += `\n💡 打开文件：open "${filepath}"\n`;
  output += `💡 打开目录：open "${path.dirname(filepath)}"\n`;
  
  // 快捷操作
  output += `\n**快捷操作**:\n`;
  output += `1️⃣ 提取音频 (回复「音频」)\n`;
  output += `2️⃣ 打开文件夹 (回复「打开」)\n`;
  output += `3️⃣ 删除文件 (回复「删除」)\n`;
  
  return output;
}

// ============================================================================
// Phase 4: 快捷命令
// ============================================================================

/**
 * 快捷命令定义
 */
const QuickCommands = {
  '/search': {
    description: '搜索视频',
    usage: '/search <关键词>',
    example: '/search lol 或 /search B 站 教程',
    handler: async (args, context) => {
      if (!args || args.length === 0) {
        console.log('❌ 请提供搜索关键词');
        console.log('用法：/search <关键词>');
        console.log('示例：/search lol');
        return;
      }
      const query = args.join(' ');
      const { search } = require('./search');
      await search(query, context.options || {});
    }
  },
  '/download': {
    description: '下载视频',
    usage: '/download <URL>',
    example: '/download https://youtube.com/watch?v=xxx',
    handler: async (args, context) => {
      if (!args || args.length === 0) {
        console.log('❌ 请提供视频 URL');
        console.log('用法：/download <URL>');
        return;
      }
      const url = args[0];
      const { download } = require('./download');
      await download(url, context.options || {});
    }
  },
  '/audio': {
    description: '提取音频',
    usage: '/audio <URL>',
    example: '/audio https://youtube.com/watch?v=xxx',
    handler: async (args, context) => {
      if (!args || args.length === 0) {
        console.log('❌ 请提供视频 URL');
        console.log('用法：/audio <URL>');
        return;
      }
      const url = args[0];
      const { download } = require('./download');
      await download(url, { ...context.options, audioOnly: true });
    }
  },
  '/history': {
    description: '查看历史',
    usage: '/history',
    example: '/history 或 /history 20',
    handler: async (args, context) => {
      const limit = args[0] || '10';
      const { showHistory } = require('./download');
      showHistory(parseInt(limit));
    }
  },
  '/cancel': {
    description: '取消当前任务',
    usage: '/cancel',
    example: '/cancel',
    handler: async (args, context) => {
      console.log('🚫 已取消当前任务');
      if (context.onCancel) {
        context.onCancel();
      }
    }
  },
  '/help': {
    description: '帮助信息',
    usage: '/help',
    example: '/help',
    handler: async (args, context) => {
      showHelp();
    }
  }
};

/**
 * 显示帮助信息
 */
function showHelp() {
  console.log(`
🎬 **videodown 快捷命令**

┌────────────┬──────────────────────┬─────────────────────┐
│ 命令       │ 功能                 │ 示例                │
├────────────┼──────────────────────┼─────────────────────┤
│ /search    │ 搜索视频             │ /search lol         │
│ /download  │ 下载视频             │ /download <URL>     │
│ /audio     │ 提取音频             │ /audio <URL>        │
│ /history   │ 查看历史             │ /history            │
│ /cancel    │ 取消当前任务         │ /cancel             │
│ /help      │ 帮助信息             │ /help               │
└────────────┴──────────────────────┴─────────────────────┘

💡 **自然语言也支持**:
- "找个 lol 视频" → 自动搜索
- "下载这个" + URL → 自动下载
- "只要音频" + URL → 提取音频

📚 **更多文档**: 
- GitHub: https://github.com/chenlong1314/videodown
- 中文文档：README_CN.md
`);
}

/**
 * 解析并执行快捷命令
 * @param {string} input - 用户输入
 * @param {Object} context - 上下文
 * @returns {Promise<boolean>} 是否执行了命令
 */
async function parseQuickCommand(input, context = {}) {
  const trimmed = input.trim();
  
  // 检查是否是快捷命令
  if (!trimmed.startsWith('/')) {
    return false;
  }

  const parts = trimmed.split(/\s+/);
  const command = parts[0].toLowerCase();
  const args = parts.slice(1);

  const cmd = QuickCommands[command];
  if (!cmd) {
    console.log(`❌ 未知命令：${command}`);
    console.log('输入 /help 查看可用命令');
    return true;
  }

  try {
    await cmd.handler(args, context);
    return true;
  } catch (error) {
    console.error(`❌ 执行命令失败：${error.message}`);
    return true;
  }
}

/**
 * 检查 URL 是否有效
 * @param {string} url - URL 字符串
 * @returns {boolean} 是否有效
 */
function isValidUrl(url) {
  const patterns = [
    /^https?:\/\/(www\.)?youtube\.com\/watch\?v=[a-zA-Z0-9_-]+/,
    /^https?:\/\/youtu\.be\/[a-zA-Z0-9_-]+/,
    /^https?:\/\/(www\.)?bilibili\.com\/video\/(BV[a-zA-Z0-9]+|[a-zA-Z0-9]+)/,
    /^https?:\/\/(www\.)?bilibili\.com\/video\/av[0-9]+/
  ];

  return patterns.some(pattern => pattern.test(url));
}

// ============================================================================
// 导出
// ============================================================================

module.exports = {
  // Phase 1: 错误处理
  ErrorTypes,
  ErrorMessages,
  formatError,
  handleError,
  
  // Phase 2: 确认机制
  ConfirmTypes,
  ConfirmMessages,
  checkConfirmRequired,
  showConfirm,
  
  // Phase 3: 结果展示
  formatSearchResults,
  formatDownloadProgress,
  formatCompletion,
  
  // Phase 4: 快捷命令
  QuickCommands,
  parseQuickCommand,
  showHelp,
  isValidUrl
};
