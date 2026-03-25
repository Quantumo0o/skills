# -*- coding: utf-8 -*-
"""JAKA 简单舞蹈"""
import sys, os, time, math
sys.stdout.reconfigure(encoding='utf-8')

JAKA_DIR = "C:/Users/Administrator/.openclaw-fullbackup-20260313-161518/workspace/projects/OpenClaw_Jaka_Integration"
sys.path.insert(0, JAKA_DIR)
try: os.add_dll_directory(JAKA_DIR)
except: pass
import jkrc

r = jkrc.RC("192.168.57.128")
r.login(1)

print("舞蹈开始！")

# 回零
r.joint_move((0,0,0,0,0,0), 0, True, 0.5)

# 1. 摇头
print("1. 摇头")
r.joint_move((0.5,0,0,0,0,0), 0, True, 0.8)
time.sleep(0.3)
r.joint_move((-0.5,0,0,0,0,0), 0, True, 0.8)
time.sleep(0.3)
r.joint_move((0.3,0,0,0,0,0), 0, True, 0.8)
time.sleep(0.3)
r.joint_move((-0.3,0,0,0,0,0), 0, True, 0.8)

# 2. 点头
print("2. 点头")
r.joint_move((0,-0.5,0.5,0,0,0), 0, True, 0.8)
time.sleep(0.3)
r.joint_move((0,0.3,-0.3,0,0,0), 0, True, 0.8)
time.sleep(0.3)
r.joint_move((0,-0.3,0.3,0,0,0), 0, True, 0.8)
time.sleep(0.3)

# 3. 转手腕
print("3. 转手腕")
r.joint_move((0,0,0,0,0,1.5), 0, True, 1.0)
time.sleep(0.3)
r.joint_move((0,0,0,0,0,-1.5), 0, True, 1.0)
time.sleep(0.3)
r.joint_move((0,0,0,0,0,0.8), 0, True, 1.0)
time.sleep(0.3)

# 4. 侧倾
print("4. 侧倾")
r.joint_move((0,0,0,0.5,0.3,0), 0, True, 0.8)
time.sleep(0.3)
r.joint_move((0,0,0,-0.5,-0.3,0), 0, True, 0.8)
time.sleep(0.3)

# 5. 结束 Pose
print("5. 结束 Pose")
r.joint_move((0.2,-0.4,0.4,0.2,0.2,0.5), 0, True, 0.6)
time.sleep(0.5)

# 回零谢幕
print("谢幕!")
r.joint_move((0,0,0,0,0,0), 0, True, 0.5)

print("舞蹈完成！🎉")
r.logout()
