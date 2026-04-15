# 测试用例代码模板

## 模式1：基础模式（首屏应用直接点击验证）

适用于应用在首屏可见，无需滚动。

```python
import argparse
import time
import uiautomator2 as u2
from src.main.TestcaseRunner import AndroidSystemTestFramework, TestcaseRunner
from src.main.models.module import Systemui
from src.main.utils.UiTools import UiUtils
from src.main.utils.test_decorators import retry


class OpenApplistClick{{AppNameEn}}(AndroidSystemTestFramework):
    """打开应用中心，打开{{AppNameCn}}"""
    module = Systemui.dock
    maintainer = "{{email}}"

    def set_up(self):
        self.logger.info("################### set_up ###################")
        self.ui = u2.connect(self.serial_no)
        self.logger.info("挂p档")
        self.device.shell("vdt rp VCU_CURRENT_GEARLEV 4")
        self.tools = UiUtils(self)
        self.tools.make_initialization6()
        time.sleep(5)

    @retry
    def clickapplist(self):
        self.logger.info("进入应用中心")
        self.device.shell("am start -n com.xiaopeng.applist.ivi/ivi.AppListActivity")
        time.sleep(3)
        self.tools.os6DragApplist()
        time.sleep(5)

        self.tools.search_xml_by_texts(["{{AppNameCn}}"])
        self.tools.click_app_by_center("{{AppNameCn}}")
        self.tools.os6DragFullScreean()

        time.sleep(5)
        self.screenshot(is_instrument_required=False, sceenshot_name="{{screenshot_name}}", pic_num=1,
                        interval=1, is_RSE_required=False, is_CNSL_required=False,
                        is_PSG_required=False)

        ask = "检测当前页面是否{{验证描述}},返回boolean到result中"
        res = self.tools.CheckResApi(ask, [self.picture_path_list[-1]])
        assert res["data"]["result"] == True

    def operation(self):
        if self.tools.checkV6Rom():
            self.clickapplist()
        else:
            print("非V6版本跳过执行")

    def tear_down(self):
        super().tear_down()
```

### 占位符说明

| 占位符 | 说明 | 示例 |
|--------|------|------|
| `{{AppNameEn}}` | 应用英文名（大驼峰） | `MyCar`、`DV`、`CarGuide` |
| `{{AppNameCn}}` | 应用中文名 | `我的车辆`、`行车录像`、`用车指南` |
| `{{email}}` | 维护人邮箱 | `zhangsan@xiaopeng.com` |
| `{{screenshot_name}}` | 截图文件名 | `mycar`、`guide` |
| `{{验证描述}}` | AI 断言的验证描述 | `展示车辆相关的信息` |

---

## 模式2：滚动查找模式（应用不在首屏）

适用于需要向下滑动才能找到的应用（如 Apple CarPlay、HUAWEI HiCar）。

```python
    @retry
    def clickapplist(self):
        self.logger.info("进入应用中心")
        self.device.shell("am start -n com.xiaopeng.applist.ivi/ivi.AppListActivity")
        time.sleep(3)
        self.tools.os6DragApplist()
        time.sleep(3)

        screen_width, screen_height = self.ui.window_size()
        center_x = screen_width / 2
        # 初始化：向上滑动回到顶部
        start_y_init = screen_width * 3 / 4
        end_y_init = screen_height / 4
        swipe_init_cmd = f"input swipe {center_x} {end_y_init} {center_x} {start_y_init}"
        self.device.shell(swipe_init_cmd)
        time.sleep(1)

        # 滑动参数
        swipe_start_y = screen_height * 5 / 7
        swipe_end_y = screen_height * 2 / 7
        swipe_duration = 800
        down_scroll_count = 0

        while down_scroll_count < 3:
            self.logger.info(f"向下滚动 {down_scroll_count + 1}/3 次")
            swipe_cmd = f"input swipe {center_x} {swipe_start_y} {center_x} {swipe_end_y} {swipe_duration}"
            self.device.shell(swipe_cmd)
            down_scroll_count += 1
            time.sleep(3)

            if self.ui(text="{{AppNameCn}}"):
                # 抖动检测（可选）
                self.screenshot(is_instrument_required=False, sceenshot_name="appcheck", pic_num=1,
                                interval=1, is_RSE_required=False, is_CNSL_required=False,
                                is_PSG_required=False)
                ask = "当前显示的是汽车的'应用中心'界面，界面内排列着多排应用图标,如果存在app左上角有\"x\"号，则可以判断该页面处于抖动状态，基于此请判断当前页面是否处于抖动的状态"
                res = self.tools.CheckResApi(ask, [self.picture_path_list[-1]])
                if res["data"]["result"]:
                    self.logger.warning("当前页面处于抖动状态，请检查")
                    self.tools.clickOther()
                break

        self.tools.click_app_by_center("{{AppNameCn}}")
        self.tools.os6DragFullScreean()

        time.sleep(5)
        self.screenshot(is_instrument_required=False, sceenshot_name="{{screenshot_name}}", pic_num=1,
                        interval=1, is_RSE_required=False, is_CNSL_required=False,
                        is_PSG_required=False)

        ask = "检测当前页面是否{{验证描述}},返回boolean到result中"
        res = self.tools.CheckResApi(ask, [self.picture_path_list[-1]])
        assert res["data"]["result"] == True
```

---

## 模式3：前置条件模式（需要特殊 VDT 信号）

适用于需要额外系统状态准备的场景（如睡眠空间需要设置续航里程）。

在 `clickapplist()` 方法开头添加前置命令：

```python
    @retry
    def clickapplist(self):
        self.logger.info("进入{{AppNameCn}}的前置准备")
        os.system("adb root")
        os.system("adb remount")
        self.device.shell("vdt logctrl SIGNALLOST 0")
        self.device.shell("vdt rp VCU_CURRENT_GEARLEV 4")
        # 添加场景所需的 VDT 信号
        self.device.shell("vdt rp {{SIGNAL_NAME}} {{SIGNAL_VALUE}}")

        # 后续同基础模式...
```

---

## 模式4：设备过滤模式（限定/排除车型）

在 `operation()` 中添加设备型号判断：

```python
    def operation(self):
        if self.tools.checkV6Rom():
            # 排除不支持的车型
            excluded = ("E29", "E28", "H93", "D55", "D20", "D21", "D22")
            if self.tools.get_device_model() in excluded:
                print("非{{功能名}}车型跳过执行")
            else:
                self.clickapplist()
        else:
            print("非V6版本跳过执行")
```

---

## 模式5：二次验证模式（首次断言失败后重试）

适用于页面加载较慢或内容动态变化的场景：

```python
        ask = "检测当前页面是否{{验证描述1}},返回boolean到result中"
        res = self.tools.CheckResApi(ask, [self.picture_path_list[-1]])
        if res["data"]["result"] == False:
            self.logger.info("未检测到相关文字")
            time.sleep(2)
            self.screenshot(is_instrument_required=False, sceenshot_name="{{screenshot_name}}", pic_num=1,
                            interval=1, is_RSE_required=False, is_CNSL_required=False,
                            is_PSG_required=False)
            ask = "检测当前页面是否{{验证描述2}},返回boolean到result中"
            res2 = self.tools.CheckResApi(ask, [self.picture_path_list[-1]])
            assert res2["data"]["result"] == True
```

---

## 模式6：弹窗处理模式（用户协议/提示弹窗）

适用于首次打开应用时有弹窗需要处理：

```python
        # 处理用户协议弹窗
        if self.ui(resourceId="{{package}}:id/checkbox").exists():
            self.logger.info("点击用户协议")
            self.ui(resourceId="{{package}}:id/checkbox").click()
            time.sleep(2)
            if self.ui(text="同意并继续").exists:
                self.ui(text="同意并继续").click()

        # 处理提示弹窗
        if self.ui(text="知道了").exists():
            self.ui(text="知道了").click()
```
