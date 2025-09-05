from pydantic import BaseModel
from typing import List, Optional


class KeywordExtractRequest(BaseModel):
    text: str


class QuestionGenerateRequest(BaseModel):
    text: str
    keywords: List[str]
    company_name: Optional[str] = None


class ProcessCompleteRequest(BaseModel):
    company_name: Optional[str] = None
