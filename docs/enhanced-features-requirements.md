# Forky 향상된 기능 요구사항 명세서

## 🎯 핵심 목표
기존 텍스트 기반 면접 시뮬레이터에 **음성 인식(STT)** 기능과 **구조화된 질문 시스템**을 추가하여 더욱 현실적인 면접 경험을 제공합니다.

---

## 📋 기능별 상세 요구사항

### 1. 음성 인식(STT) 기능 추가

#### 🔍 현재 상태 (AS-IS)
- 사용자가 텍스트로만 답변 입력 가능

#### 🚀 목표 상태 (TO-BE)
- 텍스트 입력 + 음성 입력 **병행 지원**
- 사용자가 선택적으로 음성 또는 텍스트로 답변 가능

#### 🛠 구현 요구사항
```
MUST IMPLEMENT:
1. Web Speech API 또는 외부 STT 서비스 연동
2. 마이크 권한 요청 및 음성 녹음 기능
3. 실시간 음성-텍스트 변환
4. 음성 입력 중 시각적 피드백 (녹음 상태 표시)
5. 음성 입력 완료 후 텍스트 편집 가능
```

---

### 2. 구조화된 질문 시스템 개편

#### 🔍 현재 상태 (AS-IS)
- 연속적인 질문 진행 방식

#### 🚀 목표 상태 (TO-BE)
- **2단계 질문 구조**: 메인 질문 → 꼬리 질문
- **선택적 진행**: 사용자가 질문 순서 결정

#### 📊 질문 구조 설계
```
총 질문 구조:
├── 메인 질문 10개 (포트폴리오 기반 생성)
└── 각 메인 질문당 꼬리 질문 3개
    = 총 최대 30개 질문 (10 메인 + 3 꼬리)
```

#### 🔄 진행 플로우
```
STEP 1: 메인 질문 선택
- 10개 메인 질문을 카드/리스트 형태로 표시
- 사용자가 1개 선택

STEP 2: 꼬리 질문 진행
- 선택된 메인 질문에 대한 답변 입력
- 답변 기반으로 꼬리 질문 3개 순차 진행
- 각 꼬리 질문마다 실시간 피드백 제공

STEP 3: 반복
- 완료된 질문은 비활성화 표시
- 남은 9개 메인 질문 중 다시 선택
- 모든 메인 질문 완료까지 반복

STEP 4: 결과 생성
- 전체 면접 결과 및 점수 표시
- PDF 다운로드 기능 제공
```

---

### 3. 실시간 피드백 시스템 유지

#### 📝 요구사항
```
MUST MAINTAIN:
1. 각 답변에 대한 즉시 피드백
2. 답변 품질 평가 (점수/등급)
3. 개선 제안사항 제공
4. 답변 시간 측정 및 표시
```

---

### 4. 결과 페이지 및 PDF 다운로드

#### 📄 결과 페이지 구성요소
```
MUST INCLUDE:
1. 전체 면접 요약
   - 총 소요 시간
   - 답변한 질문 수
   - 전체 평균 점수

2. 질문별 상세 결과
   - 질문 내용
   - 사용자 답변 (텍스트)
   - 점수 및 평가
   - 개선 제안사항

3. 강점 및 약점 분석
   - 잘한 부분 요약
   - 개선이 필요한 부분
   - 추천 학습 방향

4. PDF 다운로드 버튼
   - 위 모든 내용을 PDF로 생성
   - 깔끔한 레이아웃으로 포맷팅
```

---

## 🏗 기술적 구현 가이드

### Frontend 변경사항

#### 1. 새로운 컴포넌트 필요
```typescript
// 음성 입력 관련
- VoiceRecorder.tsx: 음성 녹음 및 STT 처리
- AudioVisualizer.tsx: 음성 입력 시각적 피드백

// 질문 시스템 관련  
- QuestionSelector.tsx: 메인 질문 선택 인터페이스
- InterviewProgress.tsx: 진행 상황 표시
- QuestionCard.tsx: 개별 질문 카드 컴포넌트

// 결과 관련
- InterviewResult.tsx: 최종 결과 페이지
- PDFGenerator.tsx: PDF 생성 및 다운로드
```

#### 2. 상태 관리 구조
```typescript
interface InterviewState {
  mainQuestions: Question[];           // 10개 메인 질문
  currentMainQuestion: Question | null; // 현재 선택된 메인 질문
  followUpQuestions: Question[];       // 현재 꼬리 질문들
  completedQuestions: string[];        // 완료된 질문 ID들
  answers: Answer[];                   // 모든 답변 기록
  currentStep: 'selection' | 'answering' | 'result';
  isVoiceMode: boolean;               // 음성/텍스트 모드
}
```

### Backend 변경사항

#### 1. API 엔드포인트 추가/수정
```python
# 새로운 엔드포인트
POST /api/generate-structured-questions  # 구조화된 질문 생성
POST /api/generate-followup-questions    # 꼬리 질문 생성  
POST /api/evaluate-answer               # 답변 평가 (기존 유지)
POST /api/generate-final-report         # 최종 결과 생성
POST /api/generate-pdf                  # PDF 생성

# STT 관련 (선택사항 - 프론트엔드에서 처리 가능)
POST /api/speech-to-text               # 음성을 텍스트로 변환
```

#### 2. 데이터 모델 수정
```python
class StructuredQuestions(BaseModel):
    main_questions: List[MainQuestion]
    
class MainQuestion(BaseModel):
    id: str
    title: str
    content: str
    category: str
    difficulty: str
    
class FollowUpQuestion(BaseModel):
    id: str
    parent_question_id: str
    content: str
    based_on_answer: str
```

---

## 🎨 UI/UX 설계 가이드

### 1. 메인 질문 선택 화면
```
레이아웃:
- 그리드 형태로 10개 질문 카드 배치
- 각 카드에 질문 제목, 카테고리, 난이도 표시
- 완료된 질문은 체크마크와 함께 비활성화
- 진행률 표시바 상단에 배치
```

### 2. 답변 입력 화면
```
레이아웃:
- 질문 표시 영역 (상단)
- 답변 입력 영역 (중앙)
  - 텍스트 입력창
  - 음성 입력 버튼 (마이크 아이콘)
  - 음성 입력 시 파형 애니메이션
- 실시간 피드백 영역 (하단)
```

### 3. 결과 페이지
```
레이아웃:
- 전체 요약 카드 (상단)
- 질문별 상세 결과 (아코디언 형태)
- 강점/약점 분석 차트
- PDF 다운로드 버튼 (고정 위치)
```

---

## ✅ 구현 체크리스트

### Phase 1: 음성 인식 기능
- [ ] Web Speech API 연동
- [ ] 마이크 권한 처리
- [ ] 음성 녹음 UI 구현
- [ ] 실시간 STT 변환
- [ ] 음성/텍스트 모드 전환

### Phase 2: 구조화된 질문 시스템
- [ ] 메인 질문 생성 API 수정
- [ ] 질문 선택 UI 구현
- [ ] 꼬리 질문 생성 로직
- [ ] 진행 상태 관리
- [ ] 질문 완료 처리

### Phase 3: 결과 및 PDF 기능
- [ ] 최종 결과 페이지 구현
- [ ] PDF 생성 라이브러리 연동
- [ ] 결과 데이터 구조화
- [ ] PDF 다운로드 기능

### Phase 4: 통합 테스트
- [ ] 전체 플로우 테스트
- [ ] 음성 인식 정확도 검증
- [ ] PDF 생성 품질 확인
- [ ] 사용자 경험 최적화

---

## 🚨 주의사항 및 제약조건

1. **음성 인식 정확도**: 한국어 STT 정확도 고려하여 텍스트 편집 기능 필수
2. **브라우저 호환성**: Web Speech API 지원 브라우저 확인 필요
3. **성능 최적화**: 음성 데이터 처리로 인한 메모리 사용량 관리
4. **사용자 경험**: 음성 입력 실패 시 대체 방안 제공
5. **데이터 보안**: 음성 데이터 처리 시 개인정보 보호 고려

---

## 📚 참고 자료

- [Web Speech API Documentation](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API)
- [jsPDF Library](https://github.com/parallax/jsPDF)
- [React Speech Kit](https://github.com/MikeyParton/react-speech-kit)
- [html2canvas for PDF](https://github.com/niklasvh/html2canvas)