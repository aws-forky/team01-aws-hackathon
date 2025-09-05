import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    # Upstage API 연결 설정
    upstage_api_key: str = os.getenv("UPSTAGE_API_KEY", "")
    upstage_base_url: str = os.getenv("UPSTAGE_BASE_URL", "https://api.upstage.ai")
    upstage_model: str = os.getenv("UPSTAGE_MODEL", "solar-pro2")
    
    # 성능 최적화 설정
    api_timeout: int = int(os.getenv("API_TIMEOUT", "30"))
    max_text_length: int = int(os.getenv("MAX_TEXT_LENGTH", "2000"))
    max_output_tokens: int = int(os.getenv("MAX_OUTPUT_TOKENS", "6500"))
    rate_limit_interval: float = float(os.getenv("RATE_LIMIT_INTERVAL", "1.0"))

settings = Settings()
