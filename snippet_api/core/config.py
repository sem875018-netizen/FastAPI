from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./snippets.db"
    # Для реального проекта обязательно замените секрет через переменную окружения.
    secret_key: str = "CHANGE-ME-use-a-long-random-secret-in-production"
    access_token_minutes: int = 60
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
