"""
JSON数据格式示例：
[
    {
        "errcode": 0,
        "errmsg": "ok",
        "userid": "1290",
        "name": "xx",
        "department": [2, 28, 73],
        "position": "",
        "status": 1,
        "isleader": 0,
        "extattr": {
            "attrs": [
                {
                    "name": "身份证号",
                    "value": "",
                    "type": 0,
                    "text": {"value": ""}
                },
                {
                    "name": "物理卡号",
                    "value": "4219393059",
                    "type": 0,
                    "text": {"value": "4219393059"}
                },
                {
                    "name": "英文名",
                    "value": "",
                    "type": 0,
                    "text": {"value": ""}
                }
            ]
        },
        "english_name": "1290",
        "telephone": "",
        "enable": 1,
        "hide_mobile": 0,
        "main_department": 2,
        "alias": "1290"
    }
]
"""

import json
from typing import List, Dict

# 以下是原有代码
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

async def process_users_from_json(json_data: List[Dict]) -> List[Dict[str, bool]]:
    """从JSON数据处理并添加用户"""
    results = []

    for user in json_data:
        if user.get('errcode') != 0:
            continue

        # 提取英文名（优先使用extattr中的英文名）
        english_name = ''
        for attr in user.get('extattr', {}).get('attrs', []):
            if attr['name'] == '英文名':
                english_name = attr['text'].get('value', '')
                break
        if not english_name:
            english_name = user.get('english_name', '')

        # 构建用户数据
        user_data = {
            'wecom': user.get('userid', 'None'),
            'wecom_id': user.get('userid', '0'),
            'name': user.get('name', 'None'),
            'department': str(user.get('department', [0])[0]),
            'position': user.get('position', 'B312'),
            'email': f"{user.get('userid')}@bj35.com",
            'language': 'zh',
            'avatar': ''
        }

        result = await add_user(user_data)
        results.append(result)

        if result['success']:
            logging.info(f"成功添加用户: {user_data['name']}")
        else:
            logging.error(f"添加用户失败: {user_data['name']}")

    return results


async def main():
    """主函数"""
    # 读取JSON文件
    with open('all_users_info_old.json', 'r', encoding='utf-8') as f:
        users_data = json.load(f)

    # 处理用户数据
    results = await process_users_from_json(users_data)

    # 统计结果
    success_count = sum(1 for r in results if r['success'])
    total_count = len(results)

    print(f"添加完成。成功：{success_count}/{total_count}")


if __name__ == '__main__':
    asyncio.run(main())