from dataclasses import asdict

from fastapi import APIRouter, status, HTTPException
from fastapi.responses import ORJSONResponse
from dishka.integrations.fastapi import inject
from dishka import FromDishka

from application.api.config.models import CDNConfigUpdateRequest
from application.dto.config import InUpdateCDNConfig
from application.commands.config import GetConfigInteractor, UpdateConfigInteractor
from domain.entity.config import CDNConfig
from infrastructure.exceptions.repository import NotFoundError

router = APIRouter(tags=["CDN Config Management"])


@router.get("/config", response_model=CDNConfig)
@inject
async def get_config(
    get_config: FromDishka[GetConfigInteractor],
    id: int | None = None,
) -> ORJSONResponse:
    try:
        config = await get_config(id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return ORJSONResponse(content=asdict(config), status_code=status.HTTP_200_OK)


@router.patch("/config")
@inject
async def update_config(
    data: CDNConfigUpdateRequest,
    update_config: FromDishka[UpdateConfigInteractor],
) -> ORJSONResponse:
    try:
        config = await update_config(
            data=InUpdateCDNConfig(
                id=data.id,
                cdn_host=data.cdn_host,
                distribution_rate=data.distribution_rate,
            )
        )
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return ORJSONResponse(content=asdict(config), status_code=status.HTTP_200_OK)
