from application.dto.request import InBalanceRequest, OutBalanceRequest
from application.protocols.request_counter import RequestCounterGateway
from application.protocols.request_cache import RequestCacheGateway
from application.protocols.config_repo import CDNConfigRepositoryGateway
from application.actions.url_transform import create_target_url


class BalanceRequestInteractor:
    def __init__(
        self,
        request_counter: RequestCounterGateway,
        request_cache: RequestCacheGateway,
        config_repo: CDNConfigRepositoryGateway,
    ):
        self._request_counter = request_counter
        self._request_cache = request_cache
        self._config_repo = config_repo

    async def __call__(self, request_data: InBalanceRequest) -> OutBalanceRequest:
        request_count = await self._request_counter.increase_request_count()
        cdn_config = await self._config_repo.get_one()
        if request_count % cdn_config.distribution_rate == 0:
            return OutBalanceRequest(target_url=request_data.origin_url)

        cached_url = await self._request_cache.get_request_cache(request_data.origin_url)
        if cached_url:
            return OutBalanceRequest(target_url=cached_url)
        target_url = create_target_url(request_data.origin_url, cdn_config)
        await self._request_cache.set_request_cache(request_data.origin_url, target_url)

        return OutBalanceRequest(target_url=target_url)
