# Assumption: Using dataclasses instead of Pydantic for Python 3.13 compatibility
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

# Enum Types
class QuestionType(str, Enum):
    TECHNICAL = "technical"
    BEHAVIORAL = "behavioral"
    SITUATIONAL = "situational"

class DifficultyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class KeywordCategory(str, Enum):
    LANGUAGE = "language"
    FRAMEWORK = "framework"
    TOOL = "tool"
    DATABASE = "database"
    CLOUD = "cloud"

# Data Models
@dataclass
class Keyword:
    name: str
    category: str
    importance: int

@dataclass
class Question:
    question: str
    answer: str
    type: str
    difficulty: str

@dataclass
class Company:
    name: str
    description: str
    tech_stack: List[str]

@dataclass
class Portfolio:
    text: str
    metadata: dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

# Request Models
@dataclass
class KeywordExtractionRequest:
    text: str

@dataclass
class QuestionGenerationRequest:
    keywords: List[str]
    company: str

# Response Models
@dataclass
class UploadResponse:
    success: bool
    file_id: str
    extracted_text: str
    message: str = ""

@dataclass
class KeywordResponse:
    success: bool
    keywords: List[dict]
    is_fallback: bool = False
    message: str = ""

@dataclass
class QuestionResponse:
    success: bool
    questions: List[dict]
    is_fallback: bool = False
    fallback_reason: str = ""
    message: str = ""

@dataclass
class CompanyListResponse:
    success: bool
    companies: List[dict]

@dataclass
class HealthResponse:
    status: str
    version: str = "1.0.0"

# 기존 기능을 위한 모델들
@dataclass
class FeedbackAnalysis:
    overall_score: int
    star_analysis: dict
    technical_accuracy: dict
    improvement_suggestions: list
    strengths: list
    next_steps: list

@dataclass
class FollowUpQuestion:
    question: str
    type: str  # 깊이_파기, 대안_탐색, 문제_상황, 확장_시나리오, 비즈니스_연결
    intent: str
    difficulty: str
    expected_keywords: list

@dataclass
class InterviewFeedback:
    feedback: FeedbackAnalysis
    follow_up_questions: list
    interviewer_comment: str
    next_action: str

@dataclass
class CompanyProfile:
    name: str
    industry: str
    size: str
    tech_stack: list
    culture_keywords: list
    interview_style: dict
    typical_questions: list
    success_tips: list
    red_flags: list

@dataclass
class PortfolioAnalysis:
    overall_score: int
    target_score: int
    market_fit: int
    detailed_analysis: dict
    priority_improvements: list
    company_specific_advice: str

@dataclass
class InterviewSession:
    session_id: str
    user_id: str
    company: str
    position: str
    interviewer_persona: str
    current_question_depth: int
    max_depth: int
    questions_asked: list
    session_status: str

# 구조화된 질문 시스템을 위한 새로운 모델들
@dataclass
class MainQuestion:
    id: str
    title: str
    content: str
    category: str
    difficulty: str  # Easy, Medium, Hard
    estimated_time: int  # 예상 답변 시간 (분)
    is_completed: bool = False

@dataclass
class FollowUpQuestionNew:
    id: str
    parent_question_id: str
    content: str
    order: int  # 1, 2, 3 순서
    based_on_answer: str = ""  # 이전 답변 기반 생성된 경우

@dataclass
class Answer:
    id: str
    question_id: str
    question_type: str  # main, followup
    content: str
    input_method: str  # text, voice
    timestamp: str
    duration: int  # 답변 시간 (초)
    feedback: Optional[FeedbackAnalysis] = None

@dataclass
class StructuredInterviewSession:
    id: str
    main_questions: List[MainQuestion]
    current_main_question_id: Optional[str]
    follow_up_questions: List[FollowUpQuestionNew]
    completed_main_questions: List[str]
    answers: List[Answer]
    start_time: str
    current_step: str  # selection, main-answer, followup, completed
    current_followup_index: int = 0

@dataclass
class GenerateStructuredQuestionsRequest:
    portfolio_text: str
    company_info: Optional[str] = None
    job_position: Optional[str] = None

@dataclass
class GenerateFollowUpRequest:
    main_question_id: str
    main_question_content: str
    user_answer: str
    followup_count: int = 3

@dataclass
class EvaluateAnswerRequest:
    question: str
    answer: str
    question_type: str  # main, followup
    context: dict = None

@dataclass
class StructuredQuestionsResponse:
    success: bool
    main_questions: List[dict]
    message: str = ""

@dataclass
class FollowUpResponse:
    success: bool
    followup_question: dict
    message: str = ""

@dataclass
class InterviewFeedbackResponse:
    success: bool
    feedback: FeedbackAnalysis
    message: str = ""
