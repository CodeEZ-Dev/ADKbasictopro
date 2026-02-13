"""
Pydantic Settings fix for compatibility
"""
from pydantic import BaseModel, Field
from typing import List
import os

try:
    from pydantic_settings import BaseSettings
except ImportError:
    # Fallback for older pydantic versions
    from pydantic import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str = Field(default="", env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4", env="OPENAI_MODEL")
    database_url: str = Field(default="postgresql://localhost/adr_analyzer", env="DATABASE_URL")
    database_pool_size: int = Field(default=5, env="DATABASE_POOL_SIZE")
    database_max_overflow: int = Field(default=10, env="DATABASE_MAX_OVERFLOW")
    jira_api_url: str = Field(default="", env="JIRA_API_URL")
    jira_api_token: str = Field(default="", env="JIRA_API_TOKEN")
    jira_username: str = Field(default="", env="JIRA_USERNAME")
    debug: bool = Field(default=False, env="DEBUG")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
