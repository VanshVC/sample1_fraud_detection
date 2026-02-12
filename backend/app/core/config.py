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

settings = Settings()
