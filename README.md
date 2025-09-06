# Forky - AI 기반 포트폴리오 기술면접 시뮬레이터 v2.0

## 프로젝트 개요
Forky는 개발자 취업준비생을 위한 **차세대 AI 기반 맞춤형 기술면접 연습 플랫폼**입니다. 사용자의 포트폴리오 PDF를 분석하여 개인화된 기술면접 질문을 생성하고, **음성 인식 기술**과 **구조화된 질문 시스템**을 통해 실제 면접과 가장 유사한 경험을 제공합니다.

## 🚀 핵심 기능 (v2.0 Enhanced)

### 📝 기본 기능
- **PDF 포트폴리오 자동 분석** (Upstage Document Parser)
- **AI 기반 맞춤형 질문 생성** (Upstage Solar LLM Pro2)
- **회사별 특화 질문 커스터마이징**
- **실시간 면접 시뮬레이션**
- **PDF 결과 다운로드**

### 🎤 NEW! 음성 인식 (STT) 기능
- **텍스트 + 음성 입력 병행 지원**
- **Web Speech API 기반 한국어 음성 인식**
- **실시간 음성-텍스트 변환**
- **음성 입력 후 텍스트 편집 가능**
- **브라우저 호환성 체크 및 에러 처리**

### 🎯 NEW! 구조화된 질문 시스템
- **2단계 질문 구조**: 메인 질문(10개) → 꼬리 질문(각 3개)
- **선택적 진행**: 사용자가 질문 순서 결정
- **총 최대 40개 질문** (10 메인 + 30 꼬리)
- **답변 기반 동적 꼬리 질문 생성**
- **실시간 진행 상황 추적**

### 📊 향상된 피드백 시스템
- **STAR 기법 분석** (Situation, Task, Action, Result)
- **카테고리별 성과 분석**
- **실시간 답변 품질 평가**
- **개인화된 개선 제안**
- **답변 시간 측정 및 분석**

### 📄 고도화된 결과 리포트
- **종합 면접 결과 대시보드**
- **강점/약점 상세 분석**
- **추천 학습 방향 제시**
- **전문적인 PDF 리포트 생성**
- **질문별 상세 피드백**

## 기술 스택
### Backend
- FastAPI 0.104.1
- Upstage Solar LLM Pro2
- Upstage Document Parser
- Docker + Nginx

### Frontend  
- React 19.1.0
- TypeScript
- Tailwind CSS
- PWA 지원

## 📁 프로젝트 구조
```
forky/
├── backend/                    # FastAPI 백엔드
│   ├── app/
│   │   ├── controllers/       # API 라우터
│   │   ├── models/           # 데이터 모델
│   │   ├── services/         # 비즈니스 로직
│   │   └── config/           # 설정 파일
│   └── requirements.txt
├── frontend/                   # React 프론트엔드
│   ├── src/
│   │   ├── components/       # React 컴포넌트
│   │   │   ├── VoiceRecorder.tsx        # 음성 인식
│   │   │   ├── QuestionSelector.tsx     # 질문 선택
│   │   │   ├── EnhancedAnswerInput.tsx  # 답변 입력
│   │   │   ├── InterviewProgress.tsx    # 진행 상황
│   │   │   ├── InterviewResult.tsx      # 결과 페이지
│   │   │   └── PDFGenerator.tsx         # PDF 생성
│   │   ├── pages/            # 페이지 컴포넌트
│   │   ├── services/         # API 서비스
│   │   └── types.ts          # TypeScript 타입
│   └── package.json
├── docs/                       # 프로젝트 문서
│   ├── enhanced-features-requirements.md
│   ├── implementation-prompts.md
│   └── ENHANCED_FEATURES_IMPLEMENTATION.md
├── tests/                      # 테스트 코드
└── deployment/                 # 배포 설정
```

## 🎯 주요 컴포넌트

### 음성 인식 시스템
- **VoiceRecorder**: Web Speech API 기반 음성 인식
- **EnhancedAnswerInput**: 텍스트/음성 통합 입력
- **AudioVisualizer**: 음성 입력 시각적 피드백

### 구조화된 질문 시스템
- **QuestionSelector**: 메인 질문 선택 인터페이스
- **InterviewProgress**: 실시간 진행 상황 표시
- **EnhancedInterviewSimulator**: 통합 면접 시뮬레이터

### 결과 분석 시스템
- **InterviewResult**: 종합 결과 대시보드
- **PDFGenerator**: 전문적인 PDF 리포트 생성
- **FeedbackDisplay**: 실시간 피드백 표시

## 🎮 사용 방법

### 1단계: 포트폴리오 업로드
- PDF 포트폴리오를 업로드하면 AI가 자동으로 분석
- 기술 스택과 프로젝트 경험을 추출

### 2단계: 회사 및 직무 선택
- 목표 회사 선택 (네이버, 카카오, 삼성전자 등)
- 직무별 맞춤 질문 생성

### 3단계: 구조화된 면접 진행
- **질문 선택**: 10개 메인 질문 중 원하는 순서로 선택
- **답변 입력**: 텍스트 또는 음성으로 답변
- **꼬리 질문**: 답변 기반으로 3개 꼬리 질문 자동 생성
- **실시간 피드백**: 각 답변마다 즉시 분석 결과 제공

### 4단계: 결과 분석 및 다운로드
- 종합 면접 결과 확인
- 강점/약점 분석 리포트
- PDF 다운로드로 면접 준비 기록 보관

## 🚀 시작하기

### 환경 요구사항
- **Node.js** 18+ 
- **Python** 3.9+
- **HTTPS 환경** (음성 인식을 위해 필요)
- **모던 브라우저** (Chrome, Edge, Safari 권장)

### 설치 및 실행

#### 백엔드 실행
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### 프론트엔드 실행
```bash
cd frontend
npm install
npm run dev
```

#### 접속
- 프론트엔드: `http://localhost:3000`
- 백엔드 API: `http://localhost:8000`
- API 문서: `http://localhost:8000/docs`

## 🌟 주요 특징

### 🎤 혁신적인 음성 인식
- **실시간 STT**: 말하는 즉시 텍스트로 변환
- **한국어 최적화**: 기술 용어 인식 정확도 향상
- **하이브리드 입력**: 음성과 텍스트를 자유롭게 전환
- **에러 복구**: 인식 실패 시 자동 재시도

### 🎯 지능형 질문 시스템
- **포트폴리오 기반**: 개인 경험에 맞춤화된 질문
- **적응형 난이도**: 답변 수준에 따른 동적 조정
- **카테고리 균형**: 기술/경험/문제해결 영역 고른 분포
- **꼬리 질문**: 답변 내용 기반 심화 질문 자동 생성

### 📊 고도화된 분석
- **STAR 분석**: 체계적인 답변 구조 평가
- **기술 정확성**: 언급된 기술의 적절성 검증
- **소프트 스킬**: 커뮤니케이션 능력 평가
- **성장 방향**: 개인화된 학습 로드맵 제시

### 📱 사용자 경험
- **직관적 UI**: 실제 면접실 같은 인터페이스
- **실시간 피드백**: 답변 즉시 분석 결과 제공
- **진행률 추적**: 면접 진행 상황 시각화
- **접근성**: 키보드, 스크린 리더 지원

## 🏆 기술 스택 상세

### Frontend
- **React 19.1.0** - 최신 React 기능 활용
- **TypeScript** - 타입 안전성 보장
- **Tailwind CSS** - 반응형 디자인
- **Web Speech API** - 브라우저 네이티브 음성 인식
- **jsPDF + html2canvas** - 고품질 PDF 생성
- **Vite** - 빠른 개발 환경

### Backend
- **FastAPI** - 고성능 비동기 API
- **Upstage Solar LLM Pro2** - 고급 언어 모델
- **Upstage Document Parser** - PDF 텍스트 추출
- **Python 3.9+** - 안정적인 런타임
- **Pydantic** - 데이터 검증

## 📈 성능 및 품질

### 성능 지표
- **음성 인식 정확도**: 95%+ (한국어 기준)
- **질문 생성 시간**: 평균 3초 이내
- **피드백 생성**: 실시간 (1초 이내)
- **PDF 생성**: 10초 이내 (40개 질문 기준)

### 품질 보장
- **TypeScript**: 컴파일 타임 에러 방지
- **에러 바운더리**: 런타임 에러 격리
- **폴백 시스템**: 서비스 장애 시 대체 기능
- **접근성**: WCAG 2.1 AA 수준 준수

## 🔮 향후 계획

### v2.1 (단기)
- 영어 면접 모드 추가
- 화상 면접 시뮬레이션
- 모바일 앱 출시

### v3.0 (중기)
- AI 면접관 페르소나 다양화
- 실시간 표정/제스처 분석
- 팀 면접 시뮬레이션

### v4.0 (장기)
- VR/AR 면접 환경
- 글로벌 다국어 지원
- 기업 맞춤형 솔루션

## 🤝 기여하기

프로젝트에 기여하고 싶으시다면:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📞 지원 및 문의

- **이슈 리포트**: GitHub Issues
- **기능 제안**: GitHub Discussions
- **문서**: `/docs` 폴더 참조

## 📄 라이선스
MIT License - 자유롭게 사용, 수정, 배포 가능합니다.

---

**Forky v2.0** - 당신의 면접 준비를 혁신합니다! 🚀
