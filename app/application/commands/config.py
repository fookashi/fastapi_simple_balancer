from application.protocols.config_repo import CDNConfigRepositoryGateway
from domain.entity.config import CDNConfig

from application.dto.config import InUpdateCDNConfig


class BaseConfigInteractor:
    def __init__(self, config_repo: CDNConfigRepositoryGateway):
        self._config_repo = config_repo


class GetConfigInteractor(BaseConfigInteractor):
    async def __call__(self, config_id: int | None = None) -> CDNConfig:
        return await self._config_repo.get_one(config_id)


class UpdateConfigInteractor(BaseConfigInteractor):
    async def __call__(self, data: InUpdateCDNConfig) -> CDNConfig:
        cdn_config = await self._config_repo.get_one(data.id)
        if data.cdn_host is not None:
            cdn_config.cdn_host = data.cdn_host
        if data.distribution_rate is not None:
            cdn_config.distribution_rate = data.distribution_rate
        return await self._config_repo.update_one(cdn_config)
