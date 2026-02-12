import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv() # Load variables from .env file

class Settings(BaseSettings):
    PROJECT_NAME: str = "Fraud Detection System"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/fraud_detection_db")

    class Config:
        case_sensitive = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Fix for Render or other environments adding quotes or spaces
        if self.DATABASE_URL:
             self.DATABASE_URL = self.DATABASE_URL.strip().strip("'").strip('"')
        # Fix for Supabase/Postgres returning postgres:// which SQLAlchemy 1.4+ dislikes
        if self.DATABASE_URL and self.DATABASE_URL.startswith("postgres://"):
            self.DATABASE_URL = self.DATABASE_URL.replace("postgres://", "postgresql://", 1)

settings = Settings()
