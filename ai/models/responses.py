from pydantic import BaseModel
from typing import List, Optional

class DocumentParseResponse(BaseModel):
    html_content: str
    success: bool = True
    
class KeywordExtractResponse(BaseModel):
    keywords: List[str]
    success: bool = True
    
class QuestionGenerateResponse(BaseModel):
    questions: List[str]
    success: bool = True
    
class FollowingQuestionResponse(BaseModel):
    following_question: str
    success: bool = True
    
class QuestionEvaluateResponse(BaseModel):
    feedback: str
    score: Optional[int] = None
    success: bool = True
    
class AllEvaluateResponse(BaseModel):
    overall_feedback: str
    total_score: Optional[int] = None
    success: bool = True
    
class PortfolioEvaluateResponse(BaseModel):
    portfolio_feedback: str
    completeness_score: Optional[int] = None
    success: bool = True
    
class HealthResponse(BaseModel):
    status: str = "healthy"
    timestamp: str
