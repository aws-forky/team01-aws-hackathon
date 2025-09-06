# Forky 기술 스택

## 백엔드 (Backend)

### 핵심 프레임워크
- **FastAPI 0.104.1** - Python 웹 프레임워크
- **Python 3.13** - 프로그래밍 언어
- **Uvicorn** - ASGI 서버

### 라이브러리 & 의존성
- **httpx** - 비동기 HTTP 클라이언트 (외부 API 호출)
- **Pydantic** - 데이터 검증 및 모델링
- **python-multipart** - 파일 업로드 처리

### 아키텍처 패턴
- **MVC 패턴** - Model-View-Controller 구조
- **RESTful API** - REST 기반 API 설계

## 프론트엔드 (Frontend)

### 핵심 프레임워크
- **React 19.1.0** - UI 라이브러리
- **TypeScript** - 정적 타입 언어
- **Vite** - 빌드 도구 및 개발 서버

### UI & 스타일링
- **Tailwind CSS** - 유틸리티 기반 CSS 프레임워크
- **PostCSS** - CSS 후처리기

### 상태 관리 & 라우팅
- **React Context API** - 전역 상태 관리
- **React Router** - 클라이언트 사이드 라우팅

### HTTP 클라이언트
- **Axios** - HTTP 요청 라이브러리

### 개발 도구
- **ESLint** - 코드 품질 검사
- **TypeScript Compiler** - 타입 체크

## 외부 API & 서비스

### AI 서비스
- **Forky AI API** (`https://forky-ai.kms39273.synology.me/`)
  - Document Parser API - PDF 텍스트 추출
  - Keyword Extract API - 기술 키워드 분석
  - Question Generate API - 면접 질문 생성

### 기존 (대체됨)
- ~~Upstage Solar LLM Pro2~~ - AI 언어 모델
- ~~Upstage Document Parser~~ - 문서 파싱

## 개발 환경 & 도구

### 패키지 관리
- **npm** - Node.js 패키지 매니저
- **pip** - Python 패키지 매니저
- **venv** - Python 가상 환경

### 개발 서버
- **Vite Dev Server** - 프론트엔드 개발 서버 (포트 3000)
- **Uvicorn** - 백엔드 개발 서버 (포트 8000)

### 버전 관리
- **Git** - 소스 코드 버전 관리
- **GitHub** - 원격 저장소

## 배포 & 인프라 (예정)

### 컨테이너화
- **Docker** - 애플리케이션 컨테이너화
- **Nginx** - 리버스 프록시 및 정적 파일 서빙

### 클라우드 서비스
- **AWS** - 클라우드 플랫폼
  - EC2 - 서버 인스턴스
  - RDS - 데이터베이스 (필요시)
  - S3 - 파일 저장소

### CI/CD
- **GitHub Actions** - 자동화된 배포 파이프라인

## 보안 & 설정

### 환경 변수 관리
- **.env 파일** - 환경별 설정
- **python-dotenv** - 환경 변수 로딩

### CORS 설정
- **FastAPI CORS Middleware** - 크로스 오리진 요청 처리

### 파일 처리
- **임시 파일 시스템** - PDF 업로드 처리
- **파일 검증** - 크기 및 타입 체크

## 데이터 모델

### 백엔드 모델 (Pydantic)
```python
- Keyword: 기술 키워드 모델
- Question: 면접 질문 모델  
- Company: 회사 정보 모델
- QuestionType: 질문 유형 (technical/behavioral)
- DifficultyLevel: 난이도 (beginner/intermediate/advanced)
- KeywordCategory: 키워드 분류 (language/framework/tool/database/cloud)
```

### 프론트엔드 타입 (TypeScript)
```typescript
- UploadResponse: 파일 업로드 응답
- KeywordResponse: 키워드 추출 응답
- QuestionResponse: 질문 생성 응답
- CompanyListResponse: 회사 목록 응답
```

## 프로젝트 구조

```
forky/
├── backend/           # FastAPI 백엔드
│   ├── app/          # MVC 구조
│   │   ├── controllers/  # API 라우터
│   │   ├── models/      # 데이터 모델
│   │   ├── services/    # 비즈니스 로직
│   │   └── config/      # 설정
│   └── docs/         # 백엔드 문서
├── frontend/         # React 프론트엔드
│   ├── src/
│   │   ├── components/  # UI 컴포넌트
│   │   ├── pages/      # 페이지 컴포넌트
│   │   ├── services/   # API 서비스
│   │   └── context/    # 상태 관리
│   └── docs/         # 프론트엔드 문서
└── docs/             # 프로젝트 문서
```

## 주요 특징

- **타입 안전성**: TypeScript + Pydantic으로 전체 스택 타입 안전성 확보
- **비동기 처리**: FastAPI + httpx로 고성능 비동기 API
- **모던 개발 환경**: Vite + React 19로 최신 개발 경험
- **확장 가능한 구조**: MVC 패턴으로 유지보수성 향상
- **외부 API 통합**: Forky AI API와 완전 통합