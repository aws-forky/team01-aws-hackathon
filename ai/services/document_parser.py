import httpx
import base64
from config import config

class DocumentParser:
    def __init__(self):
        self.api_key = config.UPSTAGE_API_KEY
        self.parse_url = config.UPSTAGE_DOCUMENT_PARSE_URL
        self.max_file_size = 10 * 1024 * 1024  # 10MB
    
    async def parse_document_bytes(self, file_data: bytes) -> str:
        """바이트 데이터로 문서 파싱"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }
        
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
            
            # content.html에서 HTML 추출
            content = result.get("content", {})
            html_content = content.get("html", "") if isinstance(content, dict) else ""
            
            # 디버깅용 로그
            print(f"=== UPSTAGE RESPONSE DEBUG ===")
            print(f"Status: {response.status_code}")
            print(f"Content type: {type(content)}")
            print(f"Final HTML length: {len(html_content)}")
            print(f"HTML preview: {html_content[:200]}...")
            
            return html_content
    
    async def parse_document(self, file_content: str) -> str:
        """기존 base64 방식 (하위 호환성)"""
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
        
        return await self.parse_document_bytes(file_data)
