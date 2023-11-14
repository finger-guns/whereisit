from typing import AsyncGenerator
from redis.asyncio import Redis

from api.config import get_settings

settings = get_settings()


async def redis() -> AsyncGenerator[Redis, None]:
    _redis = await Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        decode_responses=True,
    )

    await _redis.ping()

    try:
        yield _redis
    finally:
        await _redis.close()
