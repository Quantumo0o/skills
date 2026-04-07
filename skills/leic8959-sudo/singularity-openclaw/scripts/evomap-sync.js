#!/usr/bin/env node
import { pullGenes, fullSync, printGeneSummary, matchGenes, hubFetch, hubApply, reportCapsule, getStats } from '../lib/evomap.js';
import { loadCredentials, createPost, createComment, votePost, fetchHotPosts, fetchNotifications, fetchSubmoltPosts, getFollowers, followUser } from '../lib/api.js';

const [cmd, ...args] = process.argv.slice(2);

const cmds = {
  pull: async () => {
    const sinceDays = parseInt(args.find(a => a.startsWith('--days='))?.split('=')[1] || '7');
    console.log('增量同步 Gene（最近 ' + sinceDays + ' 天）...');
    const result = await pullGenes(sinceDays);
    console.log('完成：新增 ' + result.pulled + ' 个 Gene，耗时 ' + result.duration + 'ms');
    if (result.errors.length) console.error('错误：' + result.errors.join(', '));
    return result;
  },
  sync: async () => {
    console.log('全量同步（Gene + Stats）...');
    return await fullSync();
  },
  list: () => printGeneSummary(),
  match: async () => {
    const taskType = args.find(a => a.startsWith('--task='))?.split('=')[1] || 'NETWORK_REQUEST';
    const sigArg = args.find(a => a.startsWith('--signals='))?.split('=')[1] || '';
    const signals = sigArg ? sigArg.split(',') : ['network_timeout'];
    const matched = matchGenes(taskType, signals);
    console.log('匹配到 ' + matched.length + ' 个 Gene：');
    for (const g of matched) console.log('  [' + g.gdiScore + '] ' + g.displayName + ' (' + g.taskType + ')');
  },
  fetch: async () => {
    const sigArg = args.find(a => a.startsWith('--signals='))?.split('=')[1] || 'network_timeout';
    const signals = sigArg.split(',');
    const taskType = args.find(a => a.startsWith('--task='))?.split('=')[1] || 'NETWORK_REQUEST';
    const minConf = parseFloat(args.find(a => a.startsWith('--min-conf='))?.split('=')[1] || '0.5');
    const { assets, error } = await hubFetch({ signals, taskType, minConfidence: minConf });
    if (error) { console.error('错误：' + error); return; }
    console.log('Hub 返回 ' + assets.length + ' 个资源：');
    for (const a of assets) console.log('  [confidence=' + a.confidence + '] ' + a.asset_type + ' ' + (a.genes || []).join(', '));
  },
  apply: async () => {
    const capsuleId = args.find(a => !a.startsWith('--'));
    if (!capsuleId) { console.error('用法：evomap-sync.js apply <capsule_id>'); return; }
    const result = await hubApply(capsuleId);
    console.log(result.success ? '应用成功！' : '应用失败：' + result.error);
  },
  stats: async () => {
    const period = args.find(a => a.startsWith('--period='))?.split('=')[1] || 'month';
    const s = await getStats(period);
    if (!s) { console.error('获取统计失败'); return; }
    console.log('\n=== EvoMap 统计（' + period + '）===');
    console.log('我的 Gene：' + s.myGenes.total + ' 个，总使用 ' + s.myGenes.totalUsage + ' 次');
    console.log('应用他人：' + s.appliedGenes.total + ' 次');
    console.log('社区影响：被他人使用 ' + s.communityImpact.genesUsedByOthers + ' 次');
    console.log('排行：第 ' + s.ranking.rank + ' 名（总计 ' + s.ranking.totalAgents + ' 个 Agent）');
  },

  // ===== 新增：社交互动命令 =====

  /** 浏览热帖 */
  feed: async () => {
    const limit = parseInt(args.find(a => a.startsWith('--limit='))?.split('=')[1] || '10');
    const sort = args.find(a => a.startsWith('--sort='))?.split('=')[1] || 'hot';
    const cred = loadCredentials();
    const data = await fetchHotPosts(cred.api_key, limit);
    if (!data.data?.length) { console.log('暂无帖子'); return; }
    console.log('\n=== 热帖（' + sort + '）===');
    for (const p of data.data) {
      const votes = p.upvotes || p.likeCount || 0;
      console.log('\n[' + p.id + '] ' + p.title);
      console.log('  板块：' + (p.submolt?.name || 'unknown') + ' | 票数：' + votes + ' | 评论：' + (p.commentCount || 0));
      if (p.content) console.log('  内容：' + p.content.substring(0, 80) + (p.content.length > 80 ? '...' : ''));
    }
  },

  /** 发帖 */
  post: async () => {
    const titleArg = args.find(a => a.startsWith('--title='));
    const contentArg = args.find(a => a.startsWith('--content='));
    const submoltArg = args.find(a => a.startsWith('--submolt='));
    if (!titleArg || !contentArg) { console.error('用法：post --title="标题" --content="内容" [--submolt=general]'); return; }
    const title = titleArg.split('=').slice(1).join('=');
    const content = contentArg.split('=').slice(1).join('=');
    const submolt = submoltArg ? submoltArg.split('=')[1] : 'general';
    const cred = loadCredentials();
    const result = await createPost(cred.api_key, { title, content, submolt });
    console.log(result.id ? '发帖成功！ID: ' + result.id : '发帖失败：' + (result.error || JSON.stringify(result)));
  },

  /** 投票 */
  vote: async () => {
    const postId = args.find(a => !a.startsWith('--'));
    const type = args.find(a => a.startsWith('--type='))?.split('=')[1] || 'up';
    if (!postId) { console.error('用法：vote <post_id> [--type=up|down]'); return; }
    const cred = loadCredentials();
    const result = await votePost(cred.api_key, postId, type);
    console.log(result.success !== false ? '投票成功！' : '投票失败：' + (result.error || JSON.stringify(result)));
  },

  /** 浏览某板块帖子 */
  browse: async () => {
    const slug = args.find(a => a.startsWith('--slug='))?.split('=')[1] || 'general';
    const limit = parseInt(args.find(a => a.startsWith('--limit='))?.split('=')[1] || '10');
    const cred = loadCredentials();
    const data = await fetchSubmoltPosts(cred.api_key, slug, { limit, sort: 'hot' });
    if (!data.data?.length) { console.log('板块 ' + slug + ' 暂无帖子'); return; }
    console.log('\n=== #' + slug + ' 热帖 ===');
    for (const p of data.data) {
      console.log('[' + p.id + '] ' + p.title + ' | 票：' + (p.upvotes || 0) + ' | 评论：' + (p.commentCount || 0));
    }
  },

  /** 查看通知 */
  notify: async () => {
    const cred = loadCredentials();
    const data = await fetchNotifications(cred.api_key, false);
    if (!data.notifications?.length) { console.log('无通知'); return; }
    console.log('\n=== 通知（' + data.notifications.length + ' 条）===');
    for (const n of data.notifications.slice(0, 10)) {
      console.log('[' + n.type + '] ' + (n.message || n.content || JSON.stringify(n).substring(0, 60)));
    }
  },

  /** 关注用户（传入 AGENT_NAME，不是 userId）*/
  follow: async () => {
    const agentName = args.find(a => !a.startsWith('--'));
    if (!agentName) { console.error('用法：follow <agent_name>'); return; }
    const cred = loadCredentials();
    const result = await followUser(cred.api_key, agentName);
    console.log(result.success !== false ? '关注成功！' : '关注失败：' + (result.error || JSON.stringify(result)));
  },
};

if (cmds[cmd]) {
  const fn = cmds[cmd];
  const result = fn();
  (result instanceof Promise ? result : Promise.resolve(result))
    .catch(err => { console.error(err.message); process.exit(1); });
} else {
  console.log('用法：');
  console.log('  # EvoMap / Gene');
  console.log('  node evomap-sync.js pull [--days=7]          # 增量拉取 Gene');
  console.log('  node evomap-sync.js sync                      # 全量同步 Gene+Stats');
  console.log('  node evomap-sync.js list                      # 查看本地 Gene 缓存');
  console.log('  node evomap-sync.js match --signals=x         # 匹配 Gene');
  console.log('  node evomap-sync.js fetch --signals=x        # 从 Hub 搜索 Capsule');
  console.log('  node evomap-sync.js apply <capsule_id>       # 应用他人 Capsule');
  console.log('  node evomap-sync.js stats [--period=month]   # 统计仪表盘');
  console.log('');
  console.log('  # 社交互动');
  console.log('  node evomap-sync.js feed [--limit=10] [--sort=hot|new]  # 浏览热帖');
  console.log('  node evomap-sync.js post --title=X --content=X [--submolt=general]  # 发帖');
  console.log('  node evomap-sync.js vote <post_id> [--type=up|down]  # 投票/点赞');
  console.log('  node evomap-sync.js browse --slug=general [--limit=10]  # 浏览板块帖子');
  console.log('  node evomap-sync.js notify                   # 查看通知');
  console.log('  node evomap-sync.js follow <user_id>         # 关注用户');
}
