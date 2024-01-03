import asyncio
from pathlib import Path

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ChatType
from aiogram.filters import CommandStart
from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, setup_dialogs
from aiohttp import ClientSession
from fluent.runtime import FluentLocalization, FluentResourceLoader
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from weather_forecast.application.common.repositories.user import UserRepository
from weather_forecast.application.create_user.interactor import CreateUser
from weather_forecast.domain.entities.user import User
from weather_forecast.infrastructure.config import load_telegram_config
from weather_forecast.infrastructure.services.weather import WeatherServiceImpl
from weather_forecast.presentation.telegram.create_user.dialog import create_user
from weather_forecast.presentation.telegram.middlewares.database_session import (
    DatabaseSessionMiddleware,
    UserRepoMiddleware,
)
from weather_forecast.presentation.telegram.middlewares.i18n import I18nMiddleware
from weather_forecast.presentation.telegram.states import CreateUserSG
from weather_forecast.presentation.telegram.update_user_city.dialog import (
    update_user_city,
)


async def cmd_start(
    msg: Message, dialog_manager: DialogManager, user_repo: UserRepository
) -> None:
    if msg.from_user:
        await CreateUser(user_repo)(User(id=msg.from_user.id))
        state = CreateUserSG.choose_language
        if await user_repo.get_language(User(id=msg.from_user.id)):
            state = CreateUserSG.main
        await dialog_manager.start(state, mode=StartMode.RESET_STACK)


async def main() -> None:
    config = load_telegram_config(Path(__file__).parents[3] / "config.toml")

    engine = create_async_engine(config.database.make_dsn())

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

    for middleware in [
        DatabaseSessionMiddleware(async_sessionmaker(engine)),
        UserRepoMiddleware(),
        I18nMiddleware(dp["l10ns"]),
    ]:
        dp.message.middleware(middleware)
        dp.callback_query.middleware(middleware)

    dp.include_routers(create_user, update_user_city)
    setup_dialogs(dp)

    try:
        await dp.start_polling(bot)
    finally:
        await engine.dispose()
        await session.close()


if __name__ == "__main__":
    asyncio.run(main())
