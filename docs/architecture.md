# System Architecture

## 역할
Forky 시스템의 전체 아키텍처와 구성 요소 간의 관계를 설명합니다.

## 전체 아키텍처

### 1. 클라이언트-서버 구조
```
Frontend (React) ↔ Backend (FastAPI) ↔ Upstage AI APIs
```

### 2. 마이크로서비스 지향 설계
- Frontend: 사용자 인터페이스 및 상태 관리
- Backend: API 서버 및 비즈니스 로직
- AI Services: 문서 파싱 및 질문 생성

### 3. 데이터 플로우
1. 사용자가 PDF 파일 업로드
2. Document Parser로 텍스트 추출
3. Solar LLM으로 키워드 분석
4. 회사 정보와 결합하여 질문 생성
5. 결과를 사용자에게 반환

## 기술 스택

### Frontend
- React 19.1.0 + TypeScript
- Tailwind CSS (스타일링)
- React Router v6 (라우팅)
- Axios (HTTP 클라이언트)
- PWA (오프라인 지원)

### Backend
- FastAPI 0.104.1 (웹 프레임워크)
- Pydantic (데이터 검증)
- httpx (비동기 HTTP 클라이언트)
- Docker (컨테이너화)

### AI Services
- Upstage Document Parser (PDF 분석)
- Upstage Solar LLM Pro2 (질문 생성)

### Infrastructure
- Nginx (리버스 프록시)
- Docker Compose (오케스트레이션)
- SSL/TLS (보안)

## 보안 고려사항
- API 키 암호화 저장
- 파일 업로드 검증
- CORS 설정
- Rate Limiting
- HTTPS 강제
