from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application configuration settings."""
    
    # Database
    DATABASE_URL: str
    
    # Application
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    # API
    API_TITLE: str = "FastAPI Backend"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "A production-ready FastAPI backend for managing posts"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()
