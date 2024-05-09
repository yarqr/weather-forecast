from abc import ABC, abstractmethod
from typing import Optional

from backend.domain.entities.weather import Weather


class WeatherService(ABC):
    @abstractmethod
    async def get_by_city(self, city: str) -> Optional[Weather]: ...
