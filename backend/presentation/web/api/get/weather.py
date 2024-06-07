from typing import cast, Optional
from fastapi import Request
from backend.application.common.services.weather import WeatherService


async def get_weather(
    city: str, request: Request
) -> Optional[dict[str, float | int | str]]:
    weather = await cast(WeatherService, request.app.state.weather_service).get_by_city(
        city
    )
    if weather is not None:
        return {
            "temperature": weather.temperature,
            "feels_like": weather.feels_like,
            "humidity": weather.humidity,
            "wind_speed": weather.wind_speed,
            "description": weather.description,
            "country": weather.country,
        }
    return None
