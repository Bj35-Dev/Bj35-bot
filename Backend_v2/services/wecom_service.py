"""
Bj35 Bot v2
Refactor by: AptS:1547
Date: 2025-04-19
Description: 这是在 v1 基础上重构的版本，主要改进了代码结构和可读性。
使用 GPLv3 许可证。
Copyright (C) 2025 AptS:1547

本文件定义了与企业微信相关的服务，包括获取access_token、发送消息等功能。
"""
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
from utils import RedisConnector
from utils.exceptions import GetWeComTokenError

logger = logging.getLogger(__name__)


class WeComService:
    """企业微信服务类，处理与企业微信相关的所有业务逻辑"""

    __access_token: str = ""
    __token_expire_time: int = 0
    __BASE_URL: str = "https://qyapi.weixin.qq.com/cgi-bin"

    @classmethod
    async def get_access_token(cls):
        """获取企业微信的access_token"""
        logger.debug("开始获取access_token")
        current_time = int(datetime.now().timestamp())

        if cls.__access_token and cls.__token_expire_time > current_time + 60:
            logger.debug("使用缓存的access_token，有效期至: %s",
                         datetime.fromtimestamp(cls.__token_expire_time).strftime('%Y-%m-%d %H:%M:%S'))
            return cls.__access_token

        logger.debug("缓存的token已过期或不存在，开始请求新token")
        url = cls.__BASE_URL + f"/gettoken?corpid={settings.WECOM_CORP_ID}&corpsecret={settings.WECOM_SECRET}"

        async with aiohttp.ClientSession() as session:
            logger.debug("发送GET请求到: %s", url.replace(settings.WECOM_SECRET, '*' * 8))
            async with session.get(url) as response:
                result = await response.json()
                logger.debug("获取到响应: %s", {k: v if k != 'access_token' else '***' for k, v in result.items()})

                if result.get("errcode") == 0:
                    cls.__access_token = result.get("access_token")
                    cls.__token_expire_time = current_time + result.get("expires_in")
                    logger.debug("成功获取新token，将在%d秒后过期", result.get("expires_in"))
                    return cls.__access_token

        error_msg = f"获取access_token失败: {result}"
        logger.error(error_msg)
        raise GetWeComTokenError(error_msg)

    @classmethod
    async def _send_message(cls, access_token, user_id, message_content):
        """发送消息"""
        logger.debug("准备发送消息给用户: %s", user_id)
        url = cls.__BASE_URL + f"/message/send?access_token={access_token}"

        data = {
            "touser": user_id,
            "msgtype": "text",
            "agentid": settings.WECOM_AGENT_ID,
            "text": {"content": message_content}
        }

        logger.debug("消息内容: %s", json.dumps(data, ensure_ascii=False))

        headers = {"Content-Type": "application/json"}
        async with aiohttp.ClientSession() as session:
            logger.debug("发送POST请求到: %s", url)
            async with session.post(url, headers=headers, data=json.dumps(data)) as response:
                result = await response.json()
                logger.debug("接收到响应: %s", result)

                if result.get("errcode") == 0:
                    logger.info("消息发送成功！用户: %s", user_id)
                else:
                    logger.error("消息发送失败: %s, 用户: %s", result, user_id)

    @classmethod
    async def send(cls, user_id, message_content):
        """发送消息"""
        logger.debug("开始发送消息流程，用户: %s", user_id)
        access_token = await cls.get_access_token()
        await cls._send_message(access_token, user_id, message_content)

    @classmethod
    async def get_oauth_url(cls):
        """获取企业微信 OAuth 授权 URL"""
        logger.debug("开始生成OAuth授权URL")

        corp_id = settings.WECOM_CORP_ID
        redirect_uri = quote(settings.WECOM_REDIRECT_URI, safe='')
        agent_id = settings.WECOM_AGENT_ID

        state = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=16))
        logger.debug("生成随机state: %s", state)

        success = await RedisConnector.store_oauth_state(state)
        logger.debug("state存储状态: %s", "成功" if success else "失败")

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

        logger.debug("生成OAuth URL: %s", oauth_url)
        return oauth_url

    @classmethod
    async def get_user_info(cls, code: str, state: str):
        """通过授权码获取用户信息"""
        logger.debug("开始获取用户信息，code: %s, state: %s", code, state)

        if not await RedisConnector.verify_oauth_state(state):
            logger.warning("state验证失败: %s", state)
            return None

        logger.debug("state验证通过，开始获取access_token")
        access_token = await cls.get_access_token()
        if not access_token:
            logger.error("获取access_token失败")
            return None

        logger.debug("开始获取用户ID")
        user_info = await cls.__get_user_id(access_token, code)
        if not user_info or user_info.get('userid') is None:
            logger.error("获取用户ID失败: %s", user_info)
            return None

        logger.debug("获取用户基本信息，userid: %s", user_info.get('userid'))
        user_detail = await cls.__get_user_detail(access_token, user_info.get('userid'))
        if not user_detail:
            logger.error("获取用户详细信息失败")
            return None

        if user_info.get('user_ticket'):
            logger.debug("存在user_ticket，获取敏感信息")
            sensitive_info = await cls.__get_sensitive_info(access_token, user_info.get('user_ticket'))
            if sensitive_info:
                user_detail.update(sensitive_info)
                logger.debug("成功更新用户敏感信息")

        logger.debug("完成用户信息获取: %s",
                     {k: v if k not in ['mobile', 'email'] else '***' for k, v in user_detail.items()})
        return user_detail

    @classmethod
    async def __get_user_id(cls, access_token, code):
        """通过授权码获取用户ID"""
        logger.debug("开始通过code获取用户ID: %s", code)
        url = cls.__BASE_URL + f"/auth/getuserinfo?access_token={access_token}&code={code}"

        try:
            async with aiohttp.ClientSession() as session:
                logger.debug("发送GET请求到: %s", url)
                async with session.get(url) as response:
                    data = await response.json()
                    logger.debug("收到响应: %s", data)

                if data.get('errcode') == 0:
                    result = {
                        'userid': data.get('userid'),
                        'user_ticket': data.get('user_ticket')
                    }
                    logger.debug("成功获取用户ID信息: %s", result)
                    return result

                logger.error("获取用户ID失败，错误信息: %s", data)
                return None
        except Exception as e:
            logger.error("获取用户ID时发生异常: %s", str(e))
            return None

    @classmethod
    async def __get_user_detail(cls, access_token, userid):
        """获取用户基本信息"""
        logger.debug("开始获取用户详细信息: %s", userid)
        url = cls.__BASE_URL + f"/user/get?access_token={access_token}&userid={userid}"

        try:
            async with aiohttp.ClientSession() as session:
                logger.debug("发送GET请求到: %s", url)
                async with session.get(url) as response:
                    data = await response.json()
                    logger.debug("收到响应: %s", data)

            if data.get('errcode') == 0:
                result = {
                    'userid': data.get('userid'),
                    'name': data.get('name'),
                    'department': data.get('department'),
                    'position': data.get('position'),
                    'wecom': data.get('alias', '')
                }
                logger.debug("成功获取用户详细信息: %s", result)
                return result

            logger.error("获取用户详细信息失败: %s", data)
            return None
        except Exception as e:
            logger.error("获取用户详细信息时发生异常: %s", str(e))
            return None

    @classmethod
    async def __get_sensitive_info(cls, access_token, user_ticket):
        """获取用户敏感信息"""
        logger.debug("开始获取用户敏感信息")
        url = cls.__BASE_URL + f"/user/getuserdetail?access_token={access_token}"
        data = {"user_ticket": user_ticket}

        try:
            async with aiohttp.ClientSession() as session:
                logger.debug("发送POST请求到: %s", url)
                async with session.post(url, data=json.dumps(data)) as response:
                    result = await response.json()
                    logger.debug("收到响应: %s",
                                 {k: v if k not in ['mobile', 'email'] else '***' for k, v in result.items()})

            if result.get('errcode') == 0:
                sensitive_data = {
                    'mobile': result.get('mobile'),
                    'email': result.get('email'),
                    'avatar': result.get('avatar')
                }
                logger.debug("成功获取敏感信息")
                return sensitive_data

            logger.error("获取敏感信息失败: %s", result)
            return None
        except Exception as e:
            logger.error("获取敏感信息时发生异常: %s", str(e))
            return None