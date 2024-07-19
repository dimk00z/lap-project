from abc import abstractmethod
from typing import Any, Protocol


class Service(Protocol):
    """Interface for services."""

    def __call__(self) -> Any:
        """Do main service logic."""


class DBSession(Protocol):
    """Interface for database sessions."""

    async def commit(self) -> None:
        """Commit changes to the database."""

    @abstractmethod
    async def flush(self) -> None:
        """Flush changes to the database."""
