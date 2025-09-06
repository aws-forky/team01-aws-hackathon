# Assumption: Using environment variables for configuration with sensible defaults
import os
from typing import List
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Settings:
    # Upstage API Settings
    UPSTAGE_API_KEY: str = os.getenv("UPSTAGE_API_KEY", "")
    UPSTAGE_BASE_URL: str = os.getenv("UPSTAGE_BASE_URL", "https://api.upstage.ai")
    UPSTAGE_MODEL: str = os.getenv("UPSTAGE_MODEL", "solar-pro2")
    
    # AI Server Settings (External AI Service)
    AI_SERVER_URL: str = "https://ai-f.kms39273.synology.me"
    
    # AI API Endpoints
    DOCUMENT_PARSER_URL: str = f"{AI_SERVER_URL}/api/v1/documents/parse"
    KEYWORD_EXTRACT_URL: str = f"{AI_SERVER_URL}/api/v1/keywords/extract"
    QUESTION_GENERATE_URL: str = f"{AI_SERVER_URL}/api/v1/questions/generate"
    QUESTION_FOLLOWING_URL: str = f"{AI_SERVER_URL}/api/v1/questions/following"
    QUESTION_EVALUATE_URL: str = f"{AI_SERVER_URL}/api/v1/questions/evaluate"
    EVALUATE_ALL_URL: str = f"{AI_SERVER_URL}/api/v1/evaluate/all"
    EVALUATE_PORTFOLIO_URL: str = f"{AI_SERVER_URL}/api/v1/evaluate/portfolio"
    
    API_TIMEOUT: int = int(os.getenv("API_TIMEOUT", "30"))
    MAX_PORTFOLIO_LENGTH: int = int(os.getenv("MAX_PORTFOLIO_LENGTH", "2000"))
    MAX_OUTPUT_TOKENS: int = int(os.getenv("MAX_OUTPUT_TOKENS", "800"))
    
    # Server Settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    CORS_ORIGINS: List[str] = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://10.160.111.161:3000").split(",")
    
    # File Settings
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
    ALLOWED_FILE_TYPES: List[str] = ["application/pdf"]
    UPLOAD_DIR: str = "temp_uploads"
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

settings = Settings()
