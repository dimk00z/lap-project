from litestar import Litestar
from litestar.status_codes import HTTP_200_OK
from litestar.testing import TestClient


def test_health_check_with_fixture(
    app_client: TestClient[Litestar],
) -> None:
    response = app_client.get("/api/v1/health/")
    assert response.status_code == HTTP_200_OK
    assert response.json().get("status") == "OK"
