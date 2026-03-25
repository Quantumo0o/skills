# JAKA Robotics Control Skill

节卡机器人控制技能，支持 Zu20/Zu12/Zu7 全系列协作机器人。

## 功能特性

- ✅ 关节运动控制 (精度 < 0.01°)
- ✅ 直线插补 (精度 < 0.5mm)
- ✅ 圆弧插补 (支持整圆)
- ✅ gRPC/TCP 双模式
- ✅ 仿真同步支持
- ✅ 状态实时监控
- ✅ 命令行工具

## 快速开始

```python
from jaka_skill import JAKARobot

robot = JAKARobot("192.168.57.128", use_grpc=True)
robot.connect()

# 关节运动 (弧度)
robot.move_joint([0, 0, 0, 0, 0, 0], speed=0.5)

# 直线运动 (mm, rad)
robot.move_linear([300, 0, 200, 3.14, 0, 0], speed=100)

# 读取状态
state = robot.get_state()
print(state['joints_deg'])

robot.disconnect()
```

## 命令行工具

```bash
# 读取状态
python jaka_cmd.py state

# 回零
python jaka_cmd.py home

# 关节运动 (角度)
python jaka_cmd.py joint 90 90 90 90 90 90

# 直线运动 (mm, 度)
python jaka_cmd.py linear 300 0 200 180 0 0
```

## 演示脚本

- `demos/heart_jaka.py` - 心形 +JAKA 绘制
- `demos/spiral.py` - 阿基米德螺旋线
- `demos/pendulum.py` - 单摆模拟 (T=2s)
- `demos/dance.py` - 舞蹈序列

## 环境要求

- Python 3.8+
- JAKA SDK V2.3.1+ (jkrc.pyd)
- Windows

## 安装

1. 下载 JAKA SDK: https://www.jaka.com/docs/guide/SDK/introduction.html
2. 复制 `jkrc.pyd` 到技能目录
3. 配置机器人 IP (编辑 `jaka_cmd.py`)

## 安全提示

⚠️ 首次使用前请确保：
- 工作空间内无人
- 急停按钮可用
- 先在仿真环境测试
- 速度倍率从低速开始

## 作者

JMO / Robotqu (青岛)
- 网站：robotqu.com
- B 站：Robot_Qu 机器人社区

## 许可证

MIT-0
