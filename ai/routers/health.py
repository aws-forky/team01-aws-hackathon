# 헬스체크 엔드포인트 - 서버 상태 확인
from fastapi import APIRouter
from models.responses import BaseResponse

router = APIRouter()

@router.get("/health", response_model=BaseResponse)
async def health_check():
    """Health check endpoint"""
    return BaseResponse(success=True, message="API is running")
