"""
Bj35 Bot v2
Refactor by: AptS:1547
Date: 2025-04-19
Description: 这是在 v1 基础上重构的版本，主要改进了代码结构和可读性。
使用 GPLv3 许可证。
Copyright (C) 2025 AptS:1547

本文件定义了RedisConnector类，用于连接和操作Redis数据库。
"""

import logging
import socket
from typing import Optional
from urllib.parse import urlparse

import redis.asyncio as redis
from redis.exceptions import RedisError
from redis.asyncio.connection import ConnectionPool

from utils.settings import settings
from utils.exceptions import RedisConnectionError

logger = logging.getLogger(__name__)


class RedisConnector:
    """Redis连接器类，提供异步Redis操作"""

    __pool: Optional[ConnectionPool] = None
    __client: Optional[redis.Redis] = None
    __initialized: bool = False

    @classmethod
    async def initialize(cls) -> None:
        """初始化Redis连接池"""
        if cls.__initialized:
            return

        try:
            # 先解析主机名
            parsed_url = urlparse(settings.REDIS_URL)
            socket.gethostbyname(parsed_url.hostname)

            # 创建连接池
            cls.__pool = redis.ConnectionPool.from_url(
                url=settings.REDIS_URL,
                password=settings.REDIS_PASSWORD,
                max_connections=settings.REDIS_POOL_MAX_SIZE,
                encoding="utf-8",
                decode_responses=True
            )

            # 创建测试连接并验证
            test_client = redis.Redis(connection_pool=cls.__pool)
            await test_client.ping()
            await test_client.close()

            cls.__initialized = True

        except socket.gaierror as e:
            logger.error("Redis主机名解析失败: %s", str(e))
            raise RedisConnectionError(f"Redis主机名无法解析: {str(e)}") from e
        except RedisError as e:
            logger.error("Redis连接失败: %s", str(e))
            cls.__pool = None
            raise RedisConnectionError(f"Redis连接测试失败: {str(e)}") from e
        except Exception as e:
            logger.error("Redis初始化时发生未知错误: %s", str(e))
            cls.__pool = None
            raise RedisConnectionError(f"Redis初始化失败: {str(e)}") from e

    @classmethod
    async def _get_client(cls) -> redis.Redis:
        """获取Redis客户端实例"""
        if not cls.__initialized:
            await cls.initialize()

        if cls.__client is None and cls.__pool is not None:
            cls.__client = redis.Redis(connection_pool=cls.__pool)
        return cls.__client

    @classmethod
    async def close(cls) -> None:
        """关闭Redis连接"""
        if cls.__client:
            await cls.__client.close()
            cls.__client = None

        if cls.__pool:
            await cls.__pool.disconnect()
            cls.__pool = None

        cls.__initialized = False

    @classmethod
    async def get(cls, key: str) -> Optional[str]:
        """获取键值"""
        try:
            client = await cls._get_client()
            return await client.get(key)
        except RedisError as e:
            logger.error("Redis GET操作失败 [%s]: %s", key, str(e))
            return None

    @classmethod
    async def set(cls, key: str, value: str, expire: Optional[int] = None) -> bool:
        """设置键值，可选过期时间（秒）"""
        try:
            conn = await cls._get_client()
            if expire:
                await conn.set(key, value, ex=expire)
            else:
                await conn.set(key, value)
            return True
        except RedisError as e:
            logger.error("Redis SET操作失败 [%s]: %s", key, str(e))
            return False

    @classmethod
    async def delete(cls, *keys) -> int:
        """删除一个或多个键，返回删除成功的键数量"""
        if not keys:
            return 0

        try:
            conn = await cls._get_client()
            return await conn.delete(*keys)
        except RedisError as e:
            logger.error("Redis DEL操作失败 [%s]: %s", keys, str(e))
            return 0

    @classmethod
    async def exists(cls, key: str) -> bool:
        """检查键是否存在"""
        try:
            conn = await cls._get_client()
            exists = await conn.exists(key)
            return exists > 0
        except RedisError as e:
            logger.error("Redis EXISTS操作失败 [%s]: %s", key, str(e))
            return False

    # 应用特定方法 - 适用于 WeComService 的 state 管理
    @classmethod
    async def store_oauth_state(cls, state: str, expire_seconds: int = 60) -> bool:
        """存储OAuth state参数，设置过期时间"""
        return await cls.set(f"wecom:oauth:state:{state}", "1", expire=expire_seconds)

    @classmethod
    async def verify_oauth_state(cls, state: str) -> bool:
        """验证OAuth state参数并删除"""
        key = f"wecom:oauth:state:{state}"
        exists = await cls.exists(key)
        if exists:
            await cls.delete(key)
        return exists
