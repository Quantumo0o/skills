/**
 * YouTube 搜索模块
 * 使用 yt-dlp 的 ytsearch: 语法，无需 API Key
 */

const { execSync } = require('child_process');

/**
 * 搜索 YouTube 视频
 * @param {string} query - 搜索关键词
 * @param {number} limit - 结果数量
 * @returns {Promise<Array>} 搜索结果列表
 */
async function searchYouTube(query, limit = 10) {
  try {
    // 使用 yt-dlp 搜索
    const command = `yt-dlp --flat-playlist --dump-json "ytsearch${limit}:${query}"`;
    const output = execSync(command, {
      encoding: 'utf-8',
      maxBuffer: 10 * 1024 * 1024
    });

    // 解析 JSON 结果（每行一个 JSON 对象）
    const results = output
      .trim()
      .split('\n')
      .filter(line => line.trim())
      .map(line => {
        try {
          const data = JSON.parse(line);
          return {
            title: data.title || '未知标题',
            url: `https://www.youtube.com/watch?v=${data.id}`,
            duration: formatDuration(data.duration),
            uploader: data.uploader || data.channel || '未知频道',
            view_count: data.view_count,
            thumbnail: data.thumbnail
          };
        } catch (e) {
          return null;
        }
      })
      .filter(r => r !== null);

    return results;
  } catch (error) {
    if (error.status === 127) {
      console.error('❌ 未找到 yt-dlp，请先安装：npm install -g yt-dlp');
    } else {
      console.error('❌ YouTube 搜索失败:', error.message);
    }
    return [];
  }
}

/**
 * 格式化时长（秒 -> MM:SS）
 */
function formatDuration(seconds) {
  if (!seconds) return 'N/A';
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins}:${secs.toString().padStart(2, '0')}`;
}

module.exports = { searchYouTube };
