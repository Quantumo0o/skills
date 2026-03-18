/**
 * 视频搜索模块
 */

const { searchYouTube } = require('./search-yt');
const { searchBilibili } = require('./search-bili');
const { download } = require('./download');
const readline = require('readline');
const { 
  formatSearchResults, 
  handleError, 
  ErrorTypes,
  formatDownloadProgress,
  formatCompletion,
  checkConfirmRequired,
  showConfirm
} = require('./interaction');

/**
 * 搜索视频
 * @param {string} query - 搜索关键词
 * @param {Object} options - 搜索选项
 */
async function search(query, options = {}) {
  const {
    platform = 'all',
    limit = 10,
    duration,
    select
  } = options;

  console.log(`🔍 搜索：${query}`);
  console.log(`平台：${platform} | 数量：${limit}`);

  let results = [];

  // 根据平台搜索
  if (platform === 'youtube' || platform === 'all') {
    console.log('\n📺 搜索 YouTube...');
    const ytResults = await searchYouTube(query, parseInt(limit));
    results = results.concat(ytResults.map(r => ({ ...r, platform: 'youtube' })));
  }

  if (platform === 'bilibili' || platform === 'all') {
    console.log('\n📺 搜索 Bilibili...');
    const biliResults = await searchBilibili(query, parseInt(limit));
    results = results.concat(biliResults.map(r => ({ ...r, platform: 'bilibili' })));
  }

  if (results.length === 0) {
    // 使用错误处理模块
    handleError(ErrorTypes.ERR_SEARCH, { keyword: query });
    return;
  }

  // 使用新的格式化函数显示结果
  console.log(formatSearchResults(results, true));

  // 如果指定了直接下载
  if (select) {
    const index = parseInt(select) - 1;
    if (index >= 0 && index < results.length) {
      const video = results[index];
      console.log(`\n📥 下载第 ${select} 个结果：${video.title}`);
      await downloadWithProgress(video.url, {
        title: video.title,
        platform: video.platform
      });
      return;
    } else {
      console.error(`❌ 无效的序号：${select}`);
      return;
    }
  }

  // 交互式选择
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  rl.question('\n⬇️  请输入序号下载（1-' + results.length + '）或 q 退出：', async (answer) => {
    rl.close();

    if (answer.toLowerCase() === 'q') {
      console.log('👋 已退出');
      return;
    }

    // 支持"下载 X"格式
    const match = answer.match(/(?:下载\s*)?(\d+)/);
    if (match) {
      const index = parseInt(match[1]) - 1;
      if (index >= 0 && index < results.length) {
        const video = results[index];
        console.log(`\n📥 开始下载：${video.title}`);
        console.log(`🔗 URL: ${video.url}`);
        await downloadWithProgress(video.url, {
          title: video.title,
          platform: video.platform
        });
      } else {
        console.error('❌ 无效的选择，请输入 1-' + results.length + ' 之间的数字');
      }
    } else {
      console.error('❌ 无效的选择，请输入序号或 q 退出');
    }
  });
}

/**
 * 带进度显示的下载函数
 * @param {string} url - 视频 URL
 * @param {Object} options - 下载选项
 */
async function downloadWithProgress(url, options = {}) {
  const { download: originalDownload } = require('./download');
  
  // 这里可以扩展 download.js 以支持进度回调
  // 目前先使用原有下载函数，后续可添加进度监听
  await originalDownload(url, options);
}

module.exports = { search };
