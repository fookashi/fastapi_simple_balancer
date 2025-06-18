from application.protocols.request_cache import RequestCacheGateway

from redis.asyncio import Redis


class RedisRequestCacheGateway(RequestCacheGateway):
    def __init__(self, redis_client: Redis):
        self._redis_client = redis_client

    async def get_request_cache(self, origin_url: str) -> str | None:
        cached_url = await self._redis_client.get(origin_url)
        return cached_url

    async def set_request_cache(self, origin_url: str, target_url: str) -> None:
        await self._redis_client.set(origin_url, target_url)
