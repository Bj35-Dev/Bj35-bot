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
import asyncio
import logging
from typing import List, Dict, Any
from argon2 import PasswordHasher
from pypinyin import pinyin, Style
import asyncpg

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 数据库配置
DB_CONFIG = {
    'host': 'postgresql',
    'port': 5432,
    'user': 'postgres',
    'password': 'yourpassword',
    'database': 'bj35bot',
}


def process_name(name: str) -> str:
    """处理名字，中文转换为拼音首字母，英文去除空格"""
    name = name.replace(' ', '')
    if any('\u4e00' <= char <= '\u9fff' for char in name):
        py = pinyin(name, style=Style.FIRST_LETTER)
        result = ''.join(letter[0].upper() if i == 0 else letter[0].lower()
                         for i, letter in enumerate(py))
        return result
    return name


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

    @classmethod
    async def fetch_val(cls, query: str, *args):
        pool = await cls.get_pool()
        async with pool.acquire() as conn:
            return await conn.fetchval(query, *args)

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
        position = data.get('position', 'Bj35')
        mobile = data.get('telephone', 'None')
        email = data.get('email', f"{wecom_id}@bj35.com")
        language = data.get('language', 'zh')
        avatar_text = data.get('avatar', 'None')

        print(f"添加用户: {name} (wecom_id: {wecom_id}), 部门: {department}, 职位: {position}, 手机: {mobile}, 邮箱: {email}, 语言: {language}, 头像: {avatar_text}")

        await PostgreSQLConnector.execute('''
                    INSERT INTO userinfo (wecom, wecom_id, name, password, department, 
                                        position, mobile, language, email, avatar_text)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                    RETURNING uid
                ''', wecom, wecom_id, name, password, department, position,
                                          mobile, language, email, avatar_text)

        logger.info("用户信息已添加: %s (uid: %s)", name, wecom_id)
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

        # 获取并处理英文名
        wecom = next((attr.get('text', {}).get('value')
                      for attr in user.get('extattr', {}).get('attrs', [])
                      if attr.get('name') == '英文名' and attr.get('text', {}).get('value')),
                     user.get('english_name'))

        if not wecom or wecom == user.get('userid'):
            wecom = process_name(user.get('name', 'None'))

        # 构建用户数据
        user_data = {
            'wecom': wecom,
            'wecom_id': user.get('userid', '0'),
            'name': user.get('name', 'None'),
            'department': str(user.get('department', [0])[0]),
            'position': user.get('position', 'Bj35'),
            'telephone': user.get('telephone', 'None'),
            'email': f"{user.get('userid')}@bj35.com",
            'language': 'zh',
            'role': 'user',
            'avatar': ''
        }

        result = await add_user(user_data)
        results.append(result)

        if result['success']:
            logging.info(f"成功添加用户: {user_data['name']} (wecom_id: {user_data['wecom_id']})")
        else:
            logging.error(f"添加用户失败: {user_data['name']} (wecom_id: {user_data['wecom_id']})")

    return results


async def main():
    """主函数"""
    try:
        # 读取JSON文件
        with open('testusers.json', 'r', encoding='utf-8') as f:
            users_data = json.load(f)

        # 处理用户数据
        results = await process_users_from_json(users_data)

        # 统计结果
        success_count = sum(1 for r in results if r['success'])
        total_count = len(results)

        print(f"添加完成。成功：{success_count}/{total_count}")

    except FileNotFoundError:
        logger.error("未找到JSON文件")
    except json.JSONDecodeError:
        logger.error("JSON文件格式错误")
    except Exception as e:
        logger.error("处理过程中出现错误: %s", str(e))
    finally:
        if PostgreSQLConnector._pool:
            await PostgreSQLConnector._pool.close()


if __name__ == '__main__':
    asyncio.run(main())