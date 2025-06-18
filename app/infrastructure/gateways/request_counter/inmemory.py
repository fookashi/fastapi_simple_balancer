from itertools import count

from application.protocols.request_counter import RequestCounterGateway


class InmemoryRequestCounter(RequestCounterGateway):
    def __init__(self) -> None:
        self._counter = count(start=1)

    async def increase_request_count(self) -> int:
        return next(self._counter)
