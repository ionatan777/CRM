from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "WhatsBackup API"
    API_V1_STR: str = "/api/v1"
    
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: str
    
    SECRET_KEY: str
    DOMAIN: str = "localhost"

    model_config = ConfigDict(
        case_sensitive=True,
        env_file=".env",
        extra="ignore"  # Ignore extra fields from .env
    )

settings = Settings()
