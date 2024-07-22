# from litestar import Litestar
# from litestar.status_codes import HTTP_200_OK
# from litestar.testing import TestClient


# def test_users_count(
#     app_client: TestClient[Litestar],
# ) -> None:
#     response = app_client.get("/api/v1/users/count")
#     assert response.status_code == HTTP_200_OK
#     assert int(response.text) == 0
