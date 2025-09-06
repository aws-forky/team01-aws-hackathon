from fastapi import APIRouter, HTTPException
from models.requests import KeywordExtractRequest
from models.responses import KeywordExtractResponse
from services.llm_processor import LLMProcessor

router = APIRouter()
llm_processor = LLMProcessor()

@router.post("/keywords/extract", response_model=KeywordExtractResponse)
async def extract_keywords(request: KeywordExtractRequest):
    try:
        keywords = await llm_processor.extract_keywords(request.html_content)
        return KeywordExtractResponse(keywords=keywords)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
