from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Back, Next, Select, Start, SwitchTo
from aiogram_dialog.widgets.text import Format
from dishka.integrations.aiogram import CONTAINER_NAME

from backend.application.common.repositories.user import UserRepository
from backend.application.create_user.interactor import CreateUser
from backend.application.update_user_language.interactor import (
    UpdateUserLanguage,
    UpdateUserLanguageInput,
)
from backend.domain.entities.user import User
from backend.presentation.telegram.states import CreateUserSG, UpdateUserCitySG
from backend.presentation.telegram.widgets.i18n_format import (
    I18N_FORMAT_KEY,
    I18nFormat,
)


async def add_user(
    cq: CallbackQuery, _: Select[str], manager: DialogManager, language: str
) -> None:
    user_repo: UserRepository = await manager.middleware_data[CONTAINER_NAME].get(
        UserRepository
    )
    user = await user_repo.get_by_tg_id(cq.from_user.id)
    if user is not None:
        update_user_interactor: UpdateUserLanguage = await manager.middleware_data[
            CONTAINER_NAME
        ].get(UpdateUserLanguage)
        await update_user_interactor(
            UpdateUserLanguageInput(tg_id=cq.from_user.id, language=language)
        )
    else:
        create_user_interactor: CreateUser = await manager.middleware_data[
            CONTAINER_NAME
        ].get(CreateUser)
        await create_user_interactor(User(tg_id=cq.from_user.id, language=language))
    manager.middleware_data[I18N_FORMAT_KEY] = manager.middleware_data["l10ns"][
        language
    ].format_value
    await manager.next()


def create_user() -> Dialog:
    return Dialog(
        Window(
            I18nFormat("choose-language"),
            Select(
                Format("{item}"),
                "choose_lang",
                lambda x: x.partition(" ")[-1].lower(),
                ["🇷🇺 RU", "🏴󠁧󠁢󠁥󠁮󠁧󠁿 EN"],
                on_click=add_user,
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
