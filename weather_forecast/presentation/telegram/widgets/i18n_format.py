from typing import Any

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.text import Text

I18N_FORMAT_KEY = "aiogram_dialog_i18n_format"


class I18nFormat(Text):
    def __init__(self, key: str, when: WhenCondition = None):
        super().__init__(when)
        self.key = key

    async def _render_text(self, data: Any, manager: DialogManager) -> str:
        return manager.middleware_data[I18N_FORMAT_KEY](  # type: ignore[no-any-return]
            self.key, data
        )
