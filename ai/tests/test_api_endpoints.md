# tests/test_api_endpoints.py - API 엔드포인트 테스트

## 역할
FastAPI 애플리케이션의 모든 API 엔드포인트를 검증하고 HTTP 요청/응답 처리의 정확성을 보장하는 통합 테스트 코드입니다.

## 주요 기능

### 1. 엔드포인트 기능 테스트
- 모든 API 엔드포인트 동작 검증
- HTTP 메서드별 요청 처리 확인
- 응답 형식 및 상태 코드 검증

### 2. 데이터 검증 테스트
- 요청 데이터 유효성 검사
- Pydantic 모델 검증 동작
- 오류 응답 형식 확인

### 3. 통합 워크플로우 테스트
- 전체 파이프라인 동작 검증
- 단계별 데이터 흐름 확인
- 엔드포인트 간 연동 테스트

## 테스트 케이스 구성

### 1. 헬스체크 엔드포인트 테스트
#### test_health_check()
- GET /api/v1/health 엔드포인트 테스트
- 200 상태 코드 반환 확인
- 응답 메시지 검증

#### test_health_check_response_format()
- BaseResponse 모델 형식 확인
- success 필드 true 값 검증
- 적절한 메시지 내용 확인

### 2. 문서 파싱 엔드포인트 테스트
#### test_parse_document_success()
- POST /api/v1/documents/parse 성공 케이스
- 다양한 파일 형식 업로드 테스트
- 추출된 텍스트 내용 검증

#### test_parse_document_no_file()
- 파일 없이 요청 시 400 오류
- 적절한 오류 메시지 반환
- 오류 응답 형식 확인

#### test_parse_document_large_file()
- 50MB 초과 파일 업로드 시 413 오류
- 파일 크기 제한 동작 확인
- 오류 처리 메시지 검증

#### test_parse_document_invalid_format()
- 지원하지 않는 파일 형식 처리
- 적절한 오류 응답 반환
- 폴백 처리 동작 확인

### 3. 키워드 추출 엔드포인트 테스트
#### test_extract_keywords_success()
- POST /api/v1/keywords/extract 성공 케이스
- 유효한 텍스트 입력 처리
- 키워드 목록 응답 검증

#### test_extract_keywords_empty_text()
- 빈 텍스트 입력 시 400 오류
- 입력 검증 동작 확인
- 오류 메시지 적절성 검증

#### test_extract_keywords_response_format()
- KeywordExtractResponse 모델 검증
- 키워드 목록 형식 확인
- 폴백 정보 포함 여부

### 4. 질문 생성 엔드포인트 테스트
#### test_generate_questions_success()
- POST /api/v1/questions/generate 성공 케이스
- 텍스트와 키워드 입력 처리
- 5개 질문 생성 확인

#### test_generate_questions_with_company()
- 회사명 포함 질문 생성
- 개인화된 질문 내용 확인
- 회사 정보 반영 검증

#### test_generate_questions_missing_keywords()
- 키워드 누락 시 400 오류
- 필수 필드 검증 동작
- 적절한 오류 응답

#### test_generate_questions_response_structure()
- QuestionGenerateResponse 모델 검증
- 질문 구조 및 필드 확인
- 질문 유형 분포 검증

### 5. 완전 처리 파이프라인 테스트
#### test_process_complete_success()
- POST /api/v1/questions/process-complete 성공
- 파일 업로드부터 질문 생성까지 전체 플로우
- 모든 단계 결과 포함 확인

#### test_process_complete_with_company()
- 회사명 포함 완전 처리
- Form 데이터 처리 확인
- 개인화된 결과 검증

#### test_process_complete_large_file()
- 대용량 파일 처리 시 413 오류
- 파일 크기 제한 적용
- 적절한 오류 처리

#### test_process_complete_response_format()
- ProcessCompleteResponse 모델 검증
- 모든 단계 결과 포함 확인
- 폴백 정보 추적 검증

### 6. 오류 처리 테스트
#### test_404_not_found()
- 존재하지 않는 엔드포인트 요청
- 404 상태 코드 반환 확인
- FastAPI 기본 오류 응답

#### test_405_method_not_allowed()
- 잘못된 HTTP 메서드 사용
- 405 상태 코드 반환 확인
- 허용된 메서드 정보 포함

#### test_422_validation_error()
- 잘못된 요청 데이터 형식
- Pydantic 검증 오류 처리
- 상세한 검증 오류 메시지

#### test_500_internal_server_error()
- 서버 내부 오류 시뮬레이션
- 500 상태 코드 반환 확인
- 안전한 오류 응답

### 7. 인증 및 보안 테스트
#### test_cors_headers()
- CORS 헤더 설정 확인
- 크로스 오리진 요청 허용
- 적절한 헤더 값 검증

#### test_content_type_validation()
- Content-Type 헤더 검증
- multipart/form-data 처리
- application/json 처리

#### test_file_upload_security()
- 파일 업로드 보안 검증
- 악성 파일 차단 확인
- 안전한 파일 처리

## 테스트 환경 설정

### 1. FastAPI 테스트 클라이언트
- TestClient를 사용한 API 테스트
- 실제 HTTP 요청 시뮬레이션
- 비동기 엔드포인트 테스트 지원

### 2. 테스트 데이터 준비
- 다양한 형식의 테스트 파일
- 샘플 텍스트 및 키워드 데이터
- 오류 시나리오용 데이터

### 3. 모킹 설정
- 외부 서비스 의존성 모킹
- DocumentParser, LLMProcessor 모킹
- 일관된 테스트 결과 보장

## 성능 테스트

### 1. 응답 시간 측정
- 각 엔드포인트별 응답 시간
- 파일 크기별 처리 시간
- 동시 요청 처리 성능

### 2. 부하 테스트
- 다중 클라이언트 시뮬레이션
- 동시 요청 처리 능력
- 리소스 사용량 모니터링

### 3. 스트레스 테스트
- 극한 상황 처리 능력
- 메모리 부족 상황 대응
- 서비스 안정성 검증

## 테스트 실행 방법

### 1. 기본 실행
```bash
# 전체 API 테스트 실행
pytest tests/test_api_endpoints.py

# 특정 엔드포인트 테스트
pytest tests/test_api_endpoints.py -k "health"

# 상세 출력 포함
pytest tests/test_api_endpoints.py -v
```

### 2. 커버리지 포함 실행
```bash
# 커버리지 측정 포함
pytest --cov=routers tests/test_api_endpoints.py

# HTML 리포트 생성
pytest --cov=routers --cov-report=html tests/test_api_endpoints.py
```

### 3. 성능 테스트 실행
```bash
# 성능 테스트 포함
pytest tests/test_api_endpoints.py --performance

# 부하 테스트 실행
pytest tests/test_api_endpoints.py --load-test
```

## 테스트 데이터 관리

### 1. 픽스처 활용
- 공통 테스트 데이터 관리
- 테스트 클라이언트 설정
- 데이터베이스 상태 관리

### 2. 파라미터화 테스트
- 다양한 입력값 조합 테스트
- 파일 형식별 테스트 자동화
- 오류 케이스 체계적 검증

### 3. 테스트 격리
- 테스트 간 독립성 보장
- 상태 초기화 및 정리
- 부작용 방지

## 지속적 통합

### 1. CI/CD 파이프라인 통합
- GitHub Actions 워크플로우
- 자동화된 테스트 실행
- 테스트 결과 리포팅

### 2. 품질 게이트
- 테스트 통과 필수 조건
- 커버리지 임계값 설정
- 성능 기준 검증

### 3. 모니터링 및 알림
- 테스트 실패 시 알림
- 성능 저하 감지
- 품질 메트릭 추적

## 문서화 및 리포팅

### 1. 테스트 결과 문서화
- 테스트 실행 결과 요약
- 커버리지 리포트
- 성능 벤치마크 결과

### 2. API 문서 검증
- OpenAPI 스키마 일치성
- 예제 응답 정확성
- 문서 업데이트 필요성

### 3. 품질 메트릭
- 테스트 통과율
- 코드 커버리지
- 성능 지표 추이
