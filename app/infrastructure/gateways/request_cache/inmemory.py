from pydantic import HttpUrl
from application.protocols.request_cache import RequestCacheGateway


class InmemoryRequestCache(RequestCacheGateway):
    def __init__(self) -> None:
        self._cache: dict[HttpUrl, HttpUrl] = {}

    async def get_request_cache(self, origin_url: HttpUrl) -> HttpUrl | None:
        return self._cache.get(origin_url)

    async def set_request_cache(self, origin_url: HttpUrl, target_url: HttpUrl) -> None:
        self._cache[origin_url] = target_url
