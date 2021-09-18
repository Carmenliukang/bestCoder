# -*- coding: utf-8 -*-

from __future__ import annotations

import inspect
import logging
import threading

from redis import Redis, ConnectionPool
from dogpile.cache import CacheRegion, make_region
from dogpile.cache.util import sha1_mangle_key

from settings import (
    REDIS_DB,
    REDIS_HOST,
    REDIS_PASS,
    REDIS_PORT,
    CACHE_REDIS_DB,
    CACHE_REDIS_HOST,
    CACHE_REDIS_PASS,
    CACHE_REDIS_PORT,
    CACHE_DEFAULT_EXPIRE,
)

from typing import Any, Callable

redis_db = Redis(
    connection_pool=ConnectionPool(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        password=REDIS_PASS,
        max_connections=128,
    )
)


def _kw_generator(namespace, fn):
    if namespace is None:
        namespace = f"{fn.__module__}:{fn.__name__}"
    else:
        namespace = f"{namespace}|{fn.__module__}:{fn.__name__}"

    params = list(inspect.signature(fn).parameters.keys())

    def generate_key(*args, **kw):
        if args:
            if inspect.isclass(args[0]) or params[0] == "self":
                args = args[1:]
        tuples = sorted(kw.items())
        return f"{namespace}|{args}{tuples}"

    return generate_key


def _async_creation_runner(
        _cache: CacheRegion, key: str, creator: Callable, mutex: Any
):
    """Used by dogpile.core:Lock when appropriate"""

    def runner():
        try:
            value = creator()
            _cache.set(key, value)
        finally:
            mutex.release()

    threading.Thread(target=runner, daemon=True).start()


sync_cache = make_region(
    key_mangler=lambda key: "cache:app.test:v0_1_0:" + sha1_mangle_key(key),
    function_key_generator=_kw_generator,
).configure(
    "dogpile.cache.redis",
    expiration_time=CACHE_DEFAULT_EXPIRE,
    arguments={
        "host": CACHE_REDIS_HOST,
        "port": CACHE_REDIS_PORT,
        "db": CACHE_REDIS_DB,
        "password": CACHE_REDIS_PASS,
        "redis_expiration_time": 3600 * 24,
        "distributed_lock": True,
        "thread_local_lock": False,
        "lock_timeout": 10,
    },
)

async_cache = make_region(
    key_mangler=lambda key: "cache:app.test:v0_4_6:" + sha1_mangle_key(key),
    function_key_generator=_kw_generator,
    async_creation_runner=_async_creation_runner,
).configure(
    "dogpile.cache.redis",
    expiration_time=CACHE_DEFAULT_EXPIRE,
    arguments={
        "host": CACHE_REDIS_HOST,
        "port": CACHE_REDIS_PORT,
        "db": CACHE_REDIS_DB,
        "password": CACHE_REDIS_PASS,
        "redis_expiration_time": 3600 * 24,
        "distributed_lock": True,
        "thread_local_lock": False,
        "lock_timeout": 10,
    },
)

redis_cache = Redis(
    connection_pool=ConnectionPool(
        host=CACHE_REDIS_HOST,
        port=CACHE_REDIS_PORT,
        db=CACHE_REDIS_DB,
        password=CACHE_REDIS_PASS,
    )
)

mem_cache = make_region(function_key_generator=_kw_generator).configure(
    "dogpile.cache.memory"
)


def dont_cache_empty(value: Any) -> bool:
    if isinstance(value, dict) or isinstance(value, list):
        return len(value) > 0

    if value is False:
        return False

    return value is not None


# change dogpile logging to debug by default
logging.getLogger("dogpile.cache").setLevel(logging.DEBUG)
