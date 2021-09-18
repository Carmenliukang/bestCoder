# -*- coding: utf-8 -*-

from __future__ import annotations

import os
import asyncio
import inspect
import functools
import collections

import orjson
from blinker import signal
from sqlalchemy import exc, event, create_engine
from sqlalchemy.engine.base import Engine as SQLAlchemyEngine
from sqlalchemy.orm import UOWTransaction, sessionmaker, scoped_session
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import AsyncSession as _AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_scoped_session

from settings import DB_DSN, DB_POOL_SIZE, DB_MAX_OVERFLOW, DB_POOL_RECYCLE

engine: SQLAlchemyEngine = create_engine(
    DB_DSN,
    pool_size=DB_POOL_SIZE,
    max_overflow=DB_MAX_OVERFLOW,
    pool_recycle=DB_POOL_RECYCLE,
    json_serializer=lambda obj: orjson.dumps(obj).decode(),
    json_deserializer=lambda obj: orjson.loads(obj),
)

# Constructs a scoped DBSession.
Session = scoped_session(
    sessionmaker(engine, expire_on_commit=False, future=True),
)


@event.listens_for(engine, "connect")
def connect(dbapi_connection, connection_record):
    connection_record.info["pid"] = os.getpid()


@event.listens_for(engine, "checkout")
def checkout(dbapi_connection, connection_record, connection_proxy):
    pid = os.getpid()
    if connection_record.info["pid"] != pid:
        connection_record.connection = connection_proxy.connection = None
        raise exc.DisconnectionError(
            "Connection record belongs to pid %s, "
            "attempting to check out in pid %s" % (connection_record.info["pid"], pid)
        )


@event.listens_for(Session, "after_flush")
def after_flush(session, flush_context: UOWTransaction):
    if not hasattr(session, "g_changed_track_info"):
        session.g_changed_track_info = collections.defaultdict(set)

    for instances in flush_context.mappers.values():
        for instance in instances:
            session.g_changed_track_info[instance.class_.__name__].add(
                instance.identity
            )


@event.listens_for(Session, "after_commit")
def after_commit(session):
    if not hasattr(session, "g_changed_track_info"):
        return

    for model_name, primary_keys in session.g_changed_track_info.items():
        signal(model_name).send(primary_keys)
    delattr(session, "g_changed_track_info")


async_engine = create_async_engine(
    DB_DSN.replace("psycopg2", "asyncpg"),
    json_serializer=lambda obj: orjson.dumps(obj).decode(),
    json_deserializer=lambda obj: orjson.loads(obj),
    poolclass=NullPool,
)

_session_factory = sessionmaker(
    async_engine, expire_on_commit=False, class_=_AsyncSession
)


def _hooked_session_maker():
    async_session = _session_factory()

    @event.listens_for(async_session.sync_session, "after_flush")
    def _after_flush(session, flush_context: UOWTransaction):
        if not hasattr(session, "g_changed_track_info"):
            session.g_changed_track_info = collections.defaultdict(set)

        for instances in flush_context.mappers.values():
            for instance in instances:
                session.g_changed_track_info[instance.class_.__name__].add(
                    instance.identity
                )

    @event.listens_for(async_session.sync_session, "after_commit")
    def _after_commit(session):
        if not hasattr(session, "g_changed_track_info"):
            return

        for model_name, primary_keys in session.g_changed_track_info.items():
            signal(model_name).send(primary_keys)
        delattr(session, "g_changed_track_info")

    return async_session


AsyncSession = async_scoped_session(
    _hooked_session_maker,
    scopefunc=asyncio.current_task,
)


def session_scope(fn):
    """Defines session top level life time, session will be closed after scope ends."""

    if inspect.iscoroutinefunction(fn):

        @functools.wraps(fn)
        async def wrapper_decorator(*args, **kwargs):
            async with AsyncSession():
                return await fn(*args, **kwargs)

    else:

        @functools.wraps(fn)
        def wrapper_decorator(*args, **kwargs):
            with Session():
                return fn(*args, **kwargs)

    return wrapper_decorator


def commit_scope(fn):
    """Defines transaction top level life time, force begin /close transaction."""

    if inspect.iscoroutinefunction(fn):

        @functools.wraps(fn)
        async def wrapper_decorator(*args, **kwargs):
            session = AsyncSession()
            try:
                res = await fn(*args, **kwargs)
                await session.commit()
                return res

            except Exception:
                await session.rollback()
                raise

    else:

        @functools.wraps(fn)
        def wrapper_decorator(*args, **kwargs):
            session = Session()
            try:
                res = fn(*args, **kwargs)
                session.commit()
                return res
            except Exception:
                session.rollback()
                raise

    return wrapper_decorator
