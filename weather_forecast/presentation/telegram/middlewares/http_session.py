from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiohttp import ClientSession

from weather_forecast.infrastructure.services.weather import WeatherServiceImpl


class HttpSessionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        async with ClientSession() as session:
            data["http_session"] = session
            return await handler(event, data)


class WeatherServiceMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        data["weather_service"] = WeatherServiceImpl(
            data["http_session"], data["owm_token"]
        )
        return await handler(event, data)
