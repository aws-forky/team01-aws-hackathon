# Forky 통합 기능 요구사항 명세서

## 📋 문서 개요

**프로젝트**: Forky - AI 기반 포트폴리오 기술면접 시뮬레이터
**버전**: v2.0 (통합 버전)
**작성일**: 2024년 12월
**목적**: 개발자를 위한 프롬프트 친화적 상세 기능 명세

---

## 🎯 핵심 기능 3개 + 꼬리질문 시스템

### 기능 1: 실시간 면접 피드백 시스템
### 기능 2: 회사별 면접 문화 데이터베이스  
### 기능 3: 포트폴리오 자동 개선 제안
### 기능 4: AI 꼬리질문 시스템 (신규)

---

## 🔥 기능 1: 실시간 면접 피드백 + 꼬리질문 시스템

### 1.1 기능 개요
```yaml
기능명: AI 기반 실시간 면접 피드백 + 꼬리질문 엔진
목적: 사용자 답변을 즉시 분석하여 피드백 제공 + 실제 면접관처럼 심화 질문 생성
핵심가치: 실제 면접 상황 완벽 재현
처리시간: 3초 이내 (피드백 + 꼬리질문 동시 생성)
```

### 1.2 답변 분석 엔진
```python
# 프롬프트용 분석 구조
ANSWER_ANALYSIS_PROMPT = """
당신은 10년차 IT 기술면접관입니다. 사용자의 답변을 다음 기준으로 분석하세요:

[분석 항목]
1. STAR 기법 완성도 (Situation, Task, Action, Result)
2. 기술적 정확성 (언급된 기술의 올바른 이해도)
3. 구체성 수준 (정량적 지표, 구체적 사례)
4. 논리적 구조 (답변의 일관성 및 흐름)

[출력 형식]
{
  "overall_score": 85,
  "star_analysis": {
    "situation": {"present": true, "quality": "good", "suggestion": "더 구체적인 상황 설명"},
    "task": {"present": true, "quality": "excellent", "suggestion": null},
    "action": {"present": true, "quality": "good", "suggestion": "기술적 선택 이유 추가"},
    "result": {"present": false, "quality": null, "suggestion": "정량적 결과 지표 필수"}
  },
  "technical_accuracy": {
    "score": 90,
    "correct_concepts": ["Redis 캐싱", "API 최적화"],
    "missing_details": ["캐시 무효화 전략"]
  },
  "improvement_suggestions": [
    "결과 부분에 구체적 수치 추가",
    "기술 선택 근거 설명 보완"
  ]
}

질문: {question}
답변: {user_answer}
"""
```

### 1.3 꼬리질문 생성 엔진
```python
# 5가지 꼬리질문 패턴 프롬프트
FOLLOW_UP_PATTERNS = {
    "깊이_파기": {
        "trigger": "표면적 답변 감지",
        "prompt": """
        사용자가 '{기술}'에 대해 언급했지만 구체적 구현 방법이 부족합니다.
        실제 면접관처럼 구체적인 구현 세부사항을 묻는 자연스러운 질문을 생성하세요.
        
        템플릿: "구체적으로 {기술/과정}은 어떻게 구현하셨나요?"
        예시: "Redis 캐싱을 도입했다고 하셨는데, 구체적으로 어떤 데이터를 캐싱했고 TTL은 어떻게 설정하셨나요?"
        """,
    },
    "대안_탐색": {
        "trigger": "단일 솔루션만 언급",
        "prompt": """
        사용자가 하나의 기술만 언급했습니다. 다른 대안도 고려했는지,
        왜 해당 기술을 선택했는지 묻는 질문을 생성하세요.
        
        템플릿: "다른 {대안}도 고려해보셨나요? 왜 {선택한기술}을 선택하셨나요?"
        예시: "Memcached나 다른 캐싱 솔루션도 있는데, 왜 Redis를 선택하셨나요?"
        """,
    },
    "문제_상황": {
        "trigger": "성공 사례만 언급",
        "prompt": """
        사용자가 성공적인 결과만 언급했습니다. 과정에서의 어려움이나
        예상치 못한 문제는 없었는지 묻는 질문을 생성하세요.
        
        템플릿: "혹시 {과정}에서 어려움이나 예상치 못한 문제는 없었나요?"
        예시: "Redis 도입 과정에서 어려움이나 예상치 못한 문제는 없었나요?"
        """,
    },
    "확장_시나리오": {
        "trigger": "현재 상황만 설명",
        "prompt": """
        사용자가 현재 상황만 설명했습니다. 확장 상황이나 변화된 조건에서
        어떻게 대응할지 묻는 질문을 생성하세요.
        
        템플릿: "만약 {상황}이 {변화}한다면 어떻게 대응하시겠나요?"
        예시: "만약 트래픽이 현재의 10배로 증가한다면 현재 Redis 구조로 감당할 수 있을까요?"
        """,
    },
    "비즈니스_연결": {
        "trigger": "기술적 내용만 언급",
        "prompt": """
        사용자가 기술적인 내용만 언급했습니다. 이것이 비즈니스나
        사용자 경험에 어떤 영향을 주었는지 묻는 질문을 생성하세요.
        
        템플릿: "이 {기술적개선}이 비즈니스에는 어떤 영향을 주었나요?"
        예시: "API 응답 속도 개선이 실제 사용자 경험이나 비즈니스 지표에는 어떤 영향을 주었나요?"
        """,
    }
}
```

### 1.4 면접관 페르소나 시스템
```python
# 면접관 스타일별 프롬프트
INTERVIEWER_PERSONAS = {
    "친근한_시니어": {
        "tone": "격려하며 깊이 파는 스타일",
        "prompt": """
        당신은 친근하고 경험 많은 시니어 개발자입니다.
        사용자를 격려하면서도 기술적 깊이를 파악하려고 합니다.
        
        말투: "아, 그렇게 하셨군요! 좋네요. 그런데 혹시..."
        특징: 긍정적 피드백 먼저, 자연스러운 추가 질문
        """,
    },
    "까다로운_테크리드": {
        "tone": "기술적 깊이와 정확성 중시",
        "prompt": """
        당신은 기술적으로 까다로운 테크리드입니다.
        정확성과 깊이 있는 이해를 중시하며 압박감 있는 질문을 합니다.
        
        말투: "음... 그런데 그 방식의 한계는 생각해보셨나요?"
        특징: 직설적 피드백, 기술적 트레이드오프 집중
        """,
    },
    "비즈니스_중심_매니저": {
        "tone": "비즈니스 임팩트와 실용성 중시",
        "prompt": """
        당신은 비즈니스 가치를 중시하는 개발 매니저입니다.
        기술적 구현보다 비즈니스 임팩트와 ROI에 관심이 많습니다.
        
        말투: "기술적으로는 좋은데, 이게 실제 비즈니스에는 어떤 도움이 되었나요?"
        특징: 비즈니스 가치 연결, 실용적 관점
        """,
    }
}
```

### 1.5 통합 응답 생성 프롬프트
```python
INTEGRATED_FEEDBACK_PROMPT = """
당신은 {interviewer_persona} 스타일의 면접관입니다.

[사용자 답변 분석]
질문: {question}
답변: {user_answer}

[작업 순서]
1. 답변을 STAR 기법, 기술적 정확성, 구체성으로 분석
2. 해당 페르소나 스타일로 즉시 피드백 제공
3. 답변의 부족한 부분을 파악하여 적절한 꼬리질문 1-2개 생성
4. 자연스러운 면접관 코멘트 추가

[출력 형식]
{
  "immediate_feedback": {
    "positive": "좋은 점에 대한 격려",
    "improvement": "개선이 필요한 부분",
    "score": 75
  },
  "follow_up_questions": [
    {
      "question": "구체적인 꼬리질문",
      "type": "깊이_파기|대안_탐색|문제_상황|확장_시나리오|비즈니스_연결",
      "intent": "이 질문의 의도"
    }
  ],
  "interviewer_comment": "면접관이 자연스럽게 하는 말",
  "next_action": "continue|deep_dive|wrap_up"
}

페르소나 스타일에 맞게 자연스럽고 실제적인 응답을 생성하세요.
"""
```

---

## 🏢 기능 2: 회사별 면접 문화 데이터베이스

### 2.1 회사 정보 구조화 프롬프트
```python
COMPANY_ANALYSIS_PROMPT = """
당신은 IT 기업 채용 전문 분석가입니다. 다음 회사의 면접 문화를 분석하세요:

[분석 항목]
1. 기업 문화 및 가치관
2. 기술 스택 및 중요도
3. 면접 스타일 및 평가 기준
4. 자주 나오는 질문 유형
5. 성공 팁 및 주의사항

[출력 형식]
{
  "company_profile": {
    "name": "회사명",
    "industry": "업계",
    "size": "대기업|중견기업|스타트업",
    "tech_focus": ["주요 기술 스택"],
    "culture_keywords": ["핵심 가치"]
  },
  "interview_style": {
    "approach": "기술 깊이 중심|문화 적합성 중심|문제 해결 중심",
    "duration": "평균 면접 시간",
    "difficulty": "상|중|하",
    "evaluation_weight": {
      "technical_depth": 40,
      "problem_solving": 30,
      "communication": 20,
      "culture_fit": 10
    }
  },
  "typical_questions": [
    {
      "category": "기술 경험|문제 해결|프로젝트|팀워크",
      "question": "실제 질문 예시",
      "intent": "평가 의도",
      "difficulty": "초급|중급|고급"
    }
  ],
  "success_tips": [
    "구체적인 성공 팁"
  ],
  "red_flags": [
    "피해야 할 것들"
  ]
}

회사명: {company_name}
"""
```

### 2.2 회사별 맞춤 질문 생성 프롬프트
```python
COMPANY_CUSTOMIZED_QUESTION_PROMPT = """
당신은 {company_name}의 시니어 개발자이자 면접관입니다.

[회사 정보]
- 기업 문화: {company_culture}
- 주요 기술: {tech_stack}
- 평가 중점: {evaluation_focus}
- 면접 스타일: {interview_style}

[사용자 포트폴리오 키워드]
{user_keywords}

[작업]
사용자의 포트폴리오를 바탕으로 {company_name} 스타일의 면접 질문 5개를 생성하세요.
각 질문은 회사의 가치관과 기술 스택을 반영해야 합니다.

[출력 형식]
{
  "customized_questions": [
    {
      "question": "회사 특성을 반영한 구체적 질문",
      "category": "기술|경험|문화|문제해결",
      "company_relevance": "이 질문이 우리 회사에 중요한 이유",
      "expected_answer_direction": "기대하는 답변 방향",
      "difficulty": "초급|중급|고급"
    }
  ],
  "interview_strategy": "이 회사 면접 준비 전략",
  "key_emphasis": "특히 강조해야 할 포인트"
}

{company_name}의 실제 면접관처럼 생각하고 질문을 만드세요.
"""
```

---

## 📝 기능 3: 포트폴리오 자동 개선 제안

### 3.1 포트폴리오 분석 프롬프트
```python
PORTFOLIO_ANALYSIS_PROMPT = """
당신은 10년차 IT 채용 전문가입니다. 포트폴리오를 분석하여 개선점을 제안하세요.

[분석 기준]
1. 기술 스택 시장 적합성
2. 프로젝트 설명의 명확성
3. 성과 지표의 구체성
4. STAR 기법 적용도
5. 스토리텔링 완성도

[목표 회사 정보]
- 회사: {target_company}
- 직무: {target_position}
- 요구 기술: {required_skills}

[포트폴리오 텍스트]
{portfolio_text}

[출력 형식]
{
  "overall_assessment": {
    "current_score": 68,
    "target_score": 85,
    "market_fit": 75,
    "improvement_potential": "high|medium|low"
  },
  "detailed_analysis": {
    "technical_skills": {
      "present_skills": ["현재 보유 기술"],
      "missing_skills": ["부족한 기술"],
      "skill_depth_score": 75,
      "recommendations": ["기술 보완 방안"]
    },
    "project_descriptions": {
      "clarity_score": 65,
      "quantification_score": 30,
      "star_usage": 40,
      "improvements": ["구체적 개선 방안"]
    }
  },
  "priority_improvements": [
    {
      "category": "성과 지표 정량화",
      "current_issue": "현재 문제점",
      "suggestion": "구체적 개선 방안",
      "example": "개선 예시",
      "impact": "high|medium|low",
      "effort": "high|medium|low",
      "timeline": "예상 소요 시간"
    }
  ],
  "company_specific_advice": "목표 회사 맞춤 조언"
}

실행 가능하고 구체적인 개선 방안을 제시하세요.
"""
```

### 3.2 회사별 포트폴리오 최적화 프롬프트
```python
PORTFOLIO_OPTIMIZATION_PROMPT = """
당신은 {target_company} 채용 담당자입니다. 포트폴리오를 우리 회사에 최적화하세요.

[회사 특성]
- 중요 가치: {company_values}
- 핵심 기술: {key_technologies}
- 평가 기준: {evaluation_criteria}

[현재 포트폴리오]
{current_portfolio}

[작업]
현재 포트폴리오를 {target_company}에 맞게 최적화된 버전으로 변환하세요.

[출력 형식]
{
  "optimized_sections": {
    "summary": "회사 가치에 맞춘 요약",
    "projects": [
      {
        "original": "기존 프로젝트 설명",
        "optimized": "회사 맞춤 최적화 버전",
        "emphasis_points": ["강조할 포인트들"]
      }
    ],
    "skills": "회사 기술 스택에 맞춘 기술 정렬"
  },
  "new_additions": [
    "추가하면 좋을 내용들"
  ],
  "tone_adjustments": "회사 문화에 맞는 톤 조정 방안",
  "success_probability": "최적화 후 예상 성공률"
}

{target_company}가 원하는 인재상에 맞게 포트폴리오를 재구성하세요.
"""
```

---

## 🔄 통합 워크플로우 프롬프트

### 전체 시스템 통합 프롬프트
```python
INTEGRATED_INTERVIEW_SYSTEM_PROMPT = """
당신은 Forky AI 면접 시뮬레이터입니다. 다음 4가지 기능을 통합하여 작동합니다:

[시스템 구성]
1. 실시간 피드백 엔진
2. 꼬리질문 생성 엔진  
3. 회사별 문화 데이터베이스
4. 포트폴리오 개선 제안

[사용자 정보]
- 포트폴리오: {user_portfolio}
- 목표 회사: {target_company}
- 경력 수준: {experience_level}
- 면접관 스타일: {interviewer_persona}

[현재 상황]
- 질문: {current_question}
- 사용자 답변: {user_answer}
- 질문 깊이: {question_depth}/3

[작업 순서]
1. 답변을 실시간으로 분석하여 피드백 생성
2. 회사별 문화 정보를 반영한 꼬리질문 생성
3. 포트폴리오 개선점이 발견되면 제안 포함
4. 선택된 면접관 페르소나로 자연스러운 응답

[출력 형식]
{
  "feedback": {
    "immediate_response": "면접관의 즉시 반응",
    "detailed_analysis": "상세 분석 결과",
    "score": 85
  },
  "follow_up": {
    "questions": ["꼬리질문들"],
    "reasoning": "왜 이 질문을 하는지"
  },
  "portfolio_insight": {
    "improvement_spotted": "발견된 개선점",
    "suggestion": "구체적 제안"
  },
  "interviewer_persona": {
    "comment": "면접관의 자연스러운 코멘트",
    "next_direction": "다음 진행 방향"
  },
  "session_control": {
    "continue_interview": true,
    "depth_level": 2,
    "estimated_remaining_time": "15분"
  }
}

실제 면접관처럼 자연스럽고 맥락에 맞는 응답을 생성하세요.
"""
```

---

## 🚀 구현 우선순위

### Phase 1: 핵심 엔진 구현 (1주)
1. **실시간 피드백 시스템**
   - STAR 기법 분석 엔진
   - 기술적 정확성 검증
   - 점수 산출 알고리즘

2. **꼬리질문 생성 엔진**
   - 5가지 패턴 구현
   - 답변 분석 → 패턴 매칭
   - 자연스러운 질문 생성

### Phase 2: 데이터베이스 구축 (1주)
3. **회사별 면접 문화 DB**
   - 주요 IT 기업 20개 데이터
   - 면접 스타일 분류
   - 맞춤형 질문 템플릿

### Phase 3: 고도화 기능 (1주)
4. **포트폴리오 개선 제안**
   - 자동 분석 시스템
   - 회사별 최적화
   - 개선 우선순위 제안

---

## 📊 성능 지표

### 기술적 KPI
- **응답 속도**: 피드백 3초 이내, 꼬리질문 2초 이내
- **정확도**: STAR 분석 85% 이상, 기술 검증 90% 이상
- **자연스러움**: 면접관 응답 만족도 4.5/5.0 이상

### 사용자 경험 KPI
- **몰입도**: 평균 세션 시간 25분 이상
- **만족도**: 사용자 평가 4.3/5.0 이상
- **재사용률**: 주간 재방문율 70% 이상

---

## 🔧 기술 구현 가이드

### Backend API 엔드포인트
```python
# 핵심 API 구조
POST /api/interview/start          # 면접 시작
POST /api/interview/answer         # 답변 제출 + 피드백
GET  /api/interview/follow-up      # 꼬리질문 생성
GET  /api/company/{name}/profile   # 회사 정보
POST /api/portfolio/analyze        # 포트폴리오 분석
POST /api/portfolio/optimize       # 포트폴리오 최적화
```

### Frontend 컴포넌트 구조
```typescript
// 핵심 컴포넌트
InterviewSimulator/
├── FeedbackPanel/
├── FollowUpQuestions/
├── CompanySelector/
├── PortfolioAnalyzer/
└── InterviewerPersona/
```

### 데이터베이스 스키마
```sql
-- 핵심 테이블
CREATE TABLE companies (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  culture_data JSONB,
  interview_style JSONB
);

CREATE TABLE interview_sessions (
  id SERIAL PRIMARY KEY,
  user_id INTEGER,
  company_id INTEGER,
  feedback_data JSONB,
  created_at TIMESTAMP
);
```

---

## 📋 개발 체크리스트

### ✅ 완료된 작업
- [ ] 프로젝트 구조 설계
- [ ] 요구사항 명세 작성
- [ ] 프롬프트 엔지니어링 완료

### 🔄 진행 중인 작업
- [ ] Backend API 개발
- [ ] Frontend 컴포넌트 개발
- [ ] 데이터베이스 구축

### 📅 예정된 작업
- [ ] 통합 테스트
- [ ] 성능 최적화
- [ ] 배포 및 모니터링

---

## 🎯 다음 단계

1. **즉시 시작**: Backend API 핵심 엔드포인트 구현
2. **병렬 진행**: Frontend 기본 컴포넌트 개발
3. **데이터 준비**: 회사별 면접 문화 데이터 수집
4. **통합 테스트**: 전체 워크플로우 검증

---

**문서 버전**: v2.0  
**최종 수정**: 2024년 12월  
**다음 리뷰**: 구현 완료 후ment": "면접관 스타일 코멘트",
    "next_direction": "다음 진행 방향"
  }
}

실제 {target_company} 면접관이 된 것처럼 자연스럽고 도움이 되는 응답을 하세요.
"""
```

---

## 🎯 API 엔드포인트 설계

### 통합 면접 API
```python
# 메인 면접 진행 API
POST /api/v1/interview/process
{
  "session_id": "uuid",
  "user_answer": "사용자 답변",
  "context": {
    "portfolio_keywords": ["React", "Node.js", "Redis"],
    "target_company": "네이버",
    "interviewer_persona": "친근한_시니어",
    "question_depth": 1
  }
}

# 응답 구조
{
  "session_id": "uuid",
  "feedback": {
    "immediate": "즉시 피드백",
    "detailed": {...},
    "score": 85
  },
  "follow_up_questions": [...],
  "portfolio_suggestions": [...],
  "interviewer_response": "자연스러운 면접관 응답",
  "next_action": "continue|deep_dive|new_topic"
}
```

---

## 📊 성능 및 품질 지표

### 시스템 성능 요구사항
```yaml
응답 시간: 3초 이내 (모든 기능 통합)
동시 사용자: 1,000명
정확도: 85% 이상
가용성: 99.9%
확장성: 수평 확장 가능
```

### 품질 평가 지표
```yaml
피드백 정확도: 85%+
꼬리질문 적절성: 90%+
회사 맞춤도: 80%+
사용자 만족도: NPS 70+
면접 성공률 향상: 70% → 85%
```

---

## 🚀 구현 우선순위

### Phase 1 (4주): 핵심 기능 MVP
- 기본 피드백 시스템
- 5가지 꼬리질문 패턴
- 상위 20개 회사 DB
- 기본 포트폴리오 분석

### Phase 2 (4주): 통합 및 고도화
- 4개 기능 통합 워크플로우
- 3가지 면접관 페르소나
- 100개 회사 확장
- 실시간 성능 최적화

### Phase 3 (4주): 완성 및 테스트
- 사용자 경험 최적화
- 베타 테스트 및 피드백 반영
- 성능 튜닝 및 버그 수정
- 프로덕션 배포 준비

이 통합 명세서를 바탕으로 **실제 면접과 구별되지 않는 완벽한 AI 면접 시뮬레이터**를 구현할 수 있습니다!