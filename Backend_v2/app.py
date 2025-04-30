"""
Bj35 Bot v2
Refactor by: AptS:1547
Date: 2025-04-19
Description: 这是在 v1 基础上重构的版本，主要改进了代码结构和可读性。
使用 GPLv3 许可证。
Copyright (C) 2025 AptS:1547

本文件是应用的入口点，负责创建和配置 Quart 应用实例。
"""

import sys
import logging

from quart import Quart
from quart_cors import cors
from quart_jwt_extended import JWTManager

from settings import settings
from utils import PostgreSQLConnector, RedisConnector
from utils.exceptions import DatabaseConnectionError, RedisConnectionError
from utils import configure_jwt_handlers
from services import TokenManager

from routes import register_all_routes

# 配置日志


def configure_logging():
    """配置日志系统"""
    # 创建日志格式器
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(log_format)

    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # 配置根日志记录器
    root_logger = logging.getLogger()
    try:
        log_level = logging.getLevelNamesMapping().get(settings.LOG_LEVEL, logging.INFO)
    except ValueError:
        log_level = logging.INFO # Default to INFO if the LOG_LEVEL is invalid
        root_logger.warning(f"Invalid LOG_LEVEL '{settings.LOG_LEVEL}'. Using INFO level.")
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)

    root_logger.info("日志系统已配置，当前日志级别: %s", settings.LOG_LEVEL)


def create_app():
    """应用工厂函数"""
    quart_app = Quart(__name__)

    # 配置CORS和JWT
    quart_app = cors(quart_app, allow_origin="*")
    quart_app.config["JWT_SECRET_KEY"] = settings.AUTH_JWT_SECRET_KEY
    jwt = JWTManager(quart_app)

    # 配置JWT错误处理器
    configure_jwt_handlers(jwt)

    # 注册所有路由
    register_all_routes(quart_app)

    return quart_app


# 创建应用实例
app = create_app()


async def init_db():
    """初始化数据库连接"""
    try:
        await PostgreSQLConnector.initialize()
        await RedisConnector.initialize()
        logging.info("数据库连接初始化成功")
        return True
    except DatabaseConnectionError as e:
        if settings.ENV == 'development':
            logging.error("数据库初始化失败: %s", e)
            return True
        return False
    except RedisConnectionError as e:
        if settings.ENV == 'development':
            logging.error("Redis初始化失败: %s", e)
            return True
        return False


@app.before_serving
async def before_serving():
    """在应用启动前执行的函数"""
    configure_logging()

    ascii_art = """
    ██████╗     ██╗██████╗ ███████╗    ██████╗  ██████╗ ████████╗
    ██╔══██╗    ██║╚═██╔═╝ ██╔════╝    ██╔══██╗██╔═══██╗╚══██╔══╝
    ██████╔╝    ██║  ██║   ███████╗    ██████╔╝██║   ██║   ██║   
    ██╔══██╗    ██║  ██║   ╚════██║    ██╔══██╗██║   ██║   ██║   
    ██████╔╝    ██║██████╗ ███████║    ██████╔╝╚██████╔╝   ██║   
    ╚═════╝     ╚═╝╚═════╝ ╚══════╝    ╚═════╝  ╚═════╝    ╚═╝   
    Version 2.0 - Powered by AptS:1547  ╰(*°▽°*)╯
    """
    logging.info("\n%s", ascii_art)

    if await init_db():
        logging.info("数据库连接成功")
    if await TokenManager.get_valid_token():
        TokenManager.log_token_expiry()
        logging.info("获取有效的token成功")
    else:
        logging.error("获取有效的token失败，应用将退出")
        sys.exit(1)

    logging.info("应用已启动，准备接受请求 owo ~ 此版本为 1547 重构的 v2 版本")


@app.after_serving
async def after_serving():
    """在应用关闭后执行的函数"""
    await PostgreSQLConnector.close()
    logging.info("应用已关闭 owo ~")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
