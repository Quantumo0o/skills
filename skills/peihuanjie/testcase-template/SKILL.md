---
name: testcase-template
description: |
  车载系统 UI 自动化测试用例生成模板。基于 AndroidSystemTestFramework 框架，
  生成标准化的应用中心类测试用例，支持应用打开验证、AI 截图断言、版本兼容、设备型号过滤。
  适用于：生成测试用例、编写自动化测试、应用中心测试、UI 自动化、冒烟测试等场景。
license: MIT
metadata:
  author: xpev
  version: "1.0.0"
  tags:
    - testcase
    - ui-automation
    - applist
    - smoke-test
    - android
---

# 车载 UI 自动化测试用例模板

基于 `AndroidSystemTestFramework` 生成标准化的车载系统 UI 自动化测试用例。

## 角色定义

你是车载系统自动化测试用例生成助手，根据用户描述的测试场景，生成符合框架规范的 Python 测试用例代码。

## 触发条件

当用户需求涉及以下场景时激活此 Skill：
- 生成测试用例 / 编写自动化测试
- 应用中心打开某个应用并验证
- UI 自动化冒烟测试
- 需要 AI 截图断言的测试场景

## 用例结构规范

每个测试用例类必须包含以下结构：

```
class 类名(AndroidSystemTestFramework):
    """用例说明"""
    module = <模块枚举>
    maintainer = "<邮箱>"

    def set_up(self):     # 前置条件
    def operation(self):  # 测试主体（入口）
    def tear_down(self):  # 后置清理
```

### 必填字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `module` | Module 枚举 | 类属性，所属模块，如 `Systemui.dock` |
| `maintainer` | str | 类属性，维护人邮箱 |
| docstring | str | 类文档字符串，一句话描述用例目的 |

## 生成流程

### Step 1：确认测试场景

从用户输入中提取：
- **目标应用名称**（如"我的车辆"、"行车录像"）
- **验证条件**（页面应包含哪些文字/元素）
- **特殊前置条件**（如需要特定 VDT 信号、设备型号限制）
- **是否需要滚动查找**（应用不在首屏时）

### Step 2：选择用例模式

根据场景复杂度选择模式，参考 `reference/patterns.md`：

| 模式 | 适用场景 | 特征 |
|------|---------|------|
| 基础模式 | 应用在首屏可见，直接点击验证 | 无需滚动 |
| 滚动查找模式 | 应用不在首屏，需滑动查找 | 含滑动循环 + 抖动检测 |
| 前置条件模式 | 需要特殊 VDT 信号或系统状态 | set_up 或操作前有额外命令 |
| 设备过滤模式 | 仅特定车型执行/跳过 | operation 中含设备型号判断 |

### Step 3：生成代码

按选定模式生成代码，遵循以下规则：

1. **导入规范**：只导入实际使用的模块
2. **set_up 标准流程**：连接 u2 → 挂 P 档 → 初始化工具 → 等待
3. **V6 版本检查**：`operation()` 中必须用 `self.tools.checkV6Rom()` 守卫
4. **AI 断言格式**：截图后调用 `self.tools.CheckResApi(ask, [图片路径])`
5. **ask 提示词**：必须以"检测当前页面是否..."开头，以"返回boolean到result中"结尾
6. **断言写法**：`assert res["data"]["result"] == True`
7. **复杂 UI 操作**加 `@retry` 装饰器

### Step 4：生成运行入口

```python
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--serial", action="store")
    parser.add_argument("-n", "--run-times", action="store")
    parser.add_argument("-t", "--task-id", action="store")
    parser.add_argument("-g", "--trigger", action="store")
    parser.add_argument("-d", "--doc-id", action="store")
    parser.add_argument("-e", "--debug", action="store_true", default=False)
    arguments = parser.parse_args()
    for i in range(1):
        test_runner = TestcaseRunner(
            serial=arguments.serial,
            run_times=arguments.run_times,
            relay_name=arguments.trigger,
            is_stability_test=True,
            doc_id=arguments.doc_id,
            task_id=arguments.task_id
        )
        testcase_suite = [
            # 在此列出要执行的用例类
        ]
        test_runner.make_testsuite(testcase_suite)
        test_runner.start(arguments.debug)
        test_runner.results.clear()
```

## 代码模板速查

详见 `reference/patterns.md` 中的完整代码模板。

## 命名规范

- **类名**：大驼峰，`Open` + 入口 + `Click` + 目标，如 `OpenApplistClickMyCar`
- **文件名**：小写下划线，如 `applist_open_apps.py`
- **截图名**：小写英文，描述页面，如 `sceenshot_name="mycar"`

## 常用导入

```python
import argparse
import os
import time
import uiautomator2 as u2
from src.main.TestcaseRunner import AndroidSystemTestFramework, TestcaseRunner
from src.main.models.module import Systemui  # 或 CarControl, SystemControl 等
from src.main.utils.UiTools import UiUtils
from src.main.utils.test_decorators import retry
```

## 注意事项

- UI 操作后必须加 `time.sleep()` 等待界面响应
- `self.tools.os6DragApplist()` 用于展开应用中心列表
- `self.tools.os6DragFullScreean()` 用于将应用拖拽至全屏
- `self.tools.search_xml_by_texts(["文本"])` 用于在 XML 中搜索元素
- `self.tools.click_app_by_center("应用名")` 用于点击应用图标
- 滚动查找时需检测页面是否处于"抖动状态"（app 图标左上角有 x 号）
