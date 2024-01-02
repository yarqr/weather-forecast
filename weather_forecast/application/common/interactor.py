from abc import ABC, abstractmethod
from typing import Generic, TypeVar

Request = TypeVar("Request")
Response = TypeVar("Response")


class Interactor(Generic[Request, Response], ABC):
    @abstractmethod
    async def __call__(self, data: Request) -> Response:
        ...
