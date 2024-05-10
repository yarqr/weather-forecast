import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from adaptix import Retort
from sqlalchemy import URL


@dataclass
class DatabaseConfigPart:
    host: str
    port: int
    username: str
    password: str
    database: str

    def make_dsn(self) -> str:
        return URL.create(
            "postgresql+asyncpg",
            self.username,
            self.password,
            self.host,
            self.port,
            self.database,
        ).render_as_string(hide_password=False)


@dataclass
class RedisConfigPart:
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None
    database: int = 0

    def make_dsn(self) -> str:
        return URL.create(
            "redis",
            self.username,
            self.password,
            self.host,
            self.port,
            str(self.database),
        ).render_as_string(hide_password=False)


@dataclass
class BotConfigPart:
    token: str


@dataclass
class TelegramConfig:
    owm_token: str
    bot: BotConfigPart
    redis: RedisConfigPart
    database: DatabaseConfigPart


@dataclass
class WebConfigPart:
    host: str
    port: int


@dataclass
class WebConfig:
    owm_token: str
    web: WebConfigPart


def _load_database_config_part(path: Path) -> DatabaseConfigPart:
    retort = Retort()
    with open(path, "rb") as f:
        return retort.load(tomllib.load(f)["database"], DatabaseConfigPart)


def load_telegram_config(path: Path) -> TelegramConfig:
    retort = Retort()
    with open(path, "rb") as f:
        return retort.load(tomllib.load(f), TelegramConfig)


def load_web_config(path: Path) -> WebConfig:
    retort = Retort()
    with open(path, "rb") as f:
        return retort.load(tomllib.load(f), WebConfig)
