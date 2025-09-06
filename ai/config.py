import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    UPSTAGE_API_KEY = os.getenv("UPSTAGE_API_KEY")
    UPSTAGE_DOCUMENT_PARSE_URL = "https://api.upstage.ai/v1/document-ai/document-parse"
    
    # AWS 자격증명
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    
    # 기존 BEDROCK_API_KEY도 유지
    BEDROCK_API_KEY = os.getenv("BEDROCK_API_KEY")
    
    if not UPSTAGE_API_KEY:
        raise ValueError("UPSTAGE_API_KEY environment variable is required")

config = Config()
