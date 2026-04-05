#!/usr/bin/env python3
"""
安全模块 - 密码加密与解密
使用Fernet对称加密（AES-CBC）
"""

import os
import base64
import hashlib
from pathlib import Path

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except ImportError:
    import subprocess
    subprocess.check_call(['pip3', 'install', 'cryptography', '--break-system-packages'])
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class SecurityManager:
    """安全管理器 - 处理密码加密/解密"""
    
    KEY_DIR = Path.home() / ".config" / "reg-browser-bot"
    KEY_FILE = KEY_DIR / "key"
    SALT_FILE = KEY_DIR / "salt"
    
    def __init__(self):
        self.fernet = self._get_fernet()
    
    def _get_fernet(self) -> Fernet:
        """获取Fernet加密器"""
        # 确保目录存在
        self.KEY_DIR.mkdir(parents=True, exist_ok=True)
        
        # 优先使用环境变量
        env_key = os.environ.get('REG_BROWSER_KEY')
        if env_key:
            return Fernet(env_key.encode())
        
        # 尝试读取密钥文件
        if self.KEY_FILE.exists() and self.SALT_FILE.exists():
            with open(self.KEY_FILE, 'rb') as f:
                key = f.read()
            return Fernet(key)
        
        # 生成新密钥
        return self._generate_new_key()
    
    def _generate_new_key(self) -> Fernet:
        """生成新的加密密钥"""
        # 生成随机salt
        salt = os.urandom(16)
        with open(self.SALT_FILE, 'wb') as f:
            f.write(salt)
        
        # 使用PBKDF2从主密码派生密钥（这里用机器唯一特征作为主密码）
        machine_id = self._get_machine_id()
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(machine_id.encode()))
        
        # 保存密钥
        with open(self.KEY_FILE, 'wb') as f:
            f.write(key)
        
        # 设置权限
        os.chmod(self.KEY_FILE, 0o600)
        os.chmod(self.SALT_FILE, 0o600)
        
        return Fernet(key)
    
    def _get_machine_id(self) -> str:
        """获取机器唯一标识"""
        # 使用多个系统特征组合
        features = []
        for path in ['/etc/machine-id', '/var/lib/dbus/machine-id']:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    features.append(f.read().strip())
        
        if not features:
            # 回退：使用随机ID
            features = [str(os.getuid()), str(os.getgid())]
        
        return hashlib.sha256(' '.join(features).encode()).hexdigest()
    
    def encrypt_password(self, password: str) -> str:
        """加密密码，返回Fernet token（base64编码的字符串）"""
        if not password:
            return ""
        # fernet.encrypt() already returns base64-encoded bytes (b'gAAAAA...')
        return self.fernet.encrypt(password.encode()).decode()  # bytes→str
    
    def decrypt_password(self, encrypted: str) -> str:
        """解密密码，支持新旧两种格式"""
        if not encrypted:
            return ""
        try:
            # fernet.decrypt accepts base64-encoded string directly (b'gAAAAA...')
            return self.fernet.decrypt(encrypted).decode()
        except Exception:
            # 兼容旧版double-encoded格式：先base64解码（一次），再fernet解密
            try:
                decoded = base64.urlsafe_b64decode(encrypted.encode())
                return self.fernet.decrypt(decoded).decode()
            except Exception:
                pass
        raise ValueError(f"密码解密失败: 无效格式")
    
    def is_encrypted(self, value: str) -> bool:
        """判断值是否已加密（Fernet格式检测）"""
        if not value:
            return False
        try:
            decoded = base64.urlsafe_b64decode(value.encode())
            # Fernet版本字节 = 0x80，长度至少57字节（version+ts+iv+hmac）
            if len(decoded) >= 57 and decoded[0] == 0x80:
                return True
        except:
            pass
        return False


# 全局实例
_security_manager = None

def get_security_manager() -> SecurityManager:
    """获取安全管理器单例"""
    global _security_manager
    if _security_manager is None:
        _security_manager = SecurityManager()
    return _security_manager


def encrypt_password(password: str) -> str:
    """加密密码（便捷函数）"""
    return get_security_manager().encrypt_password(password)


def decrypt_password(encrypted: str) -> str:
    """解密密码（便捷函数）"""
    return get_security_manager().decrypt_password(encrypted)


def is_encrypted(value: str) -> bool:
    """判断是否已加密"""
    return get_security_manager().is_encrypted(value)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("""
安全工具

用法:
    python security.py encrypt <密码>    # 加密密码
    python security.py decrypt <密文>    # 解密密码
    python security.py test               # 测试加密/解密
        """)
        sys.exit(1)
    
    cmd = sys.argv[1]
    sm = SecurityManager()
    
    if cmd == "encrypt":
        password = sys.argv[2]
        encrypted = sm.encrypt_password(password)
        print(f"加密结果: {encrypted}")
    
    elif cmd == "decrypt":
        encrypted = sys.argv[2]
        decrypted = sm.decrypt_password(encrypted)
        print(f"解密结果: {decrypted}")
    
    elif cmd == "test":
        test_pass = "MySecret123!"
        print(f"测试密码: {test_pass}")
        
        encrypted = sm.encrypt_password(test_pass)
        print(f"加密后: {encrypted}")
        
        decrypted = sm.decrypt_password(encrypted)
        print(f"解密后: {decrypted}")
        
        if decrypted == test_pass:
            print("✅ 测试通过")
        else:
            print("❌ 测试失败")
            sys.exit(1)
