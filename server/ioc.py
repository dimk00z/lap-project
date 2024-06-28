from dishka import Provider, Scope, from_context, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from server.config import AppConfig
from server.infrastructure.database import new_session_maker


class AppProvider(Provider):
    config = from_context(
        provides=AppConfig,
        scope=Scope.APP,
    )

    @provide(scope=Scope.APP)
    def get_session_maker(
        self,
        config: AppConfig,
    ) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config.posgres_config)

    # @provide(scope=Scope.REQUEST)
    # async def get_session(
    #     self,
    #     session_maker: async_sessionmaker[AsyncSession],
    # ) -> AsyncIterable[
    #     AnyOf[
    #         AsyncSession,
    #         interfaces.DBSession,
    #     ]
    # ]:
    #     async with session_maker() as session:
    #         yield session

    # @provide(scope=Scope.REQUEST)
    # async def provide_transaction(
    #     self,
    #     session_maker: async_sessionmaker[AsyncSession],
    # ) -> AsyncIterable[
    #     AnyOf[
    #         AsyncSession,
    #         interfaces.DBSession,
    #     ]
    # ]:
    #     """Provides a transaction."""
    #     try:
    #         async with db_session.begin():
    #             yield db_session
    #     except IntegrityError as exc:
    #         logger.exception(exc)
    #         raise ClientException(
    #             status_code=HTTP_409_CONFLICT,
    #             detail=str(exc),
    #         ) from exc
