"""
Bj35 Bot v2
Refactor by: AptS:1547
Date: 2025-04-19
Description: 这是在 v1 基础上重构的版本，主要改进了代码结构和可读性。
使用 GPLv3 许可证。
Copyright (C) 2025 AptS:1547

本文件定义了令牌管理服务，包括令牌的存储、加密、检查和更新等功能。
"""
import logging
import json
import os
import platform
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

import yaml
from cryptography.fernet import Fernet

from settings import settings
from utils import update_access_token
from utils.exceptions import UpdateTokenError, TokenNotFoundError

# 根据平台选择不同的文件锁定实现
if platform.system() != 'Windows':
    import fcntl
    HAS_FCNTL = True
else:
    import msvcrt
    HAS_FCNTL = False

logger = logging.getLogger(__name__)


class FileLock:
    """跨平台的文件锁实现"""

    def __init__(self, file):
        self.file = file
        self.fd = file.fileno()
        self.locked = False

    def lock_exclusive(self):
        """排他锁，用于写入操作"""
        if self.locked:
            return

        try:
            if HAS_FCNTL:  # Unix/Linux
                fcntl.flock(self.fd, fcntl.LOCK_EX)
            else:  # Windows
                self.file.seek(0)
                msvcrt.locking(self.fd, msvcrt.LK_LOCK, os.path.getsize(self.file.name) or 1)        # pylint: disable=possibly-used-before-assignment
            self.locked = True
        except (IOError, OSError) as e:
            logger.warning("无法获取文件锁: %s", e)

    def lock_shared(self):
        """共享锁，用于读取操作"""
        if self.locked:
            return

        try:
            if HAS_FCNTL:  # Unix/Linux
                fcntl.flock(self.fd, fcntl.LOCK_SH)
            else:  # Windows - 使用非排他锁
                self.file.seek(0)
                msvcrt.locking(self.fd, msvcrt.LK_NBLCK, os.path.getsize(self.file.name) or 1)
            self.locked = True
        except (IOError, OSError) as e:
            logger.warning("无法获取文件锁: %s", e)

    def unlock(self):
        """解锁文件"""
        if not self.locked:
            return

        try:
            if HAS_FCNTL:  # Unix/Linux
                fcntl.flock(self.fd, fcntl.LOCK_UN)
            else:  # Windows
                self.file.seek(0)
                msvcrt.locking(self.fd, msvcrt.LK_UNLCK, os.path.getsize(self.file.name) or 1)
            self.locked = False
        except (IOError, OSError) as e:
            logger.warning("无法释放文件锁: %s", e)


class TokenManager:
    """令牌管理服务，处理 access token 的存储、加密、检查和更新"""

    # 配置参数 - 使用相对路径
    TOKEN_DIR = Path("data")
    TOKEN_FILE = TOKEN_DIR / "yunji_token.yaml"

    @classmethod
    def _ensure_token_dir(cls) -> None:
        """确保token目录存在"""
        cls.TOKEN_DIR.mkdir(parents=True, exist_ok=True)

    @classmethod
    def _get_encryption_key(cls) -> bytes:
        """获取用于加密的密钥"""
        key = str(settings.DATA_ENCRYPTION_KEY)
        if not key:
            # 如果不存在，直接退出
            logger.error("数据加密密钥未设置")
            raise TokenNotFoundError("数据加密密钥未设置")
        return key.encode()

    @classmethod
    def _encrypt_data(cls, data: Dict) -> str:
        """加密数据"""
        key = cls._get_encryption_key()
        f = Fernet(key)
        return f.encrypt(json.dumps(data).encode()).decode()

    @classmethod
    def _decrypt_data(cls, encrypted_data: str) -> Dict:
        """解密数据"""
        key = cls._get_encryption_key()
        f = Fernet(key)
        return json.loads(f.decrypt(encrypted_data.encode()).decode())

    @classmethod
    async def save_token_data(cls, token_data: Dict[str, Any]) -> bool:
        """
        保存token数据到文件
        
        Args:
            token_data: 要保存的token数据字典
            
        Returns:
            bool: 成功返回True，失败返回False
        """
        cls._ensure_token_dir()
        try:
            data_to_save = {
                "encrypted": cls._encrypt_data(token_data),
                "updated_at": int(datetime.now().timestamp()),
            }

            # 使用文件锁防止并发写入
            with open(cls.TOKEN_FILE, 'w+', encoding="utf-8") as f:
                lock = FileLock(f)
                lock.lock_exclusive()
                try:
                    yaml.dump(data_to_save, f)
                finally:
                    lock.unlock()

            logger.info("Token数据已保存到文件: %s", cls.TOKEN_FILE)
            return True
        except (IOError, yaml.YAMLError) as e:
            logger.error("保存token数据失败: %s", str(e))
            return False

    @classmethod
    def load_token_data(cls) -> Optional[Dict[str, Any]]:
        """
        从文件加载token数据
        
        Returns:
            Optional[Dict]: token数据字典，如果加载失败则返回None
        """
        if not cls.TOKEN_FILE.exists():
            logger.warning("Token文件不存在: %s", cls.TOKEN_FILE)
            return None

        try:
            with open(cls.TOKEN_FILE, 'r', encoding="utf-8") as f:
                lock = FileLock(f)
                lock.lock_shared()
                try:
                    data = yaml.safe_load(f)
                finally:
                    lock.unlock()

            if not data or "encrypted" not in data:
                logger.error("Token文件格式无效")
                return None

            decrypted_data = cls._decrypt_data(data["encrypted"])
            return decrypted_data
        except (IOError, yaml.YAMLError) as e:
            logger.error("加载token数据失败: %s", str(e))
            return None

    @classmethod
    async def check_token(cls) -> bool:
        """
        检查access token是否在当天过期，如果是则更新并保存
        
        Returns:
            bool: 如果检查成功返回True，发生错误返回False
        """
        try:
            # 从文件加载当前token数据
            token_data = cls.load_token_data() or {}

            # 如果没有过期时间或token，则强制更新
            if "expire_time" not in token_data or "access_token" not in token_data:
                logger.info("未找到有效的token数据，开始生成新的access token")

                try:
                    # 尝试更新token
                    access_token, expiration = await update_access_token()
                except UpdateTokenError as e:
                    logger.error("更新access token失败: %s", str(e))
                    return False

                logger.info("新的access token生成成功")

                expiration = int(datetime.strptime(expiration, "%Y-%m-%dT%H:%M:%S%z").timestamp())

                # 更新后保存新token
                await cls.save_token_data({
                    "access_token": access_token,
                    "expire_time": expiration
                })
                return True

            # 检查是否即将过期
            expire_ts = int(token_data["expire_time"])
            today = datetime.now().timestamp()

            if expire_ts <= today:
                # 如果过期时间在今天或之前，更新token
                logger.info("Access token已过期，开始生成新的access token")

                try:
                    # 尝试更新token
                    access_token, expiration = await update_access_token()

                    logger.info("新的access token生成成功")

                    expiration = int(datetime.strptime(expiration,
                                                       "%Y-%m-%dT%H:%M:%S%z").timestamp())

                    # 更新并保存新token
                    await cls.save_token_data({
                        "access_token": access_token,
                        "expire_time": expiration
                    })
                except UpdateTokenError as e:
                    logger.error("更新access token失败: %s", str(e))
                    return False

            return True
        except (IOError, yaml.YAMLError) as e:
            logger.error("检查或更新access token时出错：%s", str(e))
            return False

    @classmethod
    def log_token_expiry(cls) -> None:
        """记录距离token过期的时间"""
        try:
            token_data = cls.load_token_data()
            if not token_data or "expire_time" not in token_data:
                logger.warning("没有找到token过期信息")
                return

            expiration_ts = int(token_data["expire_time"])
            current_ts = datetime.now().timestamp()
            days_remaining = (expiration_ts - current_ts) / (60 * 60 * 24)
            logger.info("Access token将在 %.2f天后过期", days_remaining)
        except (IOError, yaml.YAMLError) as e:
            logger.error("获取token过期时间失败：%s", str(e))

    @classmethod
    async def get_valid_token(cls) -> bool:
        """
        获取有效的token，如果即将过期则自动更新
        
        Returns:
            bool: 如果获取成功返回True，发生错误返回False
        """
        try:
            # 检查确保有效token
            await cls.check_token()

            # 从文件获取最新token
            token_data = cls.load_token_data()
            if token_data and "access_token" in token_data:
                settings.YUNJI_ACCESS_TOKEN = token_data["access_token"]
                return True

            return False

        except (IOError, yaml.YAMLError) as e:
            logger.error("读取token失败: %s", str(e))
            return False
