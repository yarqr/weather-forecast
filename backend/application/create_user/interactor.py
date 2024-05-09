from backend.application.common.interactor import Interactor
from backend.application.common.repositories.user import UserRepository
from backend.application.common.unit_of_work import UnitOfWork
from backend.domain.entities.user import User


class CreateUser(Interactor[User, None]):
    def __init__(self, user_repo: UserRepository, uow: UnitOfWork) -> None:
        self.user_repo = user_repo
        self.uow = uow

    async def __call__(self, user: User) -> None:
        if await self.user_repo.exists_with_tg_id(user.tg_id) is False:
            await self.user_repo.create(user)
            await self.uow.commit()
