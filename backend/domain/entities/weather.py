from dataclasses import dataclass

from backend.domain.common.entity import Entity


@dataclass(kw_only=True)
class Weather(Entity):
    temperature: float
    feels_like: float
    humidity: int
    wind_speed: float
    description: str
    country: str
