# -*- coding: utf-8 -*-
"""
This module provides functions to interact with Yunji's API.
"""
import uuid
import time
import json
import logging
import asyncio
import aiohttp

from settings import settings

logger = logging.getLogger(__name__)

BASE_URL = 'https://open-api.yunjiai.cn/v3'

# 初始化调度器
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore

scheduler = AsyncIOScheduler(jobstores={'default': MemoryJobStore()})
scheduler.start()


def create_headers():
    """创建请求头，包含签名随机数、时间戳、访问密钥ID和访问令牌"""
    signature_nonce = str(uuid.uuid4())
    headers = {'signatureNonce': signature_nonce,
               'timestamp': str(time.strftime('%Y-%m-%dT%H:%M:%S+08:00', time.gmtime())),
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
    """异步获取指定设备的仓位位置"""
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

# 任务状态跟踪字典
task_status = {}

async def check(cabin_id):
    """检查设备状态，判断是否开门或关门"""
    res = await get_device_status(cabin_id)
    status = [res["data"]["deviceStatus"]["lockers"][0]["status"],
              res["data"]["deviceStatus"]["lockers"][1]["status"]]
    if "OPEN" in status:
        return "open"
    elif status == ["CLOSE", "CLOSE"]:
        return "close"

async def _check_status_and_proceed(job_id, cabin_id, chassis_id, location, max_retries=100):
    """状态检查调度任务"""
    if task_status.get(job_id, {}).get('retries', 0) >= max_retries:
        task_status[job_id]['status'] = 'timeout'
        scheduler.remove_job(job_id)
        return

    res = await check(cabin_id)
    logger.debug(f'Job {job_id} check: {res}')

    if res == "open":
        task_status[job_id]['flag'] = True
    elif res == "close" and task_status[job_id].get('flag', False):
        task_status[job_id]['status'] = 'completed'
        scheduler.remove_job(job_id)
        logger.info(f'任务完成 设备ID: {cabin_id}, 位置: {location}')

    task_status[job_id]['retries'] += 1


async def run(locations, cabin_id):
    """执行任务流
    Args:
        locations: 位置列表，包含机器人需要到达的目标位置
        cabin_id: 需要执行任务的上仓设备ID

    Returns:
        dict: 包含执行结果的状态码和消息
    """
    cabins = dict(settings.CABINS)
    chassis = dict(settings.CHASSIS)
    cabin_prefix = cabin_id[0:6]
    chassis_id = ""

    for key, value in cabins.items():
        if cabin_prefix in value:
            logger.info('找到匹配的CABIN: %s, 对应的位置: %s', value, key)
            try:
                chassis_id = chassis.get(key, None)
            except KeyError:
                logger.error('找不到匹配的底盘ID: %s', key)
                return {'code': 1, 'message': '找不到匹配的底盘ID'}

    if chassis_id == "" or chassis_id is None:
        return {'code': 1, 'message': f'找不到匹配的CABIN通过前缀: {cabin_prefix}'}

    try:
        if not locations:
            return {'code': 1, 'message': '位置列表不能为空'}

        logger.info('开始执行任务流，设备ID: %s, 位置列表: %s', cabin_id, locations)
        task_results = []

        async def _execute_single_task(location):
            """执行单个位置任务"""
            job_id = str(uuid.uuid4())
            task_status[job_id] = {
                'status': 'pending',
                'retries': 0,
                'flag': False
            }

            try:
                device = await get_device_by_id(cabin_id)
                if not device:
                    raise ValueError(f"找不到设备ID: {cabin_id}")

                # 提交主任务
                res = await make_task_flow_dock_cabin_and_move_target_with_wait_action(
                    cabin_id, chassis_id, location, 100)
                task_results.append(res)

                # 添加状态检查任务
                scheduler.add_job(
                    _check_status_and_proceed,
                    'interval',
                    seconds=1,
                    args=(job_id, cabin_id, chassis_id, location),
                    id=job_id
                )

                # 等待任务完成
                while task_status[job_id]['status'] not in ('completed', 'timeout'):
                    await asyncio.sleep(0.1)

                if task_status[job_id]['status'] == 'timeout':
                    raise TimeoutError(f"位置 {location} 任务超时")

                logger.info('code: 0, message: 任务执行成功 设备ID: %s, 位置: %s', cabin_id, location)
                return res

            except Exception as e:
                logger.error("位置 %s 任务执行失败: %s", location, str(e))
                raise
            finally:
                task_status.pop(job_id, None)

        # 使用异步生成器执行任务序列
        for idx, location in enumerate(locations):
            logger.info('执行第 %d 个任务，目标位置: %s', idx + 1, location)
            try:
                await _execute_single_task(location)
            except Exception as e:
                return {'code': 1, 'message': f'任务执行失败: {str(e)}'}


    except Exception as e:
        logger.error('任务流执行失败: %s', str(e))
        return {'code': 1, 'message': f'任务流执行失败: {str(e)}'}

    await (make_task_flow_dock_cabin_and_move_target_with_wait_action
           (cabin_id, chassis_id, "charge_point_1F_40300716", 100))

    # 关闭调度器时清理资源
    def shutdown_scheduler():
        if scheduler.running:
            scheduler.shutdown()

    import atexit
    atexit.register(shutdown_scheduler)
