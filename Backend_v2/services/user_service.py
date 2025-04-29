"""
Bj35 Bot v2
Refactor by: AptS:1547
Date: 2025-04-19
Description: 这是在 v1 基础上重构的版本，主要改进了代码结构和可读性。
使用 GPLv3 许可证。
Copyright (C) 2025 AptS:1547

本文件定义了UserService类，处理与用户相关的所有业务逻辑。
"""

# 特殊说明：本系统的密码处理流程是：
# 1. 前端发送MD5哈希后的密码
# 2. 后端使用Argon2对MD5哈希进行二次哈希后存储
# 3. 验证时，比较存储的Argon2(MD5(密码))与接收的MD5(密码)

import logging

from typing import Dict, Optional, Any
from argon2 import PasswordHasher

from utils.postgresql_connector import PostgreSQLConnector

logger = logging.getLogger(__name__)

class UserService:
    """用户服务类，处理所有与用户相关的业务逻辑"""

    @staticmethod
    async def add_user(data: Dict[str, Any]) -> Dict[str, bool]:
        """添加用户信息"""
        try:
            wecom = data.get('wecom', 'None')
            wecom_id = data.get('wecom_id', 0)
            name = data.get('name', 'None')
            password = data.get('password', None)

            ph = PasswordHasher()
            if password is None:
                default_pwd = str(name) + str(wecom_id)
                password = ph.hash(default_pwd)
            else:
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
    async def verify_user_credentials(username: str, password: str) -> Optional[tuple]:
        """验证用户凭据"""
        try:
            row = await PostgreSQLConnector.fetch_one("""
                SELECT
                    CASE
                        WHEN wecom = $1 THEN 'wecom'
                        WHEN name = $1 THEN 'name'
                        WHEN email = $1 THEN 'email'
                        WHEN mobile = $1 THEN 'mobile'
                    END as kind,
                    password
                FROM userinfo
                WHERE wecom = $1 OR name = $1 OR email = $1 OR mobile = $1
                LIMIT 1
            """, username)

            ph = PasswordHasher()
            if row and row.get('kind') and ph.verify(row.get('password', ''), password):
                return (username, row['kind'])
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
        allowed_columns = ['wecom', 'name', 'email', 'mobile']
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
        if 'name_old' not in data:
            raise ValueError("缺少必要的 'name_old' 字段")

        name = data['name_old']
        if len(data) < 2:
            raise ValueError("没有提供要更新的字段")

        # 获取第一个不是 'name_old' 的键作为要更新的字段
        update_kind = next((k for k in data.keys() if k != 'name_old'), None)
        if not update_kind:
            raise ValueError("没有提供要更新的字段")

        value = data[update_kind]

        # 验证更新的列名以防止SQL注入
        allowed_columns = ['wecom', 'wecom_id', 'name', 'password', 'department',
                           'position', 'mobile', 'language', 'email', 'avatar_text']
        if update_kind not in allowed_columns:
            logger.error("无效的列名: %s", update_kind)
            raise ValueError(f"无效的列名: {update_kind}")

        try:
            query = f"UPDATE userinfo SET {update_kind} = $1 WHERE name = $2"
            await PostgreSQLConnector.execute(query, value, name)
            logger.info("已更新用户信息: %s", {update_kind: value, 'name': name})
            return {"success": True}
        except Exception as e:
            logger.error("更新用户信息失败: %s", str(e))
            raise
