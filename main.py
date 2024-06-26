from dishka import make_async_container
from dishka.integrations import litestar as litestar_integration
from litestar import Litestar
from litestar.openapi import OpenAPIConfig

from server.config import AppConfig
from server.controllers.http_controllers import HTTP_CONTROLLERS
from server.ioc import AppProvider


def get_litestar_app(*, app_config: AppConfig) -> Litestar:
    """Creates a Litestar app."""
    litestar_app = Litestar(
        route_handlers=[*HTTP_CONTROLLERS],
        openapi_config=OpenAPIConfig(
            title=app_config.app_name,
            version=app_config.app_version,
        ),
    )
    return litestar_app


def connect_container(
    *,
    litestar_app: Litestar,
    app_config: AppConfig,
) -> None:
    """Connects the container to the app."""
    container = make_async_container(
        AppProvider(),
        context={AppConfig: app_config},
    )
    litestar_integration.setup_dishka(container, litestar_app)


def create_app() -> Litestar:
    """Creates the main app."""
    # faststream_app = get_faststream_app()
    app_config = AppConfig()

    litestar_app = get_litestar_app(app_config=app_config)
    connect_container(
        litestar_app=litestar_app,
        app_config=app_config,
    )

    # litestar_app.on_startup.append(faststream_app.broker.start)
    # litestar_app.on_shutdown.append(faststream_app.broker.close)
    return litestar_app
