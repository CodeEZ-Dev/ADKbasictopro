import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Gemini Configuration
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-pro")
    
    # Database Configuration
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./adr_analyzer.db")
    database_pool_size: int = int(os.getenv("DATABASE_POOL_SIZE", 5))
    database_max_overflow: int = int(os.getenv("DATABASE_MAX_OVERFLOW", 10))
    
    # JIRA Configuration
    jira_api_url: str = os.getenv("JIRA_API_URL", "")
    jira_api_token: str = os.getenv("JIRA_API_TOKEN", "")
    jira_username: str = os.getenv("JIRA_USERNAME", "")
    
    # Server Configuration
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
