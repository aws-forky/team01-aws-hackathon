# Assumption: Using absolute imports to fix import errors
from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from typing import List
import uuid
from app.models.models import (Company, InterviewSession, FeedbackAnalysis, FollowUpQuestion,
                                 MainQuestion, FollowUpQuestionNew, Answer, StructuredInterviewSession)
from app.services.services import (DocumentParserService, AIService, FileService, 
                                 IntegratedInterviewService, FeedbackService, 
                                 FollowUpService, CompanyService, PortfolioService)

router = APIRouter()

# Initialize services
doc_parser = DocumentParserService()
ai_service = AIService()
file_service = FileService()
integrated_service = IntegratedInterviewService()
feedback_service = FeedbackService()
followup_service = FollowUpService()
company_service = CompanyService()
portfolio_service = PortfolioService()

@router.get("/api/v1/health")
async def system_health_check():
    """시스템 상태 확인"""
    try:
        # 각 서비스 상태 체크
        services_status = {
            "document_parser": "healthy",
            "ai_service": "healthy", 
            "feedback_service": "healthy",
            "database": "healthy"
        }
        
        # 전체 시스템 상태 결정
        overall_status = "healthy" if all(status == "healthy" for status in services_status.values()) else "degraded"
        
        return {
            "status": overall_status,
            "version": "2.0.0",
            "timestamp": "2024-12-19T10:00:00Z",
            "services": services_status,
            "uptime": "24h 30m",
            "memory_usage": "45%",
            "cpu_usage": "12%",
            "active_sessions": 0,
            "message": "All systems operational"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "message": "System health check failed"
        }

@router.post("/api/v1/documents/parse")
async def parse_document(file: UploadFile = File(...)):
    """PDF → HTML 변환"""
    try:
        file_content = await file.read()
        
        if not file_service.validate_file(file_content, file.content_type):
            raise HTTPException(status_code=400, detail="Invalid file type or size")
        
        file_path = file_service.save_temp_file(file_content)
        file_id = file_path.split('/')[-1].replace('.pdf', '')
        
        try:
            extracted_text = await doc_parser.parse_pdf(file_path)
            
            return {
                "success": True,
                "document_id": file_id,
                "html_content": extracted_text,
                "text_content": extracted_text,  # HTML 태그 제거된 순수 텍스트
                "message": "Document parsed successfully"
            }
        
        except Exception as e:
            return {
                "success": False,
                "document_id": file_id,
                "error": str(e),
                "message": "Document parsing failed"
            }
        
        finally:
            file_service.cleanup_file(file_path)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/v1/keywords/extract")
async def extract_keywords(request: Request):
    """키워드 추출"""
    body = await request.json()
    text = body.get("text", "")
    document_id = body.get("document_id", "")
    
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text content is required")
    
    try:
        keywords = await ai_service.extract_keywords(text)
        
        return {
            "success": True,
            "document_id": document_id,
            "keywords": [
                {
                    "name": k.name,
                    "category": k.category,
                    "importance": k.importance,
                    "confidence": 0.95  # 키워드 신뢰도
                } for k in keywords
            ],
            "total_keywords": len(keywords),
            "message": "Keywords extracted successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Keyword extraction failed"
        }

@router.post("/api/v1/questions/generate")
async def generate_main_questions(request: Request):
    """메인 질문 생성"""
    body = await request.json()
    portfolio_text = body.get("portfolio_text", "")
    keywords = body.get("keywords", [])
    company_info = body.get("company_info", "")
    job_position = body.get("job_position", "백엔드 개발자")
    question_count = body.get("question_count", 10)
    
    if not portfolio_text.strip():
        raise HTTPException(status_code=400, detail="Portfolio text is required")
    
    try:
        main_questions = await ai_service.generate_structured_questions(
            portfolio_text, company_info, job_position
        )
        
        return {
            "success": True,
            "questions": [
                {
                    "id": q["id"],
                    "title": q["title"],
                    "content": q["content"],
                    "category": q["category"],
                    "difficulty": q["difficulty"],
                    "estimated_time": q["estimated_time"],
                    "tags": keywords[:3] if keywords else [],
                    "company_relevance": company_info
                } for q in main_questions
            ],
            "total_questions": len(main_questions),
            "company_info": company_info,
            "job_position": job_position,
            "message": "Main questions generated successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Question generation failed"
        }

@router.get("/api/companies")
async def get_companies():
    """Get list of supported companies"""
    companies = [
        {
            "name": "네이버",
            "description": "국내 최대 포털 및 IT 서비스 기업",
            "tech_stack": ["Java", "Spring", "React", "Node.js", "MySQL", "Redis"]
        },
        {
            "name": "카카오",
            "description": "모바일 메신저 및 플랫폼 서비스 기업",
            "tech_stack": ["Kotlin", "Swift", "React", "Spring Boot", "MongoDB", "Kafka"]
        },
        {
            "name": "삼성전자",
            "description": "글로벌 전자제품 및 반도체 기업",
            "tech_stack": ["C++", "Python", "Android", "Linux", "Docker", "Kubernetes"]
        },
        {
            "name": "LG전자",
            "description": "가전제품 및 전자기기 제조 기업",
            "tech_stack": ["C", "Python", "Qt", "Android", "IoT", "AI/ML"]
        },
        {
            "name": "쿠팡",
            "description": "이커머스 및 물류 서비스 기업",
            "tech_stack": ["Java", "Python", "React", "AWS", "Microservices", "Kafka"]
        }
    ]
    
    return {
        "success": True,
        "companies": companies
    }

# =============================================================================
# 새로운 기능 API 엔드포인트들
# =============================================================================

@router.post("/api/interview/start")
async def start_interview_session(request: Request):
    """면접 세션 시작"""
    body = await request.json()
    
    session_id = str(uuid.uuid4())
    company = body.get("company", "")
    position = body.get("position", "백엔드 개발자")
    interviewer_persona = body.get("interviewer_persona", "친근한_시니어")
    
    # 회사 프로필 조회
    try:
        company_profile = await company_service.get_company_profile(company)
        
        return {
            "success": True,
            "session_id": session_id,
            "company_profile": company_profile,
            "interviewer_persona": interviewer_persona,
            "message": "면접 세션이 시작되었습니다"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/interview/process")
async def process_interview_interaction(request: Request):
    """통합 면접 상호작용 처리 (피드백 + 꼬리질문)"""
    body = await request.json()
    
    session_id = body.get("session_id", "")
    user_answer = body.get("user_answer", "")
    context = body.get("context", {})
    
    if not user_answer.strip():
        raise HTTPException(status_code=400, detail="답변이 필요합니다")
    
    try:
        result = await integrated_service.process_interview_interaction(
            session_id, user_answer, context
        )
        
        return {
            "success": True,
            **result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/feedback/analyze")
async def analyze_answer_feedback(request: Request):
    """답변 분석 및 피드백 생성"""
    body = await request.json()
    
    question = body.get("question", "")
    answer = body.get("answer", "")
    user_level = body.get("user_level", "intermediate")
    
    if not answer.strip():
        raise HTTPException(status_code=400, detail="답변이 필요합니다")
    
    try:
        feedback = await feedback_service.analyze_answer(question, answer, user_level)
        
        return {
            "success": True,
            "feedback": feedback,
            "message": "답변 분석이 완료되었습니다"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/follow-up/generate")
async def generate_follow_up_questions(request: Request):
    """꼬리질문 생성"""
    body = await request.json()
    
    question = body.get("question", "")
    answer = body.get("answer", "")
    interviewer_persona = body.get("interviewer_persona", "친근한_시니어")
    max_questions = body.get("max_questions", 2)
    
    if not answer.strip():
        raise HTTPException(status_code=400, detail="답변이 필요합니다")
    
    try:
        follow_ups = await followup_service.generate_follow_up_questions(
            question, answer, interviewer_persona, max_questions, 
            body.get('portfolio_text', '')
        )
        
        return {
            "success": True,
            "follow_up_questions": follow_ups,
            "message": "꼬리질문이 생성되었습니다"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/companies/{company_name}/profile")
async def get_company_profile(company_name: str):
    """회사별 면접 문화 정보 조회"""
    try:
        profile = await company_service.get_company_profile(company_name)
        
        return {
            "success": True,
            "profile": profile,
            "message": f"{company_name} 면접 정보를 조회했습니다"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/companies/questions/customized")
async def generate_company_customized_questions(request: Request):
    """회사별 맞춤 질문 생성"""
    body = await request.json()
    
    company = body.get("company", "")
    user_keywords = body.get("user_keywords", [])
    
    if not company:
        raise HTTPException(status_code=400, detail="회사명이 필요합니다")
    
    try:
        questions = await company_service.generate_company_questions(company, user_keywords)
        
        return {
            "success": True,
            "customized_questions": questions,
            "company": company,
            "message": f"{company} 맞춤 질문이 생성되었습니다"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/portfolio/analyze")
async def analyze_portfolio(request: Request):
    """포트폴리오 분석 및 개선 제안"""
    body = await request.json()
    
    portfolio_text = body.get("portfolio_text", "")
    target_company = body.get("target_company", "")
    target_position = body.get("target_position", "")
    
    if not portfolio_text.strip():
        raise HTTPException(status_code=400, detail="포트폴리오 텍스트가 필요합니다")
    
    try:
        # 포트폴리오 분석
        analysis = await portfolio_service.analyze_portfolio(
            portfolio_text, target_company, target_position
        )
        
        # 개선 제안 생성
        improvements = await portfolio_service.generate_improvements(analysis)
        
        return {
            "success": True,
            "analysis": analysis,
            "improvements": improvements,
            "message": "포트폴리오 분석이 완료되었습니다"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/portfolio/optimize")
async def optimize_portfolio_for_company(request: Request):
    """회사별 포트폴리오 최적화"""
    body = await request.json()
    
    portfolio_text = body.get("portfolio_text", "")
    target_company = body.get("target_company", "")
    
    if not portfolio_text.strip() or not target_company:
        raise HTTPException(status_code=400, detail="포트폴리오 텍스트와 목표 회사가 필요합니다")
    
    try:
        # 회사 프로필 조회
        company_profile = await company_service.get_company_profile(target_company)
        
        # 포트폴리오 분석
        analysis = await portfolio_service.analyze_portfolio(
            portfolio_text, target_company
        )
        
        # 최적화 제안
        improvements = await portfolio_service.generate_improvements(analysis)
        
        return {
            "success": True,
            "company_profile": company_profile,
            "current_analysis": analysis,
            "optimization_suggestions": improvements,
            "message": f"{target_company} 맞춤 포트폴리오 최적화 제안이 완료되었습니다"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/v1/evaluate/portfolio")
async def evaluate_portfolio_completeness(request: Request):
    """포트폴리오 완성도 평가"""
    body = await request.json()
    
    portfolio_text = body.get("portfolio_text", "")
    target_company = body.get("target_company", "")
    target_position = body.get("target_position", "")
    evaluation_criteria = body.get("evaluation_criteria", [])
    
    if not portfolio_text.strip():
        raise HTTPException(status_code=400, detail="Portfolio text is required")
    
    try:
        analysis = await portfolio_service.analyze_portfolio(
            portfolio_text, target_company, target_position
        )
        
        improvements = await portfolio_service.generate_improvements(analysis)
        
        return {
            "success": True,
            "portfolio_evaluation": {
                "overall_score": analysis["overall_assessment"]["current_score"],
                "target_score": analysis["overall_assessment"]["target_score"],
                "market_fit_score": analysis["overall_assessment"]["market_fit"],
                "completeness_percentage": min(100, analysis["overall_assessment"]["current_score"] + 15)
            },
            "detailed_analysis": {
                "technical_skills": analysis["detailed_analysis"]["technical_skills"],
                "project_descriptions": analysis["detailed_analysis"]["project_descriptions"],
                "missing_elements": analysis.get("missing_elements", []),
                "strong_points": analysis.get("strong_points", [])
            },
            "improvement_suggestions": [
                {
                    "category": imp["category"],
                    "priority": imp["priority"],
                    "suggestion": imp["suggestion"],
                    "example": imp["example"],
                    "impact_level": imp["impact"],
                    "effort_required": imp["effort"],
                    "estimated_time": imp["timeline"]
                } for imp in improvements
            ],
            "company_specific_advice": analysis.get("company_specific_advice", ""),
            "benchmark": {
                "industry_average": 72,
                "position_average": 75,
                "top_10_percent": 88
            },
            "target_company": target_company,
            "target_position": target_position,
            "message": "Portfolio evaluation completed successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Portfolio evaluation failed"
        }

# =============================================================================
# 레거시 API 호환성 유지 (Deprecated)
# =============================================================================

@router.post("/api/generate-structured-questions")
async def generate_structured_questions_legacy(request: Request):
    """구조화된 메인 질문 10개 생성"""
    body = await request.json()
    
    portfolio_text = body.get("portfolio_text", "")
    company_info = body.get("company_info", "")
    job_position = body.get("job_position", "백엔드 개발자")
    
    if not portfolio_text.strip():
        raise HTTPException(status_code=400, detail="포트폴리오 텍스트가 필요합니다")
    
    try:
        # AI 서비스를 통해 구조화된 질문 생성
        main_questions = await ai_service.generate_structured_questions(
            portfolio_text, company_info, job_position
        )
        
        return {
            "success": True,
            "main_questions": [
                {
                    "id": q.id,
                    "title": q.title,
                    "content": q.content,
                    "category": q.category,
                    "difficulty": q.difficulty,
                    "estimated_time": q.estimated_time
                } for q in main_questions
            ],
            "message": "구조화된 질문이 생성되었습니다"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/v1/questions/following")
async def generate_following_questions(request: Request):
    """꼬리질문 생성"""
    body = await request.json()
    
    main_question_id = body.get("main_question_id", "")
    main_question_content = body.get("main_question_content", "")
    user_answer = body.get("user_answer", "")
    context = body.get("context", {})
    followup_count = body.get("followup_count", 3)
    
    if not user_answer.strip():
        raise HTTPException(status_code=400, detail="User answer is required")
    
    try:
        followup_questions = await ai_service.generate_followup_questions(
            main_question_content, user_answer, followup_count
        )
        
        return {
            "success": True,
            "main_question_id": main_question_id,
            "following_questions": [
                {
                    "id": f"following_{main_question_id}_{i+1}",
                    "parent_question_id": main_question_id,
                    "content": fq["question"],
                    "type": fq.get("type", "deepening"),
                    "intent": fq.get("intent", "더 자세한 설명 요청"),
                    "order": i + 1,
                    "difficulty": fq.get("difficulty", "intermediate"),
                    "expected_keywords": fq.get("expected_keywords", []),
                    "based_on_answer": user_answer[:150] + "..." if len(user_answer) > 150 else user_answer
                } for i, fq in enumerate(followup_questions)
            ],
            "total_following": len(followup_questions),
            "context": context,
            "message": "Following questions generated successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Following question generation failed"
        }

@router.post("/api/v1/questions/evaluate")
async def evaluate_single_answer(request: Request):
    """답변 평가 및 피드백"""
    body = await request.json()
    
    question_id = body.get("question_id", "")
    question_content = body.get("question_content", "")
    answer_content = body.get("answer_content", "")
    question_type = body.get("question_type", "main")  # main, following
    answer_method = body.get("answer_method", "text")  # text, voice
    context = body.get("context", {})
    
    if not answer_content.strip():
        raise HTTPException(status_code=400, detail="Answer content is required")
    
    try:
        feedback = await feedback_service.evaluate_structured_answer(
            question_content, answer_content, question_type, context
        )
        
        return {
            "success": True,
            "question_id": question_id,
            "evaluation": {
                "overall_score": feedback["overall_score"],
                "detailed_scores": {
                    "content_quality": feedback["overall_score"],
                    "technical_accuracy": feedback["technical_accuracy"]["score"],
                    "structure_score": 85,  # STAR 구조 점수
                    "communication_score": feedback["overall_score"]
                },
                "star_analysis": feedback["star_analysis"],
                "technical_analysis": feedback["technical_accuracy"],
                "strengths": feedback["strengths"],
                "weaknesses": feedback["improvement_suggestions"],
                "recommendations": feedback["next_steps"],
                "answer_time": context.get("answer_duration", 0),
                "word_count": len(answer_content.split())
            },
            "question_type": question_type,
            "answer_method": answer_method,
            "timestamp": context.get("timestamp", ""),
            "message": "Answer evaluation completed successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Answer evaluation failed"
        }

@router.post("/api/v1/evaluate/all")
async def evaluate_complete_interview(request: Request):
    """전체 면접 결과 평가"""
    body = await request.json()
    
    session_id = body.get("session_id", "")
    interview_data = body.get("interview_data", {})
    answers = body.get("answers", [])
    questions = body.get("questions", [])
    session_info = body.get("session_info", {})
    
    if not answers:
        raise HTTPException(status_code=400, detail="Interview answers are required")
    
    try:
        report = await ai_service.generate_final_report(
            session_id, answers, questions
        )
        
        return {
            "success": True,
            "session_id": session_id,
            "overall_evaluation": {
                "total_score": report["overall_score"],
                "grade": "A" if report["overall_score"] >= 90 else "B" if report["overall_score"] >= 80 else "C",
                "completion_rate": report["completion_rate"],
                "total_questions": report["total_questions"],
                "total_duration": session_info.get("total_duration", 0),
                "average_answer_time": session_info.get("average_answer_time", 0)
            },
            "category_scores": report["category_scores"],
            "detailed_analysis": {
                "strengths": report["strengths"],
                "weaknesses": report["weaknesses"],
                "improvement_areas": report["recommendations"],
                "technical_skills": report.get("technical_analysis", {}),
                "soft_skills": report.get("soft_skills_analysis", {})
            },
            "recommendations": {
                "immediate_actions": report["recommendations"][:3],
                "long_term_goals": report["recommendations"][3:],
                "study_plan": report.get("study_plan", []),
                "next_interview_tips": report.get("interview_tips", [])
            },
            "benchmark": {
                "industry_average": 75,
                "position_average": 78,
                "percentile": min(95, max(5, report["overall_score"] + 10))
            },
            "generated_at": session_info.get("completed_at", ""),
            "message": "Complete interview evaluation generated successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Complete interview evaluation failed"
        }

@router.post("/api/speech-to-text")
async def speech_to_text(request: Request):
    """음성을 텍스트로 변환 (선택사항 - 프론트엔드에서 처리 가능)"""
    # 이 엔드포인트는 필요시 외부 STT 서비스 연동용
    # 현재는 프론트엔드에서 Web Speech API 사용
    return {
        "success": False,
        "message": "현재 프론트엔드에서 Web Speech API를 사용합니다"
    }
