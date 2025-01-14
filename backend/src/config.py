
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./app.db'

class TestConfig(Settings):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'