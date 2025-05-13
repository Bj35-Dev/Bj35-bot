"""
Bj35 Bot v2
Refactor by: AptS:1547
Date: 2025-04-19
Description: 数据库初始化模块

本文件负责数据库的初始化，包括创建表、添加索引等操作。
"""

import logging
from typing import List
from pathlib import Path

from utils.db.postgresql_connector import PostgreSQLConnector

logger = logging.getLogger(__name__)


class DatabaseInitializer:
    """数据库初始化器，负责创建表和其他数据库结构"""

    @staticmethod
    async def initialize_database() -> bool:
        """初始化数据库结构"""
        try:
            # 确保数据库连接已建立
            if not PostgreSQLConnector.pool:
                await PostgreSQLConnector.initialize()

            # 检查表是否存在
            existing_tables = await DatabaseInitializer._get_existing_tables()
            if 'userinfo' in existing_tables:
                logger.info("用户信息表已存在，跳过初始化")
                return True

            # 执行schema.sql中的所有语句
            await DatabaseInitializer._execute_schema_file()

            logger.info("数据库结构初始化完成")
            return True
        except Exception as e:
            logger.error("数据库初始化失败: %s", str(e))
            return False

    @staticmethod
    async def _get_existing_tables() -> List[str]:
        """获取数据库中现有的表名"""
        if not PostgreSQLConnector.pool:
            return []

        async with PostgreSQLConnector.pool.acquire() as conn:
            tables = await conn.fetch("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            return [t['table_name'] for t in tables]

    @staticmethod
    async def _execute_schema_file() -> None:
        """执行schema.sql文件中的SQL语句"""
        if not PostgreSQLConnector.pool:
            raise ValueError("数据库连接池尚未初始化")

        # 使用 pathlib 获取 SQL 文件路径
        current_file = Path(__file__)
        project_root = current_file.parent.parent.parent  # 从当前文件上升三级到项目根目录
        schema_path = project_root / 'sql' / 'schema.sql'

        if not schema_path.exists():
            raise FileNotFoundError(f"找不到SQL文件: {schema_path}")

        # 读取SQL文件内容
        schema_sql = schema_path.read_text(encoding='utf-8')

        # 执行SQL语句
        async with PostgreSQLConnector.pool.acquire() as conn:
            await conn.execute(schema_sql)
            logger.info("成功执行SQL模式文件")
