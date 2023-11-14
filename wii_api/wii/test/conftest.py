import asyncio
from typing import AsyncIterator
from unittest.mock import AsyncMock, MagicMock

import pytest
import redis.asyncio as aioredis
from helpers.sqlalchemy_utils import create_database, database_exists, drop_database
from httpx import AsyncClient
from pytest_asyncio import fixture
from sqlalchemy import Connection, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from api.config import get_settings
from api.main import app
from api.modules._shared import Base
from api.modules.jobs.ddl.enum import JOB_REQUEST_STATUS_ENUM
from api.utils import get_async_db, redis
from api.utils.database import get_url
from api.utils.logger import logger

settings = get_settings()


@pytest.fixture(scope="function")
def mock_aioredis_client():
    mock_client = AsyncMock(spec=aioredis.Redis)

    mock_client.get = AsyncMock(return_value=b"value")
    mock_client.set = AsyncMock(return_value=True)
    mock_client.publish = AsyncMock(return_value=1)

    return mock_client


@pytest.fixture
async def redis_client(mock_aioredis_client):
    return mock_aioredis_client


@pytest.fixture(scope="session")
def event_loop(request):
    """
    Prevents error:
    ScopeMismatch: You tried to access the function scoped
    fixture event_loop with a session scoped request object
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


def execute(conn: Connection) -> None:
    conn.execute(text(JOB_REQUEST_STATUS_ENUM["create"]))


@fixture(scope="session")
async def async_engine(worker_id):
    """
    Creates a new database for each worker.
    :param worker_id: pytest-asyncio worker id.
    :return: AsyncEngine
    """
    logger().debug(f"Setting up database for worker {worker_id}...")
    async_engine = create_async_engine(
        get_url("asyncpg", f"pytest{worker_id}"),
        echo=False,
    )
    if not await database_exists(async_engine.url):
        await create_database(async_engine.url)
    else:
        await drop_database(async_engine.url)
        await create_database(async_engine.url)

    async with async_engine.begin() as connection:
        await connection.run_sync(execute)
        await connection.run_sync(Base.metadata.create_all)
    return async_engine


@pytest.fixture(scope="session")
def async_db_sessionmaker(async_engine):
    """
    Creates a new session for each worker.
    :param async_engine: AsyncEngine
    :return: AsyncSession
    """
    return async_sessionmaker(
        bind=async_engine,
        autoflush=False,
        expire_on_commit=False,
    )


@fixture(scope="function")
async def session(async_db_sessionmaker) -> AsyncIterator[AsyncSession]:
    """
    Creates a new session for each test.
    :param async_db_sessionmaker: AsyncSession
    :return: AsyncIterator[AsyncSession]
    """
    async with async_db_sessionmaker() as session:
        yield session


@fixture(scope="function")
async def async_client(session) -> AsyncIterator[AsyncClient]:
    """
    Creates a new client for each test.
    :param session: AsyncSession
    :return: AsyncIterator[AsyncClient]
    """

    async def get_aioredis_client_override():
        return redis_client

    async def override_async_db():
        return session

    async with AsyncClient(app=app, base_url="http://test") as tClient:
        # Force all endpoints to use our test db session.
        app.dependency_overrides[get_async_db] = override_async_db
        app.dependency_overrides[redis] = get_aioredis_client_override

        yield tClient
