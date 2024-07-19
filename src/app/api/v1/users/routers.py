from litestar import Router

from server.api.v1.users.controllers import UserController
from server.api.v1.users.controllers.auth_controller import AuthController

users_router = Router(
    path="/users",
    route_handlers=[
        UserController,
    ],
)

auth_router = Router(
    path="/auth",
    route_handlers=[
        AuthController,
    ],
)
