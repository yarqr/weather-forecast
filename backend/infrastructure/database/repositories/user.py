from typing import Optional, cast

from sqlalchemy import exists, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.application.common.repositories.user import UserRepository
from backend.domain.entities.user import User
from backend.infrastructure.database.models import UserModel


class UserRepositoryImpl(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User) -> None:
        self.session.add(UserModel.from_entity(user))

    async def exists_with_tg_id(self, tg_id: int) -> bool:
        return cast(
            bool,
            await self.session.scalar(
                exists().where(UserModel.tg_id == tg_id).select()
            ),
        )

    async def get_by_tg_id(self, tg_id: int) -> Optional[User]:
        res = await self.session.scalar(
            select(UserModel).where(UserModel.tg_id == tg_id)
        )
        if res is None:
            return None
        return res.to_entity()

    async def update_city_by_tg_id(self, tg_id: int, city: str) -> None:
        await self.session.execute(
            update(UserModel).values(city=city).where(UserModel.tg_id == tg_id)
        )

    async def update_language_by_tg_id(self, tg_id: int, language: str) -> None:
        await self.session.execute(
            update(UserModel).values(language=language).where(UserModel.tg_id == tg_id)
        )
