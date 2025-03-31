from functools import cache
from os import PathLike
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


type _StrPath = str | Path | PathLike[str]
type LogLevelType = Literal[
    "info",
    "debug",
    "warning",
    "error",
    "critical",
    "trace",
]


def get_root_dir() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def get_absolute_path(*paths: _StrPath, base_path: _StrPath | None = None) -> Path:
    if base_path is None:
        base_path = get_root_dir()

    return Path(base_path, *paths)


class ServerConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="./.env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="SERVER_",
        extra="ignore",
    )

    title: str = "Ace Impact"
    debug: bool = True
    version: str = "dev"
    host: str = "0.0.0.0"
    port: int = 8080
    log_level: LogLevelType = "info"
    cors_methods: list[str] = ["*"]
    cors_headers: list[str] = ["*"]
    cors_origins: list[str] = ["*"]


class Config:
    server: ServerConfig = ServerConfig()


@cache
def get_config() -> Config:
    return Config()
