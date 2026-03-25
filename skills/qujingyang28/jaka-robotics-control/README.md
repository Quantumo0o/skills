# JAKA Robotics Skill for OpenClaw

**品牌**: JAKA Robotics (节卡机器人)  
**型号**: Zu20, Zu12, Zu7 等系列  
**SDK**: jkrc V2.3.1+  
**作者**: JMO / Robotqu (青岛)  
**版本**: 1.0.0  
**日期**: 2026-03-23

---

## 📦 功能特性

### 核心功能
- ✅ **gRPC/TCP 双模式** - 支持仿真同步
- ✅ **关节运动控制** - 精度 < 0.01°
- ✅ **直线运动控制** - 精度 < 0.5mm
- ✅ **圆弧运动控制** - 支持整圆
- ✅ **状态实时监控** - 关节/TCP/错误码
- ✅ **速度倍率调节** - 1-100%
- ✅ **自动回 Home** - 任务结束自动归位

### 高级功能
- ✅ **一笔画轨迹** - 连续路径无抬笔
- ✅ **最短路径规划** - 元素间智能连接
- ✅ **参数化图形** - 心形/圆形/正方形等
- ✅ **单摆模拟** - 简谐振动演示
- ✅ **舞蹈序列** - 预设动作库

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 安装 JAKA SDK
# 下载地址：https://www.jaka.com/docs/guide/SDK/introduction.html

# 复制 jkrc.pyd 到项目目录
cp "SDK 目录/Windows/jkrc.pyd" ./jaka-integration/
```

### 2. 基础使用

```python
from jaka_skill import JAKARobot

# 连接机器人
robot = JAKARobot("192.168.57.128", use_grpc=True)
robot.connect()

# 关节运动 (弧度)
robot.move_joint([0, 0, 0, 0, 0, 0], speed=0.5)

# 直线运动 (mm, rad)
robot.move_linear([300, 0, 200, 3.14, 0, 0], speed=100)

# 读取状态
state = robot.get_state()
print(state['joints_deg'])

# 断开
robot.disconnect()
```

### 3. 命令行工具

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

---

## 📁 文件结构

```
jaka/
├── jaka_skill.py              # 核心技能类
├── jaka_cmd.py                # 命令行工具
├── demos/
│   ├── heart.py               # 心形绘制
│   ├── circle.py              # 圆形绘制
│   ├── square.py              # 正方形
│   ├── spiral.py              # 螺旋线
│   ├── pendulum.py            # 单摆模拟
│   └── dance.py               # 舞蹈序列
├── examples/
│   ├── pick_place.py          # 搬运示例
│   └── welding.py             # 焊接示例
└── README.md                  # 本文档
```

---

## ⚙️ 配置说明

### 机器人参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| IP 地址 | 192.168.57.128 | 机器人控制器 IP |
| 端口 | 502 | TCP 模式端口 |
| 模式 | gRPC | 推荐 gRPC 支持仿真 |

### 安全参数

| 参数 | 默认值 | 范围 | 说明 |
|------|--------|------|------|
| 速度倍率 | 100% | 1-100% | 示教器调整 |
| 关节速度 | 0.5 rad/s | 0.1-1.0 | 安全推荐 |
| TCP 速度 | 100 mm/s | 50-500 | 安全推荐 |

---

## 🎯 经典示例

### 1. 画心形

```python
import math
from jaka_skill import JAKARobot

robot = JAKARobot("192.168.57.128")
robot.connect()

# 移动到起点
robot.move_linear([x, y, z, rx, ry, rz], speed=100)

# 画心形 (参数方程)
SCALE = 5
for i in range(101):
    t = 2 * math.pi * i / 100
    x = 16 * (math.sin(t) ** 3) * SCALE
    y = (13*math.cos(t) - 5*math.cos(2*t) - 2*math.cos(3*t) - math.cos(4*t)) * SCALE
    robot.move_linear([x, y, z, rx, ry, rz], speed=80)

robot.disconnect()
```

### 2. 阿基米德螺旋线

```python
# 螺旋参数
R_START = 100  # mm
R_END = 400    # mm
TURNS = 3      # 圈数

for i in range(181):
    theta = 2 * math.pi * TURNS * i / 180
    radius = R_START + (R_END - R_START) * theta / (2 * math.pi * TURNS)
    x = cx + radius * math.cos(theta)
    y = cy + radius * math.sin(theta)
    robot.move_linear([x, y, z, rx, ry, rz], speed=150)
```

### 3. 单摆模拟

```python
# 单摆参数
T = 2.0          # 周期 2 秒
AMP = 30         # 振幅 ±30°
OMEGA = math.pi / T

for cycle in range(5):
    for i in range(40):
        t = cycle * T + i * 0.05
        angle = math.radians(AMP) * math.cos(OMEGA * t)
        # 应用到 J5 关节
        robot.move_joint([0, 0, 0, 0, math.radians(90)+angle, 0], speed=0.8)
        time.sleep(0.05)
```

---

## ⚠️ 注意事项

### 1. 必须使用 gRPC 模式

```python
# ✅ 正确
robot = JAKARobot("192.168.57.128", use_grpc=True)

# ❌ 错误 (不支持仿真同步)
robot = JAKARobot("192.168.57.128", use_grpc=False)
```

### 2. 速度单位

```python
# 关节速度：rad/s
robot.move_joint(target, speed=0.5)  # 0.5 rad/s ≈ 28.6°/s

# TCP 速度：mm/s
robot.move_linear(target, speed=100)  # 100 mm/s
```

### 3. Home 位置约定

```python
# 推荐 Home 位置：所有关节 90°
HOME = [math.pi/2] * 6

# 任务结束后回 Home
robot.move_joint(HOME, speed=0.5)
```

### 4. 奇异点规避

```python
# 推荐姿态：所有关节 90° (末端朝下)
# 远离奇异点，逆运动学解唯一
```

---

## 📊 性能指标

| 运动类型 | 精度 | 重复性 | 最大速度 |
|---------|------|--------|---------|
| 关节运动 | < 0.01° | 完美 | 1.0 rad/s |
| 直线运动 | < 0.5mm | < 0.1mm | 500 mm/s |
| 圆弧运动 | < 1.0mm | < 0.5mm | 300 mm/s |

---

## 🐛 已知问题

### 1. SDK 阻塞模式 Bug

```python
# ❌ 避免使用阻塞模式
robot.move_joint(target, wait=True)  # 可能卡住

# ✅ 推荐非阻塞 + 轮询
robot.move_joint(target, wait=False)
while not at_target():
    time.sleep(0.2)
```

### 2. 速度倍率显示

```python
# get_rapidrate() 返回 1.0 表示 100% (不是 1%)
# 在示教器上确认实际倍率
```

---

## 📞 技术支持

- **作者**: JMO / Robotqu
- **位置**: 青岛
- **网站**: robotqu.com
- **B 站**: Robot_Qu 机器人社区
- **GitHub**: [待补充]

---

## 📝 更新日志

### v1.0.0 (2026-03-23)
- ✅ 初始版本发布
- ✅ 核心运动控制
- ✅ 命令行工具
- ✅ 演示示例库
- ✅ 完整文档

---

## 📄 许可证

MIT License

---

**Happy Coding! 🤖**
