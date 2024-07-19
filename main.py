from litestar import Litestar
from litestar.di import Provide

from src.app.config import app as config
from src.app.config import constants, get_settings
from src.app.domain.accounts import signals as account_signals
from src.app.domain.accounts.dependencies import provide_user
from src.app.domain.accounts.guards import auth
from src.app.lib.dependencies import create_collection_dependencies
from src.app.server import openapi, plugins, routers


def create_app() -> Litestar:
    """Create ASGI application."""

    dependencies = {constants.USER_DEPENDENCY_KEY: Provide(provide_user)}
    dependencies.update(create_collection_dependencies())
    settings = get_settings()
    return Litestar(
        route_handlers=routers.route_handlers,
        cors_config=config.cors,
        debug=settings.app.DEBUG,
        openapi_config=openapi.config,
        plugins=[
            plugins.structlog,
            plugins.app_config,
            plugins.alchemy,
        ],
        on_app_init=[
            auth.on_app_init,
        ],
        listeners=[
            account_signals.user_created_event_handler,
        ],
    )
