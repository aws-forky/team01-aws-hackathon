import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    UPSTAGE_API_KEY = os.getenv("UPSTAGE_API_KEY")
    UPSTAGE_DOCUMENT_PARSE_URL = "https://api.upstage.ai/v1/document-ai/document-parse"
    UPSTAGE_CHAT_URL = "https://api.upstage.ai/v1/solar/chat/completions"
    
    if not UPSTAGE_API_KEY:
        raise ValueError("UPSTAGE_API_KEY environment variable is required")

config = Config()
