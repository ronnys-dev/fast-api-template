import os

from pydantic import BaseSettings, Field

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AppConfig(BaseSettings):
    """Конфигурация приложения."""

    class Config:  # noqa: D106
        env_file = ".env"
        env_file_encoding = "utf-8"

    # application
    project_name: str = Field(env="PROJECT_NAME", default="backend")
    debug: bool = Field(env="DEBUG", cast=bool, default=True)
    tls: str = Field(env="TLS", default="off")
    server_host: str = Field(env="SERVER_HOST", default="localhost")
    server_port: int = Field(env="SERVER_PORT", cast=int, default="8000")
    site_url: str = (
        f"https://{server_host}"
        if tls == "on"
        else f"http://{server_host}:{server_port}"
    )
    environment: str = Field(
        env="ENVIRONMENT", default="development"
    )  # development/production

    # logging
    log_level: str = Field(env="LOG_LEVEL", default="WARNING")
    json_logs: bool = Field(env="JSON_LOGS", cast=bool, default=False)


class DatabaseConfig(BaseSettings):
    """Конфигурация БД."""

    class Config:  # noqa: D106
        env_file = ".env"
        env_file_encoding = "utf-8"

    protocol: str = "postgresql+asyncpg"
    database: str = Field(env="POSTGRES_DB")
    username: str = Field(env="POSTGRES_USER")
    password: str = Field(env="POSTGRES_PASSWORD")
    host: str = Field(env="BACKEND_DATABASE_HOST")
    port: int = Field(env="BACKEND_DATABASE_PORT", cast=int)

    # Список приложений, которые используют SQLAlchemy для декларации моделей
    # Нужно для Alembic миграций
    apps: list[str] = []

    @property
    def database_url(self) -> str:
        """URL подключения к БД."""
        return "{protocol}://{username}:{password}@{host}:{port}/{database}".format(
            protocol=self.protocol,
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
        )
