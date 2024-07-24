import pytest
from httpx import AsyncClient
from litestar import Litestar, get
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from src.app.config import app as config

pytestmark = pytest.mark.anyio


def test_engine_on_app(app: Litestar, engine: AsyncEngine) -> None:
    """Test that the app's engine is patched."""
    assert app.state[config.alchemy.engine_app_state_key] is engine


@pytest.mark.anyio
async def test_db_session_dependency(
    app: Litestar,
    engine: AsyncEngine,
) -> None:
    """Test that handlers receive session attached to patched engine."""

    @get("/db-session-test", opt={"exclude_from_auth": True})
    async def db_session_dependency_patched(db_session: AsyncSession) -> dict[str, str]:
        return {"result": f"{db_session.bind is engine = }"}

    app.register(db_session_dependency_patched)
    async with AsyncClient(
        app=app,
        base_url="http://testserver",
    ) as client:
        response = await client.get("/db-session-test")
        assert response.json()["result"] == "db_session.bind is engine = True"
