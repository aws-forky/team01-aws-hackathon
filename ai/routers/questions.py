from fastapi import APIRouter, HTTPException
from models.requests import (
    QuestionGenerateRequest, 
    FollowingQuestionRequest, 
    QuestionEvaluateRequest
)
from models.responses import (
    QuestionGenerateResponse, 
    FollowingQuestionResponse, 
    QuestionEvaluateResponse
)
from services.llm_processor import LLMProcessor

router = APIRouter()
llm_processor = LLMProcessor()

@router.post("/questions/generate", response_model=QuestionGenerateResponse)
async def generate_questions(request: QuestionGenerateRequest):
    try:
        questions = await llm_processor.generate_questions(
            request.html_content, 
            request.question_count
        )
        return QuestionGenerateResponse(questions=questions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/questions/following", response_model=FollowingQuestionResponse)
async def generate_following_question(request: FollowingQuestionRequest):
    try:
        following_question = await llm_processor.generate_following_question(
            request.question, 
            request.answer
        )
        return FollowingQuestionResponse(following_question=following_question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/questions/evaluate", response_model=QuestionEvaluateResponse)
async def evaluate_answer(request: QuestionEvaluateRequest):
    try:
        feedback, score = await llm_processor.evaluate_answer(
            request.question, 
            request.answer
        )
        return QuestionEvaluateResponse(feedback=feedback, score=score)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
