import httpx
import base64
from config import config

class DocumentParser:
    def __init__(self):
        self.api_key = config.UPSTAGE_API_KEY
        self.parse_url = config.UPSTAGE_DOCUMENT_PARSE_URL
        self.max_file_size = 10 * 1024 * 1024  # 10MB
    
    async def parse_document(self, file_content: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        
        # Decode base64 content
        try:
            file_data = base64.b64decode(file_content)
        except Exception:
            raise ValueError("Invalid base64 file content")
        
        # Check file size
        if len(file_data) > self.max_file_size:
            raise ValueError("File size exceeds 10MB limit")
        
        # Check PDF header
        if not file_data.startswith(b'%PDF'):
            raise ValueError("File is not a valid PDF")
        
        files = {
            "document": ("document.pdf", file_data, "application/pdf")
        }
        
        data = {
            "output_formats": '["html"]'
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.parse_url,
                headers=headers,
                files=files,
                data=data,
                timeout=30.0
            )
            
            if response.status_code != 200:
                raise Exception(f"Document parsing failed: {response.text}")
            
            result = response.json()
            return result.get("html", "")
