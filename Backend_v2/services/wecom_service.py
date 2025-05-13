"""
Bj35 Bot v2
Refactor by: AptS:1547
Date: 2025-04-19
Description: 这是在 v1 基础上重构的版本，主要改进了代码结构和可读性。
使用 GPLv3 许可证。
Copyright (C) 2025 AptS:1547

本文件定义了与企业微信相关的服务，包括获取access_token、发送消息等功能。
"""

import json
import logging
import random
from urllib.parse import quote
from datetime import datetime

import aiohttp

from utils.settings import settings
from utils.db import RedisConnector
from utils.exceptions import GetWeComTokenError

logger = logging.getLogger(__name__)


class WeComService:
    """企业微信服务类，处理与企业微信相关的所有业务逻辑"""

    __access_token: str = ""  # 存储access_token
    __token_expire_time: int = 0  # 存储access_token的过期时间
    __BASE_URL: str = "https://qyapi.weixin.qq.com/cgi-bin"  # 企业微信API的基础URL

    @classmethod
    async def get_access_token(cls):
        """获取企业微信的access_token"""

        if (cls.__access_token and
                cls.__token_expire_time > int(datetime.now().timestamp() + 60)):
            return cls.__access_token

        url = cls.__BASE_URL + \
            f"/gettoken?corpid={settings.WECOM_CORP_ID}&corpsecret={settings.WECOM_SECRET}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                result = await response.json()
                if result.get("errcode") == 0:
                    cls.__access_token = result.get("access_token")
                    cls.__token_expire_time = int(
                        datetime.now().timestamp()) + result.get("expires_in")
                    return cls.__access_token

        raise GetWeComTokenError(f"获取access_token失败: {result}")

    # 企业微信消息发送
    @classmethod
    async def _send_message(cls, access_token, user_id, message_content):
        """发送消息"""
        url = cls.__BASE_URL + f"/message/send?access_token={access_token}"
        data = {
            "touser": user_id,  # 接收消息的用户ID
            "msgtype": "text",  # 消息类型为文本
            "agentid": settings.WECOM_AGENT_ID,  # 企业微信应用的AgentID
            "text": {
                "content": message_content  # 消息内容
            }
        }
        headers = {
            "Content-Type": "application/json"
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=json.dumps(data)) as response:
                result = await response.json()
                if result.get("errcode") == 0:
                    logger.info("消息发送成功！")
                else:
                    logger.error("消息发送失败: %s", result)

    @classmethod
    async def send(cls, user_id, message_content):
        """发送消息"""
        access_token = await cls.get_access_token()
        await cls._send_message(access_token, user_id, message_content)

    # 企业微信OAuth2.0授权
    @classmethod
    async def get_oauth_url(cls):
        """获取企业微信 OAuth 授权 URL"""
        corp_id = settings.WECOM_CORP_ID
        redirect_uri = quote(settings.WECOM_REDIRECT_URI, safe='')
        agent_id = settings.WECOM_AGENT_ID

        # 生成随机字符串作为 state 参数
        state = ''.join(random.choices(
            'abcdefghijklmnopqrstuvwxyz0123456789', k=16))

        await RedisConnector.store_oauth_state(state)

        # 构建授权URL
        oauth_url = (
            f"https://open.weixin.qq.com/connect/oauth2/authorize"
            f"?appid={corp_id}"
            f"&redirect_uri={redirect_uri}"
            f"&response_type=code"
            f"&scope=snsapi_privateinfo"
            f"&state={state}"
            f"&agentid={agent_id}"
            f"#wechat_redirect"
        )

        return oauth_url

    @classmethod
    async def get_user_info(cls, code: str, state: str):
        """通过授权码获取用户信息"""
        if not await RedisConnector.verify_oauth_state(state):
            logger.warning("无效的state参数，可能是CSRF攻击")
            return None

        # 1. 获取访问令牌
        access_token = await cls.get_access_token()
        if not access_token:
            logger.error("Failed to get access token")
            return None

        # 2. 使用授权码获取用户身份
        user_info = await cls.__get_user_id(access_token, code)
        if not user_info or user_info.get('userid') is None:
            # 判断非企业成员 / 接口错误
            logger.error("Failed to get user ID")
            return None

        # 3. 获取用户基本信息
        user_detail = await cls.__get_user_detail(access_token, user_info.get('userid'))
        if not user_detail:
            return None

        # 4. 如果有user_ticket，获取敏感信息
        if user_info.get('user_ticket'):
            sensitive_info = await cls.__get_sensitive_info \
                                    (access_token, user_info.get('user_ticket'))
            if sensitive_info:
                user_detail.update(sensitive_info)

        return user_detail

    @classmethod
    async def __get_user_id(cls, access_token, code):
        """通过授权码获取用户ID"""
        url = cls.__BASE_URL + \
            f"/auth/getuserinfo?access_token={access_token}&code={code}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    data = await response.json()

            if data is not None and data.get('errcode') == 0:
                return {
                    'userid': data.get('userid'),
                    'user_ticket': data.get('user_ticket')
                }
            logger.error("Failed to get user ID: %s", data)
            return None
        except aiohttp.ClientError as e:
            logger.error("HTTP client error getting user ID: %s", e)
            return None
        except json.JSONDecodeError as e:
            logger.error("JSON decode error getting user ID: %s", e)
            return None

    @classmethod
    async def __get_user_detail(cls, access_token, userid):
        """获取用户基本信息"""
        url = cls.__BASE_URL + \
            f"/user/get?access_token={access_token}&userid={userid}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    data = await response.json()

            if data.get('errcode') == 0:
                return {
                    'userid': data.get('userid'),
                    'name': data.get('name'),
                    'department': data.get('department'),
                    'position': data.get('position'),
                    'wecom': data.get('alias', '')
                }
            logger.error("Failed to get user detail: %s", data)
            return None
        except aiohttp.ClientError as e:
            logger.error("HTTP client error getting user detail: %s", e)
            return None
        except json.JSONDecodeError as e:
            logger.error("JSON decode error getting user detail: %s", e)
            return None

    @classmethod
    async def __get_sensitive_info(cls, access_token, user_ticket):
        """获取用户敏感信息"""
        url = cls.__BASE_URL + \
            f"/user/getuserdetail?access_token={access_token}"
        data = {"user_ticket": user_ticket}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url) as response:
                    data = await response.json()

            if data.get('errcode') == 0:
                return {
                    'mobile': data.get('mobile'),
                    'email': data.get('email'),
                    'avatar': data.get('avatar')
                }
            logger.error("Failed to get sensitive info: %s", data)
            return None
        except aiohttp.ClientError as e:
            logger.error("HTTP client error getting sensitive info: %s", e)
            return None
        except json.JSONDecodeError as e:
            logger.error("JSON decode error getting sensitive info: %s", e)
            return None
