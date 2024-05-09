from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from dishka.integrations.aiogram import CONTAINER_NAME
from fluent.runtime import FluentLocalization

from backend.application.common.repositories.user import UserRepository
from backend.presentation.telegram.widgets.i18n_format import I18N_FORMAT_KEY


class I18nMiddleware(BaseMiddleware):
    def __init__(
        self, l10ns: dict[str, FluentLocalization], default_locale: str = "en"
    ):
        super().__init__()
        self.l10ns = l10ns
        self.default_locale = default_locale

    async def _get_language(self, data: dict[str, Any], event: TelegramObject) -> str:
        user_repo: UserRepository = await data[CONTAINER_NAME].get(UserRepository)
        language = self.default_locale
        if hasattr(event, "from_user") and event.from_user is not None:
            user = await user_repo.get_by_tg_id(event.from_user.id)
            if user is not None:
                language = user.language
        if language not in self.l10ns:
            language = self.default_locale
        return language

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        data[I18N_FORMAT_KEY] = self.l10ns[
            await self._get_language(data, event)
        ].format_value
        return await handler(event, data)
