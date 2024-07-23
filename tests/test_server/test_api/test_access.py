import pytest
from httpx import AsyncClient
from litestar import status_codes

from src.app.domain.accounts.urls import ACCOUNT_LOGIN, ACCOUNT_LOGOUT, ACCOUNT_PROFILE
from tests.test_server.raw_data import RAW_USERS, RawUser

pytestmark = pytest.mark.anyio


@pytest.mark.parametrize(
    "userdata",
    RAW_USERS,
)
async def test_user_login(
    userdata: RawUser,
    client: AsyncClient,
    base_api_path: str,
) -> None:
    expected_status_code = (
        status_codes.HTTP_201_CREATED
        if userdata.is_active
        else status_codes.HTTP_403_FORBIDDEN
    )
    response = await client.post(
        f"{base_api_path}{ACCOUNT_LOGIN}",
        data={
            "username": userdata.email,
            "password": userdata.password,
        },
    )
    assert response.status_code == expected_status_code


@pytest.mark.parametrize(
    "userdata",
    RAW_USERS,
)
async def test_user_logout(
    client: AsyncClient,
    userdata: RawUser,
    base_api_path: str,
) -> None:
    response = await client.post(
        f"{base_api_path}{ACCOUNT_LOGIN}",
        data={
            "username": userdata.email,
            "password": userdata.password,
        },
    )
    expected_login_code = (
        status_codes.HTTP_201_CREATED
        if userdata.is_active
        else status_codes.HTTP_403_FORBIDDEN
    )
    assert response.status_code == expected_login_code

    if expected_login_code == status_codes.HTTP_403_FORBIDDEN:
        return

    cookies = dict(response.cookies)

    assert cookies.get("token") is not None

    me_response = await client.get(f"{base_api_path}{ACCOUNT_PROFILE}")
    assert me_response.status_code == 200

    response = await client.post(f"{base_api_path}{ACCOUNT_LOGOUT}")
    assert response.status_code == 200

    # the user can no longer access the /me route.
    me_response = await client.get(f"{base_api_path}{ACCOUNT_PROFILE}")
    assert me_response.status_code == 401
