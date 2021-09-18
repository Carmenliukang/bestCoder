#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import IntEnum

from typing import Optional

from pydantic import BaseModel

from datetime import datetime


class OrderStatus(IntEnum):
    # 未知
    ORDER_STATUS_UNKNOWN = 0
    # 已创建
    ORDER_STATUS_CREATED = 10
    # 已确认
    ORDER_STATUS_CONFIRMED = 20
    # 配送中
    ORDER_STATUS_SHIPPING = 30
    # 物流完成
    ORDER_STATUS_SHIPMENT_COMPLETED = 40
    # 已完成
    ORDER_STATUS_COMPLETED = 80
    # 取消
    ORDER_STATUS_CANCELED = 255


class Order(BaseModel):
    user_id: int
    creator_user_id: int  # 创建人ID
    creator_user_name: str  # 创建人
    creator_user_phone: str
    creator_user_address: str = None
    site_uid: int  # 站点
    floor: int  # 楼层
    room: str  # 具体位置，只能限定位置
    desc: Optional[str] = None  # 备注说明
    order_status: Optional[OrderStatus] = 0  # 这里需要异步协程监听状态同步完成修改

    # 放货人信息
    sender_user_id: int = None
    sender_user_name: str = None
    sender_user_phone: str = None
    sender_user_address: str = None

    # 收货人信息
    receiver_user_id: int = None
    receiver_user_name: str = None
    receiver_user_phone: str = None
    receiver_user_address: str = None

    # 扩展字段
    exntend: dict = {}  # 字典格式扩展


class Message(BaseModel):
    robot: bool = True
    task_name: str


class Config(BaseModel):
    robot: bool = True
    task_name: str


def local_now_timestamp(date: datetime = datetime.now()) -> int:
    # 获取当前时区的时间戳
    return datetime.timestamp(date).__int__()
