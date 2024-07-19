from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
from sqlalchemy.ext.asyncio import AsyncSession

from server.api.v1.users.models import User


class UserRepository(SQLAlchemyAsyncRepository[User]):
    """User repository."""

    model_type = User


async def provide_users_repo(db_session: AsyncSession) -> UserRepository:
    """This provides the default Authors repository."""
    return UserRepository(session=db_session)
