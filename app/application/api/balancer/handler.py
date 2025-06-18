from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse
from pydantic import HttpUrl

from application.commands.request import BalanceRequestInteractor
from application.dto.request import InBalanceRequest
from application.exceptions.action import InvalidUrlError

router = APIRouter(tags=["Request balancer"])


@router.get("/")
@inject
async def balance_request(
    video: HttpUrl,
    interactor: FromDishka[BalanceRequestInteractor],
) -> RedirectResponse:
    try:
        balanced_request = await interactor(request_data=InBalanceRequest(origin_url=str(video)))
    except InvalidUrlError as e:
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    return RedirectResponse(
        url=balanced_request.target_url,
        status_code=status.HTTP_301_MOVED_PERMANENTLY,
    )
