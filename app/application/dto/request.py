from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class InBalanceRequest:
    origin_url: str


@dataclass(frozen=True, slots=True, kw_only=True)
class OutBalanceRequest:
    target_url: str
