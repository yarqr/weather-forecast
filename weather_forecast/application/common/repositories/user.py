from abc import ABC, abstractmethod
from typing import Optional

from weather_forecast.domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> None: ...

    @abstractmethod
    async def get_by_tg_id(self, tg_id: int) -> Optional[User]: ...

    @abstractmethod
    async def update_city_by_tg_id(self, tg_id: int, city: str) -> None: ...

    @abstractmethod
    async def update_language_by_tg_id(self, tg_id: int, language: str) -> None: ...
