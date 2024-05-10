from fastapi import APIRouter

from backend.presentation.web.api.get.weather import get_weather
from backend.presentation.web.routes.form import show_form
from backend.presentation.web.routes.result import show_result


def get_api_router() -> APIRouter:
    get = APIRouter(prefix="/get")

    get.get("/weather/{city}")(get_weather)

    router = APIRouter(prefix="/api")

    router.include_router(get)

    return router


def get_site_router() -> APIRouter:
    router = APIRouter(include_in_schema=False)

    router.get("/")(show_form)
    router.get("/result")(show_result)

    return router
