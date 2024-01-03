from typing import Optional

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from weather_forecast.application.common.repositories.user import UserRepository
from weather_forecast.domain.entities.user import User
from weather_forecast.infrastructure.database import models


class UserRepositoryImpl(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit(self) -> None:
        await self.session.commit()

    async def add(self, user: User) -> None:
        user_exists = await self.session.execute(
            exists().where(models.User.id == user.id).select()
        )
        if not user_exists.scalar():
            self.session.add(models.User(id=user.id))

    async def get_city(self, user: User) -> Optional[str]:
        city = await self.session.execute(
            select(models.User.city).where(models.User.id == user.id)
        )
        return city.scalar()

    async def get_language(self, user: User) -> Optional[str]:
        language = await self.session.execute(
            select(models.User.language).where(models.User.id == user.id)
        )
        return language.scalar()

    async def edit_city(self, user: User) -> None:
        await self.session.merge(models.User(id=user.id, city=user.city))

    async def edit_language(self, user: User) -> None:
        await self.session.merge(models.User(id=user.id, language=user.language))
