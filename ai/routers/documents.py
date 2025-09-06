from fastapi import APIRouter, HTTPException
from models.requests import DocumentParseRequest
from models.responses import DocumentParseResponse
from services.document_parser import DocumentParser

router = APIRouter()
document_parser = DocumentParser()

@router.post("/documents/parse", response_model=DocumentParseResponse)
async def parse_document(request: DocumentParseRequest):
    try:
        html_content = await document_parser.parse_document(request.file_content)
        return DocumentParseResponse(html_content=html_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
