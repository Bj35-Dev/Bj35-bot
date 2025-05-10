#!/usr/bin/env python3
"""
用户添加脚本
用途：单独运行以添加新用户
"""

import asyncio
import logging
from typing import Dict, Any
from argon2 import PasswordHasher
import asyncpg

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 数据库配置
DB_CONFIG = {
    'host': '192.168.1.9',
    'port': 54321,
    'user': 'postgres',
    'password': 'NnK%AXCQKCYTGtzF',
    'database': 'bj35bot',
}


class PostgreSQLConnector:
    """PostgreSQL连接器"""
    _pool = None

    @classmethod
    async def get_pool(cls):
        if cls._pool is None:
            cls._pool = await asyncpg.create_pool(**DB_CONFIG)
        return cls._pool

    @classmethod
    async def execute(cls, query: str, *args):
        pool = await cls.get_pool()
        async with pool.acquire() as conn:
            return await conn.execute(query, *args)


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


async def main():
    """主函数"""
    # 示例用户数据
    test_user = {
        'wecom': 'dzc',
        'wecom_id': "5712",
        'name': 'cg8',
        'password': 'dzc20070818',
        'department': '测试部门',
        'position': 'C206',
        'email': 'cg8@bj35.com',
        'language': 'zh',
        'avatar': 'https://avatars.githubusercontent.com/u/163859507'
    }

    result = await add_user(test_user)
    print(f"添加用户结果: {result}")


if __name__ == '__main__':
    asyncio.run(main())