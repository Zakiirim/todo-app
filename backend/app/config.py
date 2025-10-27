from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    database_url: str
    postgres_user: str
    postgres_password: str
    postgres_db: str
    cors_origins: str = "http://localhost:5173"

    db_pool_min_size: int = 10
    db_pool_max_size: int = 20

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    """Singleton pattern: ensures only one Settings instance exists"""
    return Settings()
