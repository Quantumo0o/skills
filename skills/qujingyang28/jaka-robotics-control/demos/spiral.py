# -*- coding: utf-8 -*-
"""JAKA 阿基米德螺旋线 - 合理臂展范围"""
import sys, os, time, math
sys.stdout.reconfigure(encoding='utf-8')

JAKA_DIR = "C:/Users/Administrator/.openclaw-fullbackup-20260313-161518/workspace/projects/OpenClaw_Jaka_Integration"
sys.path.insert(0, JAKA_DIR)
try: os.add_dll_directory(JAKA_DIR)
except: pass
import jkrc

# 螺旋参数
R_START = 100   # 起始半径 mm
R_END = 400     # 结束半径 mm (JAKA Zu20 工作空间内)
TURNS = 3       # 3 圈螺旋
STEPS = 180     # 插值点数
SPEED = 150     # mm/s

r = jkrc.RC("192.168.57.128")
r.login(1)

tcp = r.get_tcp_position()[1]
cx, cy, cz = tcp[0], tcp[1], tcp[2]
rx, ry, rz = tcp[3], tcp[4], tcp[5]
print(f"螺旋中心：X={cx:.1f} Y={cy:.1f} Z={cz:.1f}")
print(f"半径范围：{R_START}mm ~ {R_END}mm ({TURNS}圈)")

# 阿基米德螺旋：r = a + b*θ
a = R_START
b = (R_END - R_START) / (2 * math.pi * TURNS)

# 移动到起点 (θ=0)
start_x = cx + a
print(f"移动到起点：X={start_x:.1f} Y={cy:.1f}")
r.linear_move((start_x, cy, cz, rx, ry, rz), 0, True, SPEED)
time.sleep(0.3)

# 螺旋插值
print(f"画螺旋中 ({STEPS} 点)...")
start_time = time.time()
for i in range(1, STEPS + 1):
    theta = 2 * math.pi * TURNS * i / STEPS
    radius = a + b * theta
    
    px = cx + radius * math.cos(theta)
    py = cy + radius * math.sin(theta)
    
    r.linear_move((px, py, cz, rx, ry, rz), 0, True, SPEED)
    
    if i % (STEPS // TURNS) == 0:
        turn = i // (STEPS // TURNS)
        elapsed = time.time() - start_time
        print(f"  第{turn}圈完成 -> r={radius:.1f}mm (耗时{elapsed:.1f}s)")

elapsed = time.time() - start_time
print(f"\n螺旋完成！总耗时：{elapsed:.1f}s")

# 验证终点
tcp = r.get_tcp_position()[1]
err = math.sqrt((tcp[0]-cx)**2 + (tcp[1]-cy)**2)
print(f"终点半径误差：{abs(err - R_END):.2f}mm")
print(f"最终位置：X={tcp[0]:.1f} Y={tcp[1]:.1f} Z={tcp[2]:.1f}")

r.logout()
