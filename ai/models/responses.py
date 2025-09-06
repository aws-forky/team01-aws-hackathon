from pydantic import BaseModel
from typing import List, Optional

class DocumentParseResponse(BaseModel):
    html_content: str
    success: bool = True
    
class KeywordExtractResponse(BaseModel):
    keywords: List[str]
    success: bool = True

class QuestionItem(BaseModel):
    question: str
    tip: str
    
class QuestionGenerateResponse(BaseModel):
    questions: List[QuestionItem]
    success: bool = True
    
class FollowingQuestionResponse(BaseModel):
    following_question: str
    success: bool = True
    
class QuestionEvaluateResponse(BaseModel):
    feedback: str
    success: bool = True
    
class AllEvaluateResponse(BaseModel):
    overall_feedback: str
    success: bool = True
    
class PortfolioEvaluateResponse(BaseModel):
    portfolio_feedback: str
    success: bool = True
    
class HealthResponse(BaseModel):
    status: str = "healthy"
    timestamp: str
