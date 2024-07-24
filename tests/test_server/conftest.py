from collections.abc import AsyncIterator
from dataclasses import asdict
from typing import Any

import pytest
from advanced_alchemy.base import UUIDAuditBase
from litestar import Litestar
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from src.app.config.base import Settings
from src.app.db.models import User
from src.app.domain.accounts.guards import auth
from src.app.domain.accounts.services import UserService
from src.app.server.plugins import alchemy
from tests.test_server.raw_data import RAW_USERS, SUPER_USER_EMAIL, COMMON_USER_EMAIl

pytestmark = pytest.mark.anyio


@pytest.fixture
def super_user_email() -> str:
    return SUPER_USER_EMAIL


@pytest.fixture
def common_user_email() -> str:
    return COMMON_USER_EMAIl


@pytest.fixture(name="raw_users")
def fx_raw_users() -> list[dict[str, Any]]:
    """Unstructured user representations."""

    return [asdict(raw_user) for raw_user in RAW_USERS]


@pytest.fixture(name="sessionmaker")
def fx_session_maker_factory(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
    )


@pytest.fixture(autouse=True)
async def _seed_db(
    settings: Settings,
    engine: AsyncEngine,
    sessionmaker: async_sessionmaker[AsyncSession],
    raw_users: list[User | dict[str, Any]],
) -> AsyncIterator[None]:
    """Populate test database with.

    Args:
        engine: The SQLAlchemy engine instance.
        sessionmaker: The SQLAlchemy sessionmaker factory.
        raw_users: Test users to add to the database

    """

    # fixtures_path = Path(settings.db.FIXTURE_PATH)
    metadata = UUIDAuditBase.registry.metadata
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)

    async with UserService.new(sessionmaker()) as users_service:
        await users_service.create_many(
            raw_users,
            auto_commit=True,
        )

    yield


@pytest.fixture(autouse=True)
def _patch_db(
    app: Litestar,
    engine: AsyncEngine,
    sessionmaker: async_sessionmaker[AsyncSession],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        alchemy._config,
        "session_maker",
        sessionmaker,
    )
    if isinstance(alchemy._config, list):
        monkeypatch.setitem(
            app.state,
            alchemy._config[0].engine_app_state_key,
            engine,
        )
        monkeypatch.setitem(
            app.state,
            alchemy._config[0].session_maker_app_state_key,
            async_sessionmaker(bind=engine, expire_on_commit=False),
        )
        return
    monkeypatch.setitem(
        app.state,
        alchemy._config.engine_app_state_key,
        engine,
    )
    monkeypatch.setitem(
        app.state,
        alchemy._config.session_maker_app_state_key,
        async_sessionmaker(
            bind=engine,
            expire_on_commit=False,
        ),
    )


def get_auth_header(email: str) -> dict[str, str]:
    token = auth.create_token(identifier=email)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(name="superuser_token_headers")
def fx_superuser_token_headers(
    super_user_email: str,
) -> dict[str, str]:
    """Valid superuser token."""
    return get_auth_header(super_user_email)


@pytest.fixture(name="user_token_headers")
def fx_user_token_headers(
    common_user_email: str,
) -> dict[str, str]:
    """Valid user token."""
    return get_auth_header(common_user_email)
