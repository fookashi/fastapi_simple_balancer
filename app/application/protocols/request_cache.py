from abc import abstractmethod
from typing import Protocol


class RequestCacheGateway(Protocol):
    @abstractmethod
    async def get_request_cache(self, origin_url: str) -> str | None: ...

    @abstractmethod
    async def set_request_cache(self, origin_url: str, target_url: str) -> None: ...
