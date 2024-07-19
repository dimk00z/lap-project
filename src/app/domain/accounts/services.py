"""Accounts services."""

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from src.app.db.models import Role, User, UserRole


class UserService(SQLAlchemyAsyncRepositoryService[User]):
    """Handles database operations for users."""


class RoleService(SQLAlchemyAsyncRepositoryService[Role]):
    """Handles database operations for users roles."""


class UserRoleService(SQLAlchemyAsyncRepositoryService[UserRole]):
    """Handles database operations for user roles."""
