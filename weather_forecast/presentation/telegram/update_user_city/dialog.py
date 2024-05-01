from typing import Any, Optional

from aiogram import F
from aiogram.types import Message
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.input import ManagedTextInput, TextInput
from aiogram_dialog.widgets.kbd import Cancel, Next

from weather_forecast.application.common.repositories.user import UserRepository
from weather_forecast.application.common.services.weather import WeatherService
from weather_forecast.application.update_user_city.interactor import UpdateUserCity
from weather_forecast.domain.entities.user import User
from weather_forecast.domain.entities.weather import Weather
from weather_forecast.presentation.telegram.states import UpdateUserCitySG
from weather_forecast.presentation.telegram.widgets.i18n_format import I18nFormat


async def go_next(
    msg: Message, _: ManagedTextInput[str], manager: DialogManager, data: str
) -> None:
    if msg.from_user and data:
        await UpdateUserCity(manager.middleware_data["user_repo"])(
            User(
                msg.from_user.id,
                city=data,
            )
        )
    await manager.next()


async def city_getter(
    dialog_manager: DialogManager, user_repo: UserRepository, **_: Any
) -> dict[str, Optional[str]]:
    if dialog_manager.event.from_user:
        return {
            "city": await user_repo.get_city(User(dialog_manager.event.from_user.id))
        }
    return {}


async def weather_getter(
    dialog_manager: DialogManager,
    weather_service: WeatherService,
    user_repo: UserRepository,
    **_: Any,
) -> dict[str, Weather]:
    input_widget = dialog_manager.find("input_city")
    if dialog_manager.event.from_user and input_widget:
        city = input_widget.get_value()
        return {
            "weather": await weather_service.get_by_user(
                User(
                    dialog_manager.event.from_user.id,
                    city=city
                    if city != "None"
                    else await user_repo.get_city(
                        User(dialog_manager.event.from_user.id)
                    ),
                )
            )
        }
    return {}


update_user_city = Dialog(
    Window(
        TextInput("input_city", on_success=go_next, filter=F.text.isalpha()),
        I18nFormat("input-city"),
        Next(I18nFormat("btn-last-city"), when="city"),
        Cancel(I18nFormat("btn-back")),
        getter=city_getter,
        state=UpdateUserCitySG.input_city,
    ),
    Window(
        I18nFormat("weather-info"),
        Cancel(I18nFormat("btn-to-main-menu")),
        getter=weather_getter,
        state=UpdateUserCitySG.result,
    ),
)
