from fastapi import APIRouter, HTTPException, UploadFile, File
from models.responses import DocumentParseResponse
from services.document_parser import DocumentParser

router = APIRouter()
document_parser = DocumentParser()

@router.post("/documents/parse", response_model=DocumentParseResponse)
async def parse_document(file: UploadFile = File(...)):
    try:
        # 파일 내용 읽기
        file_content = await file.read()
        
        # PDF 파일 검증
        if not file_content.startswith(b'%PDF'):
            raise HTTPException(status_code=400, detail="Invalid PDF file")
        
        # 파일 크기 검증 (10MB)
        if len(file_content) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File size exceeds 10MB limit")
        
        html_content = await document_parser.parse_document_bytes(file_content)
        return DocumentParseResponse(html_content=html_content)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
