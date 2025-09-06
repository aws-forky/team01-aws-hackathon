# Forky 향상된 기능 구현을 위한 AI 프롬프팅 가이드

## 🤖 AI 구현 지시사항

이 문서는 AI가 Forky 프로젝트의 향상된 기능을 정확하게 구현할 수 있도록 작성된 구체적인 프롬프팅 가이드입니다.

---

## 📝 프롬프팅 전략 적용

### 1. 역할 기반 프롬프팅 (Role-Based Prompting)
```
당신은 React/TypeScript와 FastAPI를 전문으로 하는 풀스택 개발자입니다.
Forky 프로젝트의 기존 코드베이스를 분석하고, 새로운 기능을 기존 아키텍처와 일관성 있게 통합해야 합니다.
```

### 2. 단계별 분해 프롬프팅 (Step-by-Step Decomposition)
```
다음 순서로 구현하세요:
1단계: 기존 코드 구조 분석
2단계: 새로운 컴포넌트 설계
3단계: 상태 관리 로직 구현
4단계: API 연동
5단계: UI/UX 구현
6단계: 테스트 및 최적화
```

### 3. 예시 기반 프롬프팅 (Few-Shot Prompting)
```
기존 컴포넌트 패턴을 따라 구현하세요:

예시 1 - 기존 질문 컴포넌트:
// components/Question.tsx
interface QuestionProps {
  question: string;
  onAnswer: (answer: string) => void;
}

예시 2 - 새로운 음성 컴포넌트 (구현 필요):
// components/VoiceRecorder.tsx  
interface VoiceRecorderProps {
  onTranscript: (text: string) => void;
  isRecording: boolean;
}
```

---

## 🎯 구체적 구현 프롬프트

### Phase 1: 음성 인식 기능 구현

#### 프롬프트 1-1: VoiceRecorder 컴포넌트 생성
```
다음 요구사항에 따라 VoiceRecorder.tsx 컴포넌트를 생성하세요:

REQUIREMENTS:
- Web Speech API의 SpeechRecognition 사용
- 한국어 음성 인식 지원 (lang: 'ko-KR')
- 실시간 음성-텍스트 변환
- 녹음 상태 시각적 표시 (마이크 아이콘 + 파형 애니메이션)
- 음성 인식 오류 처리
- TypeScript 타입 안전성 보장

INTERFACE:
interface VoiceRecorderProps {
  onTranscript: (text: string) => void;
  onError?: (error: string) => void;
  isActive: boolean;
  className?: string;
}

MUST INCLUDE:
- 마이크 권한 요청 처리
- 브라우저 호환성 체크
- 음성 입력 중 시각적 피드백
- 음성 인식 중단/재시작 기능
```

#### 프롬프트 1-2: 음성/텍스트 통합 입력 컴포넌트
```
기존 텍스트 입력을 확장하여 음성 입력도 지원하는 AnswerInput.tsx를 수정하세요:

CURRENT STATE:
- 텍스트 입력만 지원
- 실시간 피드백 연동

TARGET STATE:  
- 텍스트 + 음성 입력 병행 지원
- 모드 전환 버튼 (텍스트 ↔ 음성)
- 음성 입력 결과를 텍스트 영역에 자동 입력
- 음성 입력 후 텍스트 편집 가능

IMPLEMENTATION GUIDE:
1. useState로 inputMode 상태 관리 ('text' | 'voice')
2. VoiceRecorder 컴포넌트 조건부 렌더링
3. 음성 인식 결과를 기존 텍스트 상태에 병합
4. 모드 전환 시 부드러운 애니메이션 적용
```

### Phase 2: 구조화된 질문 시스템 구현

#### 프롬프트 2-1: 질문 데이터 구조 설계
```
다음 TypeScript 인터페이스를 정의하고 관련 타입을 생성하세요:

REQUIRED TYPES:
interface MainQuestion {
  id: string;
  title: string;        // 질문 제목 (카드에 표시)
  content: string;      // 실제 질문 내용
  category: string;     // 기술 분야 (예: "React", "알고리즘")
  difficulty: 'Easy' | 'Medium' | 'Hard';
  estimatedTime: number; // 예상 답변 시간 (분)
}

interface FollowUpQuestion {
  id: string;
  parentQuestionId: string;
  content: string;
  order: number;        // 1, 2, 3 순서
  basedOnAnswer?: string; // 이전 답변 기반 생성된 경우
}

interface InterviewSession {
  id: string;
  mainQuestions: MainQuestion[];
  currentMainQuestionId: string | null;
  followUpQuestions: FollowUpQuestion[];
  completedMainQuestions: string[];
  answers: Answer[];
  startTime: Date;
  currentStep: 'selection' | 'main-answer' | 'followup' | 'completed';
}

VALIDATION RULES:
- 메인 질문은 정확히 10개
- 각 메인 질문당 꼬리 질문 최대 3개
- ID는 UUID 형태로 생성
```

#### 프롬프트 2-2: QuestionSelector 컴포넌트 구현
```
메인 질문 선택을 위한 QuestionSelector.tsx 컴포넌트를 구현하세요:

LAYOUT REQUIREMENTS:
- 3x4 그리드 레이아웃 (10개 + 2개 빈 공간)
- 각 카드는 200x150px 크기
- 반응형 디자인 (모바일에서는 2열)

CARD DESIGN:
- 질문 제목 (최대 2줄, 말줄임표 처리)
- 카테고리 배지 (색상 구분)
- 난이도 표시 (별점 또는 색상)
- 완료 상태 표시 (체크마크)
- 호버 효과 및 클릭 애니메이션

STATE MANAGEMENT:
- 선택 가능한 질문만 활성화
- 완료된 질문은 비활성화 (회색 처리)
- 선택 시 부모 컴포넌트에 콜백 전달

ACCESSIBILITY:
- 키보드 네비게이션 지원
- 스크린 리더 호환성
- 포커스 표시
```

#### 프롬프트 2-3: 면접 진행 로직 구현
```
InterviewFlow.tsx 컴포넌트에서 전체 면접 진행을 관리하세요:

FLOW CONTROL:
1. 초기 상태: 10개 메인 질문 표시
2. 질문 선택: 사용자가 1개 선택
3. 메인 답변: 선택된 질문에 답변
4. 꼬리 질문: 답변 기반으로 3개 꼬리 질문 순차 진행
5. 완료 처리: 해당 메인 질문을 완료 목록에 추가
6. 반복: 남은 질문이 있으면 1단계로 돌아감
7. 종료: 모든 질문 완료 시 결과 페이지로 이동

STATE TRANSITIONS:
selection → main-answer → followup-1 → followup-2 → followup-3 → selection
                                                                    ↓
                                                               completed

ERROR HANDLING:
- 네트워크 오류 시 재시도 옵션
- 답변 저장 실패 시 로컬 백업
- 세션 만료 시 복구 기능

PROGRESS TRACKING:
- 전체 진행률 표시 (완료된 메인 질문 / 10)
- 현재 단계 표시
- 예상 남은 시간 계산
```

### Phase 3: 결과 페이지 및 PDF 구현

#### 프롬프트 3-1: InterviewResult 컴포넌트 구현
```
최종 면접 결과를 표시하는 InterviewResult.tsx를 구현하세요:

LAYOUT STRUCTURE:
1. 헤더 섹션
   - 면접 완료 축하 메시지
   - 전체 소요 시간
   - 총 점수 (100점 만점)

2. 요약 카드 섹션
   - 답변한 질문 수: 40개 (10 메인 + 30 꼬리)
   - 평균 답변 시간
   - 카테고리별 점수 분포

3. 상세 결과 섹션 (아코디언)
   - 각 메인 질문별로 그룹화
   - 메인 답변 + 3개 꼬리 답변
   - 각 답변의 점수, 피드백, 개선사항

4. 분석 섹션
   - 강점 분석 (잘한 부분)
   - 약점 분석 (개선 필요)
   - 추천 학습 방향

5. 액션 섹션
   - PDF 다운로드 버튼
   - 새로운 면접 시작 버튼
   - 결과 공유 기능

DATA VISUALIZATION:
- 카테고리별 점수 레이더 차트
- 시간별 답변 품질 그래프
- 난이도별 성과 막대 차트
```

#### 프롬프트 3-2: PDF 생성 기능 구현
```
jsPDF와 html2canvas를 사용하여 PDFGenerator.tsx를 구현하세요:

PDF STRUCTURE:
페이지 1: 커버 페이지
- Forky 로고
- 면접자 정보 (선택사항)
- 면접 일시
- 전체 점수

페이지 2-3: 요약 및 분석
- 전체 요약 통계
- 강점/약점 분석
- 카테고리별 성과 차트

페이지 4-N: 상세 질문별 결과
- 각 메인 질문당 1페이지
- 질문 내용
- 사용자 답변
- 점수 및 피드백
- 꼬리 질문들과 답변

FORMATTING REQUIREMENTS:
- A4 사이즈 (210 x 297mm)
- 여백: 상하좌우 20mm
- 폰트: 나눔고딕 또는 시스템 기본 폰트
- 색상: 브랜드 컬러 적용
- 페이지 번호 및 헤더/푸터

IMPLEMENTATION DETAILS:
1. HTML 템플릿을 숨겨진 div에 렌더링
2. html2canvas로 각 섹션을 이미지로 변환
3. jsPDF로 이미지들을 PDF에 조합
4. 다운로드 진행률 표시
5. 생성 완료 후 파일 자동 다운로드
```

### Phase 4: 백엔드 API 수정

#### 프롬프트 4-1: 구조화된 질문 생성 API
```
backend/routes.py에 새로운 엔드포인트를 추가하세요:

ENDPOINT: POST /api/generate-structured-questions
INPUT: 
- portfolio_text: str (분석된 포트폴리오 텍스트)
- company_info: Optional[str] (회사 정보)
- job_position: Optional[str] (지원 직무)

OUTPUT:
{
  "main_questions": [
    {
      "id": "uuid",
      "title": "React 상태 관리 경험",
      "content": "프로젝트에서 Redux를 사용한 이유와 장단점을 설명해주세요.",
      "category": "React",
      "difficulty": "Medium",
      "estimated_time": 3
    }
    // ... 9개 더
  ]
}

GENERATION LOGIC:
1. 포트폴리오에서 기술 스택 추출
2. 각 기술별로 1-2개 질문 생성
3. 난이도 분산 (Easy: 3개, Medium: 5개, Hard: 2개)
4. 카테고리 균형 맞추기
5. 회사/직무 정보 반영하여 맞춤화

PROMPT TEMPLATE:
"다음 포트폴리오를 분석하여 기술면접 질문 10개를 생성하세요.
각 질문은 구체적이고 실무 중심적이어야 하며, 포트폴리오의 기술 스택과 연관되어야 합니다.
질문 형식: 경험 기반 + 기술적 깊이 + 문제 해결 능력 평가"
```

#### 프롬프트 4-2: 꼬리 질문 생성 API
```
ENDPOINT: POST /api/generate-followup-questions
INPUT:
- main_question_id: str
- main_question_content: str  
- user_answer: str
- followup_count: int (1, 2, 또는 3)

OUTPUT:
{
  "followup_question": {
    "id": "uuid",
    "parent_question_id": "main_question_id",
    "content": "방금 말씀하신 Redux의 단점을 해결하기 위해 어떤 대안을 고려해보셨나요?",
    "order": 1,
    "based_on_answer": "user_answer의 핵심 키워드"
  }
}

GENERATION STRATEGY:
1차 꼬리질문: 답변의 구체적 예시 요구
2차 꼬리질문: 문제 상황 및 해결 과정
3차 꼬리질문: 개선 방안 및 미래 계획

PROMPT ENGINEERING:
"사용자의 답변을 분석하여 다음 단계의 꼬리질문을 생성하세요.
- 답변의 핵심 키워드를 파악
- 더 깊이 있는 기술적 이해도 확인
- 실무 경험의 구체성 검증
- 문제 해결 능력 평가"
```

---

## 🔧 구현 시 주의사항

### 코드 품질 가이드라인
```
1. TypeScript 엄격 모드 사용
2. ESLint/Prettier 규칙 준수
3. 컴포넌트당 200줄 이하 유지
4. 커스텀 훅으로 로직 분리
5. 에러 바운더리 적용
6. 로딩 상태 및 에러 처리
7. 접근성 가이드라인 준수
8. 성능 최적화 (React.memo, useMemo)
```

### 테스트 전략
```
1. 단위 테스트: 각 컴포넌트별 Jest + RTL
2. 통합 테스트: 전체 플로우 시나리오
3. E2E 테스트: 음성 인식 포함 전체 과정
4. 성능 테스트: 대용량 데이터 처리
5. 접근성 테스트: 스크린 리더 호환성
```

### 배포 고려사항
```
1. 환경변수 설정 (STT API 키 등)
2. HTTPS 필수 (음성 인식 권한)
3. 브라우저 호환성 체크
4. 모바일 반응형 최적화
5. 성능 모니터링 설정
```

---

## 📋 최종 검증 체크리스트

### 기능 검증
- [ ] 음성 인식이 정확하게 작동하는가?
- [ ] 10개 메인 질문이 올바르게 생성되는가?
- [ ] 꼬리 질문이 답변에 기반하여 생성되는가?
- [ ] 전체 플로우가 끊김없이 진행되는가?
- [ ] PDF 다운로드가 정상 작동하는가?

### 사용자 경험 검증
- [ ] 직관적인 인터페이스인가?
- [ ] 로딩 시간이 적절한가?
- [ ] 에러 상황에서 적절한 안내가 제공되는가?
- [ ] 모바일에서도 사용하기 편한가?
- [ ] 접근성 요구사항을 만족하는가?

### 기술적 검증
- [ ] 코드 품질이 기존 프로젝트와 일관성이 있는가?
- [ ] 성능 최적화가 적용되었는가?
- [ ] 보안 취약점이 없는가?
- [ ] 테스트 커버리지가 충분한가?
- [ ] 문서화가 완료되었는가?