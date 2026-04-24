"""
Application configuration loaded from environment variables.
Uses pydantic-settings for type-safe config management.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Gemini API
    GEMINI_API_KEY: str = "your_gemini_api_key_here"
    GEMINI_API_KEY_FALLBACK: str | None = None

    # Session Configuration
    SESSION_TTL_MINUTES: int = 30
    MAX_SESSIONS: int = 500
    MAX_TURNS_PER_SESSION: int = 20
    MAX_IMAGES_PER_SESSION: int = 20

    # Request Limits
    MAX_IMAGE_SIZE_MB: int = 10
    RATE_LIMIT_RPM: int = 10

    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    # App
    DEBUG: bool = False
    LOG_LEVEL: str = "info"

    @property
    def allowed_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    @property
    def max_image_size_bytes(self) -> int:
        return self.MAX_IMAGE_SIZE_MB * 1024 * 1024

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
