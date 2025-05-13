"""
This module contains decorators for handling errors and authentication.
"""
import logging
from functools import wraps
from quart import jsonify

from services import TokenManager

logger = logging.getLogger(__name__)

def error_handler(func):
    """异常处理装饰器"""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            response = await func(*args, **kwargs)
            if isinstance(response, dict):
                if response.get('code') == 11012:
                    logger.warning("YUNJI Token expired, refreshing token")
                    await TokenManager.get_valid_token()
                    re_response = await func(*args, **kwargs)
                    return jsonify(re_response), response.get('status_code', 500)
            return response
        except Exception as e:
            logger.error("Error in %s : %s", func.__name__, str(e))
            return jsonify({'code': 1, 'message': str(e), 'data': []}), 500

    return wrapper
