from litestar import Router

from server.api.v1.healtcheck.controllers import HealthCheckController
from server.api.v1.users.routers import auth_router, users_router

v1_router = Router(
    path="/v1",
    route_handlers=[
        HealthCheckController,
        users_router,
        auth_router,
    ],
)
