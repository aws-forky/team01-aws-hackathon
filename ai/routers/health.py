from fastapi import APIRouter
from models.responses import HealthResponse
from datetime import datetime

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat()
    )
