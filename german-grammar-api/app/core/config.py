from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "German Grammar & Context API"
    api_v1_prefix: str = "/api/v1"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    whisper_model: str = "base"
    max_upload_mb: int = 25

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
