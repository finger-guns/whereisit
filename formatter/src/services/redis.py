from redis.asyncio.client import Redis, PubSub
from logging import info


async def connection(host: str = 'localhost', port: int = 6379) -> Redis:
    info(f'connecting to {host}:{port}')
    return Redis(host=host, port=port)


async def pubsub(client: Redis) -> PubSub:
    info(f'creating pubsub client')
    return PubSub(connection_pool=client.connection_pool) # type: ignore


async def subscribe(pubsub: PubSub, channel_name: str = 'to-format') -> PubSub:
    info(f'subscribing to {channel_name}')
    await pubsub.subscribe(channel_name)
    return pubsub
