from typing import cast

from fastapi import Request
from starlette.templating import _TemplateResponse


async def show_result(
    request: Request,
) -> _TemplateResponse:
    return cast(
        _TemplateResponse,
        request.app.state.templates.TemplateResponse(request, "result/index.html"),
    )
