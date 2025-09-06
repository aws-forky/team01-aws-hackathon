# AI 기반 면접 시스템 개선 요구사항

## 📋 개요

현재 면접 시스템의 꼬리 질문 생성과 실시간 피드백 기능을 AI API 기반으로 개선하여 사용자 답변에 맞춤화된 개인화 경험을 제공합니다.

## 🔍 현재 시스템 분석

### 현재 문제점

1. **고정된 꼬리 질문**
   - `"방금 말씀하신 해당 기술에 대해 좀 더 구체적으로 설명해주실 수 있나요?"` 등 템플릿 기반
   - 사용자 답변 내용과 무관한 일반적인 질문
   - Fallback 질문으로 개인화 부족

2. **제한적인 피드백 시스템**
   - AI 서버 연결 실패 시 기본 피드백으로 대체
   - 실시간 피드백이 일부 컴포넌트에서 제대로 표시되지 않음
   - 피드백 품질의 일관성 부족

### 현재 구현 위치

- **백엔드**: `backend/app/services/services.py`
  - `AIService.generate_followup_questions()` (라인 434-469)
  - `FeedbackService.analyze_answer()` (라인 561-705)

- **프론트엔드**: `frontend/src/components/EnhancedInterviewSimulator.tsx`
  - 꼬리 질문 생성 및 표시 로직
  - 실시간 피드백 표시 영역

## 🎯 개선 목표

### 1. 완전한 AI 기반 개인화 질문 생성
- 모든 꼬리 질문을 사용자 답변 기반으로 AI가 생성
- Fallback 질문 완전 제거
- 답변 맥락을 고려한 심화 질문

### 2. 향상된 실시간 피드백
- AI API를 통한 상세하고 개인화된 피드백
- 기술적 정확성, 개선 제안, 잘한 점 등 구조화된 분석
- 실시간 표시 기능 완전 작동

## 📊 요구사항 세부 분석

### A. 꼬리 질문 시스템 개선

#### 현재 상태
```python
# backend/app/services/services.py (라인 438-444)
followup_templates = [
    "방금 말씀하신 {keyword}에 대해 좀 더 구체적으로 설명해주실 수 있나요?",
    "그 과정에서 어려웠던 점이나 예상치 못한 문제가 있었나요?",
    "다시 구현한다면 어떤 부분을 다르게 하시겠나요?",
    "그 기술을 선택한 특별한 이유가 있나요?",
    "성능이나 확장성 측면에서 고려한 점이 있나요?"
]
```

#### 개선 방향
- AI API 호출을 통한 완전 동적 질문 생성
- 사용자 답변의 핵심 내용 분석
- 기술적 깊이, 경험 수준, 프로젝트 맥락 고려

### B. 피드백 시스템 개선

#### 현재 피드백 구조
```json
{
  "overall_score": 75,
  "strengths": ["경험 기반 답변"],
  "improvement_suggestions": [
    "답변을 더 자세히 설명해주세요",
    "상황과 과제를 명확히 설명해주세요"
  ],
  "technical_accuracy": {
    "score": 35,
    "status": "보완 필요"
  }
}
```

#### 개선된 피드백 구조
```json
{
  "overview": {
    "strengths": ["구체적인 기술 스택 언급", "실무 경험 기반 답변"],
    "improvements": [
      "STAR 기법 활용한 구조화",
      "정량적 성과 지표 추가",
      "기술적 트레이드오프 설명"
    ]
  },
  "technical_accuracy": {
    "score": 85,
    "status": "우수",
    "details": "Spring Boot와 JPA 활용 경험이 잘 드러남"
  },
  "communication_score": 78,
  "personalized_advice": "백엔드 개발자로서 API 설계 경험을 더 구체적으로 설명하시면 좋겠습니다."
}
```

## 🔧 기술적 구현 계획

### Phase 1: 백엔드 API 개선 (1주)

#### 1.1 꼬리 질문 생성 API 개선
- **위치**: `backend/app/services/services.py`
- **메서드**: `generate_followup_questions()`

```python
async def generate_followup_questions(self, main_question: str, user_answer: str, count: int = 3) -> List:
    """AI 기반 개인화 꼬리 질문 생성"""
    try:
        # AI 서버 API 호출
        async with httpx.AsyncClient(timeout=60) as client:
            payload = {
                'main_question': main_question,
                'user_answer': user_answer,
                'context': {
                    'interview_type': 'technical',
                    'experience_level': 'intermediate',
                    'followup_count': count
                }
            }
            
            response = await client.post(
                "https://ai-f.kms39273.synology.me/api/v1/questions/followup-personalized",
                headers={'Content-Type': 'application/json'},
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                return self._format_followup_questions(result)
            else:
                raise Exception("AI 서버 오류")
                
    except Exception as e:
        # 완전 제거: Fallback 질문 없음
        raise Exception(f"개인화된 꼬리 질문 생성 실패: {str(e)}")
```

#### 1.2 피드백 분석 API 개선
- **위치**: `backend/app/services/services.py`
- **메서드**: `analyze_answer()`

```python
async def analyze_answer(self, question: str, answer: str, user_level: str = "intermediate") -> dict:
    """AI 기반 상세 피드백 생성"""
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            payload = {
                'question': question,
                'answer': answer,
                'analysis_type': 'comprehensive',
                'feedback_categories': [
                    'technical_accuracy',
                    'communication_clarity', 
                    'experience_demonstration',
                    'improvement_suggestions'
                ],
                'user_level': user_level
            }
            
            response = await client.post(
                "https://ai-f.kms39273.synology.me/api/v1/feedback/comprehensive",
                headers={'Content-Type': 'application/json'},
                json=payload
            )
            
            if response.status_code == 200:
                return self._format_comprehensive_feedback(response.json())
            else:
                raise Exception("피드백 생성 실패")
                
    except Exception as e:
        # AI 서버 실패 시에도 기본 피드백 대신 오류 반환
        raise Exception(f"AI 피드백 생성 실패: {str(e)}")
```

### Phase 2: 프론트엔드 UI/UX 개선 (1주)

#### 2.1 실시간 피드백 표시 개선
- **위치**: `frontend/src/components/EnhancedInterviewSimulator.tsx`
- **개선 사항**:
  - 피드백 로딩 상태 표시
  - 오류 처리 개선
  - 피드백 카테고리별 시각화

#### 2.2 꼬리 질문 흐름 개선
- **개인화 표시**: "답변 내용을 바탕으로 생성된 심화 질문입니다"
- **로딩 애니메이션**: AI가 질문을 생성하는 과정 시각화
- **오류 처리**: AI 생성 실패 시 명확한 안내

### Phase 3: 에러 처리 및 안정성 개선 (1주)

#### 3.1 Graceful Degradation 제거
- Fallback 시스템 완전 제거
- AI 서버 의존성 100% 전환
- 서비스 중단 시 명확한 안내 메시지

#### 3.2 모니터링 및 로깅 강화
- AI API 호출 성공률 추적
- 응답 시간 모니터링
- 사용자 피드백 품질 지표

## 📈 성능 목표

### 응답 시간
- **꼬리 질문 생성**: 3초 이내
- **피드백 분석**: 2초 이내
- **전체 인터랙션**: 5초 이내

### 품질 지표
- **개인화 정확도**: 85% 이상
- **피드백 만족도**: 4.0/5.0 이상
- **API 성공률**: 99% 이상

## 🔄 API 엔드포인트 변경사항

### 새로운 AI API 엔드포인트

#### 1. 개인화 꼬리 질문 생성
```
POST /api/v1/questions/followup-personalized
```

**Request:**
```json
{
  "main_question": "프로젝트에서 사용한 기술 스택을 설명해주세요",
  "user_answer": "Spring Boot와 React를 사용해서 웹 애플리케이션을 개발했습니다...",
  "context": {
    "interview_type": "technical",
    "experience_level": "intermediate",
    "followup_count": 3
  }
}
```

**Response:**
```json
{
  "success": true,
  "followup_questions": [
    {
      "content": "Spring Boot에서 JPA를 활용할 때 N+1 문제를 어떻게 해결하셨나요?",
      "reasoning": "사용자가 Spring Boot 언급, 데이터베이스 관련 심화 질문",
      "difficulty": "intermediate",
      "category": "technical_deep_dive"
    }
  ]
}
```

#### 2. 종합 피드백 분석
```
POST /api/v1/feedback/comprehensive
```

**Request:**
```json
{
  "question": "프로젝트 경험을 설명해주세요",
  "answer": "Spring Boot로 REST API를 개발했습니다...",
  "analysis_type": "comprehensive",
  "feedback_categories": ["technical_accuracy", "communication_clarity"],
  "user_level": "intermediate"
}
```

**Response:**
```json
{
  "success": true,
  "feedback": {
    "overview": {
      "strengths": ["구체적인 기술 스택 언급"],
      "improvements": ["STAR 기법 활용", "정량적 성과 추가"]
    },
    "technical_accuracy": {
      "score": 85,
      "status": "우수",
      "details": "Spring Boot 이해도 높음"
    },
    "communication_score": 78,
    "personalized_advice": "API 설계 경험을 더 구체적으로 설명하세요"
  }
}
```

## 🚀 구현 우선순위

### High Priority (1-2주) - ✅ 완료
1. ✅ **꼬리 질문 AI 생성**: 완전 AI 기반 전환 완료
2. ✅ **피드백 시스템 개선**: 상세하고 개인화된 분석 완료
3. ✅ **Fallback 제거**: 의존성 완전 전환 완료

### Medium Priority (3-4주)
1. **UI/UX 개선**: 실시간 표시 최적화
2. **에러 처리**: 사용자 친화적 메시지
3. **성능 최적화**: 응답 시간 단축

### Low Priority (5-6주)
1. **모니터링 대시보드**: 품질 지표 추적
2. **A/B 테스트**: 개선 효과 측정
3. **사용자 피드백**: 지속적 개선

## 📋 체크리스트

### 백엔드 개발
- [x] AI API 엔드포인트 연동
- [x] 꼬리 질문 생성 로직 교체
- [x] 피드백 분석 API 개선
- [x] Fallback 시스템 제거
- [x] 에러 처리 강화

### 프론트엔드 개발
- [x] 실시간 피드백 UI 개선
- [x] 로딩 상태 표시
- [x] 오류 처리 UI
- [x] 개인화 표시 추가
- [x] 성능 최적화

### 테스트 및 검증
- [ ] API 연동 테스트
- [ ] 사용자 시나리오 테스트
- [ ] 성능 테스트
- [ ] 품질 지표 측정
- [ ] 사용자 피드백 수집

## 📊 예상 결과

### 개선 효과
- **질문 개인화**: 85% → 95% 향상
- **피드백 만족도**: 3.2/5 → 4.3/5 향상
- **사용자 참여도**: 30% 증가
- **재사용률**: 45% 증가

### 기술적 안정성
- **AI 의존성**: 100% (완전 전환)
- **응답 시간**: 평균 3초 이내
- **성공률**: 99% 이상 유지
- **확장성**: 동시 사용자 50명 → 200명

---

**작성일**: 2024년 12월
**담당자**: AI 면접 시스템 개발팀
**버전**: v2.0
