from sqlalchemy.ext.asyncio import AsyncSession

from weather_forecast.application.common.unit_of_work import UnitOfWork


class UnitOfWorkImpl(UnitOfWork):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit(self) -> None:
        await self.session.commit()
