#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ujson
import asyncio
import uvicorn
from enum import Enum
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


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


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


@app.get("/async/")
async def read_async_root():
    # result = await get_root()
    return {"root": "hello"}


@app.get("/async/items/{item_id}")
async def read_async_item(item_id: int, q: Optional[str] = None):
    return {"item": item_id, "q": q}


def get_root():
    asyncio.sleep(1)
    # yield {"root": "hello"}
    return {"root": "hello"}


@app.get("/model/{model_name}")
def read_model_name(model_name: ModelName):
    if model_name == ModelName.lenet:
        return {"model_name": ModelName.lenet, "desc": f"{ModelName.lenet.value}"}
    if model_name.value == "resnet":
        return {"model_name": ModelName.resnet, "desc": f"{ModelName.resnext.value}"}
    return {"model_name": ModelName.alexnet, "desc": f"{ModelName.alexnet.value}"}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


# @app.post()

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
