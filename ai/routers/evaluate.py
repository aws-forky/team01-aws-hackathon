from fastapi import APIRouter, HTTPException
from models.requests import AllEvaluateRequest, PortfolioEvaluateRequest
from models.responses import AllEvaluateResponse, PortfolioEvaluateResponse
from services.llm_processor import LLMProcessor

router = APIRouter()
llm_processor = LLMProcessor()

@router.post("/evaluate/all", response_model=AllEvaluateResponse)
async def evaluate_all_answers(request: AllEvaluateRequest):
    try:
        feedback, score = await llm_processor.evaluate_all_answers(request.qa_pairs)
        return AllEvaluateResponse(overall_feedback=feedback, total_score=score)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/evaluate/portfolio", response_model=PortfolioEvaluateResponse)
async def evaluate_portfolio(request: PortfolioEvaluateRequest):
    try:
        feedback, score = await llm_processor.evaluate_portfolio(request.html_content)
        return PortfolioEvaluateResponse(
            portfolio_feedback=feedback, 
            completeness_score=score
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
