from dataclasses import dataclass
from typing import Literal

from src.app.__about__ import __version__ as current_version
from src.app.config.base import get_settings

__all__ = ("SystemHealth",)

settings = get_settings()


@dataclass
class SystemHealth:
    """System Health Response."""

    status: Literal["online"] = "online"
    app: str = settings.app.NAME
    version: str = current_version
