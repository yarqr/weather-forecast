from abc import ABC, abstractmethod

from weather_forecast.domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> None:
        ...

    @abstractmethod
    async def get_city(self, user: User) -> None:
        ...

    @abstractmethod
    async def get_language(self, user: User) -> None:
        ...

    @abstractmethod
    async def edit_city(self, user: User) -> None:
        ...

    @abstractmethod
    async def edit_language(self, user: User) -> None:
        ...
