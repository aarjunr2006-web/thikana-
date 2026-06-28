from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Lachoo Student Portal API"
    DATABASE_URL: str = "sqlite+aiosqlite:///./portal.db"

    model_config = SettingsConfigDict(case_sensitive=True)

settings = Settings()
