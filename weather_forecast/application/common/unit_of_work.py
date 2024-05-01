from abc import abstractmethod, ABC


class UnitOfWork(ABC):
    @abstractmethod
    async def commit(self) -> None: ...
