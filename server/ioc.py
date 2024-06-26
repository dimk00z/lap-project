from dishka import Provider, Scope, from_context

from server.config import AppConfig


class AppProvider(Provider):
    config = from_context(
        provides=AppConfig,
        scope=Scope.APP,
    )
