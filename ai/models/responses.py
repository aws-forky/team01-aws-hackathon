from pydantic import BaseModel
from typing import List, Optional, Any


class BaseResponse(BaseModel):
    success: bool
    message: str


class DocumentParseResponse(BaseResponse):
    content: Optional[str] = None


class KeywordResponse(BaseModel):
    tech: str
    category: str
    reason: str


class KeywordExtractResponse(BaseResponse):
    keywords: Optional[List[str]] = None
    detailed_keywords: Optional[List[KeywordResponse]] = None
    is_fallback: bool = False
    fallback_reason: Optional[str] = None


class QuestionResponse(BaseModel):
    id: str
    type: str
    text: str
    explanation: str


class QuestionGenerateResponse(BaseResponse):
    questions: Optional[List[QuestionResponse]] = None
    is_fallback: bool = False
    fallback_reason: Optional[str] = None


class ProcessCompleteResponse(BaseResponse):
    document_content: Optional[str] = None
    keywords: Optional[List[str]] = None
    detailed_keywords: Optional[List[KeywordResponse]] = None
    questions: Optional[List[QuestionResponse]] = None
    keyword_fallback: bool = False
    question_fallback: bool = False
    fallback_reasons: Optional[List[str]] = None
from pydantic import BaseModel
from typing import List, Optional, Any


class BaseResponse(BaseModel):
    success: bool
    message: str


class DocumentParseResponse(BaseResponse):
    content: Optional[str] = None


class KeywordResponse(BaseModel):
    tech: str
    category: str
    reason: str


class KeywordExtractResponse(BaseResponse):
    keywords: Optional[List[str]] = None
    detailed_keywords: Optional[List[KeywordResponse]] = None
    is_fallback: bool = False
    fallback_reason: Optional[str] = None


class QuestionResponse(BaseModel):
    id: str
    type: str
    text: str
    explanation: str


class QuestionGenerateResponse(BaseResponse):
    questions: Optional[List[QuestionResponse]] = None
    is_fallback: bool = False
    fallback_reason: Optional[str] = None


class ProcessCompleteResponse(BaseResponse):
    document_content: Optional[str] = None
    keywords: Optional[List[str]] = None
    detailed_keywords: Optional[List[KeywordResponse]] = None
    questions: Optional[List[QuestionResponse]] = None
    keyword_fallback: bool = False
    question_fallback: bool = False
    fallback_reasons: Optional[List[str]] = None
