from collections.abc import AsyncGenerator, AsyncIterator
from typing import Callable

import pytest
from httpx import AsyncClient
from litestar import Litestar
from pytest import MonkeyPatch
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from src.app.config import get_settings
from src.app.config.base import Settings

pytestmark = pytest.mark.anyio


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(name="app")
def fx_app(
    pytestconfig: pytest.Config,
    monkeypatch: MonkeyPatch,
) -> Litestar:
    """App fixture.

    Returns:
        An application instance, configured via plugin.
    """
    from main import create_app

    return create_app()


@pytest.fixture(name="client")
async def fx_client(app: Litestar) -> AsyncIterator[AsyncClient]:
    """Async client that calls requests on the app.

    ```text
    ValueError: The future belongs to a different loop than the one specified as the loop argument
    ```
    """
    async with AsyncClient(
        app=app,
        base_url="http://testserver",
    ) as client:
        yield client


@pytest.fixture
def settings() -> Settings:
    return get_settings()


@pytest.fixture(name="engine", autouse=True)
async def fx_engine(settings: Settings) -> AsyncEngine:
    """Postgresql instance for end-to-end testing.

    Returns:
        Async SQLAlchemy engine instance.
    """
    return settings.db.get_engine()


@pytest.fixture(name="sessionmaker")
def fx_session_maker_factory(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
    )


@pytest.fixture(name="session")
async def fx_session(
    sessionmaker: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    async with sessionmaker() as session:
        yield session


@pytest.fixture
def get_endpoint_path() -> Callable[[str], str]:
    def _wrapper(endpoint_path: str) -> str:
        return f"/api/v1{endpoint_path}"

    return _wrapper
