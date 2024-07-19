from litestar import Router

from server.api.v1 import router

api_router = Router(
    path="/api",
    route_handlers=[
        router.v1_router,
    ],
)
