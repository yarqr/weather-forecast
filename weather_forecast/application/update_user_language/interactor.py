from weather_forecast.application.common.interactor import Interactor
from weather_forecast.application.common.repositories.user import UserRepository
from weather_forecast.domain.entities.user import User


class UpdateUserLanguage(Interactor[User, None]):
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def __call__(self, user: User) -> None:
        await self.user_repo.edit_language(user)
        await self.user_repo.commit()
