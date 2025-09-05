# tests/test_document_parser.py - 문서 파서 테스트

## 역할
DocumentParser 클래스의 모든 기능을 검증하고 다양한 시나리오에서의 동작을 보장하는 테스트 코드입니다.

## 주요 기능

### 1. 단위 테스트 (Unit Tests)
- DocumentParser 클래스의 개별 메서드 테스트
- 정상 케이스와 예외 케이스 모두 검증
- 모킹을 통한 외부 의존성 격리

### 2. 통합 테스트 (Integration Tests)
- Upstage API와의 실제 연동 테스트
- 다양한 파일 형식별 파싱 결과 검증
- 네트워크 오류 상황 시뮬레이션

### 3. 성능 테스트 (Performance Tests)
- 대용량 파일 처리 성능 측정
- 동시 요청 처리 능력 검증
- 메모리 사용량 모니터링

## 테스트 케이스 구성

### 1. 정상 동작 테스트
#### test_parse_pdf_document()
- PDF 파일 파싱 성공 케이스
- 올바른 텍스트 추출 검증
- 응답 시간 측정

#### test_parse_docx_document()
- DOCX 파일 파싱 성공 케이스
- 문서 구조 보존 확인
- 특수 문자 처리 검증

#### test_parse_image_document()
- 이미지 파일 OCR 처리
- 텍스트 인식 정확도 확인
- 다양한 이미지 형식 지원

### 2. 오류 처리 테스트
#### test_invalid_file_format()
- 지원하지 않는 파일 형식 처리
- 적절한 오류 메시지 반환 확인
- 폴백 처리 동작 검증

#### test_corrupted_file()
- 손상된 파일 처리
- 예외 상황 처리 확인
- 안전한 오류 복구

#### test_api_connection_failure()
- Upstage API 연결 실패 시뮬레이션
- 폴백 메커니즘 동작 확인
- 타임아웃 처리 검증

### 3. 폴백 시스템 테스트
#### test_fallback_text_extraction()
- API 실패 시 폴백 처리
- 텍스트 파일 직접 처리
- JSON 파일 구조화 처리

#### test_fallback_quality_validation()
- 추출된 텍스트 품질 검증
- 최소 길이 요구사항 확인
- 빈 결과 처리

### 4. 보안 테스트
#### test_file_size_validation()
- 파일 크기 제한 검증 (50MB)
- 대용량 파일 거부 확인
- 메모리 보호 기능

#### test_malicious_file_handling()
- 악성 파일 처리 안전성
- 스크립트 인젝션 방지
- 안전한 파일 처리

### 5. 성능 테스트
#### test_large_file_processing()
- 대용량 파일 처리 성능
- 메모리 사용량 모니터링
- 처리 시간 측정

#### test_concurrent_requests()
- 동시 다중 요청 처리
- 리소스 경합 상황 테스트
- 스레드 안전성 검증

## 테스트 데이터 관리

### 1. 테스트 파일 준비
- 다양한 형식의 샘플 파일
- 정상 파일과 손상된 파일
- 다양한 크기의 테스트 파일

### 2. 모킹 데이터
- Upstage API 응답 시뮬레이션
- 다양한 오류 상황 모킹
- 네트워크 지연 시뮬레이션

### 3. 기대 결과 데이터
- 파일별 예상 추출 텍스트
- 오류 케이스별 예상 응답
- 성능 기준값 설정

## 테스트 환경 설정

### 1. 의존성 관리
- pytest 프레임워크 사용
- httpx 모킹을 위한 respx
- 비동기 테스트 지원

### 2. 환경 변수 설정
- 테스트 전용 API 키
- 테스트 환경 구성
- 격리된 테스트 실행

### 3. CI/CD 통합
- GitHub Actions 워크플로우
- 자동화된 테스트 실행
- 테스트 결과 리포팅

## 테스트 실행 방법

### 1. 로컬 실행
```bash
# 전체 테스트 실행
pytest tests/test_document_parser.py

# 특정 테스트 실행
pytest tests/test_document_parser.py::test_parse_pdf_document

# 커버리지 포함 실행
pytest --cov=services.document_parser tests/test_document_parser.py
```

### 2. 테스트 카테고리별 실행
```bash
# 단위 테스트만 실행
pytest -m unit tests/test_document_parser.py

# 통합 테스트만 실행
pytest -m integration tests/test_document_parser.py

# 성능 테스트만 실행
pytest -m performance tests/test_document_parser.py
```

## 테스트 결과 분석

### 1. 커버리지 분석
- 코드 커버리지 측정
- 미테스트 영역 식별
- 테스트 품질 개선

### 2. 성능 메트릭
- 응답 시간 분석
- 메모리 사용량 추적
- 처리량 측정

### 3. 오류 패턴 분석
- 실패 케이스 분석
- 오류 빈도 추적
- 개선 포인트 식별

## 유지보수 가이드

### 1. 테스트 업데이트
- 새 기능 추가 시 테스트 확장
- API 변경 시 테스트 수정
- 정기적인 테스트 리뷰

### 2. 테스트 데이터 관리
- 샘플 파일 정기 업데이트
- 테스트 시나리오 확장
- 실제 사용 패턴 반영

### 3. 성능 기준 조정
- 성능 기준값 정기 검토
- 하드웨어 변경 시 기준 조정
- 사용자 요구사항 반영
