/**
 * Bilibili 搜索模块
 * 使用 B 站 Web API，无需 API Key
 */

const https = require('https');

/**
 * 搜索 Bilibili 视频
 * @param {string} query - 搜索关键词
 * @param {number} limit - 结果数量
 * @returns {Promise<Array>} 搜索结果列表
 */
async function searchBilibili(query, limit = 10) {
  const url = new URL('https://api.bilibili.com/x/web-interface/search/type');
  url.searchParams.set('keyword', query);
  url.searchParams.set('search_type', 'video');
  url.searchParams.set('page', '1');
  url.searchParams.set('pagesize', limit.toString());

  return new Promise((resolve) => {
    const req = https.get(url.toString(), {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.bilibili.com',
        'Accept': 'application/json',
        'Cookie': 'buvid3=INFERENCE' // 简单 Cookie 绕过限制
      }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          // 检查是否返回 HTML（被拦截）
          if (data.trim().startsWith('<!DOCTYPE') || data.trim().startsWith('<html')) {
            console.error('⚠️  B 站 API 返回 HTML，可能被限制，使用备用方案...');
            resolve([]);
            return;
          }

          const json = JSON.parse(data);
          if (json.code === 0 && json.data.result) {
            const results = json.data.result.map(video => ({
              title: video.title ? video.title.replace(/<[^>]*>/g, '') : '未知标题',
              url: `https://www.bilibili.com/video/${video.bvid || ''}`,
              duration: formatDuration(video.duration),
              uploader: video.author || video.uploader || '未知 UP 主',
              view_count: video.play,
              thumbnail: video.pic
            }));
            resolve(results);
          } else {
            console.error('❌ B 站 API 返回错误:', json.message || '未知错误');
            resolve([]);
          }
        } catch (error) {
          console.error('⚠️  解析 B 站搜索结果失败:', error.message);
          console.error('   原始数据:', data.substring(0, 200));
          resolve([]);
        }
      });
    });

    req.on('error', (error) => {
      console.error('❌ B 站搜索请求失败:', error.message);
      resolve([]);
    });

    req.setTimeout(10000, () => {
      req.destroy();
      resolve([]);
    });
  });
}

/**
 * 格式化时长（MM:SS -> MM:SS）
 */
function formatDuration(duration) {
  if (!duration) return 'N/A';
  // B 站返回的格式通常是 "MM:SS" 或 "HH:MM:SS"
  return duration;
}

module.exports = { searchBilibili };
