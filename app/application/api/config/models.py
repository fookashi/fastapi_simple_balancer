from pydantic import BaseModel, model_validator


class CDNConfigUpdateRequest(BaseModel):
    id: int
    cdn_host: str | None = None
    distribution_rate: int | None = None

    @model_validator(mode="after")
    def at_least_one_field(cls, values):
        if values.cdn_host is None and values.distribution_rate is None:
            raise ValueError("Хотя бы одно поле должно быть указано для обновления")
        return values
