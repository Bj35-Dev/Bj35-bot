"""
Bj35 Bot v2
Refactor by: AptS:1547
Date: 2025-04-19
Description: 这是在 v1 基础上重构的版本，主要改进了代码结构和可读性。
使用 GPLv3 许可证。
Copyright (C) 2025 AptS:1547

本文件定义了PostgreSQLConnector类，用于管理PostgreSQL数据库连接和操作。
"""

import logging
import asyncio
from asyncio import Lock
from typing import Dict, Optional, Any
from contextlib import asynccontextmanager

import asyncpg

from utils.settings import settings
from utils.exceptions import DatabaseConnectionError

logger = logging.getLogger(__name__)


class PostgreSQLConnector:
    """PostgreSQL 数据库连接管理类，提供数据库操作的各种方法。"""
    pool: Optional[asyncpg.Pool] = None
    lock: Lock = Lock()

    @classmethod
    async def initialize(cls) -> None:
        """初始化数据库连接池"""
        if cls.pool:
            # 检查现有连接是否有效
            try:
                async with cls.pool.acquire() as conn:
                    await conn.execute('SELECT 1')
                logger.info("数据库连接池已存在且连接正常")
                return
            except asyncpg.PostgresError as e:
                logger.warning("现有连接池出错，将重新创建: %s", str(e))
                cls.pool = None

        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
            try:
                cls.pool = await asyncpg.create_pool(
                    user=settings.DB_USER,
                    password=settings.DB_PASSWORD,
                    database=settings.DB_NAME,
                    host=settings.DB_HOST,
                    port=settings.DB_PORT,
                    min_size=settings.DB_POOL_MIN_SIZE,
                    max_size=settings.DB_POOL_MAX_SIZE,
                    ssl=settings.DB_SSL,
                    timeout=60,
                    command_timeout=60,
                    max_inactive_connection_lifetime=300,
                )

                # 测试连接
                async with cls.pool.acquire() as conn:
                    await conn.execute('SELECT 1')
                    logger.info("数据库连接成功")

                return
            except (asyncpg.PostgresError, OSError) as e:
                retry_count += 1
                if retry_count >= max_retries:
                    logger.error("PostgreSQL 连接失败，已重试 %d 次，退出", max_retries)
                    raise DatabaseConnectionError(f"无法连接到 PostgreSQL 数据库: {str(e)}") from e

                wait_time = 2 ** retry_count
                logger.warning("PostgreSQL 连接失败，正在重试 %d/%d 次，等待 %d 秒: %s",
                               retry_count, max_retries, wait_time, str(e))
                await asyncio.sleep(wait_time)

    @classmethod
    async def execute(cls, query: str, *args) -> None:
        """执行不返回结果的SQL语句"""
        if not cls.pool:
            raise ValueError("数据库连接池尚未初始化")

        async with cls.lock:
            try:
                async with cls.pool.acquire() as conn:
                    await conn.execute(query, *args)
            except Exception as e:
                logger.error("SQL执行失败: %s", str(e))
                raise

    @classmethod
    async def fetch_one(cls, query: str, *args) -> Optional[Dict[str, Any]]:
        """执行查询并返回一条记录"""
        if not cls.pool:
            raise ValueError("数据库连接池尚未初始化")

        async with cls.lock:
            try:
                async with cls.pool.acquire() as conn:
                    row = await conn.fetchrow(query, *args)
                    return dict(row) if row else None
            except Exception as e:
                logger.error("SQL查询失败: %s", str(e))
                raise

    @classmethod
    async def fetch_all(cls, query: str, *args) -> list:
        """执行查询并返回所有记录"""
        if not cls.pool:
            raise ValueError("数据库连接池尚未初始化")

        async with cls.lock:
            try:
                async with cls.pool.acquire() as conn:
                    rows = await conn.fetch(query, *args)
                    return [dict(row) for row in rows]
            except Exception as e:
                logger.error("SQL查询失败: %s", str(e))
                raise

    @classmethod
    async def fetch_val(cls, query: str, *args) -> Any:
        """执行查询并返回单个值"""
        if not cls.pool:
            raise ValueError("数据库连接池尚未初始化")

        async with cls.lock:
            try:
                async with cls.pool.acquire() as conn:
                    return await conn.fetchval(query, *args)
            except Exception as e:
                logger.error("SQL查询失败: %s", str(e))
                raise

    @classmethod
    @asynccontextmanager
    async def transaction(cls):
        """
        创建并返回一个数据库事务上下文管理器
        
        示例:
            async with PostgreSQLConnector.transaction():
                await PostgreSQLConnector.execute("INSERT INTO ...")
                await PostgreSQLConnector.execute("UPDATE ...")
        """
        if not cls.pool:
            raise ValueError("数据库连接池尚未初始化")

        conn = await cls.pool.acquire()
        tx = conn.transaction()
        try:
            await tx.start()
            yield conn
            await tx.commit()
        except Exception as e:
            await tx.rollback()
            logger.error("事务执行失败，已回滚: %s", str(e))
            raise
        finally:
            await cls.pool.release(conn)

    @classmethod
    async def close(cls) -> None:
        """关闭数据库连接池，释放资源"""
        if cls.pool:
            await cls.pool.close()
            logger.info("PostgreSQL 连接池已关闭")
