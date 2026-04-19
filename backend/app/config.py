"""
Configuration management using Pydantic Settings
Loads environment variables and provides type-safe configuration
"""

from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import List
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    DATABASE_URL: str = Field(
        default="postgresql://postgres:YOUR_DB_PASSWORD@localhost:5432/krishi_drishti",
        description="PostgreSQL database URL"
    )
    
    # JWT Authentication
    SECRET_KEY: str = Field(
        default="",
        min_length=0,
        description="Secret key for JWT token generation (set via environment)"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # OTP Service
    OTP_SERVICE: str = "twilio"  # or "msg91"
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""
    MSG91_AUTH_KEY: str = ""
    MSG91_SENDER_ID: str = "KRISHI"
    MSG91_ROUTE: str = "4"
    OTP_EXPIRY_MINUTES: int = 10
    OTP_MAX_ATTEMPTS: int = 3
    
    # Weather API
    WEATHER_API_KEY: str = ""
    WEATHER_API_URL: str = "https://api.openweathermap.org/data/2.5"
    WEATHER_CACHE_HOURS: int = 3
    IMD_API_KEY: str = ""
    
    # Data.gov.in
    DATA_GOV_API_KEY: str = ""
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 5242880  # 5MB
    UPLOAD_DIR: str = "./uploads"
    ALLOWED_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "pdf"]
    
    # ML Models
    MODEL_DIR: str = "./app/ml_models"
    CROP_MODEL_PATH: str = "./app/ml_models/crop_suitability_model.pkl"
    YIELD_MODEL_PATH: str = "./app/ml_models/yield_prediction_model.pkl"
    OPTIMIZATION_MODEL_PATH: str = "./app/ml_models/optimization_model.pkl"
    
    # OCR Configuration
    TESSERACT_CMD: str = "/usr/bin/tesseract"
    OCR_LANGUAGES: str = "eng+hin+tam+tel+kan"
    OCR_MIN_CONFIDENCE: float = 60.0
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    @validator("ALLOWED_ORIGINS", pre=True)
    def parse_origins(cls, v):
        """Parse comma-separated origins string"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @validator("ALLOWED_EXTENSIONS", pre=True)
    def parse_extensions(cls, v):
        """Parse comma-separated extensions string"""
        if isinstance(v, str):
            return [ext.strip() for ext in v.split(",")]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create global settings instance
settings = Settings()

# Create upload directory if it doesn't exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.MODEL_DIR, exist_ok=True)
