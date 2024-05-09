from dataclasses import dataclass

from backend.application.common.interactor import Interactor
from backend.application.common.repositories.user import UserRepository
from backend.application.common.unit_of_work import UnitOfWork


@dataclass(kw_only=True)
class UpdateUserCityInput:
    tg_id: int
    city: str


class UpdateUserCity(Interactor[UpdateUserCityInput, None]):
    def __init__(self, user_repo: UserRepository, uow: UnitOfWork) -> None:
        self.user_repo = user_repo
        self.uow = uow

    async def __call__(self, data: UpdateUserCityInput) -> None:
        await self.user_repo.update_city_by_tg_id(data.tg_id, data.city)
        await self.uow.commit()
