from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal['test', 'local', 'dev', 'prod']
    APP_TITLE: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_PORT: int
    DB_HOST: str

    REDIS_HOST: str
    REDIS_PORT: int

    @property
    def CELERY_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    @property
    def DB_URL(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
    
    model_config = SettingsConfigDict(env_file='.env', extra='allow')



@lru_cache
def get_settings() -> Settings:
    return Settings()