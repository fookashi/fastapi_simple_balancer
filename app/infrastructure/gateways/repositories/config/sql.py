from datetime import datetime, UTC

import asyncpg


from application.protocols.config_repo import CDNConfigRepositoryGateway
from domain.entity.config import CDNConfig
from infrastructure.exceptions.repository import NotFoundError, ConfigIdNotSpecifiedError


class SQLCDNConfigRepository(CDNConfigRepositoryGateway):
    def __init__(self, connection: asyncpg.Connection):
        self._connection = connection

    async def get_one(self, config_id: int | None = None) -> CDNConfig:
        if config_id is not None:
            row = await self._connection.fetchrow(
                """
                SELECT id, cdn_host, distribution_rate, created_at, updated_at
                FROM cdn_config WHERE id = $1 LIMIT 1
                """,
                config_id,
            )
        else:
            row = await self._connection.fetchrow(
                """
                SELECT id, cdn_host, distribution_rate, created_at, updated_at
                FROM cdn_config LIMIT 1
                """
            )
        if not row:
            raise NotFoundError("Не найден ни один CDN конфиг")

        return CDNConfig(
            id=row["id"],
            cdn_host=row["cdn_host"],
            distribution_rate=row["distribution_rate"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    async def update_one(self, config: CDNConfig) -> CDNConfig:
        if config.id is None:
            raise ConfigIdNotSpecifiedError("Для обновления конфигурации должен быть указан id")

        updated_at = datetime.now(UTC)
        await self._connection.execute(
            """
            UPDATE cdn_config
            SET cdn_host = $1, distribution_rate = $2, updated_at = $3
            WHERE id = $4
            """,
            config.cdn_host,
            config.distribution_rate,
            updated_at,
            config.id,
        )

        return CDNConfig(
            id=config.id,
            cdn_host=config.cdn_host,
            distribution_rate=config.distribution_rate,
            created_at=config.created_at,
            updated_at=updated_at,
        )
