"""
Bj35 Bot v2
Refactor by: AptS:1547
Date: 2025-04-19
Description: 这是在 v1 基础上重构的版本，主要改进了代码结构和可读性。
使用 GPLv3 许可证。
Copyright (C) 2025 AptS:1547

本文件是 Bj35 Bot v2 的工具模块的初始化文件。
"""

from .jwt_handlers import configure_jwt_handlers

from .decorators import error_handler

from . import exceptions

from .settings import settings

__all__ = [
    'configure_jwt_handlers', 'error_handler',

    'exceptions',

    'settings'
]
