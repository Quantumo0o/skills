# -*- coding: utf-8 -*-
"""
OpenClaw CN Robot Skills - JAKA Skill
Brand: JAKA Robotics (节卡)
SDK: jkrc (Official Python SDK)
Docs: https://www.jaka.com/docs/guide/SDK/introduction.html

功能:
- 支持 TCP 和 gRPC 两种通信模式
- 关节运动控制
- 直线运动控制
- 状态读取与监控
- 仿真同步支持
"""

import sys
import os
import time
import math
from typing import Dict, List, Optional, Tuple
from pathlib import Path

# 添加项目目录（包含 jkrc.pyd）
JAKA_INTEGRATION_DIR = "C:/Users/Administrator/.openclaw-fullbackup-20260313-161518/workspace/projects/OpenClaw_Jaka_Integration"
PROJECT_DIR = str(Path(__file__).parent)

sys.path.insert(0, JAKA_INTEGRATION_DIR)
sys.path.insert(0, PROJECT_DIR)

try:
    os.add_dll_directory(JAKA_INTEGRATION_DIR)
except:
    pass

import jkrc


class JAKARobot:
    """
    JAKA 机器人控制类
    
    ⚠️ 重要：必须使用 gRPC 模式 (use_grpc=True)
    原因：
    - gRPC 支持多路并发，可同时控制真机 + 仿真同步
    - TCP 模式只支持单路通信，仿真无法同步
    - JAKA Studio Pro 仿真软件需要 gRPC 通道
    
    用法:
        robot = JAKARobot("192.168.57.128", use_grpc=True)  # ⚠️ 必须 use_grpc=True
        robot.connect()
        robot.move_joint([0, 0, 0, 0, 0, 0])
        robot.disconnect()
    """
    
    def __init__(self, ip: str, port: int = 502, use_grpc: bool = True):
        """
        初始化机器人
        
        Args:
            ip: 机器人 IP 地址
            port: 端口号 (TCP 模式用)
            use_grpc: ⚠️ 必须为 True! 使用 gRPC 模式支持仿真同步
        """
        """
        初始化机器人
        
        Args:
            ip: 机器人 IP 地址
            port: 端口号 (TCP 模式用)
            use_grpc: 是否使用 gRPC 模式 (推荐 True)
        """
        self.ip = ip
        self.port = port
        self.use_grpc = use_grpc
        self.robot = None
        self.connected = False
        self.last_state = None
    
    def connect(self, timeout: int = 3) -> bool:
        """
        连接机器人
        
        Args:
            timeout: 连接超时时间 (秒)
            
        Returns:
            bool: 连接是否成功
        """
        try:
            self.robot = jkrc.RC(self.ip)
            
            for attempt in range(timeout):
                mode_str = "gRPC" if self.use_grpc else "TCP"
                print(f"[JAKA] 正在{mode_str}模式连接 {self.ip}...")
                
                ret = self.robot.login(1 if self.use_grpc else 0)
                
                if ret and ret[0] == 0:
                    self.connected = True
                    print(f"[JAKA] 连接成功!")
                    return True
                else:
                    print(f"[JAKA] 连接失败 ({attempt+1}/{timeout}): {ret}")
                    time.sleep(1)
            
            return False
            
        except Exception as e:
            print(f"[JAKA] 连接异常：{e}")
            return False
    
    def disconnect(self):
        """断开连接"""
        if self.robot and self.connected:
            try:
                self.robot.logout()
                print("[JAKA] 已断开连接")
            except:
                pass
            self.connected = False
    
    def get_state(self) -> Optional[Dict]:
        """
        读取机器人状态
        
        Returns:
            Dict 包含关节位置、TCP 位置等，失败返回 None
        """
        if not self.connected:
            return None
        
        try:
            # 读取关节位置 (保持 SDK 原始精度，不做转换)
            pos_ret = self.robot.get_joint_position()
            if pos_ret is None or len(pos_ret) < 2:
                return None
            
            # 直接保存原始弧度值
            position_rad = list(pos_ret[1])
            
            # 读取 TCP 位置
            tcp_ret = self.robot.get_tcp_position()
            tcp_pos = tcp_ret[1] if tcp_ret and len(tcp_ret) > 1 else None
            
            state = {
                "timestamp": time.time(),
                "joint_names": ["joint1", "joint2", "joint3", "joint4", "joint5", "joint6"],
                "position": position_rad,  # 原始弧度值
                "position_deg": [math.degrees(p) for p in position_rad],  # 角度值（只读，不参与控制）
                "tcp_position": list(tcp_pos) if tcp_pos else None
            }
            
            self.last_state = state
            return state
            
        except Exception as e:
            print(f"[JAKA] 读取状态失败：{e}")
            return None
    
    def move_joint(self, target_pos: List[float], 
                   speed: float = 0.2, 
                   wait: bool = True) -> bool:
        """
        关节运动
        
        Args:
            target_pos: 目标位置 [J1, J2, J3, J4, J5, J6] (弧度)
            speed: 速度 (0.0-1.0)
            wait: 是否等待完成
            
        Returns:
            bool: 是否成功
        """
        if not self.connected:
            print("[JAKA] 未连接")
            return False
        
        try:
            # 确保 6 个关节
            if len(target_pos) < 6:
                target_pos = target_pos + [0.0] * (6 - len(target_pos))
            
            # 发送指令
            ret = self.robot.joint_move(
                tuple(target_pos[:6]),
                0,  # ABS 绝对运动
                wait,
                speed
            )
            
            if ret and ret[0] == 0:
                print(f"[JAKA] 关节运动成功")
                return True
            else:
                print(f"[JAKA] 关节运动失败：{ret}")
                return False
                
        except Exception as e:
            print(f"[JAKA] 运动异常：{e}")
            return False
    
    def move_linear(self, position: List[float],
                    speed: float = 0.1,
                    wait: bool = True) -> bool:
        """
        直线运动
        
        Args:
            position: [X, Y, Z, RX, RY, RZ] (mm, rad)
            speed: 速度
            wait: 是否等待完成
            
        Returns:
            bool: 是否成功
        """
        if not self.connected:
            print("[JAKA] 未连接")
            return False
        
        try:
            if len(position) < 6:
                position = position + [0.0] * (6 - len(position))
            
            ret = self.robot.linear_move(
                tuple(position[:6]),
                0,  # ABS
                wait,
                speed
            )
            
            if ret and ret[0] == 0:
                print(f"[JAKA] 直线运动成功")
                return True
            else:
                print(f"[JAKA] 直线运动失败：{ret}")
                return False
                
        except Exception as e:
            print(f"[JAKA] 运动异常：{e}")
            return False
    
    def move_jog(self, joint_id: int, direction: int = 1, 
                 speed: float = 0.1, duration: float = 0.5) -> bool:
        """
        点动 (JOG) 运动
        
        Args:
            joint_id: 关节编号 (1-6)
            direction: 方向 (1=正向，-1=反向)
            speed: 速度
            duration: 持续时间 (秒)
            
        Returns:
            bool: 是否成功
        """
        if not self.connected:
            return False
        
        try:
            # 启动 JOG
            ret = self.robot.jog(
                joint_id - 1,  # 0-based
                jkrc.MoveMode.INCR if hasattr(jkrc, 'MoveMode') else 1,
                0,  # BASE 坐标
                speed,
                direction * 0.1
            )
            
            # 持续指定时间
            time.sleep(duration)
            
            # 停止 JOG
            self.robot.jog_stop(joint_id - 1)
            
            print(f"[JAKA] JOG 完成：J{joint_id} {direction*duration}秒")
            return True
            
        except Exception as e:
            print(f"[JAKA] JOG 异常：{e}")
            return False
    
    def power_on(self) -> bool:
        """上电"""
        if not self.robot:
            return False
        ret = self.robot.power_on()
        return ret is None or (ret and ret[0] == 0)
    
    def enable(self) -> bool:
        """使能机器人"""
        if not self.robot:
            return False
        ret = self.robot.enable_robot()
        return ret is None or (ret and ret[0] == 0)
    
    def get_info(self) -> Optional[Dict]:
        """获取机器人信息"""
        if not self.connected:
            return None
        
        try:
            ver_ret = self.robot.get_sdk_version()
            if ver_ret and len(ver_ret) > 1:
                v = ver_ret[1]
                return {
                    "sdk_version": f"{v[0]}.{v[1]}.{v[2]}.{v[3]}",
                    "ip": self.ip,
                    "mode": "gRPC" if self.use_grpc else "TCP"
                }
            return None
        except:
            return None
    
    def print_state(self):
        """打印当前状态"""
        state = self.get_state()
        if not state:
            print("[JAKA] 无法读取状态")
            return
        
        print("\n" + "=" * 50)
        print(f"时间：{time.strftime('%H:%M:%S')}")
        print(f"IP: {self.ip} ({'gRPC' if self.use_grpc else 'TCP'})")
        print("=" * 50)
        print("关节位置:")
        for i, (name, deg) in enumerate(zip(state['joint_names'], state['position_deg']), 1):
            print(f"  J{i} ({name}): {deg:7.2f}°")
        
        if state.get('tcp_position'):
            tcp = state['tcp_position']
            print(f"\nTCP 位置:")
            print(f"  X={tcp[0]:6.1f}mm, Y={tcp[1]:6.1f}mm, Z={tcp[2]:6.1f}mm")
            print(f"  RX={math.degrees(tcp[3]):6.1f}°, RY={math.degrees(tcp[4]):6.1f}°, RZ={math.degrees(tcp[5]):6.1f}°")
        print("=" * 50 + "\n")


# 快捷函数
def connect_robot(ip: str, use_grpc: bool = True) -> Optional[JAKARobot]:
    """快速连接机器人"""
    robot = JAKARobot(ip, use_grpc=use_grpc)
    if robot.connect():
        return robot
    return None


def move_to_home(robot: JAKARobot) -> bool:
    """回到home位置 (0,0,0,0,0,0)"""
    home_pos = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    return robot.move_joint(home_pos, speed=0.2, wait=True)


def test_motion(robot: JAKARobot, joint_id: int, angle_deg: float = 90):
    """测试单个关节运动"""
    state = robot.get_state()
    if not state:
        return False
    
    # 计算目标位置
    target = state['position'].copy()
    target[joint_id - 1] += math.radians(angle_deg)
    
    print(f"[TEST] J{joint_id} 旋转 {angle_deg}°")
    robot.move_joint(target, speed=0.15, wait=True)
    time.sleep(2)
    
    # 验证
    state2 = robot.get_state()
    if state2:
        actual = math.degrees(state2['position'][joint_id - 1])
        print(f"[OK] 实际位置：{actual:.2f}°")
    
    return True
