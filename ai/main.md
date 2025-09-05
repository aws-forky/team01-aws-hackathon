# main.py - FastAPI 애플리케이션 진입점

## 역할
FastAPI 애플리케이션의 메인 진입점으로, 전체 API 서버를 초기화하고 설정하는 핵심 파일입니다.

## 주요 기능

### 1. FastAPI 앱 초기화
- 애플리케이션 메타데이터 설정 (제목, 설명, 버전)
- API 문서 자동 생성 설정

### 2. 미들웨어 설정
- CORS 미들웨어 추가로 크로스 오리진 요청 허용
- 모든 오리진, 메서드, 헤더 허용 설정

### 3. 라우터 등록
- `/api/v1` 접두사로 모든 API 엔드포인트 등록
- 기능별 라우터 모듈 통합:
  - `health.router` - 헬스체크
  - `documents.router` - 문서 파싱
  - `keywords.router` - 키워드 추출
  - `questions.router` - 질문 생성 및 완전처리

### 4. 서버 실행 설정
- 개발 환경에서 직접 실행 시 uvicorn 서버 시작
- 호스트: 0.0.0.0, 포트: 8000

## 의존성
- FastAPI: 웹 프레임워크
- CORSMiddleware: 크로스 오리진 요청 처리
- 각 기능별 라우터 모듈들

## 실행 방법
```bash
python main.py
```

## API 문서 접근
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
