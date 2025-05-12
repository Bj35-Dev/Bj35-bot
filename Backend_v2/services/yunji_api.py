# -*- coding: utf-8 -*-
"""
This module provides functions to interact with Yunji's API.
"""
import uuid
import json
from datetime import datetime
import logging
import asyncio
import aiohttp

from settings import settings

logger = logging.getLogger(__name__)

BASE_URL = 'https://open-api.yunjiai.cn/v3'


def create_headers():
    """创建请求头，包含签名随机数、时间戳、访问密钥ID和访问令牌"""
    signature_nonce = str(uuid.uuid4())
    headers = {'signatureNonce': signature_nonce,
               'timestamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00'),
               'accessKeyId': settings.YUNJI_ACCESS_KEY_ID,
               'token': str(settings.YUNJI_ACCESS_TOKEN)}
    return headers


async def get_device_list():
    """步获取设备列表"""
    headers = create_headers()
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(BASE_URL + f'/device/list?accessToken%3D{settings.YUNJI_ACCESS_TOKEN}') as response:
            return json.loads(await response.text())


async def get_device_status(chassis_id):
    """异步获取指定设备的状态"""
    headers = create_headers()
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(
                BASE_URL + f'/robot/{chassis_id}/status?accessToken%3D{settings.YUNJI_ACCESS_TOKEN}') as response:
            return json.loads(await response.text())


async def get_device_task(chassis_id):
    """异步获取指定设备的任务列表"""
    headers = create_headers()
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(BASE_URL + f'/robots/{chassis_id}/tasks') as response:
            return json.loads(await response.text())


async def get_school_tasks(page_size, current):
    """异步获取学校任务列表，支持分页"""
    headers = create_headers()
    async with aiohttp.ClientSession(headers=headers) as session:
        params = {'storeIds': settings.YUNJI_STORE_ID,
                  'pageSize': page_size,
                  'current': current
                  }
        async with session.get(BASE_URL + '/rcs/task/list', params=params) as response:
            return json.loads(await response.text())


async def get_cabin_position(cabin_id):
    """
    异步获取指定设备的仓位位置
    注意：执行back时无论发到哪里都只会显示chargepoint
    """
    headers = create_headers()
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(BASE_URL + f'/robot/{cabin_id}/position') as response:
            return json.loads(await response.text())


async def reset_cabin_position(cabin_id, position):
    """异步重置指定设备的仓位位置"""
    headers = create_headers()
    data = {"marker": position}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.put(
                BASE_URL + f'/robot/up/cabin/{cabin_id}/reset-position', json=data) as response:
            return json.loads(await response.text())


async def get_running_task():
    """异步获取正在运行的任务列表"""
    headers = create_headers()
    data = {'storeId': settings.YUNJI_STORE_ID}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(
                BASE_URL + '/rcs/task/running-task/list', json=data) as response:
            return json.loads(await response.text())


async def make_task_flow_move_target_and_lift_down(cabin_id, target):
    """异步创建任务流，移动到指定目标并放下货柜"""
    headers = create_headers()
    data = {
        "outTaskId": str(uuid.uuid4()),
        "templateId": "dock_cabin_and_move_target_and_lift_down",
        "storeId": settings.YUNJI_STORE_ID,
        "params": {
            "dockCabinId": cabin_id,
            "target": target
        }
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(BASE_URL + '/rcs/task/flow/execute', json=data) as response:
            return json.loads(await response.text())


async def make_task_flow_docking_cabin_and_move_target(cabin_id, chassis_id, target):
    """异步创建任务流，对接货柜并移动到指定目标"""
    headers = create_headers()
    data = {
        "outTaskId": str(uuid.uuid4()),
        "templateId": "docking_cabin_and_move_target",
        "storeId": settings.YUNJI_STORE_ID,
        "params": {
            "dockCabinId": cabin_id,
            "chassisId": chassis_id,
            "target": target
        }
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(
                BASE_URL + '/rcs/task/flow/execute', json=data) as response:
            return json.loads(await response.text())


async def make_task_flow_dock_cabin_and_move_target_with_wait_action(cabin_id, chassis_id, target, overtime):
    """
    异步创建任务流，对接货柜并移动到指定目标，支持等待操作
        cabin_id 上仓ID
        chassis_id 底盘ID
        target 目标位置
        overttime 等待时间
    """
    headers = create_headers()
    data = {
        "outTaskId": str(uuid.uuid4()),
        "templateId": "dock_cabin_and_move_target_with_wait_action",
        "storeId": settings.YUNJI_STORE_ID,
        "params": {
            "dockCabinId": cabin_id,
            "chassisId": chassis_id,
            "target": target,
            "overtime": overtime,
            "overtimeEvent": "back"
        }
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(BASE_URL + '/rcs/task/flow/execute', json=data) as response:
            return json.loads(await response.text())


async def make_task_flow_move_and_lift_down(cabin_id, chassis_id, target):
    """异步创建任务流，移动到指定目标并放下货柜"""
    headers = create_headers()
    data = {
        "outTaskId": str(uuid.uuid4()),
        "templateId": "dock_cabin_to_move_and_lift_down",
        "storeId": settings.YUNJI_STORE_ID,
        "params": {
            "dockCabinId": cabin_id,
            "chassisId": chassis_id,
            "target": target
        }
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(BASE_URL + '/rcs/task/flow/execute', json=data) as response:
            return json.loads(await response.text())


async def get_device_by_id(cabin_id):
    """根据设备ID获取设备对象"""
    return {"id": cabin_id, "type": "robot"}
