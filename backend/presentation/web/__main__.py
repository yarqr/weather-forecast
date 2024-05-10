import asyncio
from pathlib import Path

from aiohttp import ClientSession
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from uvicorn import Server, Config

from backend.infrastructure.config import load_web_config
from backend.infrastructure.services.weather import WeatherServiceImpl
from backend.presentation.web.setup import get_api_router, get_site_router


async def main() -> None:
    config = load_web_config(Path(__file__).parents[3] / "config.toml")

    app = FastAPI()

    session = ClientSession()
    app.state.weather_service = WeatherServiceImpl(session, config.owm_token)

    frontend_path = str(Path(__file__).parents[3] / "frontend")
    app.state.templates = Jinja2Templates(frontend_path)
    app.mount("/frontend", StaticFiles(directory=frontend_path))
    app.mount(
        "/assets", StaticFiles(directory=str(Path(__file__).parents[3] / "assets"))
    )

    app.include_router(get_api_router())
    app.include_router(get_site_router())

    server = Server(Config(app, config.web.host, config.web.port))

    try:
        await server.serve()
    finally:
        await session.close()


if __name__ == "__main__":
    asyncio.run(main())
