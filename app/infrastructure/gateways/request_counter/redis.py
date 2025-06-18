from redis.asyncio import Redis
from application.protocols.request_counter import RequestCounterGateway


class RedisRequestCounter(RequestCounterGateway):
    REQUEST_COUNT_KEY = "application:request_count"

    def __init__(self, redis_client: Redis):
        self._redis_client = redis_client

    async def increase_request_count(self) -> int:
        return await self._redis_client.incr(self.REQUEST_COUNT_KEY)
