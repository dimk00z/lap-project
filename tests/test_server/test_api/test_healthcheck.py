from typing import Callable

import pytest
from httpx import AsyncClient
from litestar.status_codes import HTTP_200_OK

from src.app.__about__ import __version__
from src.app.domain.accounts.system.urls import LIVENESS, SYSTEM_HEALTH

pytestmark = pytest.mark.anyio


async def test_health(
    client: AsyncClient,
    get_endpoint_path: Callable[[str], str],
) -> None:
    response = await client.get(
        get_endpoint_path(SYSTEM_HEALTH),
    )
    assert response.status_code == HTTP_200_OK

    expected = {
        "status": "online",
        "app": "app",
        "version": __version__,
    }

    assert response.json() == expected


async def test_liveness(
    client: AsyncClient,
    get_endpoint_path: Callable[[str], str],
) -> None:
    response = await client.get(
        get_endpoint_path(LIVENESS),
    )
    assert response.status_code == HTTP_200_OK

    assert response.text == "OK"
