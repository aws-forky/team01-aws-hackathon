# 문서 파싱 엔드포인트 - 파일 업로드 및 텍스트 추출
from fastapi import APIRouter, UploadFile, File, HTTPException
import logging

from services.document_parser import DocumentParser
from models.responses import DocumentParseResponse

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/documents/parse", response_model=DocumentParseResponse)
async def parse_document(file: UploadFile = File(...)):
    """Parse document and extract text content"""
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Validate file size (50MB limit)
        content = await file.read()
        if len(content) > 50 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="File too large (max 50MB)")
        
        parser = DocumentParser()
        extracted_text = await parser.parse_document(content, file.filename)
        
        return DocumentParseResponse(
            success=True,
            message="Document parsed successfully",
            content=extracted_text
        )
        
    except ValueError as e:
        logger.error(f"Document parsing validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Document parsing error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
