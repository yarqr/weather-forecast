from abc import ABC, abstractmethod

from weather_forecast.domain.entities.weather import Weather


class WeatherService(ABC):
    @abstractmethod
    async def get_by_city(self, city: str) -> Weather: ...
