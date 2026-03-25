# -*- coding: utf-8 -*-
"""JAKA 单摆模拟 - 周期 2 秒"""
import sys, os, time, math
sys.stdout.reconfigure(encoding='utf-8')

JAKA_DIR = "C:/Users/Administrator/.openclaw-fullbackup-20260313-161518/workspace/projects/OpenClaw_Jaka_Integration"
sys.path.insert(0, JAKA_DIR)
try: os.add_dll_directory(JAKA_DIR)
except: pass
import jkrc

# 单摆参数
T = 2.0         # 周期 2 秒
OMEGA = math.pi / T  # 角频率 π rad/s
AMP = math.radians(30)  # 振幅 ±30°
CYCLES = 5      # 摆动 5 个周期
DT = 0.05       # 控制周期 50ms

r = jkrc.RC("192.168.57.128")
r.login(1)

print("=" * 50)
print(f"  单摆模拟 - 周期{T}秒，振幅±30°")
print(f"  使用 J5 关节 (手腕)")
print("=" * 50)

# 读取初始位置
pos = r.get_joint_position()[1]
base_joints = list(pos)
print(f"\n初始位置：J5={math.degrees(base_joints[4]):.1f}°")

# 先移动到平衡位置 (90°)
base_joints[4] = math.radians(90)
r.joint_move(tuple(base_joints), 0, True, 0.5)
print("移动到平衡位置 (90°)")
time.sleep(0.5)

# 单摆运动
print(f"\n开始摆动 ({CYCLES}个周期，约{CYCLES*T}秒)...")
start_time = time.time()

for cycle in range(CYCLES):
    # 每个周期采样 40 点 (2 秒/40 = 50ms)
    for i in range(40):
        t = cycle * T + i * DT
        # 单摆方程：θ = θ₀ * cos(ωt)
        angle = AMP * math.cos(OMEGA * t)
        
        # 叠加到基础位置 (90°平衡点)
        target = base_joints.copy()
        target[4] = math.radians(90) + angle
        
        # 发送指令 (非阻塞)
        r.joint_move(tuple(target), 0, False, 0.8)
        time.sleep(DT)
    
    # 每周期报告
    elapsed = time.time() - start_time
    print(f"  周期{cycle+1}/{CYCLES} 完成 (耗时{elapsed:.1f}s)")

elapsed = time.time() - start_time
print(f"\n摆动完成！总耗时：{elapsed:.1f}s")

# 回到平衡位置
r.joint_move(tuple(base_joints), 0, True, 0.5)
print("回到平衡位置")

# 读取最终位置
pos = r.get_joint_position()[1]
print(f"最终 J5={math.degrees(pos[4]):.1f}°")

print("\n" + "=" * 50)
print("  单摆模拟完成！")
print("=" * 50)

r.logout()
