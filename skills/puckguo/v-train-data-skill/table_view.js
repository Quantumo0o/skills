import fs from 'fs';

// 动态提取数据中的动作类型
function extractExerciseTypes(data) {
  const types = new Set();

  // 从运动分析中提取动作名称
  data.motion_analysis.forEach(ma => {
    if (ma.exercise_name) {
      types.add(ma.exercise_name);
    }
  });

  return Array.from(types);
}

// 根据描述识别动作类型（动态匹配）
function classifyExerciseDynamic(description, exerciseTypes) {
  if (!description) return '其他';
  const desc = description.toLowerCase();

  // 按长度降序匹配，优先匹配更具体的动作名称
  const sortedTypes = [...exerciseTypes].sort((a, b) => b.length - a.length);

  for (const type of sortedTypes) {
    if (desc.includes(type.toLowerCase())) {
      return type;
    }
  }

  // 常见动作关键词库（用于识别未在运动分析中出现的动作）
  const commonKeywords = [
    ['深蹲', ['深蹲', 'squat']],
    ['硬拉', ['硬拉', 'deadlift']],
    ['卧推', ['卧推', 'bench']],
    ['引体向上', ['引体', 'pullup', 'pull-up']],
    ['双力臂', ['双力臂', 'muscle up', 'muscle-up']],
    ['推举', ['推举', '借力推', '肩推', 'press']],
    ['划船', ['划船', 'row']],
    ['弯举', ['弯举', 'curl']],
    ['臂屈伸', ['臂屈伸', 'dip']],
    ['核心', ['核心', '卷腹', '平板', 'plank']]
  ];

  for (const [type, keywords] of commonKeywords) {
    for (const keyword of keywords) {
      if (desc.includes(keyword.toLowerCase())) {
        return type;
      }
    }
  }

  return '其他';
}

// 按动作类型分组视频
function groupVideosByExercise(data) {
  const exerciseTypes = extractExerciseTypes(data);
  const groups = {};

  for (const video of data.compare_form_videos) {
    const type = classifyExerciseDynamic(video.description, exerciseTypes);
    if (!groups[type]) {
      groups[type] = [];
    }
    groups[type].push(video);
  }

  // 按数量排序，但"其他"放到最后
  const sorted = Object.entries(groups)
    .filter(([type]) => type !== '其他')
    .sort((a, b) => b[1].length - a[1].length);

  if (groups['其他']) {
    sorted.push(['其他', groups['其他']]);
  }

  return sorted.reduce((obj, [key, value]) => {
    obj[key] = value;
    return obj;
  }, {});
}

function loadData(filename) {
  const content = fs.readFileSync(filename, 'utf8');
  return JSON.parse(content).data;
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleString('zh-CN');
}

function truncate(str, maxLen = 50) {
  if (!str) return 'N/A';
  return str.length > maxLen ? str.substring(0, maxLen) + '...' : str;
}

function createTable(headers, rows) {
  // 计算列宽
  const colWidths = headers.map((h, i) => {
    const maxDataWidth = rows.reduce((max, row) => {
      const cell = String(row[i] || '');
      return Math.max(max, cell.length);
    }, 0);
    return Math.max(h.length, maxDataWidth) + 2;
  });

  // 创建分隔线
  const line = '+' + colWidths.map(w => '-'.repeat(w)).join('+') + '+';

  // 创建表头
  const headerRow = '|' + headers.map((h, i) => ' ' + h.padEnd(colWidths[i] - 1)).join('|') + '|';

  // 创建数据行
  const dataRows = rows.map(row => {
    return '|' + row.map((cell, i) => ' ' + String(cell || '').padEnd(colWidths[i] - 1)).join('|') + '|';
  });

  return [line, headerRow, line, ...dataRows, line].join('\n');
}

function printUserTable(data) {
  const user = data.user;
  const profile = user.profile || {};

  console.log('\n## 用户信息\n');
  const headers = ['字段', '值'];
  const rows = [
    ['邮箱', user.email],
    ['昵称', profile.nickname || 'N/A'],
    ['性别', profile.gender === 'male' ? '男' : profile.gender === 'female' ? '女' : 'N/A'],
    ['VIP状态', profile.vip || '普通'],
    ['身高', (profile.height || 'N/A') + ' cm'],
    ['体重', (profile.weight || 'N/A') + ' kg'],
    ['体脂率', (profile.body_fat || 'N/A') + ' %'],
    ['目标', profile.eat_target || 'N/A'],
    ['Token余额', profile.token || 0]
  ];
  console.log(createTable(headers, rows));
}

function printMotionAnalysisTable(data) {
  console.log('\n## 运动分析记录 (' + data.motion_analysis.length + '条)\n');

  if (data.motion_analysis.length === 0) {
    console.log('暂无运动分析数据\n');
    return;
  }

  const headers = ['序号', '动作名称', '帧数', '时长(秒)', '分析日期'];
  const rows = data.motion_analysis.map((ma, i) => [
    i + 1,
    ma.exercise_name,
    ma.frame_count,
    ma.total_time?.toFixed(2) || 'N/A',
    formatDate(ma.created_at)
  ]);

  console.log(createTable(headers, rows));

  console.log('\n**视频链接**:');
  data.motion_analysis.forEach((ma, i) => {
    console.log(`${i + 1}. ${ma.video_url}`);
  });
}

function printCompareVideosByGroup(data, limitPerGroup = 10) {
  const grouped = groupVideosByExercise(data);

  console.log('\n' + '='.repeat(60));
  console.log('📊 对比视频统计（按动作类型分组）');
  console.log('='.repeat(60));

  // 统计概览
  const headers = ['动作类型', '视频数量'];
  const rows = Object.entries(grouped).map(([type, videos]) => [type, videos.length]);
  console.log('\n' + createTable(headers, rows));

  // 各组详情
  console.log('\n' + '='.repeat(60));
  console.log('📹 各动作类型详情（每组显示最新 ' + limitPerGroup + ' 条）');
  console.log('='.repeat(60));

  for (const [type, videos] of Object.entries(grouped)) {
    console.log(`\n## ${type} (${videos.length}条)\n`);

    const displayVideos = videos.slice(0, limitPerGroup);
    const headers = ['序号', '训练描述', '上传日期'];
    const rows = displayVideos.map((video, i) => [
      i + 1,
      truncate(video.description || '无描述', 35),
      formatDate(video.created_at)
    ]);

    console.log(createTable(headers, rows));

    console.log('\n视频链接:');
    displayVideos.forEach((video, i) => {
      console.log(`  ${i + 1}. ${video.video_url}`);
    });
  }
}

function generateMarkdownReport(data, outputFile = 'vtrain_report.md') {
  const user = data.user;
  const profile = user.profile || {};
  const grouped = groupVideosByExercise(data);

  let md = '# V-Train 用户数据报告\n\n';
  md += `**导出时间**: ${formatDate(data.exported_at)}\n\n`;

  // 用户信息
  md += '## 用户信息\n\n';
  md += '| 字段 | 值 |\n';
  md += '|------|-----|\n';
  md += `| 邮箱 | ${user.email} |\n`;
  md += `| 昵称 | ${profile.nickname || 'N/A'} |\n`;
  md += `| 性别 | ${profile.gender === 'male' ? '男' : profile.gender === 'female' ? '女' : 'N/A'} |\n`;
  md += `| VIP状态 | ${profile.vip || '普通'} |\n`;
  md += `| 身高 | ${profile.height || 'N/A'} cm |\n`;
  md += `| 体重 | ${profile.weight || 'N/A'} kg |\n`;
  md += `| 体脂率 | ${profile.body_fat || 'N/A'} % |\n`;
  md += `| 目标 | ${profile.eat_target || 'N/A'} |\n`;
  md += `| Token余额 | ${profile.token || 0} |\n\n`;

  // 运动分析
  md += `## 运动分析记录 (${data.motion_analysis.length}条)\n\n`;
  if (data.motion_analysis.length > 0) {
    md += '| 序号 | 动作名称 | 帧数 | 时长(秒) | 分析日期 |\n';
    md += '|------|----------|------|----------|----------|\n';
    data.motion_analysis.forEach((ma, i) => {
      md += `| ${i + 1} | ${ma.exercise_name} | ${ma.frame_count} | ${ma.total_time?.toFixed(2) || 'N/A'} | ${formatDate(ma.created_at)} |\n`;
    });
    md += '\n**视频链接**:\n\n';
    data.motion_analysis.forEach((ma, i) => {
      md += `${i + 1}. [${ma.exercise_name}](${ma.video_url})\n`;
    });
  } else {
    md += '暂无运动分析数据\n';
  }
  md += '\n';

  // 对比视频 - 按动作类型分组
  md += `## 对比视频记录（按动作类型分组，共${data.compare_form_videos.length}条）\n\n`;

  // 统计概览
  md += '### 动作类型统计\n\n';
  md += '| 动作类型 | 视频数量 |\n';
  md += '|----------|----------|\n';
  for (const [type, videos] of Object.entries(grouped)) {
    md += `| ${type} | ${videos.length} |\n`;
  }
  md += '\n';

  // 各组详情
  for (const [type, videos] of Object.entries(grouped)) {
    if (type === '其他') continue;

    md += `### ${type} (${videos.length}条)\n\n`;
    md += '| 序号 | 训练描述 | 上传日期 |\n';
    md += '|------|----------|----------|\n';

    videos.slice(0, 20).forEach((video, i) => {
      md += `| ${i + 1} | ${video.description || '无描述'} | ${formatDate(video.created_at)} |\n`;
    });

    md += '\n**视频链接**:\n\n';
    videos.slice(0, 20).forEach((video, i) => {
      md += `${i + 1}. [${truncate(video.description || '无描述', 30)}](${video.video_url})\n`;
    });
    md += '\n';
  }

  // 未分类视频
  if (grouped['其他'] && grouped['其他'].length > 0) {
    md += `### 未分类/其他 (${grouped['其他'].length}条)\n\n`;
    md += '| 序号 | 训练描述 | 上传日期 |\n';
    md += '|------|----------|----------|\n';

    grouped['其他'].slice(0, 20).forEach((video, i) => {
      md += `| ${i + 1} | ${video.description || '无描述'} | ${formatDate(video.created_at)} |\n`;
    });

    md += '\n**视频链接**:\n\n';
    grouped['其他'].slice(0, 20).forEach((video, i) => {
      md += `${i + 1}. [${truncate(video.description || '无描述', 30)}](${video.video_url})\n`;
    });
  }

  fs.writeFileSync(outputFile, md, 'utf8');
  console.log(`\n✅ Markdown 报告已保存到: ${outputFile}`);
}

function main() {
  const filename = process.argv[2] || 'vtrain_user_data.json';

  try {
    console.log('📊 正在加载数据...');
    const data = loadData(filename);

    // 打印表格到控制台
    printUserTable(data);
    printMotionAnalysisTable(data);
    printCompareVideosByGroup(data, 10);

    // 生成 Markdown 报告
    generateMarkdownReport(data, 'vtrain_report.md');

    console.log('\n✅ 表格化展示完成！');

  } catch (err) {
    console.error('❌ 错误:', err.message);
    console.log('使用方法: node table_view.js [json文件路径]');
  }
}

main();
