from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresConfig(BaseSettings):
    host: str = Field(
        alias="POSTGRES_HOST",
        default="db",
    )
    port: int = Field(
        alias="POSTGRES_PORT",
        default=5432,
    )
    login: str = Field(
        alias="POSTGRES_USER",
        default="postgres",
    )
    password: str = Field(
        alias="POSTGRES_PASSWORD",
        default="postgres",
    )
    database: str = Field(
        alias="POSTGRES_DB",
        default="postgres",
    )

    model_config = SettingsConfigDict(
        env_file="../config/.env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    @property
    def connection_string(self) -> str:
        """PostgreSQL connection string."""
        return f"postgresql+psycopg://{self.login}:{self.password}@{self.host}:{self.port}/{self.database}"


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
    posgres_config: PostgresConfig = PostgresConfig()
