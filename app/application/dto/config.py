from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class InUpdateCDNConfig:
    id: int
    cdn_host: str | None = None
    distribution_rate: int | None = None
