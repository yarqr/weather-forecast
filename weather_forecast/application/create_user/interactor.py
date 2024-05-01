from weather_forecast.application.common.interactor import Interactor
from weather_forecast.application.common.repositories.user import UserRepository
from weather_forecast.application.common.unit_of_work import UnitOfWork
from weather_forecast.domain.entities.user import User


class CreateUser(Interactor[User, None]):
    def __init__(self, user_repo: UserRepository, uow: UnitOfWork) -> None:
        self.user_repo = user_repo
        self.uow = uow

    async def __call__(self, user: User) -> None:
        if await self.user_repo.exists_with_tg_id(user.tg_id) is False:
            await self.user_repo.create(user)
            await self.uow.commit()
