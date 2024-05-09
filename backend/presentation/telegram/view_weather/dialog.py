from typing import Any, cast

from aiogram import F
from aiogram.types import Message
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.input import ManagedTextInput, TextInput
from aiogram_dialog.widgets.kbd import Cancel, Next
from dishka import FromDishka
from dishka.integrations.aiogram import CONTAINER_NAME

from backend.application.common.repositories.user import UserRepository
from backend.application.common.services.weather import WeatherService
from backend.application.update_user_city.interactor import (
    UpdateUserCity,
    UpdateUserCityInput,
)
from backend.domain.entities.weather import Weather
from backend.presentation.telegram.di.injects import inject_getter
from backend.presentation.telegram.states import UpdateUserCitySG
from backend.presentation.telegram.widgets.i18n_format import I18nFormat

from aiogram.types import User as AiogramUser


async def go_next(
    msg: Message, _: ManagedTextInput[str], manager: DialogManager, city: str
) -> None:
    update_user_city: UpdateUserCity = await manager.middleware_data[
        CONTAINER_NAME
    ].get(UpdateUserCity)
    await update_user_city(
        UpdateUserCityInput(tg_id=cast(AiogramUser, msg.from_user).id, city=city)
    )
    await manager.next()


@inject_getter
async def city_getter(
    dialog_manager: DialogManager, user_repo: FromDishka[UserRepository], **_: Any
) -> dict[str, str]:
    user = await user_repo.get_by_tg_id(
        cast(AiogramUser, dialog_manager.event.from_user).id
    )
    if user is not None and user.city is not None:
        return {"city": user.city}
    return {}


@inject_getter
async def weather_getter(
    dialog_manager: DialogManager,
    weather_service: WeatherService,
    user_repo: FromDishka[UserRepository],
    **_: Any,
) -> dict[str, Weather]:
    city = cast(ManagedTextInput[str], dialog_manager.find("input_city")).get_value()
    if city == "None":
        user = await user_repo.get_by_tg_id(
            cast(AiogramUser, dialog_manager.event.from_user).id
        )
        if user is not None and user.city is not None:
            city = user.city
    return {"weather": await weather_service.get_by_city(city)}


def view_weather() -> Dialog:
    return Dialog(
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
