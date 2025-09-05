# Upstage 문서파싱 연동 - 다양한 문서 형식에서 텍스트 추출
import json
import logging
import httpx
import sys
import os
from typing import Optional

# 상위 디렉토리를 Python path에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import settings

logger = logging.getLogger(__name__)

class DocumentParser:
    def __init__(self):
        self.api_url = f"{settings.upstage_base_url}/v1/document-ai/document-parse"
        self.headers = {"Authorization": f"Bearer {settings.upstage_api_key}"}
        self.timeout = 60.0

    async def parse_document(self, file_content: bytes, filename: str) -> str:
        """Upstage Document Parser API로 문서에서 텍스트 추출"""
        try:
            files = {"document": (filename, file_content, "application/octet-stream")}
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(self.api_url, headers=self.headers, files=files)

            if response.status_code == 200:
                result = response.json()
                html_content = self._extract_content(result)
                
                # 내용이 원시 JSON 형태인지 확인 (추출 실패 시)
                if html_content.strip().startswith('{') and html_content.strip().endswith('}'):
                    logger.warning("Extracted content appears to be raw JSON, trying fallback")
                    return await self._fallback_extraction(file_content, filename)
                
                return html_content
            else:
                return await self._fallback_extraction(file_content, filename)
                
        except Exception as e:
            logger.error(f"Document parsing failed: {e}")
            return await self._fallback_extraction(file_content, filename)

    def _extract_content(self, result: dict) -> str:
        """API 응답에서 HTML 콘텐츠 추출"""
        if isinstance(result, dict):
            # HTML 콘텐츠 우선 추출
            if "html" in result and isinstance(result["html"], str):
                return result["html"]
            
            # 중첩된 HTML 콘텐츠 확인
            if "content" in result and isinstance(result["content"], dict):
                content = result["content"]
                if "html" in content and isinstance(content["html"], str):
                    return content["html"]
            
            # 마지막 수단: 디버깅용 JSON 문자열 반환
            return json.dumps(result, ensure_ascii=False, indent=2)
        
        return str(result)

    async def _fallback_extraction(self, file_content: bytes, filename: str) -> str:
        """API 실패시 폴백 처리 (간단한 형식만 지원)"""
        try:
            ext = filename.lower().split(".")[-1] if "." in filename else ""
            
            if ext in ["txt", "md"]:
                content = file_content.decode("utf-8", errors="ignore")
            elif ext == "json":
                data = json.loads(file_content.decode("utf-8"))
                content = json.dumps(data, indent=2, ensure_ascii=False)
            else:
                content = file_content.decode("utf-8", errors="ignore")

            if len(content.strip()) < 10:
                raise ValueError("Not enough content extracted")
            
            return content
            
        except Exception as e:
            logger.error(f"Fallback extraction failed: {e}")
            raise ValueError(f"Failed to process file: {e}")
