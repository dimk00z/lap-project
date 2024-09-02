from typing import Callable

import pytest
from httpx import AsyncClient
from litestar import status_codes

from src.app.domain.accounts.urls import ACCOUNT_LIST
from tests.test_server.raw_data import COMMON_USER, SUPER_USER

pytestmark = pytest.mark.anyio


async def test_accounts_list(
    client: AsyncClient,
    superuser_token_headers: dict[str, str],
    get_endpoint_path: Callable[[str], str],
) -> None:
    response = await client.get(
        get_endpoint_path(ACCOUNT_LIST),
        headers=superuser_token_headers,
    )
    assert response.status_code == status_codes.HTTP_200_OK
    assert int(response.json()["total"]) > 0


async def test_update_user_no_auth(
    client: AsyncClient,
    get_endpoint_path: Callable[[str], str],
) -> None:
    uuid = SUPER_USER.id
    response = await client.patch(
        f"{get_endpoint_path(ACCOUNT_LIST)}/{uuid}",
        json={"name": "TEST UPDATE"},
    )
    assert response.status_code == status_codes.HTTP_401_UNAUTHORIZED
    response = await client.post(
        get_endpoint_path(ACCOUNT_LIST),
        json={"name": "A User", "email": "new-user@example.com", "password": "S3cret!"},
    )
    assert response.status_code == status_codes.HTTP_401_UNAUTHORIZED
    response = await client.get(
        f"{get_endpoint_path(ACCOUNT_LIST)}/{uuid}",
    )
    assert response.status_code == status_codes.HTTP_401_UNAUTHORIZED
    response = await client.get(
        get_endpoint_path(ACCOUNT_LIST),
    )
    assert response.status_code == status_codes.HTTP_401_UNAUTHORIZED
    response = await client.delete(
        f"{get_endpoint_path(ACCOUNT_LIST)}/{uuid}",
    )
    assert response.status_code == status_codes.HTTP_401_UNAUTHORIZED


async def test_accounts_get(
    client: AsyncClient,
    superuser_token_headers: dict[str, str],
    get_endpoint_path: Callable[[str], str],
) -> None:
    uuid = SUPER_USER.id

    response = await client.get(
        f"{get_endpoint_path(ACCOUNT_LIST)}/{uuid}",
        headers=superuser_token_headers,
    )
    assert response.status_code == status_codes.HTTP_200_OK
    assert response.json()["email"] == SUPER_USER.email


async def test_accounts_create(
    client: AsyncClient,
    superuser_token_headers: dict[str, str],
    get_endpoint_path: Callable[[str], str],
) -> None:
    response = await client.post(
        get_endpoint_path(ACCOUNT_LIST),
        json={
            "name": "A User",
            "email": "new-user@example.com",
            "password": "S3cret!",
        },
        headers=superuser_token_headers,
    )
    assert response.status_code == status_codes.HTTP_201_CREATED


async def test_accounts_update(
    client: AsyncClient,
    superuser_token_headers: dict[str, str],
    get_endpoint_path: Callable[[str], str],
) -> None:
    new_name = "Name Changed"
    response = await client.patch(
        f"{get_endpoint_path(ACCOUNT_LIST)}/{COMMON_USER.id}",
        json={
            "name": new_name,
        },
        headers=superuser_token_headers,
    )
    assert response.status_code == status_codes.HTTP_200_OK
    assert response.json()["name"] == new_name


async def test_accounts_delete(
    client: AsyncClient,
    superuser_token_headers: dict[str, str],
    get_endpoint_path: Callable[[str], str],
) -> None:
    response = await client.delete(
        f"{get_endpoint_path(ACCOUNT_LIST)}/{COMMON_USER.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == status_codes.HTTP_204_NO_CONTENT
