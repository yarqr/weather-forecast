from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
)

from backend.application.common.repositories.user import UserRepository
from backend.application.common.unit_of_work import UnitOfWork
from backend.application.create_user.interactor import CreateUser
from backend.application.update_user_city.interactor import UpdateUserCity
from backend.application.update_user_language.interactor import (
    UpdateUserLanguage,
)
from backend.infrastructure.config import DatabaseConfigPart
from dishka import Provider, provide, Scope

from backend.infrastructure.database.repositories.user import (
    UserRepositoryImpl,
)
from backend.infrastructure.database.unit_of_work import UnitOfWorkImpl


class DatabaseProvider(Provider):
    def __init__(self, config: DatabaseConfigPart):
        super().__init__()
        self._config = config

    @provide(scope=Scope.APP)
    async def get_engine(self) -> AsyncGenerator[AsyncEngine, None]:
        engine = create_async_engine(self._config.make_dsn())
        yield engine
        await engine.dispose()

    @provide(scope=Scope.APP)
    async def get_session_maker(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncGenerator[AsyncSession, None]:
        async with session_maker() as session:
            yield session

    uow = provide(UnitOfWorkImpl, scope=Scope.REQUEST, provides=UnitOfWork)

    @provide(scope=Scope.REQUEST)
    async def get_user_repo(self, session: AsyncSession) -> UserRepository:
        return UserRepositoryImpl(session)


class InteractorProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_create_user(
        self, user_repo: UserRepository, uow: UnitOfWork
    ) -> CreateUser:
        return CreateUser(user_repo, uow)

    @provide(scope=Scope.REQUEST)
    async def get_update_user_city(
        self, user_repo: UserRepository, uow: UnitOfWork
    ) -> UpdateUserCity:
        return UpdateUserCity(user_repo, uow)

    @provide(scope=Scope.REQUEST)
    async def get_update_user_language(
        self, user_repo: UserRepository, uow: UnitOfWork
    ) -> UpdateUserLanguage:
        return UpdateUserLanguage(user_repo, uow)
