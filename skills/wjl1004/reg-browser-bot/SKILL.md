# reg-browser-bot 技能文档

**版本**: 5.4.0  
**更新日期**: 2026-04-04  
**架构**: Phase 2 重构版 + Phase 3 功能完善 + Phase 4 反爬加固 + Phase 5 架构优化 + Phase A OCR升级 + Phase B SQLite存储集成 + Phase C fake-useragent集成 + **Phase D Playwright替换Selenium**

---

## 概述

reg-browser-bot 是一个基于 Selenium + Chrome 的浏览器自动化工具包，支持多账号管理、数据采集、自动化运营和验证码识别。

**Phase D 新增**: Playwright 浏览器支持（替代 Selenium），更好的隐身模式和反爬对抗能力

**Phase 5 新增**: 架构优化（BrowserManager 单例、Pipeline 流水线、TaskScheduler 调度器、数据模型）

**Phase 4 新增**: 反爬对抗能力（UA池轮换、代理支持、指纹伪装、请求间隔随机化）

---

## 架构说明

### Phase 2 重构内容

1. **BrowserConfig 单例模式**
   - 统一的 Chrome Options 配置
   - 共享目录路径管理
   - 统一日志配置
   - 浏览器指纹伪装

2. **统一异常处理**
   - `BrowserBotException` 基类
   - 细分异常类型（BrowserInitError, LoginError, CookieError 等）

3. **浏览器模块合并**
   - `browser.py` 和 `browser_auto.py` 合并为 `browser.py`
   - 统一的 `Browser` 类接口

4. **argparse 统一 CLI**
   - 每个模块支持 `--help`
   - 命令风格统一
   - 统一的 `tool.py` 入口

### Phase 3 功能完善

1. **滑块验证码识别 (`SliderCaptcha`)**
   - OpenCV 模板匹配计算缺口距离（TM_SQDIFF_NORMED）
   - ActionChains 模拟拖动（支持缓动函数轨迹）
   - 两种拖动模式：`drag_to`（标准）和 `drag_to_slow`（更慢，更像人）

2. **点选验证码接口 (`ClickCaptcha`)**
   - 预留第三方打码 API 接口（云打码、超级鹰等）
   - 支持按比例坐标点击

3. **WebDriverWait 全面替换 `time.sleep`**
   - 页面导航等待：`WebDriverWait` + `document.readyState`
   - 元素等待：`WebDriverWait` + `EC.presence_of_element_located`
   - 批量操作间隔：`WebDriverWait` + 超时等待

4. **重试装饰器 (`@retry`)**
   - 支持指数退避（backoff）
   - 可配置异常类型
   - 模块化日志记录

5. **缓动函数 + 滑块轨迹生成**
   - `ease_out_quad`、`ease_in_out_quad`、`ease_out_cubic`、`ease_out_quart`
   - `generate_slider_track()` 生成非匀速拖动轨迹，防机器人检测

### Phase 4 反爬加固（新增）

1. **UA 池轮换**
   - 30+ 预置 User-Agent（PC Chrome/Firefox/Safari/Edge + Mobile iOS/Android）
   - 支持 Mobile UA 占比配置
   - 每次创建浏览器随机选择 UA

2. **代理支持**
   - `ProxyManager` 代理管理器类
   - 支持 HTTP/HTTPS/SOCKS5 代理
   - 代理池配置 + 自动切换
   - 失败代理自动标记和跳过

3. **浏览器指纹伪装**
   - Canvas 指纹噪声注入
   - WebGL 指纹伪装（渲染器、厂商）
   - Timezone 伪装
   - Language 伪装
   - Screen resolution 配置
   - navigator.webdriver / plugins / languages 伪装

4. **请求间隔随机化**
   - `DelayConfig` 延迟配置
   - 操作前随机延迟（3-8秒可配置）
   - 输入模拟（逐字输入，有随机间隔）
   - 操作后小延迟

5. **undetected-chromedriver 支持**
   - 可选使用 undetected-chromedriver 替代原生 webdriver

### Phase 5 架构优化（新增）

1. **BrowserManager 单例模式** (`browser_manager.py`)
   - 全局唯一的浏览器管理器
   - 引用计数管理浏览器生命周期
   - 支持多Profile隔离（不同账号用不同浏览器实例）
   - 全局共享复用，避免重复创建浏览器
   - `BrowserContext` 上下文管理器，自动管理引用计数

2. **Pipeline 流水线架构** (`pipeline.py`)
   - 步骤化任务编排
   - 支持错误处理和重试机制
   - 预置流水线：`LoginPipeline`、`CollectPipeline`、`PostPipeline`
   - 支持步骤完成回调和错误回调
   - `create_pipeline()` 工厂函数快速创建

3. **TaskScheduler 任务调度器** (`task_scheduler.py`)
   - 基于 APScheduler 的后台调度器
   - 支持 cron/interval/date 触发器
   - 任务持久化（保存到 JSON 文件）
   - 任务执行状态跟踪
   - 便捷函数：`schedule_task()`, `get_scheduler()`

4. **数据模型** (`models.py`)
   - 统一的数据结构定义（dataclass）
   - `Account`, `Task`, `CollectedData`, `CaptchaRecord`, `Proxy`
   - `PipelineExecution` 流水线执行记录
   - 可选 SQLite 存储（`DatabaseManager`）

### Phase D Playwright 替换 Selenium（新增）

1. **Playwright 浏览器类** (`browser_playwright.py`)
   - 与 Selenium `Browser` 类接口兼容
   - 原生隐身模式（`--incognito`），更难被检测
   - 更快的页面加载和操作
   - 内置智能等待机制
   - 无需 WebDriver，自动处理

2. **双版本并存**
   - `browser.py` → Selenium 版（保留，所有现有代码兼容）
   - `browser_playwright.py` → Playwright 版（新）
   - 通过 `config.create_browser(use_playwright=True/False)` 切换

3. **Playwright 版滑块拖动**
   - `slider_drag()` 函数（带轨迹防检测）
   - `slider_drag_slow()` 函数（慢速版，更像人类）
   - 与 Selenium `ActionChains` 等效，但使用 `page.mouse`

4. **启动参数优化**
   - `--incognito` 隐身模式
   - `--disable-extensions` / `--disable-plugins`
   - `--disable-background-networking` / `--disable-sync`
   - 自动使用 UA 池

---

## 目录结构

```
reg-browser-bot/
├── __init__.py           # 模块导出（含 Phase 5 新增）
├── browser_config.py     # 共享配置（单例）+ Phase 4 反爬增强
├── browser_manager.py    # Phase 5 浏览器管理器单例
├── pipeline.py           # Phase 5 流水线架构（含 Phase B SQLite 集成）
├── task_scheduler.py      # Phase 5 任务调度器
├── models.py             # Phase 5 数据结构定义 + Phase B DatabaseManager
├── proxy.py              # 代理管理器
├── exceptions.py         # 统一异常定义
├── browser.py            # Selenium 浏览器控制（保留）
├── browser_playwright.py # Phase D Playwright 浏览器控制（新增）
├── captcha.py            # 验证码识别（含滑块+点选）
├── collector.py          # 数据采集（含 Phase B SQLite 集成）
├── account.py            # 账号管理（含 Phase B SQLite 集成）
├── poster.py             # 自动化运营
├── tool.py               # 统一入口
├── utils.py              # 工具函数
├── security.py           # 密码加密
├── migrate_passwords.py  # 密码迁移
├── migrate_json_to_sqlite.py  # Phase B 数据迁移脚本
└── SKILL.md              # 本文档
```

---

## 核心 API

### BrowserConfig

```python
from browser_config import get_config

config = get_config()  # 获取单例

# 基础配置
config.set_headless(True)
config.set_user_agent("Mozilla/5.0 ...")
config.info("日志消息")

# === Phase 4 反爬配置 ===

# UA 池
config.enable_ua_pool(enabled=True, mobile_ratio=0.3)  # 启用 UA 池，Mobile 占 30%
ua = config.get_random_user_agent()  # 获取随机 UA

# 代理设置
config.set_proxy(
    host="127.0.0.1",
    port=7890,
    proxy_type="http",  # http, https, socks5
    username="user",    # 可选
    password="pass"    # 可选
)

# 指纹伪装
config.set_fingerprint(
    timezone="Asia/Shanghai",
    language="zh-CN",
    screen_resolution="1920x1080"
)
config.enable_fingerprint_randomization(enabled=True)  # 随机化指纹

# 延迟控制
config.set_delay(min_seconds=3, max_seconds=8, enabled=True)

# undetected-chromedriver
config.use_undetected_uc(enabled=True)
```

### ProxyManager

```python
from proxy import ProxyManager, Proxy, ProxyType

# 创建代理管理器
pm = ProxyManager([
    {"host": "127.0.0.1", "port": 7890, "type": "http"},
    {"host": "127.0.0.1", "port": 7891, "type": "socks5"},
    {"host": "127.0.0.1", "port": 7892, "type": "https", "username": "user", "password": "pass"}
])

# 获取代理
proxy = pm.get_proxy()           # 获取当前代理（轮换）
proxy = pm.get_random_proxy()    # 随机获取
proxy = pm.switch_proxy()        # 切换到下一个

# 标记失败/成功
pm.mark_proxy_failed(proxy)      # 标记当前代理失败
pm.mark_proxy_success(proxy)     # 标记代理成功
pm.reset_failed()                # 重置失败列表

# Chrome 参数
args = pm.get_chrome_proxy_args(proxy)
# ['--proxy-server=http://127.0.0.1:7890']
```

### FingerprintConfig

```python
from browser_config import FingerprintConfig

fp = FingerprintConfig(
    canvas_noise=True,
    webgl_noise=True,
    timezone="Asia/Shanghai",
    language="zh-CN",
    screen_resolution="1920x1080",
    platform="Win32"
)

fp.randomize()  # 随机化指纹参数

# 获取指纹脚本
script = fp.get_fingerprint_script()  # 返回 JavaScript 代码
```

### DelayConfig

```python
from browser_config import DelayConfig

delay = DelayConfig(min_seconds=3, max_seconds=8, enabled=True)

# 执行随机延迟
actual_delay = delay.wait()  # 返回实际等待秒数
delay.wait_fixed(2.5)        # 固定延迟
```

### Browser

```python
from browser import Browser

with Browser() as browser:
    # 导航（自动延迟）
    browser.navigate("https://example.com")
    
    # 点击（自动延迟）
    browser.click("#login-btn")
    
    # 输入（逐字输入模拟）
    browser.input("#username", "user")
    browser.input("#password", "pass", use_delay=False)  # 密码不逐字输入
    
    # 禁用延迟的批量操作
    browser.input("#search", "query", use_delay=False)
    browser.click(".search-btn", use_delay=False)
```

**Phase 4 Browser 新增参数**:
- `use_delay`: 是否使用随机延迟（默认 True）
- 内部自动在操作前后添加延迟
- 输入操作支持逐字输入模拟

---

## Phase 5 API

### BrowserManager 单例

```python
from browser_manager import BrowserManager, BrowserContext, get_browser_manager

# 获取单例
manager = BrowserManager.get_instance()

# 获取浏览器（引用计数+1）
browser = manager.get_browser(profile_id="account1")

# 使用 BrowserContext 自动管理引用计数
with BrowserContext("account1") as browser:
    browser.navigate("https://example.com")
# 离开 with 块时自动 release

# 释放浏览器（引用计数-1）
manager.release_browser(profile_id="account1")

# 强制关闭
manager.close_browser(profile_id="account1")

# 关闭所有浏览器
manager.close_all()

# 查看活跃profile
active = manager.get_active_profiles()

# 检查浏览器是否存活
is_alive = manager.is_browser_alive(profile_id="account1")
```

### Pipeline 流水线

```python
from pipeline import Pipeline, LoginPipeline, CollectPipeline, PostPipeline, create_pipeline

# 方式1：使用预置流水线
login_pipeline = LoginPipeline(account_name="myaccount")
result = login_pipeline.execute()

collect_pipeline = CollectPipeline(
    account_name="myaccount",
    target="白酒",
    max_count=10
)
result = collect_pipeline.execute()

post_pipeline = PostPipeline(
    account_name="myaccount",
    content="发布内容"
)
result = post_pipeline.execute()

# 方式2：使用工厂函数
pipeline = create_pipeline("collect", account_name="myaccount", target="白酒", max_count=10)
result = pipeline.execute()

# 方式3：自定义流水线
def my_step(context, **kwargs):
    print(f"执行中，当前context: {context}")
    return {"success": True}

pipeline = Pipeline("my_pipeline")
pipeline.add_step(my_step, "第一步")
pipeline.add_step(my_step, "第二步")

# 注册错误处理
def on_error(step_name, error):
    print(f"步骤 {step_name} 失败: {error}")

pipeline.on_error(on_error)

# 执行
result = pipeline.execute(context={"key": "value"})

# 检查结果
if result.success:
    print("流水线执行成功")
    print(f"最终context: {result.context}")
else:
    print(f"流水线执行失败: {result.error}")
```

### TaskScheduler 任务调度

```python
from task_scheduler import TaskScheduler, get_scheduler, schedule_task

# 方式1：使用全局调度器

def my_task():
    print("定时任务执行")

# 添加间隔任务（每60秒）
schedule_task(my_task, "interval", seconds=60, name="每分钟任务")

# 添加 cron 任务（每天凌晨2点）
schedule_task(my_task, "cron", hour=2, minute=0, name="每日任务")

# 启动调度器
start_scheduler()

# 方式2：使用独立调度器实例
scheduler = TaskScheduler()

# 注册函数
scheduler.register_func("my_task", my_task)

# 添加任务（使用函数名）
scheduler.add_job("my_task", "interval", seconds=60, name="每分钟任务")

# 启动
scheduler.start()

# 查看任务列表
jobs = scheduler.get_jobs()
for job in jobs:
    print(f"任务: {job['name']}, 下次执行: {job['next_run_time']}")

# 手动触发执行
scheduler.run_job("my_task")

# 暂停/恢复任务
scheduler.pause_job("my_task")
scheduler.resume_job("my_task")

# 移除任务
scheduler.remove_job("my_task")

# 关闭调度器
scheduler.shutdown()
```

### 数据模型

```python
from models import Account, Task, DatabaseManager, get_database

# 使用 dataclass
account = Account(
    name="myaccount",
    platform="douyin",
    username="user@example.com",
    password_encrypted="encrypted_password"
)

# 转换为字典
data = account.to_dict()

# 从字典创建
account2 = Account.from_dict(data)

# 使用 SQLite 数据库
db = get_database()  # 全局实例

# 保存账号
db.save_account(account)

# 获取账号
account = db.get_account("myaccount")

# 获取账号列表
accounts = db.get_accounts(platform="douyin")

# 保存和获取任务
task = Task(
    id="task_001",
    name="采集任务",
    type="collect",
    params={"keyword": "白酒", "max_count": 10}
)
db.save_task(task)
task = db.get_task("task_001")
```

---

## CLI 使用

### 统一入口 (tool.py)

```bash
# 浏览器控制
python tool.py browser navigate https://www.baidu.com
python tool.py browser click "#login-btn"
python tool.py browser screenshot --name myshot.png

# 验证码识别
python tool.py captcha recognize captcha.png
python tool.py captcha number number.png
python tool.py captcha slider-distance bg.png gap.png
python tool.py captcha slider-test

# 数据采集
python tool.py collector taobao 白酒 3
python tool.py collector jd 白酒 5
python tool.py collector douyin 白酒

# 账号管理
python tool.py account add myaccount douyin user pass
python tool.py account list
python tool.py account get myaccount

# 自动化运营
python tool.py poster douyin "发布内容"
python tool.py poster follow user1 user2
```

### 独立模块

```bash
python browser.py navigate https://www.baidu.com
python captcha.py recognize captcha.png
python captcha.py slider-distance bg.png gap.png
python collector.py taobao 白酒 3
python account.py list
python poster.py douyin "内容"
python proxy.py  # 测试代理管理器
python browser_config.py  # 测试配置
```

---

## 安全特性

1. **密码加密存储** (Phase 1)
   - 使用 Fernet (AES-CBC) 对称加密
   - 自动迁移明文密码

2. **Cookie 域校验**
   - 验证 cookie domain 匹配
   - 防止跨域注入

3. **安全 Cookie 字段**
   - 只保留安全字段（name, value, domain, path, secure, expiry, httpOnly）

4. **移除危险功能**
   - 无 Pickle 反序列化
   - 无 eval/shell 调用

---

## 反爬对抗配置（Phase 4）

### 快速开始

```python
from browser_config import get_config
from browser import Browser

# 配置反爬参数
config = get_config()
config.enable_ua_pool(enabled=True, mobile_ratio=0.2)
config.set_proxy("127.0.0.1", 7890, "http")
config.set_delay(min_seconds=3, max_seconds=8, enabled=True)
config.enable_fingerprint_randomization(enabled=True)

# 创建浏览器（自动应用所有反爬配置）
browser = Browser()
```

### 反爬配置组合

```python
# 轻度反爬（快速开发测试）
config.enable_ua_pool(enabled=True)
config.set_delay(min_seconds=1, max_seconds=3, enabled=True)
config.enable_fingerprint_randomization(enabled=False)

# 中度反爬（一般采集）
config.enable_ua_pool(enabled=True, mobile_ratio=0.2)
config.set_proxy("proxy.host", 8080, "http")
config.set_delay(min_seconds=3, max_seconds=8, enabled=True)
config.enable_fingerprint_randomization(enabled=True)

# 强度反爬（高防网站）
config.enable_ua_pool(enabled=True, mobile_ratio=0.3)
config.set_proxy("proxy1.host", 8080, "http")
config.set_delay(min_seconds=5, max_seconds=12, enabled=True)
config.enable_fingerprint_randomization(enabled=True)
config.use_undetected_uc(enabled=True)
```

---

## 配置目录

| 目录 | 默认路径 |
|------|----------|
| 截图 | `~/.openclaw/screenshots/` |
| 数据 | `~/.openclaw/data/` |
| 账号 | `~/.openclaw/accounts/` |
| 日志 | `~/.openclaw/logs/` |

---

## 异常处理

```python
from exceptions import BrowserBotException, BrowserInitError

try:
    browser = Browser()
except BrowserInitError as e:
    print(f"浏览器初始化失败: {e}")
```

---

## Phase A OCR 升级（DdddOcr 替换 pytesseract）

**日期**: 2026-04-04

### 变更说明

| 项目 | 旧方案 | 新方案 |
|------|--------|--------|
| OCR 引擎 | pytesseract | **DdddOcr** |
| 系统依赖 | 需安装 tesseract-ocr 二进制 | **纯 Python，无需系统依赖** |
| 准确率 | 一般 | 更高（深度学习模型）|
| 数字识别 | pytesseract `--psm 7` | DdddOcr 自动识别 |
| 中文识别 | pytesseract `lang=chi_sim` | DdddOcr 对中文效果更好 |

### 保留机制

- pytesseract 仍作为 **fallback** 保留（`PYTESSERACT_AVAILABLE`）
- DdddOcr 不可用时自动降级到 pytesseract
- SliderCaptcha（OpenCV）不受影响

### 代码变更

```python
# 旧：pytesseract 直接调用
import pytesseract
result = pytesseract.image_to_string(img, config='--psm 7 ...')

# 新：DdddOcr（主）+ pytesseract（fallback）
from ddddocr import DdddOcr
class CaptchaSolver:
    def __init__(self):
        self._ocr = DdddOcr()  # 初始化纯 Python OCR
    def recognize_simple(self, image_path):
        with open(image_path, 'rb') as f:
            return self._ocr.classification(f.read())
```

### 验证

```bash
python3 -c "from captcha import CaptchaSolver; s = CaptchaSolver(); print(s.recognize_simple('/tmp/test.png'))"
```

---

## Phase C fake-useragent 集成

**日期**: 2026-04-04

### 变更说明

| 项目 | 旧方案 | 新方案 |
|------|--------|--------|
| UA 来源 | 手动维护 PC_UA_LIST + MOBILE_UA_LIST | **fake-useragent**（动态获取最新 UA） |
| Chrome 版本 | 手动更新（已过时） | fake-useragent 自动维护 |
| fallback | 无 | 网络失败时自动降级到内置 UA 池 |

### 实现细节

- `get_fake_ua()` 全局缓存 fake-useragent 实例，避免重复初始化
- `get_random_user_agent()` 优先使用 `fake.random`，失败时 fallback 到 `self.ua_pool`
- 内置 UA 池（PC_UA_LIST / MOBILE_UA_LIST）完整保留作为兜底
- `FAKE_USERAGENT_AVAILABLE` 标志：无依赖时安全降级

### 验证

```bash
python3 -c "
from browser_config import get_config, get_fake_ua, FAKE_USERAGENT_AVAILABLE
print('fake-useragent available:', FAKE_USERAGENT_AVAILABLE)
config = get_config()
config.enable_ua_pool(enabled=True)
for i in range(3):
    ua = config.get_random_user_agent()
    print(f'[{i+1}] {ua[:80]}')
"
```

---

## Phase B SQLite 存储集成

**日期**: 2026-04-04

### 概述

Phase B 将 `models.py` 中的 `DatabaseManager` 集成到各模块，实现 JSON + SQLite 双写持久化存储。

### 数据库路径

```
~/.config/reg-browser-bot/reg-browser-bot.db
```

### 表结构（6张表）

| 表名 | 说明 |
|------|------|
| `accounts` | 账号信息 |
| `tasks` | 任务记录 |
| `collected_data` | 采集数据 |
| `captcha_records` | 验证码记录 |
| `proxies` | 代理配置 |
| `pipeline_executions` | 流水线执行记录 |

### 双写策略

所有模块保持 **JSON 文件为主存储**，SQLite 为辅助/索引存储：

```
写入 → JSON 文件 + SQLite（同步）
读取 → SQLite 优先，fallback 到 JSON
```

### account.py 集成

```python
from account import AccountManager

mgr = AccountManager()

# 添加账号（JSON + SQLite 双写）
mgr.add_account("myaccount", "douyin", "user@example.com", "password123")

# 获取账号（SQLite 优先）
account = mgr.get_account("myaccount")

# 列出账号（合并 SQLite + JSON，去重）
accounts = mgr.list_accounts(platform="douyin")

# 删除账号（JSON + SQLite 双删除）
mgr.delete_account("myaccount")
```

### collector.py 集成

采集方法完成后自动保存到 SQLite：

```python
from collector import DataCollector

collector = DataCollector()
collector.init_browser()

# 采集结果同时保存到 CSV 文件和 SQLite
path = collector.collect_taobao_products("白酒", pages=3)
# SQLite 中可查询: db.get_collected_data_by_task(task_id)

collector.close()
```

### pipeline.py 集成

流水线执行状态自动记录到 SQLite：

```python
from pipeline import CollectPipeline

pipeline = CollectPipeline(account_name="myaccount", target="白酒", max_count=10)
result = pipeline.execute()
# 执行记录自动保存到 pipeline_executions 表
```

### 数据迁移

将现有 JSON 数据迁移到 SQLite：

```bash
# 迁移所有数据
python migrate_json_to_sqlite.py --all

# 仅迁移账号
python migrate_json_to_sqlite.py --accounts

# 仅迁移采集数据
python migrate_json_to_sqlite.py --data

# 模拟迁移（不实际写入）
python migrate_json_to_sqlite.py --all --dry-run
```

### DatabaseManager API

```python
from models import get_database, Account, Task, CollectedData

db = get_database()

# 账号
db.save_account(Account(...))
account = db.get_account("name")
accounts = db.get_accounts(platform="douyin", status="active")

# 任务
db.save_task(Task(...))
task = db.get_task("task_id")
tasks = db.get_tasks(status="pending")

# 采集数据
db.save_collected_data(CollectedData(...))
data = db.get_collected_data("data_id")
data_list = db.get_collected_data_by_task("task_id")
```

---

## 依赖

- selenium>=4.0.0
- Pillow>=9.0.0
- **ddddocr>=1.6.0**（Phase A 新增，主 OCR）
- pytesseract（fallback only）
- opencv-python>=4.0.0
- cryptography
- undetected-chromedriver>=3.0.0 (可选，Phase 4)
- **playwright>=1.40.0**（Phase D 新增，替代 Selenium）

---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0.0 | 2026-04-01 | Phase 1 - 基础功能 + 安全修复 |
| 2.0.0 | 2026-04-04 | Phase 2 - 架构重构 + 统一配置 |
| 3.0.0 | 2026-04-04 | Phase 3 - 滑块验证码 + WebDriverWait + retry装饰器 |
| 4.0.0 | 2026-04-04 | Phase 4 - 反爬加固（UA池、代理、指纹、延迟） |
| 5.0.0 | 2026-04-04 | Phase 5 - 架构优化（BrowserManager单例、Pipeline流水线、TaskScheduler调度器、数据模型） |
| 5.1.0 | 2026-04-04 | Phase A - OCR升级（DdddOcr替换pytesseract，纯Python无需系统依赖） |
| 5.2.0 | 2026-04-04 | Phase B - SQLite存储集成（DatabaseManager集成到account/collector/pipeline，数据迁移脚本） |
| 5.3.0 | 2026-04-04 | Phase C - fake-useragent集成（UA动态获取，Chrome版本自动更新，内置UA池作fallback） |
| 5.4.0 | 2026-04-04 | Phase D - Playwright替换Selenium（双版本并存，原生隐身模式，更好的反爬能力） |
