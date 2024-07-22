# from collections.abc import Iterator

from collections.abc import AsyncIterator

import pytest
from httpx import AsyncClient
from litestar import Litestar

pytestmark = pytest.mark.anyio


@pytest.fixture(name="client")
async def fx_client(app: Litestar) -> AsyncIterator[AsyncClient]:
    """Async client that calls requests on the app.

    ```text
    ValueError: The future belongs to a different loop than the one specified as the loop argument
    ```
    """
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client
