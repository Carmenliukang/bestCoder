#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import Header
from typing import Any, Optional


async def check_token(grpc_metadata_x_token: str = Header(None)) -> bool:
    if not grpc_metadata_x_token:
        raise UnicornException()
    return True


async def check_user(grpc_metadata_x_token: str = Header(None)) -> Any:
    # todo grpc_metadata_x_token to user_id
    user = {"name": "test"}
    if not user:
        raise UnicornException()
    return user


class UnicornException(Exception):
    def __init__(self, desc: Optional[str] = None):
        self.desc = desc
