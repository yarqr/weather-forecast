from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID, uuid4

from backend.domain.common.entity import Entity


@dataclass(kw_only=True)
class User(Entity):
    tg_id: int
    language: str
    city: Optional[str] = None
    id: UUID = field(default_factory=uuid4)
