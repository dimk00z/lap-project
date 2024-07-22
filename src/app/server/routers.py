from litestar import Router
from litestar.types import ControllerRouterHandler

from src.app.domain.accounts.controllers import AccessController, UserController
from src.app.domain.accounts.system.controllers import SystemController

v1_router = Router(
    path="/v1",
    route_handlers=[
        SystemController,
        AccessController,
        UserController,
    ],
)

api_router = Router(
    path="/api",
    route_handlers=[
        v1_router,
    ],
)


route_handlers: list[ControllerRouterHandler] = [
    api_router,
]
