#!/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Query

from ..auth import check_user

from base import Order, local_now_timestamp

router = APIRouter(
    prefix="/order",
    tags=["order"],
    responses={404: {"description": "Not found"}},
)


@router.get("/list")
async def get_order(
        page_no: int = Query(1, gt=0, lt=20),
        page_size: int = Query(10, gt=1, lt=100),
        since: datetime = local_now_timestamp(),
        until: datetime = local_now_timestamp(date=datetime.now() + timedelta(days=-1)),
        phone: str = Query(None, max_length=11),
        name: str = None,
        user: dict = Depends(check_user),
):
    """
    查看订单，只能查看历史订单
    """
    return Order(name="test", phone="17621173188", site_uid=1, floor=10, room="10层茶水间")


@router.post("/create")
async def add_order(
        order: Order,
        user: dict = Depends(check_user),
):
    """
    创建订单
    创建订单一定是同一站点，todo 后期可能会进行区域划分，这里会设置规则苦
    """
    return {}


@router.post("/confirm")
async def confirm_order(
        order_id: int,
        user: dict = Depends(check_user),
):
    """
    订单确认接口
    :param order_id:
    :return:
    """
    return {}


@router.post("/deliver")
async def update_order(
        order_id: int,
        user: dict = Depends(check_user),
):
    """
    订单发货接口
    :param order_id:
    :return:
    """
    return {}


@router.post("/update")
async def update_order(
        order_id: int,
        order: Order,
        user: dict = Depends(check_user),
):
    """
    修改订单
    :param order_id:
    :param order:
    :return:
    """
    return {}


@router.post("/cancel")
async def cancel_order(
        order_id: int,
        user: dict = Depends(check_user),
):
    """
    取消订单
    :param order_id:
    :return:
    """
    return {}


@router.post("/delete")
async def delete_order(
        order_id: int,
        user: dict = Depends(check_user),
):
    """
    删除订单，只能删除历史订单
    :param order_id:
    :return:
    """
    return {}
