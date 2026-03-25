# -*- coding: utf-8 -*-
"""JAKA 画心形 + JAKA - 优化版：大间距 + 无多余轨迹"""
import sys, os, time, math
sys.stdout.reconfigure(encoding='utf-8')

JAKA_DIR = "C:/Users/Administrator/.openclaw-fullbackup-20260313-161518/workspace/projects/OpenClaw_Jaka_Integration"
sys.path.insert(0, JAKA_DIR)
try: os.add_dll_directory(JAKA_DIR)
except: pass
import jkrc

r = jkrc.RC("192.168.57.128")
r.login(1)

HOME = (math.pi/2,)*6

def draw_line(p1, p2, speed=100):
    steps = 15
    for i in range(steps+1):
        t = i/steps
        x = p1[0] + (p2[0]-p1[0])*t
        y = p1[1] + (p2[1]-p1[1])*t
        r.linear_move((x, y, p1[2], p1[3], p1[4], p1[5]), 0, True, speed)

def move_safe(p1, p2, lift=50, speed=150):
    """安全移动：抬 Z→平移→降 Z，不留轨迹"""
    # 抬 Z
    r.linear_move((p1[0], p1[1], p1[2]+lift, p1[3], p1[4], p1[5]), 0, True, speed)
    # 平移
    r.linear_move((p2[0], p2[1], p2[2]+lift, p2[3], p2[4], p2[5]), 0, True, speed)
    # 降 Z
    r.linear_move(p2, 0, True, speed)

# 先回 Home 准备
r.joint_move(HOME, 0, True, 0.5)
time.sleep(0.5)

tcp = r.get_tcp_position()[1]
base_x, base_y, base_z = tcp[0], tcp[1], tcp[2]
rx, ry, rz = tcp[3], tcp[4], tcp[5]

print("=" * 60)
print("  心形 + JAKA 优化版 (大间距 + 无多余轨迹)")
print("=" * 60)

# 大间距：每个元素 100mm
offsets = [0, 100, 200, 300, 400]
names = ["心形 ❤️", "J", "A", "K", "A"]

for idx, (offset, name) in enumerate(zip(offsets, names)):
    print(f"\n【{idx+1}】绘制 {name} (X 偏移={offset}mm)")
    
    cx = base_x + offset
    cy = base_y
    cz = base_z
    
    if idx == 0:
        # 心形
        SCALE = 10
        def heart(t):
            x = 16*(math.sin(t)**3)*SCALE
            y = (13*math.cos(t)-5*math.cos(2*t)-2*math.cos(3*t)-math.cos(4*t))*SCALE
            return (cx+x, cy+y, cz, rx, ry, rz)
        start = heart(0)
        r.linear_move(start, 0, True, 80)
        for i in range(1, 101):
            r.linear_move(heart(2*math.pi*i/100), 0, True, 80)
        current = start
    
    elif idx == 1:
        # J
        p1 = (cx+15, cy-40, cz, rx, ry, rz)
        p2 = (cx+15, cy+30, cz, rx, ry, rz)
        p3 = (cx-5, cy+40, cz, rx, ry, rz)
        if idx > 0:
            move_safe(current, p1)
        else:
            r.linear_move(p1, 0, True, 80)
        draw_line(p1, p2)
        draw_line(p2, p3)
        current = p3
    
    elif idx == 2:
        # A
        p1 = (cx, cy+40, cz, rx, ry, rz)
        p2 = (cx-18, cy-40, cz, rx, ry, rz)
        p3 = (cx+18, cy-40, cz, rx, ry, rz)
        p4 = (cx-8, cy-12, cz, rx, ry, rz)
        p5 = (cx+8, cy-12, cz, rx, ry, rz)
        move_safe(current, p1)
        draw_line(p1, p2)
        move_safe(p2, p1)
        draw_line(p1, p3)
        move_safe(p1, p4)
        draw_line(p4, p5)
        current = p5
    
    elif idx == 3:
        # K
        p1 = (cx-15, cy+40, cz, rx, ry, rz)
        p2 = (cx-15, cy-40, cz, rx, ry, rz)
        pm = (cx-15, cy, cz, rx, ry, rz)
        p3 = (cx+12, cy-25, cz, rx, ry, rz)
        p4 = (cx+12, cy+25, cz, rx, ry, rz)
        move_safe(current, p1)
        draw_line(p1, p2)
        move_safe(p2, pm)
        draw_line(pm, p3)
        move_safe(pm, pm)
        draw_line(pm, p4)
        current = p4
    
    elif idx == 4:
        # A (重复)
        p1 = (cx, cy+40, cz, rx, ry, rz)
        p2 = (cx-18, cy-40, cz, rx, ry, rz)
        p3 = (cx+18, cy-40, cz, rx, ry, rz)
        p4 = (cx-8, cy-12, cz, rx, ry, rz)
        p5 = (cx+8, cy-12, cz, rx, ry, rz)
        move_safe(current, p1)
        draw_line(p1, p2)
        move_safe(p2, p1)
        draw_line(p1, p3)
        move_safe(p1, p4)
        draw_line(p4, p5)
        current = p5
    
    print(f"  ✅ {name} 完成")

# 最后回 Home
print("\n⬅️  返回 Home...")
r.joint_move(HOME, 0, True, 0.5)

print("\n" + "=" * 60)
print("  ❤️ JAKA 完成！")
print("=" * 60)
r.logout()
