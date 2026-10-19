import os
from typing import List
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
ENV_DIR = BACKEND_DIR / ".env"

class Settings(BaseSettings):
    API_PREFIX: str = "/api"
    DEBUG: bool = False

    DATABASE_URL: str

    ALLOWED_ORIGINS: List[str] = []

    OPENAI_API_KEY: str

    # Because we are using a string for ALLOWED_ORIGINS, we need to parse it into a list of strings, .env files don't support lists, so we will use a validator to parse the string into a list of strings.
    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_allowed_origins(cls, v: any) -> List[str]:
        if isinstance(v, str):
            if not v.strip():
                return []
            return [origin.strip() for origin in v.split(",")]
        if isinstance(v, list):
            return [str(origin).strip() for origin in v]
        print(f"Allowed origins = {v}")
        return v or []

    model_config = SettingsConfigDict(
        env_file=ENV_DIR,
        env_file_encoding="utf-8",
        extra="ignore"  # Ignore any extra fields in the .env file that are not defined in the Settings class
    )
    
    
settings = Settings()