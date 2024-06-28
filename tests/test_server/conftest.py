from collections.abc import Iterator

import pytest
from litestar import Litestar
from litestar.testing import TestClient

from main import get_litestar_app
from server.config import AppConfig


@pytest.fixture
def app_config() -> Iterator[AppConfig]:
    yield AppConfig()


@pytest.fixture(scope="function")
def app_client(
    app_config: AppConfig,
) -> Iterator[TestClient[Litestar]]:
    with TestClient(app=get_litestar_app(app_config=app_config)) as client:
        yield client
