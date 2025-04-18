# -*- coding: utf-8 -*-
import sys
import os
import uuid
import time
import json
import logging
import asyncio
import aiohttp

from settings import settings

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

access_token = settings.YUNJI_ACCESS_TOKEN
logger = logging.getLogger(__name__)
# print(access_token)

def create_headers():
    # 创建请求头，包含签名随机数、时间戳、访问密钥ID和访问令牌
    signatureNonce = str(uuid.uuid4())
    headers = {'signatureNonce': signatureNonce,
               'timestamp': str(time.strftime('%Y-%m-%dT%H:%M:%S+08:00', time.gmtime())),
               'accessKeyId': settings.YUNJI_ACCESS_KEY_ID,
               'token': str(access_token)}
    return headers

async def get_device_list():
    # 异步获取设备列表
    headers = create_headers()
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f'https://open-api.yunjiai.cn/v3/device/list?accessToken%3D{access_token}') as response:
            return json.loads(await response.text())

async def get_device_status(chassis_id):
    # 异步获取指定设备的状态
    headers = create_headers()
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f'https://open-api.yunjiai.cn/v3/robot/{chassis_id}/status?accessToken%3D{access_token}') as response:
            return json.loads(await response.text())

async def get_device_task(chassis_id):
    # 异步获取指定设备的任务列表
    headers = create_headers()
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f'https://open-api.yunjiai.cn/v3/robots/{chassis_id}/tasks') as response:
            return json.loads(await response.text())

async def get_school_tasks(pageSize, current):
    # 异步获取学校任务列表，支持分页
    headers = create_headers()
    async with aiohttp.ClientSession(headers=headers) as session:
        params = {'storeIds': settings.YUNJI_STORE_ID,
                  'pageSize': pageSize,
                  'current': current
                  }
        async with session.get(f'https://open-api.yunjiai.cn/v3/rcs/task/list', params=params) as response:
            return json.loads(await response.text())

async def get_cabin_position(cabin_id):
    # 异步获取指定设备的仓位位置
    headers = create_headers()
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f'https://open-api.yunjiai.cn/v3/robot/{cabin_id}/position') as response:
            return json.loads(await response.text())

async def reset_cabin_position(cabin_id, position):
    # 异步重置指定设备的仓位位置
    headers = create_headers()
    data = {"marker": position}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.put(f'https://open-api.yunjiai.cn/v3/robot/up/cabin/{cabin_id}/reset-position', json=data) as response:
            return json.loads(await response.text())

async def get_running_task():
    # 异步获取正在运行的任务列表
    headers = create_headers()
    storeId = settings.YUNJI_STORE_ID
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f'https://open-api.yunjiai.cn/v3/rcs/task/running-task/list', json={'storeId': storeId}) as response:
            return json.loads(await response.text())

async def make_task_flow_move_target_and_lift_down(cabin_id, target):
    # 异步创建任务流，移动到指定目标并放下货柜
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
        async with session.post(f'https://open-api.yunjiai.cn/v3/rcs/task/flow/execute', json=data) as response:
            return json.loads(await response.text())

async def make_task_flow_docking_cabin_and_move_target(cabin_id,chassis_id,target):
    # 异步创建任务流，对接货柜并移动到指定目标
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
        async with session.post(f'https://open-api.yunjiai.cn/v3/rcs/task/flow/execute', json=data) as response:
            return json.loads(await response.text())

async def make_task_flow_dock_cabin_and_move_target_with_wait_action(cabin_id,chassis_id,target,overtime):
    # 异步创建任务流，对接货柜并移动到指定目标，支持等待操作
    #cabin_id 上仓ID
    #chassis_id 底盘ID
    #target 目标位置
    #overttime 等待时间
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
        async with session.post(f'https://open-api.yunjiai.cn/v3/rcs/task/flow/execute', json=data) as response:
            return json.loads(await response.text())

async def make_task_flow_move_and_lift_down(cabin_id,chassis_id, dockingMarker, target):
    # 异步创建任务流，移动到指定目标并放下货柜
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
        async with session.post(f'https://open-api.yunjiai.cn/v3/rcs/task/flow/execute', json=data) as response:
            return json.loads(await response.text())

async def get_device_by_id(cabin_id):
    """根据设备ID获取设备对象"""
     # 实现略，可从数据库或设备管理服务获取
    return {"id": cabin_id, "type": "robot"}

async def sleep(time):
    # 异步休眠指定时间
    await asyncio.sleep(time)

async def check(cabin_id):
    res=await get_device_status(cabin_id)
    status=[res["data"]["deviceStatus"]["lockers"][0]["status"], res["data"]["deviceStatus"]["lockers"][1]["status"]]
    if "OPEN" in status:
        return "open"
    elif status==["CLOSE", "CLOSE"]:
        return "close"

async def RUN(locations, cabin_id):
    """执行任务流

    Args:
        locations: 位置列表，包含机器人需要到达的目标位置
        cabin_id: 需要执行任务的上仓设备ID

    Returns:
        dict: 包含执行结果的状态码和消息
    """

    cabins = settings.CABINS
    cabin_prefix = cabin_id[0:6]

    for key, value in cabins.items():
        if cabin_prefix in value:
            logger.info(f'找到匹配的CABIN: {value}, 对应的位置: {key}')
            try:
                chassis_id = settings.CHASSIS.get(key, None)
            except:
                return {'code': 1, 'message': '找不到匹配的底盘ID'}

    if chassis_id == "" or chassis_id == None:
        return {'code': 1, 'message': f'找不到匹配的CABIN通过前缀: {cabin_prefix}'}


    try:
        if not locations:
            return {'code': 1, 'message': '位置列表不能为空'}

        logger.info(f'开始执行任务流，设备ID: {cabin_id}, 位置列表: {locations}')
        # 执行每个位置的任务
        task_results = []
        for idx, location in enumerate(locations):
            logger.info(f'执行第 {idx + 1} 个任务，目标位置: {location}')
            print(f'执行第 {idx + 1} 个任务，目标位置: {location}')
            try:
                # 获取设备对象
                device = await get_device_by_id(cabin_id)
                if not device:
                    raise ValueError(f"找不到设备ID: {cabin_id}")
                # 执行任务
                res = await make_task_flow_dock_cabin_and_move_target_with_wait_action(cabin_id,chassis_id, location, 100)
                flag = False  # 标记是否完成一次开门关门 关门为 False 开门为 True
                task_results.append(res)
                logger.info(f'位置 {location} 任务执行结果: {res}')
                while True:
                    res = await check(cabin_id)
                    print(f'flag:{flag} res:{res}')
                    if res == "open":
                        flag = True
                    if res == "close" and flag == True:
                        break
                    await asyncio.sleep(1)
                print(f'code: 0, message: 任务{idx + 1}执行成功 设备ID: {cabin_id}, 位置: {location}')
            except Exception as e:
                logger.error(f'位置 {location} 任务执行失败: {str(e)}')
                return {'code': 1, 'message': f'任务执行失败: {str(e)}'}

    except Exception as e:
        logger.error(f'任务流执行失败: {str(e)}')
        return {'code': 1, 'message': f'任务流执行失败: {str(e)}'}

    await make_task_flow_dock_cabin_and_move_target_with_wait_action(cabin_id,chassis_id, "charge_point_1F_40300716", 100)
