"""
Bj35 Bot v2
数据库迁移管理器

负责管理数据库版本和应用迁移
"""

import re
import logging
from pathlib import Path
from typing import List, Tuple

from utils.db.postgresql_connector import PostgreSQLConnector

logger = logging.getLogger(__name__)

class DatabaseMigrator:
    """数据库迁移管理器"""

    @staticmethod
    async def ensure_migrations_table():
        """确保 migrations 表存在"""
        try:
            await PostgreSQLConnector.execute("""
                CREATE TABLE IF NOT EXISTS migrations (
                    id SERIAL PRIMARY KEY,
                    version VARCHAR(50) NOT NULL UNIQUE,
                    description TEXT,
                    applied_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                )
            """)
            logger.info("已确认 migrations 表存在")
            return True
        except Exception as e:
            logger.error("创建 migrations 表失败: %s", e)
            return False

    @staticmethod
    def get_migrations_path() -> Path:
        """获取迁移文件目录路径"""
        current_file = Path(__file__)
        project_root = current_file.parent.parent.parent
        migrations_path = project_root / 'sql' / 'migrations'

        migrations_path.mkdir(parents=True, exist_ok=True)

        return migrations_path

    @staticmethod
    async def get_applied_migrations() -> List[str]:
        """获取已应用的迁移版本"""
        try:
            # 确保表存在
            await DatabaseMigrator.ensure_migrations_table()

            result = await PostgreSQLConnector.fetch_all("""
                SELECT version FROM migrations ORDER BY id
            """)
            return [row['version'] for row in result]
        except Exception as e:
            logger.error("获取已应用迁移失败: %s", e)
            return []

    @staticmethod
    def get_available_migrations() -> List[Tuple[str, Path, str]]:
        """
        获取所有可用的迁移文件
        
        返回: [(版本号, 文件路径, 描述), ...]
        """
        migrations_path = DatabaseMigrator.get_migrations_path()
        migrations = []

        for file_path in sorted(migrations_path.glob('*.sql')):
            file_name = file_path.name
            # 文件命名格式: V1.0.0__描述.sql
            match = re.match(r'V(\d+\.\d+\.\d+)__(.+)\.sql', file_name)
            if match:
                version = match.group(1)
                description = match.group(2).replace('_', ' ')
                migrations.append((version, file_path, description))

        return migrations

    @staticmethod
    async def apply_migrations() -> bool:
        """
        应用所有未执行的迁移
        
        返回: 是否成功应用了所有迁移
        """
        try:
            # 确保迁移表存在
            if not await DatabaseMigrator.ensure_migrations_table():
                logger.error("无法确保迁移表存在，中止迁移")
                return False

            # 获取已应用的迁移
            applied_migrations = await DatabaseMigrator.get_applied_migrations()
            logger.info("已应用的迁移: %s", applied_migrations)

            # 获取所有可用迁移
            available_migrations = DatabaseMigrator.get_available_migrations()
            logger.info("发现 %d 个迁移文件", len(available_migrations))

            # 筛选未应用的迁移
            pending_migrations = [
                (version, file_path, description) 
                for version, file_path, description in available_migrations 
                if version not in applied_migrations
            ]

            if not pending_migrations:
                logger.info("没有发现新的迁移")
                return True

            logger.info("准备应用 %d 个迁移", len(pending_migrations))

            # 按顺序应用每个迁移
            for version, file_path, description in pending_migrations:
                logger.info("正在应用迁移 %s: %s", version, description)

                # 读取SQL文件内容
                with open(file_path, 'r', encoding='utf-8') as sql_file:
                    sql_content = sql_file.read()

                try:
                    # 使用事务执行迁移，确保原子性
                    async with PostgreSQLConnector.transaction():
                        # 执行迁移SQL
                        await PostgreSQLConnector.execute(sql_content)

                        # 记录已应用的迁移
                        await PostgreSQLConnector.execute(
                            "INSERT INTO migrations (version, description) VALUES ($1, $2)",
                            version, description
                        )

                    logger.info("迁移 %s 应用成功", version)
                except Exception as e:
                    logger.error("应用迁移 %s 失败: %s", version, str(e))
                    return False

            return True
        except Exception as e:
            logger.error("应用迁移过程失败: %s", str(e))
            return False
