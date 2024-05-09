from dataclasses import dataclass

from backend.application.common.interactor import Interactor
from backend.application.common.repositories.user import UserRepository
from backend.application.common.unit_of_work import UnitOfWork


@dataclass(kw_only=True)
class UpdateUserLanguageInput:
    tg_id: int
    language: str


class UpdateUserLanguage(Interactor[UpdateUserLanguageInput, None]):
    def __init__(self, user_repo: UserRepository, uow: UnitOfWork) -> None:
        self.user_repo = user_repo
        self.uow = uow

    async def __call__(self, data: UpdateUserLanguageInput) -> None:
        await self.user_repo.update_language_by_tg_id(data.tg_id, data.language)
        await self.uow.commit()
