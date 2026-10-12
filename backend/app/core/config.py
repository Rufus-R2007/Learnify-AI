"""
Configuration settings for Learnify AI
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Learnify AI"
    
    # CORS Settings
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]
    
    # AI Model Settings (placeholder for future implementation)
    MAX_CONTEXT_LENGTH: int = 10
    DEFAULT_CONFIDENCE_THRESHOLD: float = 0.7
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
