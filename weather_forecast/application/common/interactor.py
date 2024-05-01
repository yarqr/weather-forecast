from abc import ABC, abstractmethod
from typing import Generic, TypeVar

Input = TypeVar("Input")
Output = TypeVar("Output")


class Interactor(Generic[Input, Output], ABC):
    @abstractmethod
    async def __call__(self, data: Input) -> Output: ...
