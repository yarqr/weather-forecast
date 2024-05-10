import asyncio
from pathlib import Path
from typing import cast

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ChatType
from aiogram.filters import CommandStart
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, setup_dialogs
from aiohttp import ClientSession
from dishka import FromDishka, make_async_container
from dishka.integrations.aiogram import inject, setup_dishka
from fluent.runtime import FluentLocalization, FluentResourceLoader

from backend.application.common.repositories.user import UserRepository
from backend.infrastructure.config import load_telegram_config
from backend.infrastructure.services.weather import WeatherServiceImpl
from backend.presentation.telegram.create_user.dialog import create_user
from backend.presentation.telegram.di.providers import (
    InteractorProvider,
    DatabaseProvider,
)
from backend.presentation.telegram.middlewares.i18n import I18nMiddleware
from backend.presentation.telegram.states import CreateUserSG
from backend.presentation.telegram.view_weather.dialog import (
    view_weather,
)
from aiogram.types import User as AiogramUser


@inject  # type: ignore[misc]
async def cmd_start(
    msg: Message, dialog_manager: DialogManager, user_repo: FromDishka[UserRepository]
) -> None:
    user = await user_repo.get_by_tg_id(cast(AiogramUser, msg.from_user).id)
    state = CreateUserSG.choose_language
    if user is not None:
        state = CreateUserSG.main
    await dialog_manager.start(state, mode=StartMode.RESET_STACK)


async def main() -> None:
    config = load_telegram_config(Path(__file__).parents[3] / "config.toml")

    session = ClientSession()

    bot = Bot(config.bot.token)
    storage = RedisStorage.from_url(
        config.redis.make_dsn(), key_builder=DefaultKeyBuilder(with_destiny=True)
    )
    dp = Dispatcher(storage=storage, events_isolation=storage.create_isolation())
    dp["weather_service"] = WeatherServiceImpl(session, config.owm_token)

    dp.message.register(cmd_start, CommandStart())
    dp.message.filter(F.chat.type == ChatType.PRIVATE)

    fluent_loader = FluentResourceLoader(
        str(Path(__file__).parents[3] / "assets" / "translations" / "{locale}")
    )
    dp["l10ns"] = {
        locale: FluentLocalization(
            [locale, "en"],
            ["messages.ftl", "buttons.ftl"],
            fluent_loader,
        )
        for locale in ["ru", "en"]
    }

    for middleware in [I18nMiddleware(dp["l10ns"])]:
        dp.message.middleware(middleware)
        dp.callback_query.middleware(middleware)

    dp.include_routers(create_user(), view_weather())
    setup_dialogs(dp)

    setup_dishka(
        make_async_container(DatabaseProvider(config.database), InteractorProvider()),
        dp,
    )

    try:
        await dp.start_polling(bot)
    finally:
        await session.close()


if __name__ == "__main__":
    asyncio.run(main())
