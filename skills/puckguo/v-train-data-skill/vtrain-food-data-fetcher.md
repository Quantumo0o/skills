# V-Train Food Data Fetcher

这个技能允许 agent 通过用户邮箱和密码直接鉴权，获取 V-Train 用户的饮食记录数据，支持按日期区间查询和餐型筛选。

## 快速开始

### 完整流程示例

```python
import requests
import json
import re
from datetime import datetime, timedelta

BASE_URL = "https://puckg.fun"

def fetch_user_data(email, password):
    """使用邮箱和密码获取用户基本信息"""
    response = requests.post(
        f"{BASE_URL}/api/agent/user-data",
        headers={"Content-Type": "application/json"},
        json={"email": email, "password": password}
    )
    return response.json()

def fetch_food_data(user_id, start_date=None, end_date=None, meal_type=None):
    """获取用户食物数据"""
    payload = {"userId": user_id}
    if start_date:
        payload["startDate"] = start_date
    if end_date:
        payload["endDate"] = end_date
    if meal_type:
        payload["mealType"] = meal_type

    response = requests.post(
        f"{BASE_URL}/api/food/analysis/by-date-range",
        headers={"Content-Type": "application/json"},
        json=payload
    )
    return response.json()

def generate_food_report(food_data, user_email, date_range, output_file):
    """生成食物数据HTML报告"""
    # 读取模板
    with open('skills/food_viewer_template.html', 'r', encoding='utf-8') as f:
        template = f.read()

    # 替换数据
    food_data_json = json.dumps(food_data, ensure_ascii=False, indent=4)

    # 使用正则替换 FOOD_DATA
    pattern = r'const FOOD_DATA = \{[\s\S]*?\};'
    replacement = f'const FOOD_DATA = {food_data_json};'
    template = re.sub(pattern, replacement, template)

    # 替换用户信息
    template = template.replace(
        'const USER_EMAIL = "user@example.com";',
        f'const USER_EMAIL = "{user_email}";'
    )

    # 替换日期范围
    template = template.replace(
        'const DATE_RANGE = {\n            start: "2026-01-01",\n            end: "2026-01-31"\n        };',
        f'const DATE_RANGE = {{\n            start: "{date_range[0]}",\n            end: "{date_range[1]}"\n        }};'
    )

    # 保存报告
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(template)

    print(f'✅ 报告已生成: {output_file}')

# 使用示例
def main():
    email = 'user@example.com'
    password = 'password123'

    # 1. 获取用户数据
    print("正在获取用户信息...")
    user_result = fetch_user_data(email, password)

    if not user_result.get('success'):
        print(f"登录失败: {user_result.get('message')}")
        return

    user_id = user_result['data']['user']['id']
    print(f"✅ 登录成功，用户ID: {user_id}")

    # 2. 获取本月食物数据
    now = datetime.now()
    start_of_month = now.replace(day=1).strftime('%Y-%m-%d')
    end_of_month = (now.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    end_of_month = end_of_month.strftime('%Y-%m-%d')

    print(f"\n正在获取 {start_of_month} 至 {end_of_month} 的食物数据...")
    food_result = fetch_food_data(user_id, start_of_month, end_of_month)

    if food_result.get('success') and food_result.get('data'):
        data = food_result['data']

        # 打印摘要
        print(f"\n{'='*60}")
        print(f"📊 食物数据摘要")
        print(f"{'='*60}")
        print(f"总记录数: {data['totalCount']}")
        print(f"总热量: {data['totalCalories']} kcal")

        print(f"\n{'='*60}")
        print(f"🍽️ 按餐型统计")
        print(f"{'='*60}")
        for meal_type, stat in data['stats'].items():
            print(f"{meal_type}: {stat['count']} 餐, {stat['totalCalories']} kcal")

        # 3. 生成HTML报告
        output_file = f'food_report_{email.split("@")[0]}_{start_of_month}.html'
        generate_food_report(data, email, (start_of_month, end_of_month), output_file)

        # 4. 保存JSON数据
        with open(f'food_data_{start_of_month}.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ 数据已保存: food_data_{start_of_month}.json")
    else:
        print(f"获取食物数据失败: {food_result.get('message')}")

if __name__ == '__main__':
    main()
```

## API 端点

### 获取用户基本信息

使用邮箱和密码鉴权，获取用户ID和基本信息：

```bash
POST https://puckg.fun/api/agent/user-data
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**返回数据结构**:
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "user_uuid",
      "email": "user@example.com",
      "profile": {
        "nickname": "昵称",
        "height": "186",
        "weight": "86",
        "body_fat": "13",
        "eat_target": "增肌"
      }
    }
  }
}
```

### 获取食物数据

使用用户ID，按日期区间获取食物数据：

```bash
POST https://puckg.fun/api/food/analysis/by-date-range
Content-Type: application/json

{
  "userId": "user_uuid",
  "startDate": "2026-01-01",
  "endDate": "2026-01-31",
  "mealType": "早餐"
}
```

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| userId | string | 是 | 用户UUID |
| startDate | string | 否 | 开始日期 (yyyy-MM-dd) |
| endDate | string | 否 | 结束日期 (yyyy-MM-dd) |
| mealType | string | 否 | 餐型筛选：早餐/breakfast、午餐/lunch、晚餐/dinner、零食/snack、甜品/dessert、夜宵/midnight snack、正餐/mainMeal |

### 返回数据结构

```json
{
  "success": true,
  "data": {
    "analyses": [
      {
        "id": "analysis_id",
        "user_id": "user_id",
        "meal_type": "早餐",
        "meal_date": "2026-01-15",
        "description": "燕麦牛奶",
        "food_items": [
          { "name": "燕麦", "description": "50g" },
          { "name": "牛奶", "description": "250ml" }
        ],
        "calories": "320",
        "ai_analysis": {
          "carbohydrates": "45g",
          "fat": "8g",
          "protein": "12g",
          "fiber": "5g",
          "vitamins_and_minerals": "富含维生素B族和钙"
        },
        "next_meal_recommendation": [
          "建议午餐增加蛋白质摄入",
          "适量增加蔬菜"
        ],
        "image_urls": [
          "https://exercise-videos-aliyun.oss-cn-beijing.aliyuncs.com/food/..."
        ],
        "status": "completed",
        "created_at": "2026-01-15T08:30:00.000Z"
      }
    ],
    "stats": {
      "早餐": {
        "count": 15,
        "totalCalories": 4800,
        "items": []
      },
      "午餐": {
        "count": 12,
        "totalCalories": 7200,
        "items": []
      }
    },
    "totalCount": 45,
    "totalCalories": 15600
  }
}
```

## 数据说明

### analyses (食物分析记录)

用户的食物记录，包含：
- `meal_type`: 餐型（早餐、午餐、晚餐、零食、甜品、夜宵、正餐）
- `meal_date`: 用餐日期
- `food_items`: 食物项目列表，每项包含名称和描述
- `calories`: 卡路里数值
- `ai_analysis`: AI分析的营养成分
  - `carbohydrates`: 碳水化合物
  - `fat`: 脂肪
  - `protein`: 蛋白质
  - `fiber`: 纤维
  - `vitamins_and_minerals`: 维生素和矿物质
- `next_meal_recommendation`: AI建议的下一餐建议
- `image_urls`: 食物图片URL数组
- `status`: 分析状态（processing/completed）

### stats (按餐型统计)

- `count`: 该餐型的记录数量
- `totalCalories`: 该餐型的总热量
- `items`: 该餐型的所有记录详情

## 使用示例

### Python 示例

```python
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "https://puckg.fun"

def fetch_user_data(email, password):
    """使用邮箱和密码获取用户基本信息"""
    response = requests.post(
        f"{BASE_URL}/api/agent/user-data",
        headers={"Content-Type": "application/json"},
        json={"email": email, "password": password}
    )
    return response.json()

def fetch_food_data(user_id, start_date=None, end_date=None, meal_type=None):
    """获取用户食物数据"""
    payload = {"userId": user_id}
    if start_date:
        payload["startDate"] = start_date
    if end_date:
        payload["endDate"] = end_date
    if meal_type:
        payload["mealType"] = meal_type

    response = requests.post(
        f"{BASE_URL}/api/food/analysis/by-date-range",
        headers={"Content-Type": "application/json"},
        json=payload
    )
    return response.json()

def print_food_summary(data):
    """打印食物数据摘要"""
    if not data.get('success') or not data.get('data'):
        print("获取食物数据失败")
        return

    analyses = data['data']['analyses']
    stats = data['data']['stats']
    total_count = data['data']['totalCount']
    total_calories = data['data']['totalCalories']

    print(f"\n{'='*60}")
    print(f"📊 食物记录统计")
    print(f"{'='*60}")
    print(f"总记录数: {total_count} 条")
    print(f"总热量: {total_calories} kcal")
    print(f"平均每餐: {total_calories // total_count if total_count > 0 else 0} kcal")

    print(f"\n{'='*60}")
    print(f"🍽️ 按餐型统计")
    print(f"{'='*60}")
    for meal_type, stat in stats.items():
        print(f"{meal_type}: {stat['count']} 餐, {stat['totalCalories']} kcal")

    print(f"\n{'='*60}")
    print(f"📋 最近5条记录")
    print(f"{'='*60}")
    for item in analyses[:5]:
        meal_date = item.get('meal_date', item['created_at'][:10])
        food_names = [f['name'] for f in item.get('food_items', [])]
        print(f"\n日期: {meal_date}")
        print(f"餐型: {item['meal_type']}")
        print(f"食物: {', '.join(food_names) if food_names else '无记录'}")
        print(f"热量: {item.get('calories', 'N/A')} kcal")
        if item.get('image_urls'):
            print(f"图片: {item['image_urls'][0]}")

def main():
    email = "user@example.com"
    password = "password123"

    # 1. 获取用户数据
    print("正在获取用户信息...")
    user_result = fetch_user_data(email, password)

    if not user_result.get('success'):
        print(f"登录失败: {user_result.get('message')}")
        return

    user_id = user_result['data']['user']['id']
    print(f"✅ 登录成功，用户ID: {user_id}")

    # 2. 获取本月食物数据
    now = datetime.now()
    start_of_month = now.replace(day=1).strftime('%Y-%m-%d')
    end_of_month = (now.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    end_of_month = end_of_month.strftime('%Y-%m-%d')

    print(f"\n正在获取 {start_of_month} 至 {end_of_month} 的食物数据...")
    food_result = fetch_food_data(user_id, start_of_month, end_of_month)

    if food_result.get('success') and food_result.get('data'):
        print_food_summary(food_result)

        # 保存数据
        with open('food_data.json', 'w', encoding='utf-8') as f:
            json.dump(food_result['data'], f, ensure_ascii=False, indent=2)
        print("\n✅ 数据已保存到 food_data.json")
    else:
        print(f"获取食物数据失败: {food_result.get('message')}")

if __name__ == "__main__":
    main()
```

### Node.js 示例

```javascript
import fs from 'fs';

const BASE_URL = "https://puckg.fun";

async function fetchUserData(email, password) {
  const response = await fetch(`${BASE_URL}/api/agent/user-data`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  return await response.json();
}

async function fetchFoodData(userId, startDate, endDate, mealType) {
  const payload = { userId };
  if (startDate) payload.startDate = startDate;
  if (endDate) payload.endDate = endDate;
  if (mealType) payload.mealType = mealType;

  const response = await fetch(`${BASE_URL}/api/food/analysis/by-date-range`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  return await response.json();
}

function printFoodSummary(data) {
  if (!data.success || !data.data) {
    console.log("获取食物数据失败");
    return;
  }

  const { analyses, stats, totalCount, totalCalories } = data.data;

  console.log('\n' + '='.repeat(60));
  console.log('📊 食物记录统计');
  console.log('='.repeat(60));
  console.log(`总记录数: ${totalCount} 条`);
  console.log(`总热量: ${totalCalories} kcal`);

  console.log('\n' + '='.repeat(60));
  console.log('🍽️ 按餐型统计');
  console.log('='.repeat(60));
  for (const [mealType, stat] of Object.entries(stats)) {
    console.log(`${mealType}: ${stat.count} 餐, ${stat.totalCalories} kcal`);
  }

  console.log('\n' + '='.repeat(60));
  console.log('📋 最近5条记录');
  console.log('='.repeat(60));
  analyses.slice(0, 5).forEach(item => {
    const mealDate = item.meal_date || item.created_at.substring(0, 10);
    const foodNames = (item.food_items || []).map(f => f.name).join(', ');
    console.log(`\n日期: ${mealDate}`);
    console.log(`餐型: ${item.meal_type}`);
    console.log(`食物: ${foodNames || '无记录'}`);
    console.log(`热量: ${item.calories || 'N/A'} kcal`);
    if (item.ai_analysis) {
      console.log(`蛋白质: ${item.ai_analysis.protein || 'N/A'}`);
    }
  });
}

async function main() {
  const email = 'user@example.com';
  const password = 'password123';

  // 获取用户数据
  console.log('正在获取用户信息...');
  const userResult = await fetchUserData(email, password);

  if (!userResult.success) {
    console.log('登录失败:', userResult.message);
    return;
  }

  const userId = userResult.data.user.id;
  console.log(`✅ 登录成功，用户ID: ${userId}`);

  // 获取本周食物数据
  const now = new Date();
  const startOfWeek = new Date(now);
  startOfWeek.setDate(now.getDate() - now.getDay() + 1);
  const endOfWeek = new Date(startOfWeek);
  endOfWeek.setDate(startOfWeek.getDate() + 6);

  const startDate = startOfWeek.toISOString().split('T')[0];
  const endDate = endOfWeek.toISOString().split('T')[0];

  console.log(`\n正在获取 ${startDate} 至 ${endDate} 的食物数据...`);
  const foodResult = await fetchFoodData(userId, startDate, endDate);

  if (foodResult.success && foodResult.data) {
    printFoodSummary(foodResult);

    // 保存到文件
    fs.writeFileSync('food_data.json', JSON.stringify(foodResult.data, null, 2), 'utf-8');
    console.log('\n✅ 数据已保存到 food_data.json');
  } else {
    console.log('获取食物数据失败:', foodResult.message);
  }
}

main();
```

### 按餐型获取数据示例

```python
# 获取本月早餐数据
breakfast_data = fetch_food_data(
    user_id,
    start_date="2026-01-01",
    end_date="2026-01-31",
    meal_type="早餐"
)

# 获取本周晚餐数据
dinner_data = fetch_food_data(
    user_id,
    start_date="2026-01-20",
    end_date="2026-01-26",
    meal_type="dinner"
)
```

## 数据表格化展示

获取食物数据后，可以使用以下脚本进行表格化展示。

### Node.js 食物数据展示脚本

```javascript
import fs from 'fs';

function loadFoodData(filename) {
  const content = fs.readFileSync(filename, 'utf8');
  return JSON.parse(content);
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleString('zh-CN');
}

function createTable(headers, rows) {
  const colWidths = headers.map((h, i) => {
    const maxDataWidth = rows.reduce((max, row) => {
      const cell = String(row[i] || '');
      return Math.max(max, cell.length);
    }, 0);
    return Math.max(h.length, maxDataWidth) + 2;
  });

  const line = '+' + colWidths.map(w => '-'.repeat(w)).join('+') + '+';
  const headerRow = '|' + headers.map((h, i) => ' ' + h.padEnd(colWidths[i] - 1)).join('|') + '|';
  const dataRows = rows.map(row => {
    return '|' + row.map((cell, i) => ' ' + String(cell || '').padEnd(colWidths[i] - 1)).join('|') + '|';
  });

  return [line, headerRow, line, ...dataRows, line].join('\n');
}

function printMealTypeStats(data) {
  console.log('\n## 餐型统计\n');
  const headers = ['餐型', '数量', '总热量(kcal)', '平均热量(kcal)'];
  const rows = Object.entries(data.stats).map(([type, stat]) => [
    type,
    stat.count,
    stat.totalCalories,
    Math.round(stat.totalCalories / stat.count)
  ]);
  console.log(createTable(headers, rows));
}

function printFoodRecords(data, limit = 10) {
  console.log(`\n## 食物记录 (最新 ${limit} 条)\n`);

  const headers = ['序号', '日期', '餐型', '食物', '热量', '图片'];
  const rows = data.analyses.slice(0, limit).map((item, i) => {
    const date = (item.meal_date || item.created_at).substring(0, 10);
    const foods = item.food_items?.map(f => f.name).join(', ') || '无记录';
    const hasImage = item.image_urls?.length > 0 ? '✓' : '✗';
    return [i + 1, date, item.meal_type, foods.substring(0, 30), item.calories || 'N/A', hasImage];
  });

  console.log(createTable(headers, rows));

  console.log('\n**图片链接**:');
  data.analyses.slice(0, limit).forEach((item, i) => {
    if (item.image_urls?.length > 0) {
      console.log(`${i + 1}. ${item.image_urls[0]}`);
    }
  });
}

function printNutritionAnalysis(data) {
  console.log('\n## AI营养分析汇总\n');

  let totalProtein = 0;
  let totalFat = 0;
  let totalCarbs = 0;
  let count = 0;

  data.analyses.forEach(item => {
    if (item.ai_analysis) {
      const protein = parseInt(item.ai_analysis.protein) || 0;
      const fat = parseInt(item.ai_analysis.fat) || 0;
      const carbs = parseInt(item.ai_analysis.carbohydrates) || 0;

      totalProtein += protein;
      totalFat += fat;
      totalCarbs += carbs;
      count++;
    }
  });

  if (count > 0) {
    const headers = ['营养素', '总摄入量', '平均每餐'];
    const rows = [
      ['蛋白质(g)', totalProtein, Math.round(totalProtein / count)],
      ['脂肪(g)', totalFat, Math.round(totalFat / count)],
      ['碳水化合物(g)', totalCarbs, Math.round(totalCarbs / count)]
    ];
    console.log(createTable(headers, rows));
  } else {
    console.log('暂无AI营养分析数据');
  }
}

function main() {
  const filename = process.argv[2] || 'food_data.json';

  try {
    console.log('📊 正在加载食物数据...');
    const data = loadFoodData(filename);

    console.log('\n' + '='.repeat(60));
    console.log('🍽️  V-Train 食物数据报告');
    console.log('='.repeat(60));
    console.log(`总记录数: ${data.totalCount}`);
    console.log(`总热量: ${data.totalCalories} kcal`);

    printMealTypeStats(data);
    printFoodRecords(data, 10);
    printNutritionAnalysis(data);

    console.log('\n✅ 食物数据展示完成！');
  } catch (err) {
    console.error('❌ 错误:', err.message);
    console.log('使用方法: node food_view.js [json文件路径]');
  }
}

main();
```

**使用方法**:
```bash
node food_view.js food_data.json
```

**输出示例**:
```
============================================================
🍽️  V-Train 食物数据报告
============================================================
总记录数: 45
总热量: 15600 kcal

## 餐型统计

+----------+--------+--------------+--------------+
| 餐型     | 数量   | 总热量(kcal) | 平均热量(kcal) |
+----------+--------+--------------+--------------+
| 早餐     | 15     | 4800         | 320          |
| 午餐     | 12     | 7200         | 600          |
| 晚餐     | 10     | 2800         | 280          |
| 零食     | 8      | 800          | 100          |
+----------+--------+--------------+--------------+

## 食物记录 (最新 10 条)

+----+------------+--------+--------------+--------+------+
| 序号 | 日期       | 餐型   | 食物         | 热量   | 图片 |
+----+------------+--------+--------------+--------+------+
| 1  | 2026-01-15 | 早餐   | 燕麦, 牛奶   | 320    | ✓    |
| 2  | 2026-01-15 | 午餐   | 鸡胸肉, 米饭 | 650    | ✓    |
+----+------------+--------+--------------+--------+------+
```

## HTML 可视化模板

提供了一个可视化 HTML 模板 `food_viewer_template.html`，Agent 可直接将数据写入模板生成报告。

### 使用方法

1. **读取模板文件**
2. **替换数据区域** - 找到 `FOOD_DATA` 常量并替换为真实数据
3. **可选：设置用户信息** - 替换 `USER_EMAIL` 和 `DATE_RANGE`
4. **保存为新的 HTML 文件**
5. **在浏览器中打开查看**

### Python 示例

```python
import json
import re
from datetime import datetime

def generate_food_report(food_data, user_email, date_range, output_file):
    """生成食物数据HTML报告"""

    # 读取模板
    with open('skills/food_viewer_template.html', 'r', encoding='utf-8') as f:
        template = f.read()

    # 替换数据
    food_data_json = json.dumps(food_data, ensure_ascii=False, indent=4)

    # 使用正则替换 FOOD_DATA
    pattern = r'const FOOD_DATA = \{[\s\S]*?\};'
    replacement = f'const FOOD_DATA = {food_data_json};'
    template = re.sub(pattern, replacement, template)

    # 替换用户信息
    template = template.replace(
        'const USER_EMAIL = "user@example.com";',
        f'const USER_EMAIL = "{user_email}";'
    )

    # 替换日期范围
    template = template.replace(
        'const DATE_RANGE = {\n            start: "2026-01-01",\n            end: "2026-01-31"\n        };',
        f'const DATE_RANGE = {{\n            start: "{date_range[0]}",\n            end: "{date_range[1]}"\n        }};'
    )

    # 保存报告
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(template)

    print(f'✅ 报告已生成: {output_file}')
```

### Node.js 示例

```javascript
import fs from 'fs';

function generateFoodReport(foodData, userEmail, dateRange, outputFile) {
    // 读取模板
    let template = fs.readFileSync('skills/food_viewer_template.html', 'utf-8');

    // 替换数据
    const foodDataJson = JSON.stringify(foodData, null, 4);

    // 替换 FOOD_DATA
    const pattern = /const FOOD_DATA = \{[\s\S]*?\};/;
    const replacement = `const FOOD_DATA = ${foodDataJson};`;
    template = template.replace(pattern, replacement);

    // 替换用户信息
    template = template.replace(
        'const USER_EMAIL = "user@example.com";',
        `const USER_EMAIL = "${userEmail}";`
    );

    // 替换日期范围
    template = template.replace(
        /const DATE_RANGE = \{[\s\S]*?\};/,
        `const DATE_RANGE = {\n            start: "${dateRange[0]}",\n            end: "${dateRange[1]}"\n        };`
    );

    // 保存报告
    fs.writeFileSync(outputFile, template, 'utf-8');
    console.log(`✅ 报告已生成: ${outputFile}`);
}
```

### 模板特性

- 📊 **餐型统计卡片** - 显示各餐型的数量和热量，点击可筛选
- 📈 **每日热量趋势图** - 使用 Chart.js 绘制的折线图
- 🖼️ **食物图片展示** - 支持显示上传的食物照片
- 🔍 **筛选功能** - 支持按餐型、日期范围筛选
- 📱 **响应式设计** - 适配移动端和桌面端
- 💡 **AI 分析展示** - 显示营养成分和建议

### 数据替换区域说明

模板中有三个主要的替换区域：

1. **FOOD_DATA** - 食物数据对象（必填）
   - `analyses`: 食物记录数组
   - `stats`: 餐型统计数据
   - `totalCount`: 总记录数
   - `totalCalories`: 总热量

2. **USER_EMAIL** - 用户邮箱（可选）
   - 用于显示在报告标题

3. **DATE_RANGE** - 日期范围（可选）
   - `start`: 开始日期
   - `end`: 结束日期
   - 用于初始化日期筛选器

### 界面预览

```
┌─────────────────────────────────────────────────────┐
│  🍽️ V-Train 饮食数据报告                              │
│  记录每一餐，关注健康饮食                              │
├─────────────────────────────────────────────────────┤
│  总记录数    总热量      平均每餐    记录天数          │
│    45      15,600      347       30                │
└─────────────────────────────────────────────────────┘

┌─────────┬─────────┬─────────┬─────────┐
│  🌅早餐  │  ☀️午餐  │  🌙晚餐  │  🍿零食  │
│   15    │   12    │   10    │    8    │
│ 4800卡  │ 7200卡  │ 2800卡  │  800卡  │
└─────────┴─────────┴─────────┴─────────┘

┌─────────────────────────────────────────────────────┐
│ 📈 每日热量趋势 (折线图)                              │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ 📝 饮食记录                                          │
├─────────────────────────────────────────────────────┤
│ ┌─────────────────┐  ┌─────────────────┐             │
│ │ [食物图片]       │  │ [食物图片]       │             │
│ │ 🌅 早餐 320kcal │  │ ☀️ 午餐 650kcal │             │
│ │ 燕麦, 牛奶      │  │ 鸡胸肉, 米饭    │             │
│ │ 蛋白质: 12g     │  │ 蛋白质: 35g     │             │
│ │ 💡 建议增加蔬菜  │  │ 💡 适量饮水     │             │
│ └─────────────────┘  └─────────────────┘             │
└─────────────────────────────────────────────────────┘
```

## 错误处理

### 400 Bad Request
```json
{
  "success": false,
  "data": null,
  "message": "userId is required"
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

### 1. food_viewer_template.html

**文件路径**: `skills/food_viewer_template.html`

**功能**: 可视化 HTML 模板，Agent 可直接将数据写入模板生成报告

**使用方法**:
1. 读取模板文件
2. 替换 `FOOD_DATA` 数据区域
3. 保存为新的 HTML 文件
4. 在浏览器中打开查看

**特性**:
- 汇总卡片（总记录数、总热量、平均每天）
- 餐型统计（带图标和筛选功能）
- 每日热量趋势图
- 饮食记录卡片（图片、营养分析、AI建议）
- 响应式设计

---

## Agent 使用流程

完整的 Agent 使用流程如下：

```
1. 用户提供邮箱和密码
      ↓
2. 调用 /api/agent/user-data 获取 user_id
      ↓
3. 确定查询日期范围（本月/本周/指定区间）
      ↓
4. 调用 /api/food/analysis/by-date-range 获取数据
      ↓
5. 可选：按餐型筛选特定数据
      ↓
6. 保存 JSON 数据文件
      ↓
7. 读取 food_viewer_template.html
      ↓
8. 替换数据生成报告
      ↓
9. 保存并展示 HTML 报告
```

### 示例交互

**用户**: "帮我查看这个月的饮食记录"

**Agent**:
```python
# 1. 获取用户ID
user_result = fetch_user_data(email, password)
user_id = user_result['data']['user']['id']

# 2. 获取本月数据
now = datetime.now()
start_date = now.replace(day=1).strftime('%Y-%m-%d')
end_date = (now.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
end_date = end_date.strftime('%Y-%m-%d')

food_result = fetch_food_data(user_id, start_date, end_date)

# 3. 生成报告
generate_food_report(
    food_result['data'],
    email,
    (start_date, end_date),
    f'food_report_{start_date}.html'
)

# 4. 输出摘要
print(f"本月共记录 {food_result['data']['totalCount']} 餐")
print(f"总热量: {food_result['data']['totalCalories']} kcal")
for meal_type, stat in food_result['data']['stats'].items():
    print(f"{meal_type}: {stat['count']} 餐")
```
