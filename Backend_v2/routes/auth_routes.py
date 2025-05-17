"""
Authentication routes module.
Handles user authentication, including:
- Local username/password login
- WeChat Work (WeCom) OAuth authentication
- JWT token generation and management
"""

import datetime
import logging
from quart import jsonify, request, redirect
from quart_jwt_extended import create_access_token

from argon2.exceptions import VerifyMismatchError

from services import UserService, WeComService

from pypinyin import pinyin, Style

from utils.settings import settings

logger = logging.getLogger(__name__)

URI_PREFIX = settings.URI_PREFIX
JWT_EXPIRY_WECOM = datetime.timedelta(days=30)
JWT_EXPIRY_REMEMBER = datetime.timedelta(weeks=1)
JWT_EXPIRY_DEFAULT = datetime.timedelta(days=1)

def register_routes(app):
    """注册认证相关路由"""

    # 登录路由
    @app.route(URI_PREFIX + '/auth/login', methods=['POST'])
    async def login():
        data = await request.json
        username = data.get('username', None)
        password = data.get('password', None)
        remember_me = data.get('rememberMe', False)

        if not username or not password:
            return jsonify(code=1, message="Missing username or password"), 422

        try:
            user_info = await UserService.verify_user_credentials(username, password)

            if not user_info:
                logger.warning("User %s not found in database", username)
                return jsonify(code=1, message="User not found")

            # 创建访问令牌，可选择添加更多声明
            expires_delta = JWT_EXPIRY_REMEMBER if remember_me else JWT_EXPIRY_DEFAULT
            access_token = create_access_token(
                identity=user_info.get('uid'),  # 使用新的 uid 字段
                expires_delta=expires_delta,
                user_claims={
                    'username': user_info['username'],
                    'role': user_info['role'],
                    'wecom_id': user_info['wecom_id']
                }
            )
            logger.info("User %s logged in successfully", username)
            return jsonify(code=0, access_token=access_token)

        except VerifyMismatchError as e:
            logger.error("User verification failed: %s", str(e))
            return jsonify(code=1, message="User verification failed")

    # 企业微信OAuth路由
    @app.route(URI_PREFIX + '/auth/wecom', methods=['GET'])
    async def wecom_auth():
        """获取企业微信OAuth授权URL"""
        oauth_url = await WeComService.get_oauth_url()
        logger.debug('Redirecting to WeCom OAuth URL: %s', oauth_url)
        return redirect(oauth_url)


    @app.route(URI_PREFIX + '/auth/wecom/callback', methods=['GET'])
    async def wecom_callback():
        """处理企业微信OAuth回调"""
        code = request.args.get('code')
        state = request.args.get('state')

        if not code or not state:
            logger.error("Missing code or state in WeChat Work OAuth callback")
            return redirect(settings.WECOM_FRONTEND_URL + '/login?error=missing_parameters')

        # 获取用户信息
        user_info = await WeComService.get_user_info(code, state)

        wecom_id = user_info.get('userid', None)

        if not user_info or not wecom_id:
            logger.error("Failed to get user info from WeChat Work")
            return redirect(settings.WECOM_FRONTEND_URL + '/login?error=auth_failed')

        # 检查用户是否存在，如果不存在则创建
        user_exists = await UserService.check_user_exists_by_wecom(wecom_id)

        if not user_exists:
            name = user_info.get('name')
            # 使用 pinyin 函数获取拼音，style=Style.NORMAL 表示获取普通拼音
            pinyin_list = pinyin(name, style=Style.NORMAL)
            # 提取每个汉字拼音的首字母
            initials = ''.join([word[0][0].upper() for word in pinyin_list])
            # 生成默认用户名（姓名拼音首字母+企业微信ID）
            username = f"{initials}{wecom_id}"
            # 生成默认密码（教师姓名首字母大写+教师号）
            password = initials + str(wecom_id)

            # 添加用户到数据库 - 使用新表结构
            await UserService.add_user({
                'username': username,
                'password': password,
                'name': name,
                'role': 'user',
                'email': user_info.get('email', f"{username}@bj35.com"),
                'mobile': user_info.get('mobile', ''),
                'wecom_id': wecom_id,
                'department': ','.join(map(str, user_info.get('department', []))),
                'avatar_url': user_info.get('avatar', '')
            })

            logger.info("Created new user from WeCom: %s", username)

        # 获取用户完整信息用于生成令牌
        db_user = await UserService.get_userinfo_by_username(wecom_id, 'wecom_id')

        if not db_user:
            logger.error("User with WeChat ID %s not found after creation", wecom_id)
            return redirect(settings.WECOM_FRONTEND_URL + '/login?error=user_creation_failed')

        # 创建JWT令牌
        access_token = create_access_token(
            identity=db_user.get('uid'),  # 使用数据库中的 uid
            expires_delta=JWT_EXPIRY_WECOM,
            user_claims={
                'username': db_user.get('username'),
                'role': db_user.get('role'),
                'wecom_id': db_user.get('wecom_id'),
            }
        )

        # 重定向到前端，带上token
        logger.info("User %s logged in via WeCom", db_user.get('name'))
        return redirect(settings.WECOM_FRONTEND_URL + f"/login?token={access_token}")
