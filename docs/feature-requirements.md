# Forky 핵심 기능 요구사항 명세서

## 📋 문서 개요

**작성일**: 2024년 12월
**버전**: v1.0
**대상 기능**: 실시간 피드백, 회사별 문화DB, 포트폴리오 개선

---

## 🎯 기능 1: 실시간 면접 피드백 시스템

### 1.1 기능 개요
사용자가 면접 질문에 답변하면 AI가 실시간으로 분석하여 구체적인 피드백과 개선 제안을 제공하는 시스템

### 1.2 핵심 요구사항

#### 1.2.1 답변 분석 기능
```yaml
기능명: AI 답변 분석
입력: 질문 + 사용자 답변 (텍스트/음성)
출력: 구조화된 피드백 데이터
처리시간: 3초 이내
```

**분석 항목**:
- **STAR 기법 완성도**: Situation, Task, Action, Result 각 요소 포함 여부
- **기술적 정확성**: 언급된 기술의 올바른 사용법 및 이해도
- **구체성 수준**: 정량적 지표, 구체적 사례 포함 정도
- **논리적 구조**: 답변의 일관성 및 흐름

#### 1.2.2 실시간 피드백 제공
```yaml
기능명: 즉시 피드백 생성
응답시간: 3초 이내
피드백 형식: 구조화된 JSON + 사용자 친화적 UI
언어: 한국어 (향후 영어 확장)
```

**피드백 구조**:
```json
{
  "overall_score": 85,
  "star_analysis": {
    "situation": {"present": true, "quality": "good", "suggestion": "더 구체적인 상황 설명 필요"},
    "task": {"present": true, "quality": "excellent", "suggestion": null},
    "action": {"present": true, "quality": "good", "suggestion": "기술적 선택 이유 추가"},
    "result": {"present": false, "quality": null, "suggestion": "정량적 결과 지표 필수 추가"}
  },
  "technical_accuracy": {
    "score": 90,
    "correct_concepts": ["Redis 캐싱", "API 최적화"],
    "incorrect_concepts": [],
    "missing_details": ["캐시 무효화 전략"]
  },
  "improvement_suggestions": [
    "결과 부분에 '응답 시간 5.8배 개선' 같은 구체적 수치 추가",
    "Redis 선택 이유와 다른 대안 고려 과정 설명",
    "프로젝트 규모나 사용자 수 등 배경 정보 보완"
  ],
  "strengths": [
    "기술적 이해도가 높음",
    "실무 경험이 잘 드러남"
  ],
  "next_steps": [
    "비즈니스 임팩트 강조 연습",
    "기술 선택 근거 설명 연습"
  ]
}
```

#### 1.2.3 개선 제안 시스템
```yaml
기능명: 맞춤형 개선 제안
개인화: 사용자 레벨별 차별화 (신입/경력/시니어)
학습 추천: 부족한 영역별 학습 자료 제공
재연습: 약점 보완을 위한 추가 질문 생성
```

### 1.3 기술 요구사항

#### 1.3.1 AI API 통합
```python
# 피드백 생성 API 엔드포인트
POST /api/v1/feedback/analyze
{
  "question": "Redis 캐싱을 도입한 경험을 설명해주세요",
  "answer": "사용자 답변 텍스트",
  "user_level": "intermediate",
  "company": "네이버"
}
```

#### 1.3.2 데이터베이스 스키마
```sql
-- 피드백 히스토리 테이블
CREATE TABLE feedback_history (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    question_id UUID NOT NULL,
    answer_text TEXT NOT NULL,
    feedback_data JSONB NOT NULL,
    overall_score INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 개선 추적 테이블
CREATE TABLE improvement_tracking (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    skill_area VARCHAR(100) NOT NULL,
    initial_score INTEGER,
    current_score INTEGER,
    target_score INTEGER,
    practice_count INTEGER DEFAULT 0,
    last_practiced_at TIMESTAMP
);
```

#### 1.3.3 성능 요구사항
- **응답 시간**: 3초 이내
- **동시 사용자**: 1,000명 지원
- **가용성**: 99.9% 업타임
- **확장성**: 수평 확장 가능한 구조

### 1.4 UI/UX 요구사항

#### 1.4.1 피드백 화면 구성
```
┌─────────────────────────────────────────┐
│ 📊 답변 분석 결과                        │
├─────────────────────────────────────────┤
│ 전체 점수: 85/100 ⭐⭐⭐⭐☆              │
│                                         │
│ ✅ 잘한 점                              │
│ • 기술적 이해도가 높음                   │
│ • 실무 경험이 잘 드러남                  │
│                                         │
│ 🔧 개선할 점                            │
│ • 결과 부분에 구체적 수치 추가 필요      │
│ • 기술 선택 근거 설명 보완               │
│                                         │
│ 📚 추천 학습                            │
│ • Redis 심화 학습 자료                  │
│ • STAR 기법 연습 문제                   │
│                                         │
│ [다시 답변하기] [다음 질문]              │
└─────────────────────────────────────────┘
```

#### 1.4.2 진행률 추적 대시보드
```
┌─────────────────────────────────────────┐
│ 📈 나의 면접 실력 향상 현황              │
├─────────────────────────────────────────┤
│ STAR 기법 완성도    ████████░░ 80%      │
│ 기술적 정확성      ██████████ 100%     │
│ 구체성 수준        ██████░░░░ 60%      │
│ 논리적 구조        ████████░░ 80%      │
│                                         │
│ 🎯 이번 주 목표: 구체성 수준 80% 달성    │
│ 📅 연습 일수: 5일 연속                  │
│ 🏆 총 연습 횟수: 23회                   │
└─────────────────────────────────────────┘
```

---

## 🏢 기능 2: 회사별 면접 문화 데이터베이스

### 2.1 기능 개요
주요 IT 기업별 면접 문화, 평가 기준, 질문 스타일을 데이터베이스화하여 회사 맞춤형 면접 준비를 지원

### 2.2 핵심 요구사항

#### 2.2.1 회사 정보 데이터베이스
```yaml
기능명: 회사별 면접 문화 DB
대상 기업: 100개사 (1차), 500개사 (2차)
업데이트 주기: 월 1회
데이터 소스: 면접 후기, 채용 공고, 공식 발표 자료
```

**데이터 구조**:
```json
{
  "company_id": "naver",
  "company_name": "네이버",
  "company_info": {
    "industry": "포털/검색",
    "size": "대기업",
    "tech_stack": ["Java", "Spring", "React", "MySQL", "Redis"],
    "engineering_culture": "안정성과 확장성 중시, 대규모 서비스 운영 경험 중요"
  },
  "interview_culture": {
    "style": "기술 깊이 중심",
    "duration": "60-90분",
    "rounds": ["서류", "코딩테스트", "기술면접", "임원면접"],
    "key_values": ["기술적 깊이", "시스템 사고", "협업 능력"],
    "evaluation_criteria": {
      "technical_depth": 40,
      "problem_solving": 30,
      "communication": 20,
      "culture_fit": 10
    }
  },
  "typical_questions": [
    {
      "category": "기술 경험",
      "question": "대규모 트래픽을 처리한 경험이 있나요? 어떤 기술을 사용했고 어떤 문제를 해결했나요?",
      "intent": "확장성 있는 시스템 설계 경험 평가",
      "difficulty": "intermediate"
    },
    {
      "category": "문제 해결",
      "question": "서비스 장애 상황에서 어떻게 대응했나요? 근본 원인 분석과 재발 방지 대책은?",
      "intent": "장애 대응 능력 및 시스템 사고 평가",
      "difficulty": "advanced"
    }
  ],
  "interview_tips": [
    "구체적인 수치와 임팩트 강조",
    "대규모 서비스 운영 경험 어필",
    "기술적 트레이드오프 고려 과정 설명"
  ],
  "recent_trends": [
    "AI/ML 관련 질문 증가",
    "클라우드 네이티브 경험 중시",
    "마이크로서비스 아키텍처 이해도 평가"
  ]
}
```

#### 2.2.2 맞춤형 질문 생성
```yaml
기능명: 회사별 맞춤 질문 생성
입력: 포트폴리오 + 회사 선택
출력: 해당 회사 스타일의 맞춤 질문 5-10개
개인화: 사용자 경험 수준별 난이도 조절
```

#### 2.2.3 면접 전략 제공
```yaml
기능명: 회사별 면접 전략 가이드
내용: 준비 방법, 주의사항, 성공 팁
형식: 체크리스트 + 상세 가이드
업데이트: 실시간 면접 후기 반영
```

### 2.3 데이터 수집 및 관리

#### 2.3.1 데이터 소스
```yaml
1차 소스 (공식):
  - 회사 채용 페이지
  - 기술 블로그
  - 컨퍼런스 발표 자료
  - 공식 채용 설명회

2차 소스 (커뮤니티):
  - 블라인드 면접 후기
  - 프로그래머스 후기
  - 개발자 커뮤니티 글
  - LinkedIn 포스트

3차 소스 (자체 수집):
  - Forky 사용자 피드백
  - 면접 성공/실패 사례
  - 실제 면접 질문 수집
```

#### 2.3.2 데이터베이스 스키마
```sql
-- 회사 정보 테이블
CREATE TABLE companies (
    id UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    industry VARCHAR(50),
    size VARCHAR(20),
    tech_stack JSONB,
    culture_info JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 면접 문화 정보 테이블
CREATE TABLE interview_cultures (
    id UUID PRIMARY KEY,
    company_id UUID REFERENCES companies(id),
    style VARCHAR(100),
    duration_minutes INTEGER,
    rounds JSONB,
    evaluation_criteria JSONB,
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 질문 데이터베이스
CREATE TABLE company_questions (
    id UUID PRIMARY KEY,
    company_id UUID REFERENCES companies(id),
    category VARCHAR(50),
    question TEXT NOT NULL,
    intent TEXT,
    difficulty VARCHAR(20),
    frequency_score INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 면접 팁 테이블
CREATE TABLE interview_tips (
    id UUID PRIMARY KEY,
    company_id UUID REFERENCES companies(id),
    tip_text TEXT NOT NULL,
    category VARCHAR(50),
    priority INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 2.4 UI/UX 요구사항

#### 2.4.1 회사 선택 화면
```
┌─────────────────────────────────────────┐
│ 🏢 면접 준비할 회사를 선택하세요          │
├─────────────────────────────────────────┤
│ [🔍 검색창: 회사명 입력]                 │
│                                         │
│ 📊 인기 기업                            │
│ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐        │
│ │네이버│ │카카오│ │쿠팡 │ │배민 │        │
│ │대기업│ │대기업│ │외국계│ │유니콘│       │
│ └─────┘ └─────┘ └─────┘ └─────┘        │
│                                         │
│ 🏭 기업 규모별                          │
│ • 대기업 (50개사)                       │
│ • 유니콘 (20개사)                       │
│ • 스타트업 (100개사)                    │
│                                         │
│ 💻 기술 분야별                          │
│ • 백엔드 • 프론트엔드 • 풀스택          │
│ • AI/ML • 데이터 • 인프라               │
└─────────────────────────────────────────┘
```

#### 2.4.2 회사 정보 상세 화면
```
┌─────────────────────────────────────────┐
│ 🏢 네이버 면접 정보                      │
├─────────────────────────────────────────┤
│ 📋 기본 정보                            │
│ • 업계: 포털/검색 서비스                 │
│ • 규모: 대기업 (5,000명+)               │
│ • 주요 기술: Java, Spring, React        │
│                                         │
│ 🎯 면접 스타일                          │
│ • 기술 깊이 중심 (40%)                  │
│ • 문제 해결 능력 (30%)                  │
│ • 커뮤니케이션 (20%)                    │
│ • 문화 적합성 (10%)                     │
│                                         │
│ 💡 핵심 팁                              │
│ ✅ 대규모 서비스 운영 경험 강조          │
│ ✅ 구체적인 성과 지표 준비               │
│ ✅ 기술적 트레이드오프 고려 과정         │
│                                         │
│ 📈 최근 트렌드                          │
│ • AI/ML 관련 질문 증가 (↑30%)           │
│ • 클라우드 경험 중시 (↑25%)             │
│                                         │
│ [맞춤 질문 생성하기] [면접 후기 보기]    │
└─────────────────────────────────────────┘
```

---

## 📝 기능 3: 포트폴리오 자동 개선 제안

### 3.1 기능 개요
사용자의 포트폴리오를 AI가 분석하여 부족한 부분을 식별하고, 구체적인 개선 방안을 제시하는 시스템

### 3.2 핵심 요구사항

#### 3.2.1 포트폴리오 분석 엔진
```yaml
기능명: AI 포트폴리오 분석
입력: PDF 포트폴리오 + 목표 회사/직무
출력: 구조화된 분석 결과 + 개선 제안
분석 영역: 기술 스택, 프로젝트 설명, 성과 지표, 스토리텔링
```

**분석 항목**:
```json
{
  "analysis_result": {
    "technical_skills": {
      "present_skills": ["React", "Node.js", "MySQL"],
      "missing_skills": ["Redis", "Docker", "AWS"],
      "skill_depth_score": 75,
      "market_alignment": 80
    },
    "project_descriptions": {
      "clarity_score": 65,
      "technical_detail_score": 70,
      "business_impact_score": 45,
      "quantification_score": 30
    },
    "storytelling": {
      "star_method_usage": 40,
      "coherence_score": 75,
      "uniqueness_score": 60
    },
    "overall_score": 68
  }
}
```

#### 3.2.2 맞춤형 개선 제안
```yaml
기능명: 개선 제안 생성
우선순위: 임팩트 vs 구현 난이도 매트릭스
개인화: 목표 회사별 맞춤 제안
실행 가능성: 구체적이고 실행 가능한 액션 아이템
```

**개선 제안 구조**:
```json
{
  "improvement_suggestions": {
    "high_priority": [
      {
        "category": "성과 지표 정량화",
        "current_issue": "프로젝트 결과가 추상적으로 기술됨",
        "suggestion": "API 응답 시간 개선, 사용자 증가율 등 구체적 수치 추가",
        "example": "사용자 경험 개선 → 로딩 시간 3초에서 0.8초로 75% 단축",
        "impact": "high",
        "effort": "low"
      }
    ],
    "medium_priority": [
      {
        "category": "기술 스택 보완",
        "current_issue": "목표 회사에서 요구하는 Redis 경험 부족",
        "suggestion": "기존 프로젝트에 캐싱 레이어 추가 구현",
        "example": "사용자 세션 관리를 위한 Redis 도입 사례 추가",
        "impact": "high",
        "effort": "medium"
      }
    ],
    "low_priority": [
      {
        "category": "프로젝트 다양성",
        "current_issue": "웹 개발 프로젝트만 있음",
        "suggestion": "모바일 앱 또는 데이터 분석 프로젝트 추가",
        "example": "React Native를 활용한 모바일 앱 개발",
        "impact": "medium",
        "effort": "high"
      }
    ]
  }
}
```

#### 3.2.3 회사별 맞춤 버전 생성
```yaml
기능명: 회사별 포트폴리오 최적화
입력: 기본 포트폴리오 + 목표 회사
출력: 회사 맞춤형 포트폴리오 버전
차별화: 회사가 중시하는 가치에 맞춘 강조점 조정
```

### 3.3 기술 요구사항

#### 3.3.1 분석 API 설계
```python
# 포트폴리오 분석 API
POST /api/v1/portfolio/analyze
{
  "portfolio_text": "포트폴리오 전체 텍스트",
  "target_company": "네이버",
  "target_position": "백엔드 개발자",
  "experience_level": "3년차"
}

# 응답 구조
{
  "analysis_id": "uuid",
  "overall_score": 68,
  "detailed_analysis": {...},
  "improvement_suggestions": {...},
  "estimated_improvement_time": "2-3주",
  "success_rate_prediction": 75
}
```

#### 3.3.2 개선 추적 시스템
```sql
-- 포트폴리오 분석 히스토리
CREATE TABLE portfolio_analyses (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    portfolio_version INTEGER DEFAULT 1,
    analysis_data JSONB NOT NULL,
    overall_score INTEGER,
    target_company VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

-- 개선 제안 추적
CREATE TABLE improvement_suggestions (
    id UUID PRIMARY KEY,
    analysis_id UUID REFERENCES portfolio_analyses(id),
    category VARCHAR(100) NOT NULL,
    suggestion_text TEXT NOT NULL,
    priority VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    completed_at TIMESTAMP
);

-- 개선 진행률 추적
CREATE TABLE improvement_progress (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    suggestion_id UUID REFERENCES improvement_suggestions(id),
    progress_percentage INTEGER DEFAULT 0,
    notes TEXT,
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### 3.4 UI/UX 요구사항

#### 3.4.1 분석 결과 대시보드
```
┌─────────────────────────────────────────┐
│ 📊 포트폴리오 분석 결과                  │
├─────────────────────────────────────────┤
│ 전체 점수: 68/100 ⭐⭐⭐☆☆              │
│                                         │
│ 📈 영역별 점수                          │
│ 기술 스택 매칭    ████████░░ 80%        │
│ 프로젝트 설명     ██████░░░░ 65%        │
│ 성과 지표        ███░░░░░░░ 30%        │
│ 스토리텔링       ██████░░░░ 60%        │
│                                         │
│ 🎯 네이버 맞춤 분석                     │
│ 적합도: 75% (상위 25%)                  │
│ 부족한 영역: 대규모 시스템 경험          │
│                                         │
│ [상세 분석 보기] [개선 계획 세우기]      │
└─────────────────────────────────────────┘
```

#### 3.4.2 개선 제안 화면
```
┌─────────────────────────────────────────┐
│ 🔧 포트폴리오 개선 제안                  │
├─────────────────────────────────────────┤
│ 🚨 즉시 개선 필요 (High Priority)        │
│                                         │
│ 1. 성과 지표 정량화 ⏱️ 2일 소요          │
│    현재: "사용자 경험을 개선했습니다"     │
│    개선: "로딩 시간을 3초→0.8초로 75% 단축" │
│    💡 팁: 구체적 수치가 면접관 관심 유발  │
│    [✅ 완료] [📝 메모]                   │
│                                         │
│ 2. Redis 캐싱 경험 추가 ⏱️ 1주 소요      │
│    현재: 데이터베이스 직접 조회           │
│    개선: Redis 캐싱으로 응답속도 개선 사례 │
│    💡 팁: 네이버에서 중요하게 평가하는 기술 │
│    [🚀 시작하기] [📚 학습 자료]          │
│                                         │
│ ⚠️ 중간 우선순위 (Medium Priority)       │
│ 3. STAR 기법 적용 ⏱️ 3일 소요           │
│ 4. 팀워크 사례 보강 ⏱️ 1주 소요          │
│                                         │
│ 📊 예상 효과                            │
│ 개선 완료 시 점수: 68점 → 85점 (+17점)   │
│ 면접 합격 확률: 60% → 85% (+25%p)       │
└─────────────────────────────────────────┘
```

#### 3.4.3 회사별 비교 화면
```
┌─────────────────────────────────────────┐
│ 🏢 회사별 포트폴리오 적합도 분석         │
├─────────────────────────────────────────┤
│ 네이버     ████████░░ 80% 적합          │
│ • 강점: 대용량 데이터 처리 경험          │
│ • 약점: 시스템 모니터링 경험 부족        │
│                                         │
│ 카카오     ██████░░░░ 65% 적합          │
│ • 강점: 사용자 중심 개발 사고            │
│ • 약점: 창의적 문제 해결 사례 부족       │
│                                         │
│ 쿠팡      ███████░░░ 70% 적합           │
│ • 강점: 성능 최적화 경험                │
│ • 약점: 비즈니스 임팩트 정량화 부족      │
│                                         │
│ [네이버 맞춤 버전 생성] [전체 비교표]    │
└─────────────────────────────────────────┘
```

---

## 🚀 구현 계획

### Phase 1: 기본 기능 구현 (4주)
- **1-2주**: 실시간 피드백 시스템 MVP
- **3주**: 회사별 문화 DB 구축 (상위 20개사)
- **4주**: 포트폴리오 분석 기본 기능

### Phase 2: 고도화 (4주)
- **5-6주**: AI 피드백 정확도 향상
- **7주**: 회사 DB 확장 (100개사)
- **8주**: 개선 제안 시스템 고도화

### Phase 3: 통합 및 최적화 (4주)
- **9-10주**: 기능 간 연동 및 사용자 플로우 최적화
- **11주**: 성능 최적화 및 버그 수정
- **12주**: 베타 테스트 및 피드백 반영

## 📊 성공 지표

### 정량적 지표
- **사용자 만족도**: NPS 70+ 달성
- **피드백 정확도**: 85% 이상
- **개선 제안 실행률**: 60% 이상
- **면접 성공률**: 70% → 85% 향상

### 정성적 지표
- **사용자 피드백**: "실제 도움이 되는 구체적 조언"
- **차별화 인식**: "다른 서비스와 확실히 다름"
- **재사용 의도**: "지속적으로 사용하고 싶음"

이 명세서를 바탕으로 **3개월 내에 핵심 기능을 구현**하여 Forky의 경쟁력을 크게 향상시킬 수 있습니다!