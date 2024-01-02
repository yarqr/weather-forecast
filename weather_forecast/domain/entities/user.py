from dataclasses import dataclass
from typing import Optional

from weather_forecast.domain.common.entity import Entity


@dataclass
class User(Entity):
    id: int
    language: Optional[str] = None
    city: Optional[str] = None
