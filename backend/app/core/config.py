from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """12-factor config: everything overridable via env vars / .env."""
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Tasks API"
    database_url: str = "sqlite:///./app.db"  # Postgres in docker-compose
    cors_origins: list[str] = ["http://localhost:5173"]


@lru_cache
def get_settings() -> Settings:
    return Settings()
