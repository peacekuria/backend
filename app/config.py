import os

# Configuration class for application settings
class Settings:
    """Application configuration settings"""
    # Database URL - read from environment variable or use default SQLite
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Create global settings instance
settings = Settings()


