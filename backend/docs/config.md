# Configuration

## 역할
애플리케이션 설정 및 환경 변수를 관리합니다.

## 주요 설정

### 1. API 설정
- Upstage API 키 및 엔드포인트
- Document Parser 설정
- Solar LLM 모델 설정
- API 요청 타임아웃 및 재시도 정책

### 2. 서버 설정
- FastAPI 서버 포트 및 호스트
- CORS 허용 도메인
- 파일 업로드 제한 (크기, 형식)
- 로깅 레벨 및 형식

### 3. 보안 설정
- API 키 암호화
- 파일 업로드 보안 검증
- 요청 제한 (Rate Limiting)
- HTTPS 설정

### 4. 환경별 설정
- 개발 환경 (development)
- 스테이징 환경 (staging)
- 프로덕션 환경 (production)
- 테스트 환경 (test)

## 환경 변수
- `UPSTAGE_API_KEY` - Upstage API 인증 키
- `ENVIRONMENT` - 실행 환경
- `LOG_LEVEL` - 로깅 레벨
- `MAX_FILE_SIZE` - 최대 파일 크기
- `CORS_ORIGINS` - CORS 허용 도메인
