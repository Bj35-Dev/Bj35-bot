"""
Bj35 Bot v2
Refactor by: AptS:1547
Date: 2025-05-14
Description: 这是在 v1 基础上重构的版本，主要改进了代码结构和可读性。
使用 GPLv3 许可证。
Copyright (C) 2025 AptS:1547

本文件定义了RedisConnector类，用于连接和操作Redis数据库。
"""

import logging
from typing import Optional

import redis.asyncio as aioredis
from redis.exceptions import RedisError

from utils.settings import settings
from utils.exceptions import RedisConnectionError

logger = logging.getLogger(__name__)


class RedisConnector:
    """Redis连接器类，提供异步Redis操作"""

    __pool: Optional[aioredis.ConnectionPool] = None

    @classmethod
    async def initialize(cls) -> None:
        """初始化Redis连接池"""
        try:
            pool = await cls._get_pool()
            # 验证连接
            client = aioredis.Redis(connection_pool=pool)
            await client.ping()
            logger.info("Redis连接池已初始化")
        except RedisError as e:
            cls.__pool = None
            raise RedisConnectionError(f"无法连接到Redis: {str(e)}") from e

    @classmethod
    async def _get_pool(cls) -> aioredis.ConnectionPool:
        """获取或创建Redis连接池"""
        if cls.__pool is None:
            try:
                cls.__pool = aioredis.ConnectionPool.from_url(
                    url=settings.REDIS_URL,
                    password=settings.REDIS_PASSWORD,
                    max_connections=settings.REDIS_POOL_MAX_SIZE,
                    encoding="utf-8",
                )

                logger.debug("Redis初始化连接池成功: %s", cls.__pool)
            except RedisError as e:
                raise RedisConnectionError(f"无法连接到Redis: {str(e)}") from e

        return cls.__pool

    @classmethod
    async def _get_client(cls) -> aioredis.Redis:
        """获取Redis客户端实例"""
        pool = await cls._get_pool()
        return aioredis.Redis(connection_pool=pool)

    @classmethod
    async def close(cls) -> None:
        """关闭Redis连接池"""
        if cls.__pool is not None:
            await cls.__pool.aclose()
            cls.__pool = None
            logger.info("Redis连接池已关闭")

    # 基础操作方法
    @classmethod
    async def get(cls, key: str) -> Optional[str]:
        """获取键值"""
        try:
            conn = await cls._get_client()
            return await conn.get(key)
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
