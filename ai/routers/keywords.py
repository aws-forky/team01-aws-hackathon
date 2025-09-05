# 키워드 추출 엔드포인트 - AI 기반 기술 키워드 추출
from fastapi import APIRouter, HTTPException
import logging

from services.llm_processor import LLMProcessor
from models.requests import KeywordExtractRequest
from models.responses import KeywordExtractResponse

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/keywords/extract", response_model=KeywordExtractResponse)
async def extract_keywords(request: KeywordExtractRequest):
    """Extract technical keywords from portfolio text"""
    try:
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text content is required")
        
        processor = LLMProcessor()
        result = await processor.extract_keywords(request.text)
        
        return KeywordExtractResponse(
            success=True,
            message="Keywords extracted successfully",
            keywords=result["keywords"],
            detailed_keywords=result.get("detailed_keywords", []),
            is_fallback=result["is_fallback"],
            fallback_reason=result["fallback_reason"]
        )
        
    except Exception as e:
        logger.error(f"Keyword extraction error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
