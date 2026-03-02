from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./yondem.db"
    SUPABASE_URL: Optional[str] = None
    SUPABASE_KEY: Optional[str] = None
    BLOCKCHAIN_PROVIDER: Optional[str] = None
    PLATFORM_PRIVATE_KEY: Optional[str] = None
    JWT_SECRET: str = "change-me-in-production-32chars"
    REQUIRE_API_KEY: bool = False
    API_KEY: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
