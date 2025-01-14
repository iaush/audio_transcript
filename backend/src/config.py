import os
from pydantic_settings import BaseSettings
from pathlib import Path

# Default settings for production
class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./app.db"
    UPLOAD_DIR: Path = Path("src/uploads")

    class Config:
        env_file = ".env"  
        env_file_encoding = 'utf-8'

# Override for testing
class TestingSettings(Settings):
    DATABASE_URL: str = "sqlite:///./test.db"  


if "PYTEST_CURRENT_TEST" in os.environ:
    settings = TestingSettings()  # Use testing settings
else:
    settings = Settings()  # Use production settings
