from pydantic import BaseModel
from typing import List, Optional

class DocumentParseRequest(BaseModel):
    file_content: str  # base64 encoded file content
    
class KeywordExtractRequest(BaseModel):
    html_content: str
    
class QuestionGenerateRequest(BaseModel):
    html_content: str
    question_count: int = 5
    
class FollowingQuestionRequest(BaseModel):
    question: str
    answer: str
    
class QuestionEvaluateRequest(BaseModel):
    question: str
    answer: str
    
class AllEvaluateRequest(BaseModel):
    qa_pairs: List[dict]  # [{"question": str, "answer": str}, ...]
    
class PortfolioEvaluateRequest(BaseModel):
    html_content: str
