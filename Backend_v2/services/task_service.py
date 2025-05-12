# -*- coding: utf-8 -*-

from .yunji_api import (
    get_device_status,
    get_device_by_id,
    make_task_flow_dock_cabin_and_move_target_with_wait_action
)

import uuid
import json
from datetime import datetime
import logging
import asyncio
import aiohttp

from settings import settings

logger = logging.getLogger(__name__)

async def check_lockers_status(cabin_id):
    """检查设备状态，判断是否开门或关门"""
    res = await get_device_status(cabin_id)
    status = [res["data"]["deviceStatus"]["lockers"][0]["status"],
              res["data"]["deviceStatus"]["lockers"][1]["status"]]
    if "OPEN" in status:
        return "open"
    elif status == ["CLOSE", "CLOSE"]:
        return "close"

async def get_current_position_marker(chassis_id):
    """获取设备当前位置标记
    Args:
        chassis_id: 底盘设备ID
        
    Returns:
        str: 当前设备位置标记
    """
    res = await get_device_status(chassis_id)
    return res["data"]["deviceStatus"]["currentPositionMarker"]


def _is_at_charge_point(position: str) -> bool:
    """判断是否处于充电桩位置"""
    return "charge_point" in position.lower()


async def execute_single_task(cabin_id: str, chassis_id: str, location: str, task_num: int) -> tuple[bool, str]:
    """执行单个位置任务
    Args:
        cabin_id: 上仓设备ID
        chassis_id: 底盘设备ID
        location: 目标位置
        task_num: 任务序号
        
    Returns:
        tuple[是否成功, 错误信息]
    """
    try:
        logger.info('执行第 %d 个任务，目标位置: %s', task_num, location)
        # 获取设备对象
        device = await get_device_by_id(cabin_id)
        if not device:
            raise ValueError(f"找不到设备ID: {cabin_id}")
        # 执行任务
        res = await (make_task_flow_dock_cabin_and_move_target_with_wait_action
                     (cabin_id, chassis_id, location, 100))
        flag = False  # 标记是否完成一次开门关门 关门为 False 开门为 True
        logger.info('位置 %s 任务执行结果: %s', location, res)
        
        while True:
            await asyncio.sleep(1)
            
            # 获取设备实时状态
            status = await check_lockers_status(cabin_id)
            current_pos = await get_current_position_marker(chassis_id)
            logger.debug('门状态: %s，当前位置: %s', status, current_pos)

            # 状态处理逻辑
            if status == "open":
                flag = True
            elif status == "close" and flag:
                logger.info('完成完整的开门-关门流程')
                break  # 退出等待循环继续下一个任务
            
            # 异常检测：未开门但返回充电点
            if not flag and _is_at_charge_point(current_pos):
                logger.warning('未检测到开门直接返回充电点')
                return False, '异常返回充电点，门未开启'
                
            logger.debug('门状态标志: %s, 当前位置: %s', flag, current_pos)
        
        logger.info('任务%s执行成功 设备ID: %s, 位置: %s',
                    task_num, cabin_id, location)
        return True, ""
    except Exception as e:
        logger.error("位置 %s 任务执行失败: %s", location, str(e))
        return False, f'任务执行失败: {str(e)}'

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
        # 执行每个位置的任务
        for idx, location in enumerate(locations):
            success, message = await execute_single_task(cabin_id, chassis_id, location, idx + 1)
            if not success:
                return {'code': 1, 'message': message}

    except Exception as e:
        logger.error('任务流执行失败: %s', str(e))
        return {'code': 1, 'message': f'任务流执行失败: {str(e)}'}

    # back回返回默认充电桩，在执行完最后一个任务后再执行一个回到原地的任务
    # 触发back后会自动回到默认充电桩，省去的调env的复杂结构
    # 使用最后一个位置，以便在任务完成后返回到任务的起点
    # 10s是一个经验值，并且在其他功能中不会用到，所以直接写死
    await (make_task_flow_dock_cabin_and_move_target_with_wait_action
           (cabin_id, chassis_id, locations[-1], 10))
