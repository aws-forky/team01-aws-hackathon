# 실시간 꼬리질문 시스템 요구사항 명세서

## 📋 기능 개요

**기능명**: AI 기반 실시간 꼬리질문 시스템 (Follow-up Question Engine)
**목적**: 사용자 답변을 분석하여 실제 면접관처럼 심화 질문을 즉시 생성하고 피드백 제공
**핵심 가치**: 실제 면접 상황의 압박감과 깊이 있는 대화 재현

---

## 🎯 핵심 요구사항

### 1. 답변 분석 및 꼬리질문 생성

#### 1.1 실시간 답변 분석
```yaml
기능명: 답변 심층 분석 엔진
처리시간: 2초 이내
분석 깊이: 3단계 (표면/논리/기술)
질문 생성: 1-3개 꼬리질문 자동 생성
```

**분석 항목**:
```json
{
  "answer_analysis": {
    "surface_level": {
      "completeness": 75,
      "clarity": 80,
      "confidence": 65,
      "missing_elements": ["구체적 수치", "결과 측정"]
    },
    "logical_level": {
      "reasoning_flow": 70,
      "cause_effect": 60,
      "assumptions": ["Redis가 최선의 선택", "성능이 주요 이슈"],
      "gaps": ["다른 대안 고려 과정 누락"]
    },
    "technical_level": {
      "depth": 65,
      "accuracy": 90,
      "implementation_details": 40,
      "trade_offs": 30
    }
  }
}
```

#### 1.2 꼬리질문 생성 전략
```yaml
질문 유형: 5가지 패턴
생성 개수: 1-3개 (답변 품질에 따라)
난이도 조절: 사용자 레벨별 차별화
실제성: 실제 면접관 스타일 모방
```

**꼬리질문 패턴**:
```python
FOLLOW_UP_PATTERNS = {
    "깊이_파기": {
        "trigger": "표면적 답변 감지",
        "template": "구체적으로 {기술/과정}은 어떻게 구현하셨나요?",
        "example": "Redis 캐싱을 도입했다고 하셨는데, 구체적으로 어떤 데이터를 캐싱했고 TTL은 어떻게 설정하셨나요?"
    },
    "대안_탐색": {
        "trigger": "단일 솔루션만 언급",
        "template": "다른 {대안}도 고려해보셨나요? 왜 {선택한기술}을 선택하셨나요?",
        "example": "Memcached나 다른 캐싱 솔루션도 있는데, 왜 Redis를 선택하셨나요?"
    },
    "문제_상황": {
        "trigger": "성공 사례만 언급",
        "template": "혹시 {과정}에서 어려움이나 예상치 못한 문제는 없었나요?",
        "example": "Redis 도입 과정에서 어려움이나 예상치 못한 문제는 없었나요? 어떻게 해결하셨나요?"
    },
    "확장_시나리오": {
        "trigger": "현재 상황만 설명",
        "template": "만약 {상황}이 {변화}한다면 어떻게 대응하시겠나요?",
        "example": "만약 트래픽이 현재의 10배로 증가한다면 현재 Redis 구조로 감당할 수 있을까요?"
    },
    "비즈니스_연결": {
        "trigger": "기술적 내용만 언급",
        "template": "이 {기술적개선}이 비즈니스에는 어떤 영향을 주었나요?",
        "example": "API 응답 속도 개선이 실제 사용자 경험이나 비즈니스 지표에는 어떤 영향을 주었나요?"
    }
}
```

### 2. 대화형 면접 시뮬레이션

#### 2.1 면접 플로우 관리
```yaml
기능명: 대화형 면접 세션 관리
세션 길이: 15-30분
질문 깊이: 최대 3단계 심화
종료 조건: 충분한 정보 수집 또는 시간 초과
```

**면접 세션 구조**:
```json
{
  "interview_session": {
    "session_id": "uuid",
    "user_id": "uuid",
    "company": "네이버",
    "position": "백엔드 개발자",
    "start_time": "2024-12-20T10:00:00Z",
    "current_question_depth": 2,
    "max_depth": 3,
    "questions_asked": [
      {
        "id": 1,
        "type": "initial",
        "question": "Redis 캐싱을 도입한 경험을 설명해주세요",
        "answer": "사용자 답변...",
        "analysis": {...},
        "follow_ups": [...]
      }
    ],
    "session_status": "active"
  }
}
```

#### 2.2 실시간 피드백 + 꼬리질문
```yaml
기능명: 통합 피드백 시스템
구성: 즉시 피드백 + 심화 질문
형태: 면접관 스타일 자연스러운 대화
개인화: 사용자 답변 패턴 학습
```

**통합 응답 구조**:
```json
{
  "response": {
    "feedback": {
      "positive": "Redis 도입으로 성능 개선을 이뤄낸 점이 좋네요.",
      "improvement": "구체적인 수치가 더 있으면 좋겠어요.",
      "score": 75
    },
    "follow_up_questions": [
      {
        "id": "fq_001",
        "type": "깊이_파기",
        "question": "구체적으로 어떤 데이터를 캐싱했고, TTL은 어떻게 설정하셨나요?",
        "intent": "기술적 구현 세부사항 확인",
        "difficulty": "intermediate",
        "expected_keywords": ["세션 데이터", "사용자 정보", "TTL 전략"]
      }
    ],
    "interviewer_comment": "좋은 경험이네요. 조금 더 자세히 들어보고 싶어요.",
    "next_action": "answer_follow_up"
  }
}
```

### 3. 면접관 페르소나 시뮬레이션

#### 3.1 면접관 스타일 구현
```yaml
기능명: AI 면접관 페르소나
스타일: 5가지 면접관 유형
적응성: 사용자 답변에 따른 스타일 조정
자연스러움: 실제 면접관 말투 재현
```

**면접관 페르소나**:
```python
INTERVIEWER_PERSONAS = {
    "친근한_시니어": {
        "style": "격려하며 깊이 파는 스타일",
        "feedback_tone": "긍정적이고 건설적",
        "question_style": "자연스러운 대화형",
        "example": "아, 그렇게 하셨군요! 그런데 혹시 다른 방법도 고려해보셨나요?"
    },
    "까다로운_테크리드": {
        "style": "기술적 깊이 중시",
        "feedback_tone": "직설적이고 정확성 중시",
        "question_style": "압박감 있는 심화 질문",
        "example": "음... 그런데 그 방식의 한계는 생각해보셨나요? 확장성 측면에서는 어떨까요?"
    },
    "비즈니스_중심_매니저": {
        "style": "비즈니스 임팩트 중시",
        "feedback_tone": "실용적이고 결과 중심",
        "question_style": "ROI와 비즈니스 가치 탐구",
        "example": "기술적으로는 좋은데, 이게 실제 비즈니스에는 어떤 도움이 되었나요?"
    },
    "호기심_많은_주니어": {
        "style": "학습 의욕이 높은 스타일",
        "feedback_tone": "호기심 어린 질문",
        "question_style": "다양한 각도에서 접근",
        "example": "와, 신기하네요! 그럼 이런 상황에서는 어떻게 하셨을까요?"
    },
    "경험_많은_아키텍트": {
        "style": "시스템 전체 관점 중시",
        "feedback_tone": "아키텍처 관점에서 평가",
        "question_style": "전체적인 설계와 트레이드오프",
        "example": "전체 시스템 아키텍처에서 보면 이 선택이 다른 부분에는 어떤 영향을 주었나요?"
    }
}
```

### 4. 기술 구현 요구사항

#### 4.1 API 설계
```python
# 꼬리질문 생성 API
POST /api/v1/interview/follow-up
{
  "session_id": "uuid",
  "question_id": "initial_q1",
  "user_answer": "Redis를 도입해서 API 응답속도를 5배 개선했습니다.",
  "interviewer_persona": "친근한_시니어",
  "max_follow_ups": 2
}

# 응답 구조
{
  "session_id": "uuid",
  "feedback": {
    "immediate_response": "좋은 성과네요!",
    "detailed_feedback": {...},
    "score": 75
  },
  "follow_up_questions": [
    {
      "question": "구체적으로 어떤 데이터를 캐싱하셨나요?",
      "type": "깊이_파기",
      "expected_depth": "implementation_details"
    }
  ],
  "interviewer_comment": "조금 더 자세히 들어보고 싶어요.",
  "session_status": "continue"
}
```

#### 4.2 실시간 처리 아키텍처
```yaml
응답 시간: 2초 이내
동시 세션: 500개 지원
상태 관리: Redis 기반 세션 저장
확장성: 마이크로서비스 아키텍처
```

**시스템 아키텍처**:
```
User Input → Answer Analysis → Follow-up Generation → Response Formatting
     ↓              ↓                    ↓                    ↓
Session Store → AI Analysis API → Question Engine → Natural Language
```

#### 4.3 데이터베이스 스키마
```sql
-- 면접 세션 테이블
CREATE TABLE interview_sessions (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    company VARCHAR(100),
    position VARCHAR(100),
    interviewer_persona VARCHAR(50),
    start_time TIMESTAMP DEFAULT NOW(),
    end_time TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active',
    total_questions INTEGER DEFAULT 0,
    session_data JSONB
);

-- 질문-답변 히스토리
CREATE TABLE qa_history (
    id UUID PRIMARY KEY,
    session_id UUID REFERENCES interview_sessions(id),
    question_order INTEGER,
    question_type VARCHAR(50), -- 'initial', 'follow_up'
    parent_question_id UUID,
    question_text TEXT NOT NULL,
    answer_text TEXT,
    analysis_result JSONB,
    feedback_data JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 꼬리질문 생성 로그
CREATE TABLE follow_up_logs (
    id UUID PRIMARY KEY,
    qa_id UUID REFERENCES qa_history(id),
    trigger_pattern VARCHAR(50),
    generated_questions JSONB,
    selected_question TEXT,
    generation_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 5. UI/UX 요구사항

#### 5.1 대화형 면접 화면
```
┌─────────────────────────────────────────┐
│ 🎤 AI 면접관과의 실시간 대화             │
├─────────────────────────────────────────┤
│ 👨‍💼 면접관 (친근한 시니어)                │
│ "Redis 캐싱을 도입한 경험을 설명해주세요" │
│                                         │
│ 👤 나의 답변                            │
│ "사용자 세션 데이터를 Redis에 캐싱해서   │
│  API 응답속도를 5배 개선했습니다."       │
│                                         │
│ 👨‍💼 면접관 피드백                        │
│ ✅ "좋은 성과네요!"                      │
│ 💡 "구체적인 수치가 더 있으면 좋겠어요"   │
│                                         │
│ 🔄 꼬리질문                             │
│ "구체적으로 어떤 데이터를 캐싱했고,      │
│  TTL은 어떻게 설정하셨나요?"             │
│                                         │
│ [답변 입력창]                           │
│ [🎙️ 음성입력] [⏭️ 다음질문] [⏸️ 일시정지] │
└─────────────────────────────────────────┘
```

#### 5.2 실시간 분석 표시
```
┌─────────────────────────────────────────┐
│ 📊 실시간 답변 분석                      │
├─────────────────────────────────────────┤
│ 현재 답변 점수: 75/100                   │
│                                         │
│ 📈 분석 진행률                          │
│ 완성도     ████████░░ 80%              │
│ 기술 깊이   ██████░░░░ 60%              │
│ 구체성     ████░░░░░░ 40%              │
│                                         │
│ 🎯 면접관 관심도                        │
│ ████████░░ 높음                        │
│                                         │
│ 💭 예상 꼬리질문                        │
│ • 구현 세부사항 (90% 확률)              │
│ • 대안 기술 비교 (70% 확률)             │
│ • 문제 해결 과정 (60% 확률)             │
└─────────────────────────────────────────┘
```

#### 5.3 면접 진행 상황
```
┌─────────────────────────────────────────┐
│ 📋 면접 진행 현황                        │
├─────────────────────────────────────────┤
│ 진행 시간: 12분 / 30분                   │
│ 질문 수: 3개 (초기 1개 + 꼬리 2개)       │
│                                         │
│ 📊 질문 깊이 트리                        │
│ Q1: Redis 캐싱 경험 (초기질문)           │
│  ├─ Q1-1: 구체적 구현 방법 (꼬리질문)    │
│  └─ Q1-2: 성능 측정 방법 (꼬리질문)      │
│                                         │
│ 🎯 평가 영역 커버리지                    │
│ ✅ 기술적 깊이                          │
│ ✅ 문제 해결                            │
│ ⏳ 비즈니스 임팩트 (진행중)              │
│ ❌ 팀워크 (미진행)                      │
│                                         │
│ [면접 종료] [휴식] [다음 주제]           │
└─────────────────────────────────────────┘
```

### 6. 고급 기능

#### 6.1 적응형 난이도 조절
```yaml
기능명: 동적 난이도 조절
기준: 사용자 답변 품질 실시간 분석
조절 방식: 질문 깊이, 기술적 복잡도, 압박 수준
목표: 적절한 도전 수준 유지
```

#### 6.2 면접 스타일 학습
```yaml
기능명: 개인별 면접 패턴 학습
데이터: 사용자 답변 스타일, 강약점, 선호도
적용: 맞춤형 질문 생성 및 피드백 스타일
개선: 지속적인 개인화 향상
```

#### 6.3 실시간 스트레스 테스트
```yaml
기능명: 압박 면접 시뮬레이션
트리거: 사용자 요청 또는 고급 모드
방식: 빠른 연속 질문, 까다로운 꼬리질문
목적: 실제 면접 압박감 재현
```

## 🎯 성공 지표

### 정량적 지표
- **꼬리질문 생성 정확도**: 85% 이상
- **사용자 참여도**: 평균 세션 시간 20분+
- **면접 완주율**: 80% 이상
- **재사용률**: 주 3회 이상 사용

### 정성적 지표
- **실제성**: "실제 면접 같다" 90% 동의
- **도움 정도**: "실력 향상에 도움" 85% 동의
- **차별화**: "다른 서비스와 확실히 다름" 80% 동의

## 🚀 구현 우선순위

### Phase 1 (2주): 기본 꼬리질문 시스템
- 답변 분석 엔진 구축
- 5가지 기본 꼬리질문 패턴 구현
- 간단한 대화형 UI 개발

### Phase 2 (2주): 면접관 페르소나
- 3가지 면접관 스타일 구현
- 자연스러운 대화 톤 개발
- 실시간 피드백 통합

### Phase 3 (2주): 고도화 및 최적화
- 적응형 난이도 조절
- 성능 최적화
- 사용자 테스트 및 개선

이 꼬리질문 시스템으로 **Forky를 실제 면접과 가장 유사한 경험을 제공하는 유일한 서비스**로 만들 수 있습니다!