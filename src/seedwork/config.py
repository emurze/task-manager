import os
from pathlib import Path
from typing import Literal, ClassVar

from pydantic import BaseModel, SecretStr, Field
from pydantic_settings import SettingsConfigDict, BaseSettings

IS_DOCKER_VARIABLE = "IS_DOCKER"
LOG_DEFAULT_FORMAT = "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s  %(message)s"
BASE_DIR: Path = Path(__file__).parent.parent
MODULES_DIR: Path = BASE_DIR / "modules"


class LoggingConfig(BaseModel):
    log_level: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = "INFO"
    log_format: str = LOG_DEFAULT_FORMAT


class DatabaseConfig(BaseModel):
    echo: bool = False
    hostname: ClassVar[str] = "pgbouncer"
    dsn: str = (
        f"postgresql+asyncpg://postgres:password@{hostname}:6432/postgres"
    )
    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    def get_db_dsn_for_environment(self) -> str:
        if not os.getenv(IS_DOCKER_VARIABLE):
            return self.dsn.replace(self.hostname, "localhost")
        return self.dsn


class ApiConfig(BaseModel):
    v1_prefix: str = "/api/v1"
    title: str = "App"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    secret_key: SecretStr = "secret"
    allowed_origins: list[str] = [
        "http://localhost:3000",
    ]
    allowed_hosts: list[str] = []
    gzip_minimum_size: int = 1000
    gzip_compress_level: int = 7


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=[".env.dev", ".env"],
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="CONFIG__",
        extra="allow",
    )
    api: ApiConfig = Field(default_factory=ApiConfig)
    db: DatabaseConfig = Field(default_factory=DatabaseConfig)
    debug: bool = True
