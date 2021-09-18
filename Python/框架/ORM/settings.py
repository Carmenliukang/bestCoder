# -*- coding: utf-8 -*-

"""
AppAiyo.settings
~~~~~~~~~~~~~

Default app_aiyo settings.
"""

from typing import Optional

import orjson
from decouple import config

####
# DB
####


DB_DSN: str = config(
    "DB_DSN",
    default="postgresql+psycopg2://postgres:123456@127.0.0.1:5432/public",
)

DB_POOL_SIZE: int = config("DB_POOL_SIZE", default=10, cast=int)
DB_MAX_OVERFLOW: int = config("DB_MAX_OVERFLOW", default=200, cast=int)
DB_POOL_RECYCLE: int = config("DB_POOL_RECYCLE", default=1200, cast=int)

# 默认查询上限
DEFAULT_MAX_QUERY_LIMIT: int = config("DEFAULT_MAX_QUERY_LIMIT", default=200, cast=int)

####
# Redis
####

REDIS_HOST: str = config("REDIS_HOST", default="0.0.0.0")
REDIS_PORT: int = config("REDIS_PORT", default=6379, cast=int)
REDIS_DB: int = config("REDIS_DB", default=0, cast=int)
REDIS_PASS: Optional[str] = config("REDIS_PASS", default=None)
REDIS_PREFIX: str = config("REDIS_PREFIX", default="app_aiyo")

CACHE_REDIS_HOST: str = config("CACHE_REDIS_HOST", default="localhost")
CACHE_REDIS_PORT: int = config("CACHE_REDIS_PORT", default=6379, cast=int)
CACHE_REDIS_DB: int = config("CACHE_REDIS_DB", default=0, cast=int)
CACHE_REDIS_PASS: str = config("CACHE_REDIS_PASS", default=None)
CACHE_DEFAULT_EXPIRE: int = config(
    "CACHE_DEFAULT_EXPIRE", default=30, cast=int
)  # default expire time 3s

CONFIG_REDIS_URL: str = config("CONFIG_REDIS_URL", default="redis://127.0.0.0/0")
