from abc import ABC, abstractmethod
from typing import Optional

from weather_forecast.domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def add(self, user: User) -> None: ...

    @abstractmethod
    async def get_city(self, user: User) -> Optional[str]: ...

    @abstractmethod
    async def get_language(self, user: User) -> Optional[str]: ...

    @abstractmethod
    async def edit_city(self, user: User) -> None: ...

    @abstractmethod
    async def edit_language(self, user: User) -> None: ...
