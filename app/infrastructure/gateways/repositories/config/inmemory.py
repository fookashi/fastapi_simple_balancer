from domain.entity.config import CDNConfig
from application.protocols.config_repo import CDNConfigRepositoryGateway


class InmemoryCDNConfigRepository(CDNConfigRepositoryGateway):
    async def get_one(self, config_id: int | None = None) -> CDNConfig:
        return CDNConfig.create("localhost", 10)

    async def update_one(self, config: CDNConfig) -> CDNConfig:
        return config
