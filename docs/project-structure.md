# Forky 프로젝트 구조

## 개요
MVC 패턴을 적용한 AI 기반 포트폴리오 기술면접 시뮬레이터 프로젝트 구조입니다.

## 백엔드 구조 (FastAPI)

```
backend/
├── app/                    # 메인 애플리케이션 패키지
│   ├── config/            # 설정 관련
│   │   ├── __init__.py
│   │   └── config.py      # 환경 설정, API 키 등
│   ├── controllers/       # 컨트롤러 (라우터)
│   │   ├── __init__.py
│   │   └── routes.py      # API 엔드포인트 정의
│   ├── models/           # 데이터 모델
│   │   ├── __init__.py
│   │   └── models.py     # Pydantic 모델 정의
│   ├── services/         # 비즈니스 로직
│   │   ├── __init__.py
│   │   └── services.py   # AI API 호출, 파일 처리 등
│   ├── utils/            # 유틸리티 함수
│   │   └── __init__.py
│   └── views/            # 뷰 템플릿 (현재 미사용)
├── docs/                 # 백엔드 문서
│   ├── config.md
│   ├── main.md
│   ├── models.md
│   ├── routes.md
│   └── services.md
├── temp_uploads/         # 임시 파일 저장소
├── main.py              # FastAPI 애플리케이션 진입점
└── requirements.txt     # Python 의존성
```

## 프론트엔드 구조 (React + TypeScript)

```
frontend/
├── docs/                # 프론트엔드 문서
│   ├── components.md
│   ├── main.md
│   ├── pages.md
│   └── services.md
├── src/
│   ├── components/      # 재사용 가능한 컴포넌트
│   │   ├── FileUpload.tsx
│   │   ├── Layout.tsx
│   │   ├── LoadingSpinner.tsx
│   │   └── QuestionCard.tsx
│   ├── context/         # React Context (상태 관리)
│   │   └── AppContext.tsx
│   ├── pages/          # 페이지 컴포넌트
│   │   ├── CompanyPage.tsx
│   │   ├── InterviewPage.tsx
│   │   ├── ResultPage.tsx
│   │   ├── SetupPage.tsx
│   │   └── UploadPage.tsx
│   ├── services/       # API 호출 서비스
│   │   ├── api.ts
│   │   └── pdf.ts
│   ├── App.tsx         # 메인 앱 컴포넌트
│   ├── main.tsx        # React 진입점
│   └── types.ts        # TypeScript 타입 정의
└── package.json        # Node.js 의존성
```

## 공통 폴더

```
├── docs/               # 프로젝트 전체 문서
│   ├── api.md
│   ├── architecture.md
│   └── project-structure.md
├── deployment/         # 배포 관련 문서
│   ├── aws.md
│   └── docker.md
├── tests/             # 테스트 관련 문서
│   ├── backend-tests.md
│   └── frontend-tests.md
└── ai/                # AI 모델 관련 (현재 미사용)
```

## MVC 패턴 적용

### Model (모델)
- `backend/app/models/models.py`: 데이터 구조 정의
- `frontend/src/types.ts`: TypeScript 타입 정의

### View (뷰)
- `frontend/src/pages/`: 사용자 인터페이스
- `frontend/src/components/`: UI 컴포넌트

### Controller (컨트롤러)
- `backend/app/controllers/routes.py`: API 엔드포인트
- `frontend/src/services/api.ts`: API 호출 로직

### Service (서비스)
- `backend/app/services/services.py`: 비즈니스 로직
- `frontend/src/context/AppContext.tsx`: 상태 관리

## 주요 특징

1. **관심사 분리**: 각 레이어가 명확한 책임을 가짐
2. **모듈화**: 기능별로 파일과 폴더가 분리됨
3. **문서화**: 각 모듈별 문서가 별도 폴더에 정리됨
4. **확장성**: 새로운 기능 추가 시 구조를 유지하며 확장 가능