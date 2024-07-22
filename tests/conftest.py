import pytest
from litestar import Litestar
from pytest import MonkeyPatch


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


# @pytest.fixture(autouse=True)
# def _patch_settings(monkeypatch: MonkeyPatch) -> None:
#     """Path the settings."""

#     settings = base.Settings.from_env(".env.testing")

#     def get_settings(dotenv_filename: str = ".env.testing") -> base.Settings:
#         return settings

#     monkeypatch.setattr(base, "get_settings", get_settings)
