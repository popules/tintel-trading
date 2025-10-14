from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    FINNHUB_API_KEY: str | None = None
    ALPHAVANTAGE_API_KEY: str | None = None
    NEWSAPI_KEY: str | None = None
    SEC_API_KEY: str | None = None
    LOG_LEVEL: str = "INFO"
    ALLOWED_ORIGINS: str = "http://localhost:3000"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
