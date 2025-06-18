from typing import AsyncIterable
from dishka import Provider, Scope, provide, AsyncContainer, make_async_container
import asyncpg
from redis.asyncio import Redis

from application.common.settings import AppSettings
from application.commands.request import BalanceRequestInteractor
from application.commands.config import GetConfigInteractor, UpdateConfigInteractor
from application.protocols.config_repo import CDNConfigRepositoryGateway
from application.protocols.request_cache import RequestCacheGateway
from application.protocols.request_counter import RequestCounterGateway
from infrastructure.gateways.repositories.config.sql import SQLCDNConfigRepository
from infrastructure.gateways.request_cache.redis import RedisRequestCacheGateway
from infrastructure.gateways.request_counter.redis import RedisRequestCounter


class ConfigProvider(Provider):
    scope = Scope.APP

    @provide(scope=Scope.APP)
    def app_settings(self) -> AppSettings:
        return AppSettings()


class ConnectionProvider(Provider):
    @provide(scope=Scope.APP)
    async def pg_pool(self, config: AppSettings) -> AsyncIterable[asyncpg.Pool]:
        pool = await asyncpg.create_pool(config.pg_dsn, max_size=config.pg_pool_size)
        try:
            yield pool
        finally:
            await pool.close()

    @provide(scope=Scope.REQUEST)
    async def pg_connection(self, pg_pool: asyncpg.Pool) -> AsyncIterable[asyncpg.Connection]:
        async with pg_pool.acquire() as conn:
            yield conn


class RedisProvider(Provider):
    scope = Scope.APP

    @provide(scope=Scope.APP)
    async def redis_client(self, config: AppSettings) -> AsyncIterable[Redis]:
        redis_client = Redis.from_url(
            str(config.redis_dsn),
            decode_responses=True,
            encoding="utf-8",
        )
        try:
            yield redis_client
        finally:
            await redis_client.close()


class InfrastructureProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def config_repo(self, pg_connection: asyncpg.Connection) -> CDNConfigRepositoryGateway:
        return SQLCDNConfigRepository(pg_connection)

    @provide(scope=Scope.REQUEST)
    async def request_counter(self, redis_client: Redis) -> RequestCounterGateway:
        return RedisRequestCounter(redis_client)

    @provide(scope=Scope.REQUEST)
    async def request_cache(self, redis_client: Redis) -> RequestCacheGateway:
        return RedisRequestCacheGateway(redis_client)


class CommandsProvider(Provider):
    scope = Scope.REQUEST

    balance_request = provide(BalanceRequestInteractor)
    get_config = provide(GetConfigInteractor)
    update_config = provide(UpdateConfigInteractor)


def create_container() -> AsyncContainer:
    return make_async_container(
        ConfigProvider(),
        RedisProvider(),
        ConnectionProvider(),
        InfrastructureProvider(),
        CommandsProvider(),
    )
