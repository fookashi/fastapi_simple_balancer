from typing import Protocol
from abc import abstractmethod
from domain.entity.config import CDNConfig


class CDNConfigRepositoryGateway(Protocol):
    @abstractmethod
    async def get_one(self, config_id: int | None = None) -> CDNConfig: ...

    @abstractmethod
    async def update_one(self, config: CDNConfig) -> CDNConfig: ...
