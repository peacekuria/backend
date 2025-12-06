import os

class Settings:
    """Application configuration settings"""
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")

settings = Settings()

