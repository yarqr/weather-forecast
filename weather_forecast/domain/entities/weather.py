from dataclasses import dataclass

from weather_forecast.domain.common.entity import Entity


@dataclass(kw_only=True)
class Weather(Entity):
    temperature: float
