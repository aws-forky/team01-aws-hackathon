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
    
    # Legacy API Settings (fallback)
    API_BASE_URL: str = "https://forky-ai.kms39273.synology.me"
    DOCUMENT_PARSER_URL: str = f"{API_BASE_URL}/api/v1/documents/parse"
    KEYWORD_EXTRACT_URL: str = f"{API_BASE_URL}/api/v1/keywords/extract"
    QUESTION_GENERATE_URL: str = f"{API_BASE_URL}/api/v1/questions/generate"
    
    # 새로운 기능 API URLs
    FEEDBACK_ANALYZE_URL: str = f"{API_BASE_URL}/api/v1/feedback/analyze"
    FOLLOW_UP_GENERATE_URL: str = f"{API_BASE_URL}/api/v1/follow-up/generate"
    COMPANY_PROFILE_URL: str = f"{API_BASE_URL}/api/v1/companies"
    PORTFOLIO_ANALYZE_URL: str = f"{API_BASE_URL}/api/v1/portfolio/analyze"
    
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
