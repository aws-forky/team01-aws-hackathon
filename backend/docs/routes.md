# API Routes

## 역할
클라이언트 요청을 받아 적절한 서비스로 라우팅하고 응답을 반환합니다.

## 주요 엔드포인트

### 1. 파일 업로드 및 분석
- `POST /api/upload` - PDF 파일 업로드 및 Document Parser 분석
- 파일 검증, 임시 저장, 텍스트 추출 처리

### 2. 키워드 추출
- `POST /api/extract-keywords` - 분석된 텍스트에서 기술 키워드 추출
- Upstage Solar LLM을 활용한 지능형 키워드 분석

### 3. 질문 생성
- `POST /api/generate-questions` - 키워드와 회사 정보 기반 질문 생성
- 기술 질문과 행동 질문을 포함한 맞춤형 질문 세트 생성

### 4. 유틸리티
- `GET /health` - 서버 상태 확인
- `GET /api/companies` - 지원 가능한 회사 목록 조회

## 특징
- 비동기 처리로 높은 성능
- 상세한 에러 응답 및 상태 코드
- 요청/응답 검증 (Pydantic 모델)
- 파일 업로드 제한 및 보안 검증
