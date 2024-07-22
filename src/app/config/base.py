import binascii
import json
import os
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from advanced_alchemy.utils.text import slugify

from src.app.config.common import TRUE_VALUES
from src.app.config.db import DatabaseSettings
from src.app.config.log import LogSettings
from src.app.config.redis import RedisSettings
from src.app.config.server import ServerSettings


@dataclass
class AppSettings:
    """Application configuration"""

    URL: str = field(
        default_factory=lambda: os.getenv(
            "APP_URL",
            "http://localhost:8000",
        )
    )
    """The frontend base URL"""
    DEBUG: bool = field(
        default_factory=lambda: os.getenv(
            "LITESTAR_DEBUG",
            "False",
        )
        in TRUE_VALUES
    )
    """Run `Litestar` with `debug=True`."""
    SECRET_KEY: str = field(
        default_factory=lambda: os.getenv(
            "SECRET_KEY", binascii.hexlify(os.urandom(32)).decode(encoding="utf-8")
        ),
    )
    """Application secret key."""
    NAME: str = field(default_factory=lambda: "app")
    """Application name."""
    ALLOWED_CORS_ORIGINS: list[str] | str = field(
        default_factory=lambda: os.getenv(
            "ALLOWED_CORS_ORIGINS",
            '["*"]',
        )
    )
    """Allowed CORS Origins"""
    CSRF_COOKIE_NAME: str = field(
        default_factory=lambda: "csrftoken",
    )
    """CSRF Cookie Name"""
    CSRF_COOKIE_SECURE: bool = field(default_factory=lambda: False)
    """CSRF Secure Cookie"""
    JWT_ENCRYPTION_ALGORITHM: str = field(
        default_factory=lambda: "HS256",
    )
    """JWT Encryption Algorithm"""

    @property
    def slug(self) -> str:
        """Return a slugified name.

        Returns:
            `self.NAME`, all lowercase and hyphens instead of spaces.
        """
        return slugify(self.NAME)

    def __post_init__(self) -> None:
        # Check if the ALLOWED_CORS_ORIGINS is a string.
        if not isinstance(self.ALLOWED_CORS_ORIGINS, str):
            return

        if not (
            self.ALLOWED_CORS_ORIGINS.startswith("[")
            and self.ALLOWED_CORS_ORIGINS.endswith("]")
        ):
            self.ALLOWED_CORS_ORIGINS = [
                host.strip() for host in self.ALLOWED_CORS_ORIGINS.split(",")
            ]
            return
        try:
            # Safely evaluate the string as a Python list.
            self.ALLOWED_CORS_ORIGINS = json.loads(self.ALLOWED_CORS_ORIGINS)
        except (SyntaxError, ValueError):
            # Handle potential errors if the string is not a valid Python literal.
            msg = "ALLOWED_CORS_ORIGINS is not a valid list representation."
            raise ValueError(msg) from None


@dataclass
class Settings:
    app: AppSettings = field(
        default_factory=AppSettings,
    )
    db: DatabaseSettings = field(
        default_factory=DatabaseSettings,
    )
    server: ServerSettings = field(
        default_factory=ServerSettings,
    )
    log: LogSettings = field(
        default_factory=LogSettings,
    )
    redis: RedisSettings = field(
        default_factory=RedisSettings,
    )

    @classmethod
    def from_env(cls, dotenv_filename: str = ".env") -> "Settings":
        from litestar.cli._utils import console

        env_file = Path(f"{os.curdir}/{dotenv_filename}")
        if not env_file.is_file():
            return Settings()

        from dotenv import load_dotenv

        console.print(
            f"[yellow]Loading environment configuration from {dotenv_filename}[/]"
        )

        load_dotenv(env_file)
        return Settings()


@lru_cache(maxsize=1, typed=True)
def get_settings() -> Settings:
    return Settings.from_env()
