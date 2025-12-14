from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    service_name: str = "fa-skeleton"
    db_url: str = ""
    jwt_secret_key: str = ""
    otlp_endpoint: str = ""  # Jaeger OTLP endpoint

    # tell pydantic where/how to load configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()
