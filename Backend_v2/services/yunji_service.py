# -*- coding: utf-8 -*-
"""
云迹机器人服务封装，整合API调用和任务执行功能
"""
import uuid
import json
from datetime import datetime
import logging
import asyncio
import aiohttp

from utils.settings import settings

logger = logging.getLogger(__name__)

class YunjiService:
    """云迹机器人服务类，封装API调用和任务执行逻辑"""

    BASE_URL = 'https://open-api.yunjiai.cn/v3'

    def __init__(self):
        """初始化服务"""
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def __create_headers():
        """创建请求头，包含签名随机数、时间戳、访问密钥ID和访问令牌"""
        signature_nonce = str(uuid.uuid4())
        headers = {
            "User-Agent": "Bj35Bot/2.0",
            'signatureNonce': signature_nonce,
            'timestamp': datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00'),
            'accessKeyId': settings.YUNJI_ACCESS_KEY_ID,
            'token': str(settings.YUNJI_ACCESS_TOKEN)
        }
        return headers

    @classmethod
    async def get_device_list(cls):
        """异步获取设备列表"""
        headers = cls.__create_headers()
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(
                cls.BASE_URL + f'/device/list?accessToken%3D{settings.YUNJI_ACCESS_TOKEN}'
            ) as response:
                return json.loads(await response.text())

    @classmethod
    async def get_device_status(cls, chassis_id):
        """异步获取指定设备的状态"""
        headers = cls.__create_headers()
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(
                cls.BASE_URL + f'/robot/{chassis_id}/status?accessToken%3D{settings.YUNJI_ACCESS_TOKEN}'
            ) as response:
                return json.loads(await response.text())

    @classmethod
    async def get_device_task(cls, chassis_id):
        """异步获取指定设备的任务列表"""
        headers = cls.__create_headers()
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(cls.BASE_URL + f'/robots/{chassis_id}/tasks') as response:
                return json.loads(await response.text())

    @classmethod
    async def get_school_tasks(cls, page_size, current):
        """异步获取学校任务列表，支持分页"""
        headers = cls.__create_headers()
        async with aiohttp.ClientSession(headers=headers) as session:
            params = {
                'storeIds': settings.YUNJI_STORE_ID,
                'pageSize': page_size,
                'current': current
            }
            async with session.get(cls.BASE_URL + '/rcs/task/list', params=params) as response:
                return json.loads(await response.text())

    @classmethod
    async def get_cabin_position(cls, cabin_id):
        """异步获取指定设备的仓位位置"""
        headers = cls.__create_headers()
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(cls.BASE_URL + f'/robot/{cabin_id}/position') as response:
                return json.loads(await response.text())

    @classmethod
    async def reset_cabin_position(cls, cabin_id, position):
        """异步重置指定设备的仓位位置"""
        headers = cls.__create_headers()
        data = {"marker": position}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.put(
                cls.BASE_URL + f'/robot/up/cabin/{cabin_id}/reset-position', json=data
            ) as response:
                return json.loads(await response.text())

    @classmethod
    async def get_running_task(cls):
        """异步获取正在运行的任务列表"""
        headers = cls.__create_headers()
        data = {'storeId': settings.YUNJI_STORE_ID}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(
                cls.BASE_URL + '/rcs/task/running-task/list', json=data
            ) as response:
                return json.loads(await response.text())

    @classmethod
    async def make_task_flow_move_target_and_lift_down(cls, cabin_id, target):
        """异步创建任务流，移动到指定目标并放下货柜"""
        headers = cls.__create_headers()
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
            async with session.post(cls.BASE_URL + '/rcs/task/flow/execute', json=data) as response:
                return json.loads(await response.text())

    @classmethod
    async def make_task_flow_docking_cabin_and_move_target(cls, cabin_id, chassis_id, target):
        """异步创建任务流，对接货柜并移动到指定目标"""
        headers = cls.__create_headers()
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
                cls.BASE_URL + '/rcs/task/flow/execute', json=data
            ) as response:
                return json.loads(await response.text())

    @classmethod
    async def make_task_flow_dock_cabin_and_move_target_with_wait_action(
        cls, cabin_id, chassis_id, target, overtime
    ):
        """异步创建任务流，对接货柜并移动到指定目标，支持等待操作"""
        headers = cls.__create_headers()
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
            async with session.post(cls.BASE_URL + '/rcs/task/flow/execute', json=data) as response:
                return json.loads(await response.text())

    @classmethod
    async def make_task_flow_move_and_lift_down(cls, cabin_id, chassis_id, target):
        """异步创建任务流，移动到指定目标并放下货柜"""
        headers = cls.__create_headers()
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
            async with session.post(cls.BASE_URL + '/rcs/task/flow/execute', json=data) as response:
                return json.loads(await response.text())

    @staticmethod
    async def get_device_by_id(cabin_id):
        """根据设备ID获取设备对象"""
        return {"id": cabin_id, "type": "robot"}

    @classmethod
    async def check_lockers_status(cls, cabin_id):
        """检查设备状态，判断是否开门或关门"""
        res = await cls.get_device_status(cabin_id)
        status = [
            res["data"]["deviceStatus"]["lockers"][0]["status"],
            res["data"]["deviceStatus"]["lockers"][1]["status"]
        ]
        if "OPEN" in status:
            return "open"
        if status == ["CLOSE", "CLOSE"]:
            return "close"

    @classmethod
    async def get_current_position_marker(cls, chassis_id):
        """获取设备当前位置标记"""
        res = await cls.get_device_status(chassis_id)
        return res["data"]["deviceStatus"]["currentPositionMarker"]

    @classmethod
    def _is_at_charge_point(cls, position: str) -> bool:
        """判断是否处于充电桩位置"""
        return "charge_point" in position.lower()

    @classmethod
    async def execute_single_task(cls, cabin_id: str, chassis_id: str, location: str, task_num: int) -> tuple[bool, str]:
        """执行单个位置任务"""
        try:
            logger.info('执行第 %d 个任务，目标位置: %s', task_num, location)
            # 获取设备对象
            device = await cls.get_device_by_id(cabin_id)
            if not device:
                raise ValueError(f"找不到设备ID: {cabin_id}")
            # 执行任务
            res = await cls.make_task_flow_dock_cabin_and_move_target_with_wait_action(
                cabin_id, chassis_id, location, 100
            )
            flag = False  # 标记是否完成一次开门关门 关门为 False 开门为 True
            logger.info('位置 %s 任务执行结果: %s', location, res)

            while True:
                
                # 获取设备实时状态
                await asyncio.sleep(1)
                status = await cls.check_lockers_status(cabin_id)

                await asyncio.sleep(1)
                current_pos = await cls.get_current_position_marker(chassis_id)
                
                logger.debug('门状态: %s，当前位置: %s', status, current_pos)

                # 状态处理逻辑
                if status == "open":
                    flag = True
                elif status == "close" and flag:
                    logger.info('完成完整的开门-关门流程')
                    break  # 退出等待循环继续下一个任务

                # 异常检测：未开门但返回充电点
                if not flag and cls._is_at_charge_point(current_pos):
                    logger.warning('未检测到开门直接返回充电点')
                    return False, '异常返回充电点，门未开启'

                logger.debug('门状态标志: %s, 当前位置: %s', flag, current_pos)

            logger.info('任务%s执行成功 设备ID: %s, 位置: %s',
                            task_num, cabin_id, location)
            return True, ""
        except Exception as e:
            logger.error("位置 %s 任务执行失败: %s", location, str(e))
            return False, f'任务执行失败: {str(e)}'

    @classmethod
    async def run(cls, locations, cabin_id):
        """执行任务流"""
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
            # 执行每个位置的任务
            for idx, location in enumerate(locations):
                success, message = await cls.execute_single_task(cabin_id, chassis_id, location, idx + 1)
                if not success:
                    return {'code': 1, 'message': message}

        except Exception as e:
            logger.error('任务流执行失败: %s', str(e))
            return {'code': 1, 'message': f'任务流执行失败: {str(e)}'}

        # back回返回默认充电桩，在执行完最后一个任务后再执行一个回到原地的任务
        await cls.make_task_flow_dock_cabin_and_move_target_with_wait_action(
            cabin_id, chassis_id, locations[-1], 10
        )
