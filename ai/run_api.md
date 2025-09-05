# run_api.py - API 서버 실행 스크립트

## 역할
개발 환경에서 FastAPI 서버를 편리하게 실행하기 위한 전용 스크립트입니다. 프로덕션 배포와 분리된 개발 서버 설정을 제공합니다.

## 주요 기능

### 1. 개발 서버 설정
- 호스트: 0.0.0.0 (모든 인터페이스에서 접근 가능)
- 포트: 4700 (main.py의 8000과 구분)
- 리로드 모드: 활성화 (코드 변경 시 자동 재시작)
- 로그 레벨: info

### 2. 사용자 친화적 출력
- 서버 시작 시 유용한 정보 출력:
  - API 문서 URL: http://localhost:4700/docs
  - 헬스체크 URL: http://localhost:4700/api/v1/health
  - 종료 방법 안내 (Ctrl+C)

### 3. Uvicorn 서버 실행
- `uvicorn.run()` 함수로 서버 시작
- 모듈 경로 방식으로 main.py의 app 객체 참조
- 개발 환경에 최적화된 설정

## 실행 방법
```bash
python run_api.py
```

## 출력 예시
```
Starting AI Document Processing API...
API Documentation: http://localhost:4700/docs
Health Check: http://localhost:4700/api/v1/health
Press Ctrl+C to stop
```

## main.py와의 차이점
- `main.py`: 프로덕션 배포용 (포트 8000, 기본 설정)
- `run_api.py`: 개발 환경용 (포트 4700, 리로드 모드, 상세 로그)

## 개발 워크플로우
1. 코드 수정
2. `python run_api.py` 실행
3. 자동 리로드로 변경사항 즉시 반영
4. http://localhost:4700/docs에서 API 테스트
