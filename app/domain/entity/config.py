from dataclasses import dataclass, field
from datetime import datetime, UTC


@dataclass(slots=True)
class CDNConfig:
    id: int | None
    cdn_host: str
    distribution_rate: int
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime | None = None

    @classmethod
    def create(cls, cdn_host: str, distribution_rate: int) -> "CDNConfig":
        return cls(
            id=None,
            cdn_host=cdn_host,
            distribution_rate=distribution_rate,
        )
