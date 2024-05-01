from aiohttp import ClientSession

from weather_forecast.application.common.services.weather import WeatherService
from weather_forecast.domain.entities.weather import Weather


class WeatherServiceImpl(WeatherService):
    def __init__(self, session: ClientSession, owm_token: str):
        self.session = session
        self.owm_token = owm_token

    async def get_by_city(self, city: str) -> Weather:
        async with self.session.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": city, "appid": self.owm_token, "units": "metric"},
        ) as resp:
            data = await resp.json()
            return Weather(temperature=data["main"]["temp"])
