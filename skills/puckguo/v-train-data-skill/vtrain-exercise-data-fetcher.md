# V-Train Exercise Data Fetcher

这个技能允许 agent 通过用户邮箱和密码直接鉴权，一次性获取 V-Train 用户的所有运动数据和视频信息并下载到本地。

## API 端点

使用邮箱和密码直接鉴权，一次性获取所有运动数据：

```bash
POST https://puckg.fun/api/agent/user-data
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

### 返回数据结构

```json
{
  "success": true,
  "data": {
    "user": {
      "id": "user_uuid",
      "email": "user@example.com",
      "profile": {
        "id": "profile_id",
        "username": "username",
        "nickname": "昵称",
        "avatar_url": "头像URL",
        "gender": "male",
        "vip": "vip",
        "token": 99839,
        "height": "186",
        "weight": "86",
        "body_fat": "13",
        "eat_target": "增肌"
      }
    },
    "motion_analysis": [
      {
        "id": "analysis_id",
        "user_id": "user_id",
        "exercise_name": "硬拉",
        "video_url": "https://exercise-videos-aliyun.oss-cn-beijing.aliyuncs.com/...",
        "frame_count": 22,
        "total_time": 5.57,
        "joint_angles": {},
        "shoulder_angles": [],
        "elbow_angles": [],
        "knee_angles": [],
        "hip_angles": [],
        "shoulder_velocities": [],
        "elbow_velocities": [],
        "knee_velocities": [],
        "hip_velocities": [],
        "created_at": "2025-06-15T07:52:35.717Z"
      }
    ],
    "compare_form_videos": [
      {
        "id": "video_id",
        "user_id": "user_id",
        "exercise_id": "exercise_id",
        "video_url": "https://exercise-videos-aliyun.oss-cn-beijing.aliyuncs.com/...",
        "thumbnail_url": "https://exercise-videos-aliyun.oss-cn-beijing.aliyuncs.com/...",
        "description": "爆发深蹲 追求速度",
        "is_temporary": false,
        "created_at": "2026-03-10T10:08:08.757Z"
      }
    ],
    "exported_at": "2026-03-11T00:00:00Z"
  }
}
```

## 数据说明

### motion_analysis (运动分析数据)
用户上传的动作分析数据，包含：
- `exercise_name`: 动作名称（如：硬拉、深蹲、卧推等）
- `video_url`: 视频URL
- `frame_count`: 帧数
- `total_time`: 总时长（秒）
- `joint_angles`: 关节角度数据
- 各种关节角度和速度数据

### compare_form_videos (对比视频数据)
用户上传的健身打卡视频，包含：
- `video_url`: 视频URL
- `thumbnail_url`: 缩略图URL
- `description`: 视频描述/训练笔记
- `exercise_id`: 关联的练习ID
- `created_at`: 上传时间

## 使用示例

### Python 示例

```python
import requests
import json

BASE_URL = "https://puckg.fun"

def fetch_user_data(email, password):
    """使用邮箱和密码获取所有用户运动数据"""
    response = requests.post(
        f"{BASE_URL}/api/agent/user-data",
        headers={"Content-Type": "application/json"},
        json={"email": email, "password": password}
    )

    if not response.ok:
        error_data = response.json()
        raise Exception(error_data.get('message') or '获取数据失败')

    return response.json()

def save_to_file(data, filename):
    """保存数据到文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def print_summary(data):
    """打印数据摘要"""
    user = data['user']
    profile = user.get('profile', {})

    print(f"\n{'='*50}")
    print(f"用户: {profile.get('nickname') or user['email']}")
    print(f"{'='*50}")
    print(f"邮箱: {user['email']}")
    if profile:
        print(f"身高: {profile.get('height', 'N/A')} cm")
        print(f"体重: {profile.get('weight', 'N/A')} kg")
        print(f"体脂率: {profile.get('body_fat', 'N/A')}%")
        print(f"目标: {profile.get('eat_target', 'N/A')}")

    print(f"\n{'='*50}")
    print("数据统计")
    print(f"{'='*50}")
    print(f"运动分析记录: {len(data['motion_analysis'])} 条")
    print(f"对比视频记录: {len(data['compare_form_videos'])} 条")
    print(f"导出时间: {data['exported_at']}")

    # 显示最近的运动分析
    if data['motion_analysis']:
        print(f"\n运动分析:")
        for ma in data['motion_analysis'][:5]:
            print(f"  - {ma['exercise_name']}: {ma['video_url']}")

    # 显示最近的视频
    if data['compare_form_videos']:
        print(f"\n对比视频 (最新5条):")
        for video in data['compare_form_videos'][:5]:
            desc = video.get('description') or '无描述'
            print(f"  - {desc}: {video['video_url']}")

def main():
    email = "user@example.com"
    password = "password123"

    try:
        print("正在获取用户数据...")
        result = fetch_user_data(email, password)

        if result['success']:
            data = result['data']

            # 保存完整数据
            save_to_file(data, "exercise_data.json")
            print("\n数据已保存到 exercise_data.json")

            # 打印摘要
            print_summary(data)
        else:
            print("获取数据失败:", result.get('message'))

    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    main()
```

### Node.js 示例

```javascript
import fs from 'fs';

async function fetchUserData(email, password) {
  const response = await fetch('https://puckg.fun/api/agent/user-data', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ email, password })
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || '获取数据失败');
  }

  return await response.json();
}

function saveDataToFile(data, filename) {
  fs.writeFileSync(filename, JSON.stringify(data, null, 2), 'utf-8');
}

function printSummary(data) {
  const user = data.user;
  const profile = user.profile || {};

  console.log('\n' + '='.repeat(50));
  console.log(`用户: ${profile.nickname || user.email}`);
  console.log('='.repeat(50));
  console.log(`邮箱: ${user.email}`);
  if (profile.nickname) {
    console.log(`身高: ${profile.height || 'N/A'} cm`);
    console.log(`体重: ${profile.weight || 'N/A'} kg`);
    console.log(`体脂率: ${profile.body_fat || 'N/A'}%`);
    console.log(`目标: ${profile.eat_target || 'N/A'}`);
  }

  console.log('\n' + '='.repeat(50));
  console.log('数据统计');
  console.log('='.repeat(50));
  console.log(`运动分析记录: ${data.motion_analysis.length} 条`);
  console.log(`对比视频记录: ${data.compare_form_videos.length} 条`);
  console.log(`导出时间: ${data.exported_at}`);

  if (data.motion_analysis.length > 0) {
    console.log('\n运动分析:');
    data.motion_analysis.slice(0, 5).forEach(ma => {
      console.log(`  - ${ma.exercise_name}: ${ma.video_url}`);
    });
  }

  if (data.compare_form_videos.length > 0) {
    console.log('\n对比视频 (最新5条):');
    data.compare_form_videos.slice(0, 5).forEach(video => {
      const desc = video.description || '无描述';
      console.log(`  - ${desc}: ${video.video_url}`);
    });
  }
}

async function main() {
  const email = 'user@example.com';
  const password = 'password123';

  try {
    console.log('正在获取用户数据...');
    const result = await fetchUserData(email, password);

    if (result.success) {
      // 保存完整数据
      saveDataToFile(result.data, 'exercise-data.json');
      console.log('\n数据已保存到 exercise-data.json');

      // 打印数据摘要
      printSummary(result.data);
    } else {
      console.error('获取数据失败:', result.message);
    }
  } catch (error) {
    console.error('错误:', error.message);
  }
}

main();
```

### cURL 示例

```bash
curl -X POST https://puckg.fun/api/agent/user-data \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }' \
  > exercise_data.json
```

## 数据表格化展示

获取 JSON 数据后，可以使用以下脚本将其转换为易读的表格格式。

### Node.js 表格化脚本

```javascript
import fs from 'fs';

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

  // 常见动作关键词库
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

function generateMarkdownReport(data, outputFile = 'exercise_report.md') {
  const user = data.user;
  const profile = user.profile || {};
  const grouped = groupVideosByExercise(data);

  let md = '# V-Train 运动数据报告\n\n';
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
  const filename = process.argv[2] || 'exercise_data.json';

  try {
    console.log('📊 正在加载数据...');
    const data = loadData(filename);

    // 打印表格到控制台
    printUserTable(data);
    printMotionAnalysisTable(data);
    printCompareVideosByGroup(data, 10);

    // 生成 Markdown 报告
    generateMarkdownReport(data, 'exercise_report.md');

    console.log('\n✅ 表格化展示完成！');

  } catch (err) {
    console.error('❌ 错误:', err.message);
    console.log('使用方法: node table_view.js [json文件路径]');
  }
}

main();
```

### Python 表格化脚本

```python
import json
import re
from datetime import datetime
from collections import defaultdict

def load_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)['data']

def format_date(date_str):
    dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def truncate(text, max_len=50):
    if not text:
        return 'N/A'
    return text if len(text) <= max_len else text[:max_len] + '...'

# 动态提取数据中的动作类型
def extract_exercise_types(data):
    types = set()

    # 从运动分析中提取动作名称
    for ma in data['motion_analysis']:
        if ma.get('exercise_name'):
            types.add(ma['exercise_name'])

    return list(types)

# 根据描述识别动作类型（动态匹配）
def classify_exercise_dynamic(description, exercise_types):
    if not description:
        return '其他'
    desc = description.lower()

    # 按长度降序匹配，优先匹配更具体的动作名称
    sorted_types = sorted(exercise_types, key=len, reverse=True)

    for exercise_type in sorted_types:
        if exercise_type.lower() in desc:
            return exercise_type

    # 常见动作关键词库
    common_keywords = [
        ('深蹲', ['深蹲', 'squat']),
        ('硬拉', ['硬拉', 'deadlift']),
        ('卧推', ['卧推', 'bench']),
        ('引体向上', ['引体', 'pullup', 'pull-up']),
        ('双力臂', ['双力臂', 'muscle up', 'muscle-up']),
        ('推举', ['推举', '借力推', '肩推', 'press']),
        ('划船', ['划船', 'row']),
        ('弯举', ['弯举', 'curl']),
        ('臂屈伸', ['臂屈伸', 'dip']),
        ('核心', ['核心', '卷腹', '平板', 'plank'])
    ]

    for exercise_type, keywords in common_keywords:
        for keyword in keywords:
            if keyword.lower() in desc:
                return exercise_type

    return '其他'

# 按动作类型分组视频
def group_videos_by_exercise(data):
    exercise_types = extract_exercise_types(data)
    groups = defaultdict(list)

    for video in data['compare_form_videos']:
        exercise_type = classify_exercise_dynamic(video.get('description'), exercise_types)
        groups[exercise_type].append(video)

    # 按数量排序，但"其他"放到最后
    sorted_groups = sorted(
        [(k, v) for k, v in groups.items() if k != '其他'],
        key=lambda x: len(x[1]),
        reverse=True
    )

    if '其他' in groups:
        sorted_groups.append(('其他', groups['其他']))

    return dict(sorted_groups)

def create_table(headers, rows):
    """创建 Markdown 表格"""
    col_widths = []
    for i, header in enumerate(headers):
        max_data_width = max(len(str(row[i])) for row in rows) if rows else 0
        col_widths.append(max(len(header), max_data_width))

    lines = []
    # 表头
    header_line = '| ' + ' | '.join(h.ljust(col_widths[i]) for i, h in enumerate(headers)) + ' |'
    lines.append(header_line)
    # 分隔线
    sep_line = '|' + '|'.join('-' * (w + 2) for w in col_widths) + '|'
    lines.append(sep_line)
    # 数据行
    for row in rows:
        row_line = '| ' + ' | '.join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)) + ' |'
        lines.append(row_line)

    return '\n'.join(lines)

def print_user_table(data):
    user = data['user']
    profile = user.get('profile', {})

    print('\n## 用户信息\n')
    headers = ['字段', '值']
    rows = [
        ['邮箱', user['email']],
        ['昵称', profile.get('nickname', 'N/A')],
        ['性别', '男' if profile.get('gender') == 'male' else '女' if profile.get('gender') == 'female' else 'N/A'],
        ['VIP状态', profile.get('vip', '普通')],
        ['身高', f"{profile.get('height', 'N/A')} cm"],
        ['体重', f"{profile.get('weight', 'N/A')} kg"],
        ['体脂率', f"{profile.get('body_fat', 'N/A')} %"],
        ['目标', profile.get('eat_target', 'N/A')],
        ['Token余额', profile.get('token', 0)]
    ]
    print(create_table(headers, rows))

def print_motion_analysis_table(data):
    print(f"\n## 运动分析记录 ({len(data['motion_analysis'])}条)\n")

    if not data['motion_analysis']:
        print('暂无运动分析数据\n')
        return

    headers = ['序号', '动作名称', '帧数', '时长(秒)', '分析日期']
    rows = []
    for i, ma in enumerate(data['motion_analysis'], 1):
        rows.append([
            i,
            ma['exercise_name'],
            ma['frame_count'],
            f"{ma['total_time']:.2f}" if ma.get('total_time') else 'N/A',
            format_date(ma['created_at'])
        ])
    print(create_table(headers, rows))

    print('\n**视频链接**:')
    for i, ma in enumerate(data['motion_analysis'], 1):
        print(f"{i}. {ma['video_url']}")

def print_compare_videos_by_group(data, limit_per_group=10):
    grouped = group_videos_by_exercise(data)

    print('\n' + '=' * 60)
    print('📊 对比视频统计（按动作类型分组）')
    print('=' * 60)

    # 统计概览
    headers = ['动作类型', '视频数量']
    rows = [[exercise_type, len(videos)] for exercise_type, videos in grouped.items()]
    print('\n' + create_table(headers, rows))

    # 各组详情
    print('\n' + '=' * 60)
    print(f'📹 各动作类型详情（每组显示最新 {limit_per_group} 条）')
    print('=' * 60)

    for exercise_type, videos in grouped.items():
        print(f"\n## {exercise_type} ({len(videos)}条)\n")

        display_videos = videos[:limit_per_group]
        headers = ['序号', '训练描述', '上传日期']
        rows = []
        for i, video in enumerate(display_videos, 1):
            rows.append([
                i,
                truncate(video.get('description', '无描述'), 35),
                format_date(video['created_at'])
            ])
        print(create_table(headers, rows))

        # 打印视频链接
        print('\n视频链接:')
        for i, video in enumerate(display_videos, 1):
            print(f"  {i}. {video['video_url']}")

def generate_markdown_report(data, output_file='exercise_report.md'):
    user = data['user']
    profile = user.get('profile', {})
    grouped = group_videos_by_exercise(data)

    md = '# V-Train 运动数据报告\n\n'
    md += f"**导出时间**: {format_date(data['exported_at'])}\n\n"

    # 用户信息
    md += '## 用户信息\n\n'
    md += '| 字段 | 值 |\n'
    md += '|------|-----|\n'
    md += f"| 邮箱 | {user['email']} |\n"
    md += f"| 昵称 | {profile.get('nickname', 'N/A')} |\n"
    md += f"| 性别 | {'男' if profile.get('gender') == 'male' else '女' if profile.get('gender') == 'female' else 'N/A'} |\n"
    md += f"| VIP状态 | {profile.get('vip', '普通')} |\n"
    md += f"| 身高 | {profile.get('height', 'N/A')} cm |\n"
    md += f"| 体重 | {profile.get('weight', 'N/A')} kg |\n"
    md += f"| 体脂率 | {profile.get('body_fat', 'N/A')} % |\n"
    md += f"| 目标 | {profile.get('eat_target', 'N/A')} |\n"
    md += f"| Token余额 | {profile.get('token', 0)} |\n\n"

    # 运动分析
    md += f"## 运动分析记录 ({len(data['motion_analysis'])}条)\n\n"
    if data['motion_analysis']:
        md += '| 序号 | 动作名称 | 帧数 | 时长(秒) | 分析日期 |\n'
        md += '|------|----------|------|----------|----------|\n'
        for i, ma in enumerate(data['motion_analysis'], 1):
            md += f"| {i} | {ma['exercise_name']} | {ma['frame_count']} | {ma.get('total_time', 'N/A')} | {format_date(ma['created_at'])} |\n"
        md += '\n**视频链接**:\n\n'
        for i, ma in enumerate(data['motion_analysis'], 1):
            md += f"{i}. [{ma['exercise_name']}]({ma['video_url']})\n"
    else:
        md += '暂无运动分析数据\n'
    md += '\n'

    # 对比视频 - 按动作类型分组
    md += f"## 对比视频记录（按动作类型分组，共{len(data['compare_form_videos'])}条）\n\n"

    # 统计概览
    md += '### 动作类型统计\n\n'
    md += '| 动作类型 | 视频数量 |\n'
    md += '|----------|----------|\n'
    for exercise_type, videos in grouped.items():
        md += f"| {exercise_type} | {len(videos)} |\n"
    md += '\n'

    # 各组详情
    for exercise_type, videos in grouped.items():
        if exercise_type == '其他':
            continue  # 其他放到最后

        md += f"### {exercise_type} ({len(videos)}条)\n\n"
        md += '| 序号 | 训练描述 | 上传日期 |\n'
        md += '|------|----------|----------|\n'

        for i, video in enumerate(videos[:20], 1):
            md += f"| {i} | {video.get('description', '无描述')} | {format_date(video['created_at'])} |\n"

        md += '\n**视频链接**:\n\n'
        for i, video in enumerate(videos[:20], 1):
            md += f"{i}. [{truncate(video.get('description', '无描述'), 30)}]({video['video_url']})\n"
        md += '\n'

    # 未分类视频
    if '其他' in grouped and grouped['其他']:
        md += f"### 未分类/其他 ({len(grouped['其他'])}条)\n\n"
        md += '| 序号 | 训练描述 | 上传日期 |\n'
        md += '|------|----------|----------|\n'

        for i, video in enumerate(grouped['其他'][:20], 1):
            md += f"| {i} | {video.get('description', '无描述')} | {format_date(video['created_at'])} |\n"

        md += '\n**视频链接**:\n\n'
        for i, video in enumerate(grouped['其他'][:20], 1):
            md += f"{i}. [{truncate(video.get('description', '无描述'), 30)}]({video['video_url']})\n"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(md)
    print(f'\n✅ Markdown 报告已保存到: {output_file}')

def main():
    import sys
    filename = sys.argv[1] if len(sys.argv) > 1 else 'exercise_data.json'

    try:
        print('📊 正在加载数据...')
        data = load_data(filename)

        # 打印表格到控制台
        print_user_table(data)
        print_motion_analysis_table(data)
        print_compare_videos_by_group(data, 10)

        # 生成 Markdown 报告
        generate_markdown_report(data, 'exercise_report.md')

        print('\n✅ 表格化展示完成！')

    except Exception as e:
        print(f'❌ 错误: {e}')
        print('使用方法: python table_view.py [json文件路径]')

if __name__ == '__main__':
    main()
```

### 使用方法

**Node.js:**
```bash
node table_view.js exercise_data.json
```

**Python:**
```bash
python table_view.py exercise_data.json
```

### 输出示例

```
## 用户信息

+----------+------------------+
| 字段     | 值               |
+----------+------------------+
| 邮箱     | 979245542@qq.com |
| 昵称     | puck             |
| 性别     | 男               |
| VIP状态  | vip              |
| 身高     | 186 cm           |
| 体重     | 86 kg            |
| 体脂率   | 13 %             |
| 目标     | 增肌             |
| Token余额| 99839            |
+----------+------------------+

## 运动分析记录 (1条)

+----+------+----+-------+--------------------+
| 序号 | 动作名称 | 帧数 | 时长(秒) | 分析日期         |
+----+------+----+-------+--------------------+
| 1  | 硬拉 | 22 | 5.57  | 2025/6/15 15:52:35 |
+----+------+----+-------+--------------------+

============================================================
📊 对比视频统计（按动作类型分组）
============================================================

+----------+----------+
| 动作类型 | 视频数量 |
+----------+----------+
| 深蹲     | 35       |
| 硬拉     | 28       |
| 卧推     | 15       |
| 引体向上 | 12       |
| 双力臂   | 8        |
| 推举     | 7        |
| 其他     | 6        |
+----------+----------+
```

同时会生成 `exercise_report.md` 文件，方便查看和分享。

### 动作类型识别规则

系统通过以下方式**动态识别**动作类型：

1. **从运动分析数据中提取**：自动提取 `motion_analysis` 中的 `exercise_name` 作为已知动作类型

2. **智能匹配**：根据视频描述中的关键词匹配动作类型：
   - 优先匹配运动分析中出现的动作名称（如"硬拉"、"深蹲"等）
   - 其次匹配常见动作关键词（深蹲、squat、硬拉、deadlift、卧推、bench 等）

3. **分组展示**：将识别到的视频按动作类型分组，按数量降序排列，未分类的归入"其他"

## HTML 可视化查看器

提供了一个独立的 HTML 文件 `vtrain_viewer.html`，用于可视化展示动作数据。

### 功能特性

- **文件上传**：支持上传 JSON 数据文件
- **示例数据**：内置示例数据，方便预览效果
- **动作筛选**：
  - 按动作类型筛选
  - 按描述关键词搜索
  - 按日期范围筛选
  - 多种排序方式（日期、类型）
- **视频懒加载**：
  - 页面不预加载视频
  - 点击播放按钮后才加载视频
  - 减少页面初始加载时间
- **统计面板**：
  - 显示各动作类型视频数量
  - 点击统计卡片快速筛选
- **用户体验**：
  - 响应式设计，支持移动端
  - 搜索关键词高亮显示
  - 返回顶部按钮
  - 复制/下载视频链接

### 使用方法

1. **获取数据文件**：
```bash
curl -X POST https://puckg.fun/api/agent/user-data \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}' \
  > exercise_data.json
```

2. **打开 HTML 文件**：
   - 双击 `vtrain_viewer.html` 文件
   - 或在浏览器中打开该文件

3. **上传数据**：
   - 点击 "选择 JSON 文件" 按钮
   - 选择下载的数据文件

4. **筛选和查看**：
   - 使用筛选栏过滤视频
   - 点击统计卡片按动作类型筛选
   - 点击视频缩略图播放视频

### 界面预览

```
┌─────────────────────────────────────────────────────┐
│  🏋️ V-Train 动作数据中心                              │
│  导出时间: 2026/3/11 14:28:05                        │
└─────────────────────────────────────────────────────┘

┌──────────┬──────────┬──────────┬──────────┐
│  全部视频  │   硬拉    │   深蹲    │  引体向上 │
│    111   │    10    │    8     │    8     │
└──────────┴──────────┴──────────┴──────────┘

筛选: [全部动作 ▼] [搜索描述...] [开始日期] [结束日期] [排序 ▼]

┌─────────────────────────────────────────────────────┐
│ 硬拉 (10个视频)                                      │
├─────────────────────────────────────────────────────┤
│ ┌───────────────┐  ┌───────────────┐               │
│ │   ▶ 播放      │  │   ▶ 播放      │               │
│ │  (占位图)     │  │  (占位图)     │               │
│ └───────────────┘  └───────────────┘               │
│ 硬拉170kg 5x3        超程硬拉练底部启动              │
│ 📅 2026/1/9          📅 2026/1/18                   │
└─────────────────────────────────────────────────────┘
```

## 测试结果

使用 `979245542@qq.com` 测试的结果：
- **用户**: puck (VIP用户)
- **运动分析记录**: 1 条
  - 硬拉视频分析
- **对比视频记录**: 111 条
  - 包含深蹲、硬拉、卧推、双力臂等训练视频
  - 每条视频都有描述、视频URL和缩略图

## 错误处理

### 400 Bad Request
```json
{
  "success": false,
  "data": null,
  "message": "Email and password are required"
}
```

### 401 Unauthorized
```json
{
  "success": false,
  "data": null,
  "message": "Invalid email or password"
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "data": null,
  "message": "Error message here"
}
```

## 配套工具文件

本技能包含以下配套工具文件，位于 `skills/` 目录中：

### 1. table_view.js

**文件路径**: `skills/table_view.js`

**功能**: Node.js 脚本，用于将 JSON 数据转换为易读的表格格式

**使用方法**:
```bash
node skills/table_view.js exercise_data.json
```

**输出**:
- 控制台表格展示
- 生成 `exercise_report.md` 报告文件

---

### 2. vtrain_viewer.html

**文件路径**: `skills/vtrain_viewer.html`

**功能**: 可视化 HTML 查看器，支持视频懒加载和筛选

**使用方法**:
1. 在浏览器中打开 `skills/vtrain_viewer.html`
2. 上传 JSON 数据文件
3. 使用筛选功能查看视频

**特性**:
- 视频懒加载（点击后加载）
- 按动作类型筛选
- 关键词搜索
- 日期范围筛选
- 响应式设计
