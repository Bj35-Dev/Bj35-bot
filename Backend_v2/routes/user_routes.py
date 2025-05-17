"""
user_routes.py

This file contains the routes for user information.
"""
import logging
from quart import jsonify, request
from quart_jwt_extended import jwt_required, get_jwt_identity

from services import UserService

from utils.settings import settings

logger = logging.getLogger(__name__)

URI_PREFIX = settings.URI_PREFIX

def register_routes(app):
    """注册用户信息相关路由"""

    @app.route(URI_PREFIX + '/get_user_profile', methods=['GET'])
    @jwt_required
    async def get_user_profile():
        # 从JWT中获取用户身份
        user_id = get_jwt_identity()

        if not user_id:
            logger.error("用户身份未找到")
            return jsonify({"error": "用户身份未找到"}), 401

        logger.debug("获取用户信息: user_id=%s", user_id)

        # 使用用户ID从数据库获取完整信息
        info = await UserService.get_userinfo(user_id)

        if not info:
            logger.error("未找到用户: uid=%s", user_id)
            return jsonify({"error": "用户不存在"}), 404

        logger.debug("获取到用户信息: %s", info)
        return jsonify(info), 200

    @app.route(URI_PREFIX + '/post_user_profile', methods=['POST'])
    @jwt_required
    async def post_user_profile():
        data = await request.json
        # # 验证邮箱地址，如果需要
        # if key.lower() == "email address":
        #     if not validate_email(value):
        #         return jsonify({'success': False, 'message': 'Invalid email address.'}), 400
        #     print(f"A verification email has been sent to {value}.")

        # 调用update_user_profile方法并传入编辑后的字段和值
        update_response = await UserService.update_userinfo(data)
        # update_response = {"success": True}

        # 根据API返回的数据进行处理
        if update_response['success']:
            logger.info("%s updated profile successfully!", data['name_old'])
            return jsonify(
                {'success': True, 'message': 'Profile updated successfully!'}), 200
        return jsonify(
            {'success': False, 'message': update_response['message']}), 400

    @app.route(URI_PREFIX + '/post_user_avatar', methods=['POST'])
    @jwt_required
    async def post_user_avatar():
        data = await request.json
        update_response = {"success": True}

        # 根据API返回的数据进行处理
        if update_response['success']:
            logger.info("%s updated avatar successfully!", data['username'])
            return jsonify(
                {'success': True, 'message': 'Profile updated successfully!'}), 200
        return jsonify(
        {'success': False, 'message': update_response['message']}), 400

    @app.route(URI_PREFIX + '/change-password', methods=['POST'])
    @jwt_required
    async def update_user_password():
        data = await request.json
        wecom_id = data.get('wecom_id')
        old_password = data.get('old_password')
        new_password = data.get('new_password')

        if not all([wecom_id, old_password, new_password]):
            return jsonify({
                'success': False,
                'message': '缺少必要参数'
            }), 422

        try:
            # 使用 verify_user_credentials 验证原密码
            verification_result = await UserService.verify_user_credentials(wecom_id, old_password)
            if not verification_result:
                logger.warning("用户 %s 原密码验证失败", wecom_id)
                return jsonify({
                    'success': False,
                    'message': '原密码不正确'
                }), 400

            # 更新新密码
            update_response = await UserService.update_userinfo({
                'name_old': wecom_id,  # 确保使用正确的标识字段
                'password': new_password
            })

            if update_response['success']:
                logger.info("用户 %s 密码更新成功", wecom_id)
                return jsonify({
                    'success': True,
                    'message': '密码更新成功'
                }), 200

            return jsonify({
                'success': False,
                'message': '密码更新失败'
            }), 400

        except Exception as e:
            logger.error("密码更新失败: %s", str(e))
            return jsonify({
                'success': False,
                'message': '密码更新失败'
            }), 500
