#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ujson
import redis
import asyncio
import uvicorn
from enum import Enum
from typing import Optional
from fastapi import Depends
from fastapi import Request
from fastapi.responses import JSONResponse

from fastapi import FastAPI
from pydantic import BaseModel

from routers import order

from auth import check_token, UnicornException

app = FastAPI()


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=200,
        content={
            "error": {
                "type": "ERROR_TYPE_ERROR",
                "code": "ERROR_CODE_NOT_FOUND",
                "description": f"{exc.desc}",
                "http_status_code": 400,
            }
        },
    )


class ModelName(str, Enum):
    # 申明枚举数值
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[str] = None


@app.get("/")
def read_root():
    return {"root": "hello"}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


# 使用相关的路由
app.include_router(order.router, dependencies=[Depends(check_token)])

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
