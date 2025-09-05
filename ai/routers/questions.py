# 질문 생성 및 완전처리 엔드포인트 - 면접 질문 생성 및 전체 파이프라인
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import logging
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.document_parser import DocumentParser
from services.llm_processor import LLMProcessor
from models.requests import QuestionGenerateRequest
from models.responses import QuestionGenerateResponse, ProcessCompleteResponse

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/questions/generate", response_model=QuestionGenerateResponse)
async def generate_questions(request: QuestionGenerateRequest):
    """Generate interview questions based on portfolio text and keywords"""
    try:
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text content is required")
        
        if not request.keywords:
            raise HTTPException(status_code=400, detail="Keywords are required")
        
        processor = LLMProcessor()
        result = await processor.generate_questions(
            request.text, 
            request.keywords, 
            request.company_name
        )
        
        return QuestionGenerateResponse(
            success=True,
            message="Questions generated successfully",
            questions=result["questions"],
            is_fallback=result["is_fallback"],
            fallback_reason=result["fallback_reason"]
        )
        
    except Exception as e:
        logger.error(f"Question generation error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/questions/process-complete", response_model=ProcessCompleteResponse)
async def process_complete(
    file: UploadFile = File(...),
    company_name: Optional[str] = Form(None)
):
    """완전 자동화 파이프라인: 문서파싱 → 키워드추출 → 질문생성"""
    try:
        # 파일 검증
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        content = await file.read()
        if len(content) > 50 * 1024 * 1024:  # 50MB 제한
            raise HTTPException(status_code=413, detail="File too large (max 50MB)")
        
        # 1단계: 문서 파싱
        parser = DocumentParser()
        document_text = await parser.parse_document(content, file.filename)
        
        # 2단계: 키워드 추출
        processor = LLMProcessor()
        keyword_result = await processor.extract_keywords(document_text)
        
        # 3단계: 질문 생성
        question_result = await processor.generate_questions(
            document_text,
            keyword_result["keywords"],
            company_name
        )
        
        # 폴백 사용 여부 수집
        fallback_reasons = []
        if keyword_result["is_fallback"]:
            fallback_reasons.append(f"Keywords: {keyword_result['fallback_reason']}")
        if question_result["is_fallback"]:
            fallback_reasons.append(f"Questions: {question_result['fallback_reason']}")
        
        return ProcessCompleteResponse(
            success=True,
            message="Complete processing finished",
            document_content=document_text,
            keywords=keyword_result["keywords"],
            detailed_keywords=keyword_result.get("detailed_keywords", []),
            questions=question_result["questions"],
            keyword_fallback=keyword_result["is_fallback"],
            question_fallback=question_result["is_fallback"],
            fallback_reasons=fallback_reasons if fallback_reasons else None
        )
        
    except ValueError as e:
        logger.error(f"Processing validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Complete processing error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
