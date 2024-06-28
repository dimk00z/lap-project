from advanced_alchemy.extensions.litestar.plugins.init.config.asyncio import (
    autocommit_before_send_handler,
)
from dishka import make_async_container
from dishka.integrations import litestar as litestar_integration
from litestar import Litestar
from litestar.contrib.sqlalchemy.plugins import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    SQLAlchemyInitPlugin,
    SQLAlchemySerializationPlugin,
)
from litestar.openapi import OpenAPIConfig
from litestar.openapi.spec import Components, SecurityScheme, Tag
from loguru import logger

from server.api.api_router import api_router
from server.config import AppConfig
from server.infrastructure.database import provide_transaction
from server.ioc import AppProvider


def get_litestar_app(*, app_config: AppConfig) -> Litestar:
    """Creates a Litestar app."""

    session_config = AsyncSessionConfig(expire_on_commit=False)
    connection_string = app_config.posgres_config.connection_string
    logger.info(
        "Connection string: {conn}",
        conn=connection_string,
    )
    sqlalchemy_config = SQLAlchemyAsyncConfig(
        connection_string=connection_string,
        session_config=session_config,
        create_all=True,
        before_send_handler=autocommit_before_send_handler,
    )  # Create 'async_session' dependency.

    litestar_app = Litestar(
        route_handlers=[
            api_router,
        ],
        plugins=[
            SQLAlchemyInitPlugin(config=sqlalchemy_config),
            SQLAlchemySerializationPlugin(),
        ],
        dependencies={
            "transaction": provide_transaction,
        },
        openapi_config=OpenAPIConfig(
            title=app_config.app_name,
            version=app_config.app_version,
            tags=[
                Tag(
                    name="public",
                    description="This endpoint is for external users",
                ),
            ],
            security=[{"BearerToken": []}],
            components=Components(
                security_schemes={
                    "BearerToken": SecurityScheme(
                        type="http",
                        scheme="bearer",
                    )
                },
            ),
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
    print(list(litestar_app.dependencies))
    # litestar_app.on_startup.append(faststream_app.broker.start)
    # litestar_app.on_shutdown.append(faststream_app.broker.close)
    return litestar_app
