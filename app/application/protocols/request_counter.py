from abc import abstractmethod
from typing import Protocol


class RequestCounterGateway(Protocol):
    @abstractmethod
    async def increase_request_count(self) -> int: ...
