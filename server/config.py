from pydantic import (
    Field,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    app_name: str = Field(
        alias="APP_NAME",
        default="LAP Social App",
    )
    app_version: str = Field(
        alias="APP_VERSION",
        default="0.1.0",
    )
    model_config = SettingsConfigDict(
        env_file="../config/.env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
