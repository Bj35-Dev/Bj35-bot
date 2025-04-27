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
                response_json = response
                if response_json.get('code') == 11013:
                    logger.error("Authentication failed in %s : %s",func.__name__,response_json)
                    await TokenManager.get_valid_token()
                    return jsonify(response_json), response.get('status_code', 500)
            return response
        except Exception as e:
            logger.error("Error in %s : %s", func.__name__, str(e))
            return jsonify({'code': 1, 'message': str(e), 'data': []}), 500

    return wrapper
