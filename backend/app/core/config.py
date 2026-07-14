from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    app_name: str = "Euro Park API"
    app_service_name: str = "euro-park-api"
    app_version: str = "0.1.0"
    app_env: str = "development"
    app_debug: bool = False

    api_v1_prefix: str = "/api/v1"

    db_host: str = "localhost"
    db_port: int = 14333
    db_name: str = "euro_park"
    db_user: str = "euro_park_app"
    db_password: SecretStr

    db_driver: str = "ODBC Driver 18 for SQL Server"
    db_encrypt: bool = True
    db_trust_server_certificate: bool = True

    jwt_secret_key: SecretStr
    jwt_algorithm: Literal["HS256"] = "HS256"
    jwt_issuer: str = "euro-park-api"
    jwt_audience: str = "euro-park-client"

    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    log_level: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = "INFO"
    cors_allowed_origins: str = "http://localhost:3000,http://localhost:3001"

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_allowed_origins.split(",") if origin.strip()]

    rate_limit_enabled: bool = True
    barrier_rate_limit_requests: int = 60
    barrier_rate_limit_window_seconds: int = 60

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def database_url(self) -> URL:
        return URL.create(
            drivername="mssql+pyodbc",
            username=self.db_user,
            password=self.db_password.get_secret_value(),
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
            query={
                "driver": self.db_driver,
                "Encrypt": "yes" if self.db_encrypt else "no",
                "TrustServerCertificate": ("yes" if self.db_trust_server_certificate else "no"),
            },
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
