from uuid import UUID

from redis.asyncio import Redis


async def publish(
    redis: Redis,
    channel: str = "test",
    message: str = "Hello World",
) -> int:
    """
    Publis message to a queue, in this usecase we assume that the job_id is apart of the message.
    """
    return await redis.publish(channel, message)


async def get(
    redis: Redis,
    job_id: UUID,
) -> bytes:
    return await redis.get(f"job_request:{job_id}")
