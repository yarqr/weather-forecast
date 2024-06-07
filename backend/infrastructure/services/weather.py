from typing import Optional

from aiohttp import ClientSession

from backend.application.common.services.weather import WeatherService
from backend.domain.entities.weather import Weather


class WeatherServiceImpl(WeatherService):
    def __init__(self, session: ClientSession, owm_token: str):
        self.session = session
        self.owm_token = owm_token

    async def get_by_city(self, city: str) -> Optional[Weather]:
        async with self.session.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": city, "appid": self.owm_token, "units": "metric"},
        ) as resp:
            if resp.status != 200:
                return None
            data = await resp.json()
            main_data = data["main"]
            return Weather(
                temperature=main_data["temp"],
                feels_like=main_data["feels_like"],
                humidity=main_data["humidity"],
                wind_speed=data["wind"]["speed"],
                description=data["weather"][0]["main"],
                country=data["sys"]["country"],
            )
