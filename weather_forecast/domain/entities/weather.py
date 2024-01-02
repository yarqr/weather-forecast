from dataclasses import dataclass

from weather_forecast.domain.common.entity import Entity


@dataclass
class Weather(Entity):
    temperature: float
