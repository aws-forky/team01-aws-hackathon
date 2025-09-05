# AI Document Processing API

채용 담당자를 위한 AI 기반 문서 처리 및 면접 질문 생성 시스템

## 🎯 프로젝트 개요

지원자의 포트폴리오 PDF를 업로드하면 AI가 자동으로 기술 키워드를 추출하고 맞춤형 면접 질문을 생성하는 완전 자동화 파이프라인을 제공합니다.

## 🚀 핵심 기능

### 3단계 자동화 파이프라인
1. **문서 파싱**: Upstage Document Parser로 PDF/DOCX/이미지에서 텍스트 추출
2. **키워드 추출**: Solar LLM으로 기술 스택 키워드 5-10개 자동 분석
3. **질문 생성**: 키워드 기반 기술면접 3개 + 행동면접 2개 자동 생성

### API 엔드포인트
- `POST /api/v1/documents/parse` - 문서 → 텍스트 변환
- `POST /api/v1/keywords/extract` - 텍스트 → 키워드 추출
- `POST /api/v1/questions/generate` - 키워드 → 면접질문 생성
- `POST /api/v1/questions/process-complete` - **원스톱 전체 파이프라인**
- `GET /api/v1/health` - 시스템 상태 확인

## 🛠 기술 스택

- **Backend**: FastAPI + Uvicorn
- **AI Services**: Upstage Document Parser + Solar LLM
- **Data Validation**: Pydantic
- **HTTP Client**: httpx
- **Web Demo**: Gradio
- **Environment**: python-dotenv

## 📁 프로젝트 구조

```
ai/
├── README.md                 # 프로젝트 개요 및 사용법
├── LICENSE                   # 라이선스 정보
├── requirements.txt          # Python 의존성 목록
├── .env.example             # 환경변수 템플릿
├── main.md                  # FastAPI 애플리케이션 진입점 설명
├── config.md                # 환경설정 중앙 관리 설명
├── run_api.md              # API 서버 실행 스크립트 설명
├── models/
│   ├── requests.md         # Pydantic 요청 모델 설명
│   └── responses.md        # Pydantic 응답 모델 설명
├── routers/                # 기능별 API 라우터
│   ├── documents.md        # 문서 파싱 엔드포인트 설명
│   ├── keywords.md         # 키워드 추출 엔드포인트 설명
│   ├── questions.md        # 질문 생성 + 완전처리 엔드포인트 설명
│   └── health.md          # 헬스체크 엔드포인트 설명
├── services/               # 핵심 비즈니스 로직
│   ├── document_parser.md  # Upstage 문서파싱 연동 설명
│   └── llm_processor.md    # Solar LLM 처리 설명
├── prompts/                # AI 프롬프트 템플릿
│   ├── keyword_extraction.md   # 키워드 추출 프롬프트 설명
│   └── question_generation.md  # 질문 생성 프롬프트 설명
├── docs/                   # 추가 문서
│   ├── api_guide.md       # API 사용 가이드
│   ├── deployment.md      # 배포 가이드
│   └── troubleshooting.md # 문제 해결 가이드
├── tests/                  # 테스트 코드
│   ├── test_document_parser.md  # 문서 파서 테스트 설명
│   ├── test_llm_processor.md    # LLM 프로세서 테스트 설명
│   └── test_api_endpoints.md    # API 엔드포인트 테스트 설명
└── demo.md                 # Gradio 웹 데모 설명
```

## 🚀 빠른 시작

### 1. 환경 설정
```bash
# 환경변수 파일 생성
cp .env.example .env
# .env 파일에 Upstage API 키 설정
```

### 2. 의존성 설치
```bash
pip install fastapi uvicorn httpx python-dotenv pydantic gradio aiofiles
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
# 웹 인터페이스: http://localhost:7860
```

## 📊 성공 기준

- [x] PDF 업로드시 텍스트 정상 추출
- [x] AI가 기술 키워드 5-10개 JSON 반환
- [x] 키워드 기반 면접질문 5개 생성 (기술3개+행동2개)
- [x] API 실패시 폴백 시스템 동작
- [x] 전체 파이프라인 30초 내 완료
- [x] `/docs`에서 모든 API 테스트 가능

## 🔧 주요 특징

- **비동기 처리**: 모든 API 호출은 `async/await` 사용
- **JSON 파싱**: AI 응답에서 코드블록 제거 후 안전한 파싱
- **폴백 설계**: AI 실패시에도 사용자에게 유의미한 결과 제공
- **모듈 분리**: 각 기능을 독립적으로 테스트 가능하게 설계
- **견고성**: 다층적 오류 처리와 입력 검증

## 📝 라이선스

MIT License - 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 지원

문제가 발생하거나 질문이 있으시면 [Issues](https://github.com/your-repo/issues)를 통해 문의해주세요.
