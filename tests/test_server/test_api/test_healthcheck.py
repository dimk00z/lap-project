import pytest
from httpx import AsyncClient
from litestar.status_codes import HTTP_200_OK

from src.app.__about__ import __version__

pytestmark = pytest.mark.anyio


async def test_health(client: AsyncClient) -> None:
    response = await client.get("/api/v1/health/")
    assert response.status_code == HTTP_200_OK

    expected = {
        "status": "online",
        "app": "app",
        "version": __version__,
    }

    assert response.json() == expected


async def test_liveness(client: AsyncClient) -> None:
    response = await client.get("/api/v1/liveness/")
    assert response.status_code == HTTP_200_OK

    assert response.text == "OK"
