"""
Bj35 Bot v2
Refactor by: AptS:1547
Date: 2025-04-19
Description: 这是在 v1 基础上重构的版本，主要改进了代码结构和可读性。
使用 GPLv3 许可证。
Copyright (C) 2025 AptS:1547

本文件定义了UserService类，处理与用户相关的所有业务逻辑。
"""

import logging

from typing import Dict, Optional, Any
from argon2 import PasswordHasher

from utils.db.postgresql_connector import PostgreSQLConnector

logger = logging.getLogger(__name__)

class UserService:
    """用户服务类，处理所有与用户相关的业务逻辑"""

    @staticmethod
    async def add_user(data: Dict[str, Any]) -> Dict[str, bool]:
        """
        添加用户信息

        注意：此方法会将密码进行哈希处理后存储到数据库中。
        """
        try:
            username = data.get('username')
            password = data.get('password', None)

            if not password:
                raise ValueError("密码不能为空")
            password = PasswordHasher().hash(password)

            role = data.get('role', 'user')
            name = data.get('name', 'None')
            email = data.get('email', f"{username}@bj35.com")
            mobile = data.get('mobile', None)
            wecom_id = data.get('wecom_id', None)
            department = data.get('department', 'None')
            avatar_url = data.get('avatar_url', None)

            await PostgreSQLConnector.execute('''
                INSERT INTO userinfo (username, password, role, name, email, mobile, wecom_id, department, avatar_url)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            ''', username, password, role, name, email, mobile, wecom_id, department, avatar_url)

            logger.info("用户信息已添加: %s", name)
            return {'success': True}
        except Exception as e:
            logger.error("添加用户失败: %s", str(e))
            raise

    @staticmethod
    async def verify_user_credentials(username: str, password: str) -> Optional[Dict[str, Any]]:
        """验证用户凭据"""
        try:
            row = await PostgreSQLConnector.fetch_one("""
                SELECT *
                FROM userinfo
                WHERE username = $1 OR email = $1 OR mobile = $1 OR wecom_id = $1
                LIMIT 1
            """, username)

            ph = PasswordHasher()
            if row and ph.verify(row.get('password', ''), password):
                return row
            return None
        except Exception as e:
            logger.error("验证用户凭据失败: %s", str(e))
            raise

    @staticmethod
    async def check_user_exists_by_wecom(wecom_id: str) -> bool:
        """检查企业微信用户是否存在"""
        try:
            result = await PostgreSQLConnector.fetch_val("""
                SELECT 1 FROM userinfo WHERE wecom_id = $1 LIMIT 1
            """, wecom_id)

            return bool(result)
        except Exception as e:
            logger.error("检查企业微信用户是否存在失败: %s", str(e))
            raise

    # TODO: 移除 kind 参数
    @staticmethod
    async def get_userinfo_by_username(username: str, kind: str) -> Optional[Dict[str, Any]]:
        """根据用户名获取用户信息"""
        allowed_columns = ['username', 'name', 'email', 'mobile', 'wecom_id']
        if kind not in allowed_columns:
            logger.error("无效的列名: %s", kind)
            raise ValueError(f"无效的列名: {kind}")

        try:
            query = f"SELECT * FROM userinfo WHERE {kind} = $1"
            user_info = await PostgreSQLConnector.fetch_one(query, username)

            if user_info:
                logger.debug("已获取用户信息: %s", user_info)
                return user_info

            logger.debug("未找到用户: %s", username)
            return None

        except Exception as e:
            logger.error("获取用户信息失败: %s", str(e))
            raise

    @staticmethod
    async def update_userinfo(data: Dict[str, Any]) -> Dict[str, bool | str]:
        """更新用户信息"""
        try:
            username = data.get('username', '')
            updates = []
            values = []
            param_index = 1

            # 处理密码更新
            if 'password' in data:
                ph = PasswordHasher()
                hashed_password = ph.hash(data['password'])
                updates.append(f"password = ${param_index}")
                values.append(hashed_password)
                param_index += 1

            # 处理其他可能的更新字段
            for field in ['name', 'email', 'mobile', 'department', 'avatar_url', 'role']:
                if field in data:
                    updates.append(f"{field} = ${param_index}")
                    values.append(data[field])
                    param_index += 1

            # 构建更新SQL
            if not updates:
                return {'success': True}

            sql = f"""
                UPDATE userinfo
                SET {', '.join(updates)}
                WHERE username = ${param_index}
            """
            values.append(username)

            async with PostgreSQLConnector.transaction():
                await PostgreSQLConnector.execute(sql, *values)

            logger.info("已更新用户信息: %s", username)
            return {'success': True}

        except Exception as e:
            logger.error("更新用户信息失败: %s", str(e))
            raise
