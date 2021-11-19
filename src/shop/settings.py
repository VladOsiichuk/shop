from typing import List

from pydantic import BaseSettings, Field, PostgresDsn, validator


class DatabaseSettings(BaseSettings):
    url: str = Field(env="database_url")
    debug: bool = Field(default=False, env="debug_sql")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class Settings(BaseSettings):
    debug: bool = Field(default=False, env="debug")
    do_not_wire: List[str] = []

    db: DatabaseSettings = Field(default_factory=DatabaseSettings)

    class Config:
        validate_all = False
        env_file = ".env"
        env_file_encoding = "utf-8"
