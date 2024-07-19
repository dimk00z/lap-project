from advanced_alchemy.extensions.litestar import SQLAlchemyPlugin
from litestar.plugins.structlog import StructlogPlugin

from src.app.config import app as config
from src.app.server.builder import ApplicationConfigurator

structlog = StructlogPlugin(config=config.log)
alchemy = SQLAlchemyPlugin(config=config.alchemy)
app_config = ApplicationConfigurator()
