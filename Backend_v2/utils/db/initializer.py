"""
Bj35 Bot v2
Refactor by: AptS:1547
Date: 2025-05-14
Description: 这是在 v1 基础上重构的版本，主要改进了代码结构和可读性。
使用 GPLv3 许可证。
Copyright (C) 2025 AptS:1547

本文件负责数据库的初始化，包括创建表、添加索引等操作。
"""

import logging
from pathlib import Path

from utils.db.postgresql_connector import PostgreSQLConnector
from utils.exceptions import DatabasePoolError

logger = logging.getLogger(__name__)


class DatabaseInitializer:
    """数据库初始化器，负责创建表和其他数据库结构"""

    @staticmethod
    async def initialize_database() -> bool:
        """初始化数据库结构"""
        try:
            # 确保数据库连接已建立
            PostgreSQLConnector.get_pool()

            # 执行schema.sql中的所有语句
            await DatabaseInitializer._execute_schema_file()

            logger.info("数据库结构初始化完成")
            return True
        except DatabasePoolError as e:
            logger.error("数据库初始化失败: %s", str(e))
            return False

    @staticmethod
    async def _execute_schema_file() -> None:
        """执行schema.sql文件中的SQL语句"""
        try:
            PostgreSQLConnector.get_pool()

            project_root = Path(__file__).parent.parent.parent  # 从当前文件上升三级到项目根目录
            schema_path = project_root / 'sql' / 'schema.sql'

            if not schema_path.exists():
                raise FileNotFoundError(f"找不到SQL文件: {schema_path}")

            schema_sql = schema_path.read_text(encoding='utf-8')

            async with PostgreSQLConnector.transaction():
                await PostgreSQLConnector.execute(schema_sql)
                logger.info("成功执行SQL模式文件")

        except DatabasePoolError as e:
            logger.error("数据库连接池错误: %s", str(e))
            raise
