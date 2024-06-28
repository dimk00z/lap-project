from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
from sqlalchemy.ext.asyncio import AsyncSession

from server.api.v1.users.models import User


class UserRepository(SQLAlchemyAsyncRepository[User]):
    """User repository."""

    model_type = User


async def provide_users_repo(transaction: AsyncSession) -> UserRepository:
    """This provides the default Authors repository."""
    return UserRepository(session=transaction)


# @asynccontextmanager
# async def repository_factory() -> AsyncIterator[UserRepository]:
#     async with session_factory() as db_session:
#         try:
#             yield UserRepository(session=db_session)
#         except Exception:  # noqa: BLE001
#             await db_session.rollback()
