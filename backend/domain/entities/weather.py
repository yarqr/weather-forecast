from dataclasses import dataclass

from backend.domain.common.entity import Entity


@dataclass(kw_only=True)
class Weather(Entity):
    temperature: float
