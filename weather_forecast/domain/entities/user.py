from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID, uuid4

from weather_forecast.domain.common.entity import Entity


@dataclass(kw_only=True)
class User(Entity):
    tg_id: int
    language: Optional[str]
    city: Optional[str]
    id: UUID = field(default_factory=uuid4)
