# Forky API 엔드포인트 문서 v2.0

## 개요
Forky v2.0에서는 기능별로 분리된 API 구조를 채택하여 성능과 유지보수성을 향상시켰습니다.

## Base URL
```
http://localhost:8000/api/v1
```

---

## 📄 문서 처리 API

### POST /documents/parse
PDF → HTML 변환

**Request:**
```json
{
  "file": "multipart/form-data"
}
```

**Response:**
```json
{
  "success": true,
  "document_id": "doc_12345",
  "html_content": "<html>...</html>",
  "text_content": "extracted text...",
  "message": "Document parsed successfully"
}
```

---

## 🔍 키워드 추출 API

### POST /keywords/extract
포트폴리오에서 기술 키워드 추출

**Request:**
```json
{
  "text": "포트폴리오 텍스트 내용",
  "document_id": "doc_12345"
}
```

**Response:**
```json
{
  "success": true,
  "document_id": "doc_12345",
  "keywords": [
    {
      "name": "React",
      "category": "framework",
      "importance": 8,
      "confidence": 0.95
    }
  ],
  "total_keywords": 10,
  "message": "Keywords extracted successfully"
}
```

---

## ❓ 질문 생성 API

### POST /questions/generate
메인 질문 생성 (10개)

**Request:**
```json
{
  "portfolio_text": "포트폴리오 내용",
  "keywords": ["React", "Node.js"],
  "company_info": "네이버",
  "job_position": "백엔드 개발자",
  "question_count": 10
}
```

**Response:**
```json
{
  "success": true,
  "questions": [
    {
      "id": "q_12345",
      "title": "React 상태 관리 경험",
      "content": "프로젝트에서 React 상태 관리를 어떻게 구현하셨나요?",
      "category": "React",
      "difficulty": "Medium",
      "estimated_time": 4,
      "tags": ["React", "상태관리"],
      "company_relevance": "네이버"
    }
  ],
  "total_questions": 10,
  "company_info": "네이버",
  "job_position": "백엔드 개발자",
  "message": "Main questions generated successfully"
}
```

### POST /questions/following
꼬리질문 생성 (3개)

**Request:**
```json
{
  "main_question_id": "q_12345",
  "main_question_content": "React 상태 관리 경험에 대해 설명해주세요",
  "user_answer": "Redux를 사용하여 전역 상태를 관리했습니다...",
  "context": {
    "portfolio_text": "포트폴리오 내용",
    "company_info": "네이버"
  },
  "followup_count": 3
}
```

**Response:**
```json
{
  "success": true,
  "main_question_id": "q_12345",
  "following_questions": [
    {
      "id": "following_q_12345_1",
      "parent_question_id": "q_12345",
      "content": "Redux의 단점을 해결하기 위해 어떤 대안을 고려해보셨나요?",
      "type": "deepening",
      "intent": "더 자세한 설명 요청",
      "order": 1,
      "difficulty": "intermediate",
      "expected_keywords": ["Redux", "상태관리"],
      "based_on_answer": "Redux를 사용하여 전역 상태를 관리했습니다..."
    }
  ],
  "total_following": 3,
  "context": {},
  "message": "Following questions generated successfully"
}
```

---

## 📊 평가 API

### POST /questions/evaluate
개별 답변 평가 및 피드백

**Request:**
```json
{
  "question_id": "q_12345",
  "question_content": "React 상태 관리 경험에 대해 설명해주세요",
  "answer_content": "Redux를 사용하여...",
  "question_type": "main",
  "answer_method": "text",
  "context": {
    "answer_duration": 120,
    "timestamp": "2024-12-19T10:00:00Z"
  }
}
```

**Response:**
```json
{
  "success": true,
  "question_id": "q_12345",
  "evaluation": {
    "overall_score": 85,
    "detailed_scores": {
      "content_quality": 85,
      "technical_accuracy": 90,
      "structure_score": 80,
      "communication_score": 85
    },
    "star_analysis": {
      "situation": {"present": true, "quality": "good"},
      "task": {"present": true, "quality": "good"},
      "action": {"present": true, "quality": "excellent"},
      "result": {"present": false, "suggestion": "정량적 결과 지표 추가"}
    },
    "technical_analysis": {
      "score": 90,
      "correct_concepts": ["Redux", "상태관리"],
      "missing_details": []
    },
    "strengths": ["구체적인 기술 스택 언급", "실무 경험 기반 답변"],
    "weaknesses": ["정량적 결과 부족"],
    "recommendations": ["성과 지표 추가", "구체적 예시 보완"],
    "answer_time": 120,
    "word_count": 45
  },
  "question_type": "main",
  "answer_method": "text",
  "timestamp": "2024-12-19T10:00:00Z",
  "message": "Answer evaluation completed successfully"
}
```

### POST /evaluate/all
전체 면접 결과 평가

**Request:**
```json
{
  "session_id": "session_12345",
  "interview_data": {},
  "answers": [
    {
      "question_id": "q_12345",
      "answer_content": "답변 내용",
      "evaluation": {}
    }
  ],
  "questions": [
    {
      "id": "q_12345",
      "title": "질문 제목",
      "category": "React"
    }
  ],
  "session_info": {
    "total_duration": 1800,
    "completed_at": "2024-12-19T10:30:00Z"
  }
}
```

**Response:**
```json
{
  "success": true,
  "session_id": "session_12345",
  "overall_evaluation": {
    "total_score": 82,
    "grade": "B",
    "completion_rate": 100,
    "total_questions": 40,
    "total_duration": 1800,
    "average_answer_time": 45
  },
  "category_scores": {
    "React": 85,
    "JavaScript": 80,
    "Node.js": 78
  },
  "detailed_analysis": {
    "strengths": ["기술적 깊이", "실무 경험"],
    "weaknesses": ["정량적 지표 부족"],
    "improvement_areas": ["성과 측정", "비즈니스 임팩트"],
    "technical_skills": {},
    "soft_skills": {}
  },
  "recommendations": {
    "immediate_actions": ["STAR 기법 연습"],
    "long_term_goals": ["기술 블로그 작성"],
    "study_plan": ["알고리즘 학습"],
    "next_interview_tips": ["구체적 예시 준비"]
  },
  "benchmark": {
    "industry_average": 75,
    "position_average": 78,
    "percentile": 85
  },
  "generated_at": "2024-12-19T10:30:00Z",
  "message": "Complete interview evaluation generated successfully"
}
```

### POST /evaluate/portfolio
포트폴리오 완성도 평가

**Request:**
```json
{
  "portfolio_text": "포트폴리오 내용",
  "target_company": "네이버",
  "target_position": "백엔드 개발자",
  "evaluation_criteria": ["기술스택", "프로젝트경험"]
}
```

**Response:**
```json
{
  "success": true,
  "portfolio_evaluation": {
    "overall_score": 78,
    "target_score": 85,
    "market_fit_score": 80,
    "completeness_percentage": 85
  },
  "detailed_analysis": {
    "technical_skills": {
      "present_skills": ["React", "Node.js"],
      "missing_skills": ["Docker", "AWS"],
      "skill_depth_score": 75
    },
    "project_descriptions": {
      "clarity_score": 80,
      "quantification_score": 60,
      "star_usage": 70
    },
    "missing_elements": ["정량적 성과", "팀워크 경험"],
    "strong_points": ["기술적 깊이", "프로젝트 다양성"]
  },
  "improvement_suggestions": [
    {
      "category": "성과 지표 정량화",
      "priority": "high",
      "suggestion": "프로젝트 결과를 구체적인 수치로 표현",
      "example": "사용자 만족도 4.2에서 4.7로 12% 향상",
      "impact_level": "high",
      "effort_required": "low",
      "estimated_time": "2-3일"
    }
  ],
  "company_specific_advice": "네이버는 기술적 깊이를 중요시하므로...",
  "benchmark": {
    "industry_average": 72,
    "position_average": 75,
    "top_10_percent": 88
  },
  "target_company": "네이버",
  "target_position": "백엔드 개발자",
  "message": "Portfolio evaluation completed successfully"
}
```

---

## 🏥 시스템 API

### GET /health
시스템 상태 확인

**Response:**
```json
{
  "status": "healthy",
  "version": "2.0.0",
  "timestamp": "2024-12-19T10:00:00Z",
  "services": {
    "document_parser": "healthy",
    "ai_service": "healthy",
    "feedback_service": "healthy",
    "database": "healthy"
  },
  "uptime": "24h 30m",
  "memory_usage": "45%",
  "cpu_usage": "12%",
  "active_sessions": 0,
  "message": "All systems operational"
}
```

---

## 🔄 레거시 API 지원

기존 API와의 호환성을 위해 다음 엔드포인트들이 유지됩니다:

- `POST /api/upload` → `POST /api/v1/documents/parse`
- `POST /api/extract-keywords` → `POST /api/v1/keywords/extract`
- `POST /api/generate-questions` → `POST /api/v1/questions/generate`
- `GET /health` → `GET /api/v1/health`

---

## 📝 에러 응답 형식

모든 API는 일관된 에러 응답 형식을 사용합니다:

```json
{
  "success": false,
  "error": "상세 에러 메시지",
  "error_code": "VALIDATION_ERROR",
  "message": "사용자 친화적 메시지",
  "timestamp": "2024-12-19T10:00:00Z"
}
```

## 🔐 인증 및 보안

- 현재 버전에서는 API 키 인증을 사용하지 않습니다
- HTTPS 사용 권장 (음성 인식 기능을 위해 필수)
- CORS 설정으로 허용된 도메인에서만 접근 가능

## 📊 Rate Limiting

- 일반 API: 분당 100회 요청
- 문서 파싱: 분당 10회 요청
- 질문 생성: 분당 20회 요청
- 평가 API: 분당 50회 요청

## 🚀 성능 최적화

- 응답 시간: 평균 < 3초
- 문서 파싱: < 10초
- 질문 생성: < 5초
- 답변 평가: < 2초