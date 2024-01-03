from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Back, Next, Select, Start, SwitchTo
from aiogram_dialog.widgets.text import Format

from weather_forecast.application.update_user_language.interactor import (
    UpdateUserLanguage,
)
from weather_forecast.domain.entities.user import User
from weather_forecast.presentation.telegram.states import CreateUserSG, UpdateUserCitySG
from weather_forecast.presentation.telegram.widgets.i18n_format import (
    I18N_FORMAT_KEY,
    I18nFormat,
)


async def update_user_language(
    cq: CallbackQuery, _: Select[str], manager: DialogManager, language: str
) -> None:
    if cq.from_user:
        await UpdateUserLanguage(manager.middleware_data["user_repo"])(
            User(id=cq.from_user.id, language=language)
        )
    manager.middleware_data[I18N_FORMAT_KEY] = manager.middleware_data["l10ns"][
        language
    ].format_value
    await manager.next()


create_user = Dialog(
    Window(
        I18nFormat("choose-language"),
        Select(
            Format("{item}"),
            "choose_lang",
            lambda x: x.partition(" ")[-1].lower(),
            ["🇷🇺 RU", "🏴󠁧󠁢󠁥󠁮󠁧󠁿 EN"],
            on_click=update_user_language,
        ),
        state=CreateUserSG.choose_language,
    ),
    Window(
        I18nFormat("main"),
        Start(
            I18nFormat("btn-input-city"),
            "start_update_user_city",
            UpdateUserCitySG.input_city,
        ),
        Next(I18nFormat("btn-settings")),
        state=CreateUserSG.main,
    ),
    Window(
        I18nFormat("settings"),
        SwitchTo(
            I18nFormat("btn-edit-language"),
            "to_choose_language",
            CreateUserSG.choose_language,
        ),
        Back(I18nFormat("btn-back")),
        state=CreateUserSG.settings,
    ),
)
