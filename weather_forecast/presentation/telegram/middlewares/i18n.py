from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from fluent.runtime import FluentLocalization

from weather_forecast.application.common.repositories.user import UserRepository
from weather_forecast.domain.entities.user import User
from weather_forecast.presentation.telegram.widgets.i18n_format import I18N_FORMAT_KEY


class I18nMiddleware(BaseMiddleware):
    def __init__(
        self, l10ns: dict[str, FluentLocalization], default_locale: str = "en"
    ):
        super().__init__()
        self.l10ns = l10ns
        self.default_locale = default_locale

    async def _get_language(self, data: dict[str, Any], event: TelegramObject) -> str:
        user_repo: UserRepository = data["user_repo"]
        language = self.default_locale
        if hasattr(event, "from_user") and event.from_user:
            language = await user_repo.get_language(User(id=event.from_user.id)) or ""
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
