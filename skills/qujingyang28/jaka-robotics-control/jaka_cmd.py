# -*- coding: utf-8 -*-
"""
JAKA 通用控制脚本 - 命令行模式
用法:
  python jaka_cmd.py state                    # 读取状态
  python jaka_cmd.py home                     # 回零
  python jaka_cmd.py joint J1 J2 J3 J4 J5 J6  # 关节运动(角度)
  python jaka_cmd.py linear X Y Z RX RY RZ    # 直线运动(mm,度)
  python jaka_cmd.py jog JOINT_ID DIRECTION   # 点动
  python jaka_cmd.py power_on                  # 上电使能
  python jaka_cmd.py clear_error               # 清除错误
"""

import sys
import os
import time
import math
import json

sys.stdout.reconfigure(encoding='utf-8')

JAKA_DIR = "C:/Users/Administrator/.openclaw-fullbackup-20260313-161518/workspace/projects/OpenClaw_Jaka_Integration"
sys.path.insert(0, JAKA_DIR)
try:
    os.add_dll_directory(JAKA_DIR)
except:
    pass

import jkrc

ROBOT_IP = "192.168.57.128"

def connect():
    r = jkrc.RC(ROBOT_IP)
    ret = r.login(1)
    if ret[0] != 0:
        print(json.dumps({"ok": False, "error": f"连接失败: {ret}"}))
        sys.exit(1)
    return r

def cmd_state(r):
    pos_ret = r.get_joint_position()
    tcp_ret = r.get_tcp_position()
    status_ret = r.get_robot_status()
    rate_ret = r.get_rapidrate()
    err_ret = r.get_last_error()

    result = {"ok": True}

    if pos_ret and pos_ret[0] == 0:
        joints_rad = list(pos_ret[1])
        result["joints_rad"] = [round(j, 4) for j in joints_rad]
        result["joints_deg"] = [round(math.degrees(j), 2) for j in joints_rad]

    if tcp_ret and tcp_ret[0] == 0:
        tcp = tcp_ret[1]
        result["tcp"] = {
            "x": round(tcp[0], 1), "y": round(tcp[1], 1), "z": round(tcp[2], 1),
            "rx_deg": round(math.degrees(tcp[3]), 1),
            "ry_deg": round(math.degrees(tcp[4]), 1),
            "rz_deg": round(math.degrees(tcp[5]), 1)
        }

    if status_ret and status_ret[0] == 0:
        s = status_ret[1]
        result["mode"] = "auto" if s[2] == 1 else "manual"
        result["enabled"] = s[3] == 1

    if rate_ret and rate_ret[0] == 0:
        result["rapidrate"] = rate_ret[1]

    if err_ret and len(err_ret) > 1:
        result["error_code"] = err_ret[1][0]
        result["error_msg"] = err_ret[1][1]

    print(json.dumps(result, ensure_ascii=False))

def cmd_joint(r, args):
    if len(args) < 6:
        print(json.dumps({"ok": False, "error": "需要6个关节角度"}))
        return
    target = [math.radians(float(a)) for a in args[:6]]
    speed = float(args[6]) if len(args) > 6 else 0.5

    ret = r.joint_move(tuple(target), 0, False, speed)
    if ret[0] != 0:
        print(json.dumps({"ok": False, "error": f"指令失败: {ret}"}))
        return

    # 轮询等待完成
    for i in range(60):
        time.sleep(0.2)
        pos_ret = r.get_joint_position()
        if pos_ret and pos_ret[0] == 0:
            current = list(pos_ret[1])
            err = max(abs(c - t) for c, t in zip(current, target))
            if err < 0.01:
                actual_deg = [round(math.degrees(c), 2) for c in current]
                print(json.dumps({"ok": True, "joints_deg": actual_deg}))
                return

    print(json.dumps({"ok": False, "error": "超时"}))

def cmd_linear(r, args):
    if len(args) < 6:
        print(json.dumps({"ok": False, "error": "需要6个参数: X Y Z RX RY RZ"}))
        return
    x, y, z = float(args[0]), float(args[1]), float(args[2])
    rx = math.radians(float(args[3]))
    ry = math.radians(float(args[4]))
    rz = math.radians(float(args[5]))
    speed = float(args[6]) if len(args) > 6 else 100  # mm/s

    target = (x, y, z, rx, ry, rz)
    ret = r.linear_move(target, 0, False, speed)
    if ret[0] != 0:
        print(json.dumps({"ok": False, "error": f"指令失败: {ret}"}))
        return

    for i in range(60):
        time.sleep(0.2)
        tcp_ret = r.get_tcp_position()
        if tcp_ret and tcp_ret[0] == 0:
            tcp = tcp_ret[1]
            err = math.sqrt(sum((a - b)**2 for a, b in zip(tcp[:3], target[:3])))
            if err < 1.0:
                result = {
                    "ok": True,
                    "tcp": {"x": round(tcp[0],1), "y": round(tcp[1],1), "z": round(tcp[2],1)},
                    "error_mm": round(err, 2)
                }
                print(json.dumps(result, ensure_ascii=False))
                return

    print(json.dumps({"ok": False, "error": "超时"}))

def cmd_home(r):
    target = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    ret = r.joint_move(target, 0, False, 0.5)
    if ret[0] != 0:
        print(json.dumps({"ok": False, "error": str(ret)}))
        return

    for i in range(60):
        time.sleep(0.2)
        pos_ret = r.get_joint_position()
        if pos_ret and pos_ret[0] == 0:
            err = max(abs(c) for c in pos_ret[1])
            if err < 0.01:
                print(json.dumps({"ok": True, "msg": "已回零"}))
                return

    print(json.dumps({"ok": False, "error": "超时"}))

def cmd_power_on(r):
    r.power_on()
    time.sleep(3)
    r.enable_robot()
    time.sleep(2)
    print(json.dumps({"ok": True, "msg": "已上电使能"}))

def cmd_clear_error(r):
    ret = r.clear_error()
    print(json.dumps({"ok": ret is None or (ret and ret[0]==0), "result": str(ret)}))

def cmd_jog(r, args):
    if len(args) < 2:
        print(json.dumps({"ok": False, "error": "需要: JOINT_ID(1-6) DIRECTION(1/-1) [DURATION]"}))
        return
    joint = int(args[0]) - 1
    direction = int(args[1])
    duration = float(args[2]) if len(args) > 2 else 0.5
    speed = float(args[3]) if len(args) > 3 else 0.1

    r.joint_move(list(r.get_joint_position()[1]), 0, True, 0.01)  # 确保在运动模式

    # 使用关节小幅增量代替 jog
    pos_ret = r.get_joint_position()
    if pos_ret and pos_ret[0] == 0:
        current = list(pos_ret[1])
        step = math.radians(5) * direction  # 5度步进
        current[joint] += step
        ret = r.joint_move(tuple(current), 0, True, speed)
        print(json.dumps({"ok": ret[0]==0, "joint": joint+1, "step_deg": 5*direction}))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1].lower()
    args = sys.argv[2:]

    r = connect()
    try:
        if cmd == "state":
            cmd_state(r)
        elif cmd == "home":
            cmd_home(r)
        elif cmd == "joint":
            cmd_joint(r, args)
        elif cmd == "linear":
            cmd_linear(r, args)
        elif cmd == "jog":
            cmd_jog(r, args)
        elif cmd == "power_on":
            cmd_power_on(r)
        elif cmd == "clear_error":
            cmd_clear_error(r)
        else:
            print(json.dumps({"ok": False, "error": f"未知命令: {cmd}"}))
    finally:
        r.logout()
