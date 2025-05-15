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
            wecom = data.get('wecom', 'None')
            wecom_id = data.get('wecom_id', 0)
            name = data.get('name', 'None')
            password = data.get('password', None)

            ph = PasswordHasher()

            if not password:
                raise ValueError("密码不能为空")

            password = ph.hash(password)

            department = data.get('department', 'None')
            position = data.get('position', 'B312')
            mobile = "None"
            email = data.get('email', f"{wecom_id}@bj35.com")
            language = data.get('language', 'zh')
            avatar_text = data.get('avatar', 'None')

            await PostgreSQLConnector.execute('''
                INSERT INTO userinfo (wecom, wecom_id, name, password, department, position, mobile, language, email, avatar_text)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
            ''', wecom, wecom_id, name, password, department, position, mobile, language, email, avatar_text)

            logger.info("用户信息已添加: %s", name)
            return {'success': True}
        except Exception as e:
            logger.error("添加用户失败: %s", str(e))
            return {'success': False}

    @staticmethod
    async def verify_user_credentials(username: str, password: str) -> Optional[Dict[str, Any]]:
        """验证用户凭据"""
        try:
            row = await PostgreSQLConnector.fetch_one("""
                SELECT *
                FROM userinfo
                WHERE wecom = $1 OR name = $1 OR email = $1 OR mobile = $1 OR wecom_id = $1
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
            """, int(wecom_id))
            return bool(result)
        except Exception as e:
            logger.error("检查企业微信用户是否存在失败: %s", str(e))
            return False

    @staticmethod
    async def get_password_by_username(username: str, kind: str) -> Optional[str]:
        """根据用户名获取密码"""
        allowed_columns = ['wecom', 'name', 'email', 'mobile', 'wecom_id']
        if kind not in allowed_columns:
            logger.error("无效的列名: %s", kind)
            raise ValueError(f"无效的列名: {kind}")

        try:
            query = f"SELECT password FROM userinfo WHERE {kind} = $1"
            return await PostgreSQLConnector.fetch_val(query, username)
        except Exception as e:
            logger.error("获取密码失败: %s", str(e))
            raise

    @staticmethod
    async def get_userinfo_by_username(username: str, kind: str) -> Optional[Dict[str, Any]]:
        """根据用户名获取用户信息"""
        allowed_columns = ['wecom', 'name', 'email', 'mobile', 'wecom_id']
        if kind not in allowed_columns:
            logger.error("无效的列名: %s", kind)
            raise ValueError(f"无效的列名: {kind}")

        try:
            query = f"SELECT * FROM userinfo WHERE {kind} = $1"
            user_info = await PostgreSQLConnector.fetch_one(query, username)

            if user_info:
                logger.debug("已获取用户信息: %s", user_info)
            else:
                logger.debug("未找到用户: %s", username)

            return user_info
        except Exception as e:
            logger.error("获取用户信息失败: %s", str(e))
            raise

    @staticmethod
    async def update_userinfo(data: Dict[str, Any]) -> Dict[str, bool]:
        """更新用户信息"""
        try:
            name_old = data.get('name_old', '')
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

            # 构建更新SQL
            if not updates:
                return {'success': True}

            # 修改查询条件，使用 wecom_id
            sql = f"""
                UPDATE userinfo
                SET {', '.join(updates)}
                WHERE wecom_id = ${param_index}
            """
            values.append(name_old)

            # TODO: 这里应该用 execute() 而不是 fetch_one()
            async with PostgreSQLConnector.transaction():
                result = await PostgreSQLConnector.fetch_one(sql, *values)

            if result:
                logger.info("已更新用户信息: %s", {
                    'name': result.get('name'),
                    'wecom_id': result.get('wecom_id')
                })
                return {'success': True}
            return {
                'success': False,
                'message': '未找到用户'
            }

        except Exception as e:
            logger.error("更新用户信息失败: %s", str(e))
            return {
                'success': False,
                'message': str(e)
            }
