from dataclasses import dataclass

from weather_forecast.application.common.interactor import Interactor
from weather_forecast.application.common.repositories.user import UserRepository
from weather_forecast.application.common.unit_of_work import UnitOfWork


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
