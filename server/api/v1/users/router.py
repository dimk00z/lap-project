from litestar import Router

from server.api.v1.users.controllers import UserController

users_router = Router(
    path="/users",
    route_handlers=[
        UserController,
    ],
)
