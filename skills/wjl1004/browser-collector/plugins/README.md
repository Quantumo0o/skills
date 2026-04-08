# plugins/ - 可扩展插件目录

本目录用于放置第三方或自定义采集器插件。

## 添加插件

在 plugins/ 目录下创建新的采集器模块，例如 `my_collector.py`：

```python
from collectors.registry import register_collector

@register_collector('my_collector')
class MyCollector:
    def __init__(self, config=None):
        self.name = 'my_collector'

    def collect(self, **kwargs):
        # 实现采集逻辑
        pass
```

然后在 `collectors/cli.py` 中添加对应命令。

## 现有插件

暂无
