# AI Interview System API

포트폴리오 기반 AI 면접 시스템 - **Claude Opus 4.1** 기반

## 🎯 프로젝트 개요

포트폴리오 PDF를 업로드하여 AI가 자동으로 면접 질문을 생성하고, 사용자 답변에 대한 실시간 피드백과 꼬리질문을 제공하는 대화형 면접 시스템입니다.

## 🚀 핵심 기능

### 면접 프로세스 파이프라인
1. **문서 파싱**: PDF → HTML 변환 (Upstage Document Parser)
2. **키워드 추출**: 해시태그용 키워드 추출
3. **질문 생성**: 원하는 개수만큼 메인 질문 생성
4. **꼬리질문 생성**: 답변 기반 후속 질문 생성
5. **실시간 평가**: 각 답변에 대한 상세한 장문 피드백
6. **종합 평가**: 전체 면접 결과 분석 리포트
7. **포트폴리오 평가**: 포트폴리오 완성도 분석 리포트

### API 엔드포인트
- `POST /api/v1/documents/parse` - PDF → HTML 변환
- `POST /api/v1/keywords/extract` - 키워드 추출
- `POST /api/v1/questions/generate` - 메인 질문 생성
- `POST /api/v1/questions/following` - 꼬리질문 생성
- `POST /api/v1/questions/evaluate` - 답변 평가 및 피드백
- `POST /api/v1/evaluate/all` - 전체 면접 결과 평가
- `POST /api/v1/evaluate/portfolio` - 포트폴리오 완성도 평가
- `GET /api/v1/health` - 시스템 상태 확인

## 🛠 기술 스택

- **Backend**: FastAPI + Uvicorn
- **AI Model**: AWS Bedrock Claude Opus 4.1
- **Document Parser**: Upstage Document Parser
- **Data Validation**: Pydantic
- **HTTP Client**: httpx
- **Environment**: python-dotenv
- **Demo**: Gradio

## 📁 프로젝트 구조

```
ai/
├── README.md                 # 프로젝트 개요 및 사용법
├── LICENSE                   # 라이선스 정보
├── requirements.txt          # Python 의존성 목록
├── .env.example             # 환경변수 템플릿
├── main.py                  # FastAPI 애플리케이션 진입점
├── config.py                # 환경설정 중앙 관리
├── run_api.py              # API 서버 실행 스크립트
├── demo.py                 # Gradio 웹 데모
├── models/
│   ├── requests.py         # Pydantic 요청 모델
│   └── responses.py        # Pydantic 응답 모델
├── routers/                # 기능별 API 라우터
│   ├── documents.py        # 문서 파싱 엔드포인트
│   ├── keywords.py         # 키워드 추출 엔드포인트
│   ├── questions.py        # 질문 생성 + 평가 엔드포인트
│   ├── evaluate.py         # 전체 평가 엔드포인트
│   └── health.py          # 헬스체크 엔드포인트
├── services/               # 핵심 비즈니스 로직
│   ├── document_parser.py  # Upstage 문서파싱 연동
│   └── llm_processor.py    # Claude Opus 4.1 처리
└── prompts/                # AI 프롬프트 템플릿
    ├── keyword_extraction.py   # 키워드 추출 프롬프트
    ├── question_generation.py  # 질문 생성 프롬프트
    ├── following_question.py   # 꼬리질문 생성 프롬프트
    ├── question_evaluate.py    # 답변 평가 프롬프트
    ├── all_evaluate.py         # 전체 평가 프롬프트
    └── portfolio_evaluate.py   # 포트폴리오 평가 프롬프트
```

## 🚀 빠른 시작

### 1. 환경 설정
```bash
# 환경변수 파일 생성
cp .env.example .env
# .env 파일에 API 키 설정
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. API 서버 실행
```bash
python run_api.py
# API 문서: http://localhost:4700/docs
# 헬스체크: http://localhost:4700/api/v1/health
```

### 4. 웹 데모 실행
```bash
python demo.py
# 데모 페이지: http://localhost:7860
```

## 🔄 메인 로직 플로우

### 1. 문서 처리 단계
```
PDF 업로드 → document-parsing API → HTML 변환 → 백엔드 서버로 전송
```

### 2. 키워드 및 질문 생성
```
HTML 텍스트 → keyword-extract API → 해시태그 키워드 추출
HTML + 질문 개수 → questions-generation API → 메인 질문 생성
```

### 3. 면접 진행 단계
```
메인 질문 → 사용자 답변 → question-evaluate API → 상세 피드백 제공
질문 + 답변 → following-question-generate API → 꼬리질문 생성
꼬리질문 → 사용자 답변 → question-evaluate API → 상세 피드백 제공
(꼬리질문 개수만큼 반복)
```

### 4. 최종 평가 단계
```
모든 질문답변 완료 → all-evaluate API → 전반적 답변 품질 분석 리포트
포트폴리오 HTML → portfolio-eval API → 포트폴리오 완성도 분석 리포트
```

## 🎯 주요 특징

- **Claude Opus 4.1**: 최신 AI 모델로 고품질 면접 경험
- **점수 없는 평가**: 상세한 장문 피드백으로 실질적 도움 제공
- **비동기 처리**: 모든 API 호출은 `async/await` 사용
- **견고성**: 다층적 오류 처리와 입력 검증
- **모듈 분리**: 각 기능을 독립적으로 테스트 가능하게 설계
- **웹 데모**: Gradio 기반 사용자 친화적 인터페이스

## 📊 성공 기준

- [x] PDF 업로드시 텍스트 정상 추출
- [x] AI가 기술 키워드 5-10개 추출
- [x] 키워드 기반 면접질문 5개 생성 (기술3개+행동2개)
- [x] 답변별 상세한 장문 피드백 제공
- [x] 전체 파이프라인 안정적 동작
- [x] `/docs`에서 모든 API 테스트 가능
- [x] Gradio 웹 데모로 전체 플로우 확인 가능

## 📝 라이선스

MIT License - 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.
