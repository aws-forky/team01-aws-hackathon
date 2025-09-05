# tests/test_llm_processor.py - LLM 프로세서 테스트

## 역할
LLMProcessor 클래스의 AI 기반 키워드 추출과 질문 생성 기능을 검증하고 다양한 시나리오에서의 안정성을 보장하는 테스트 코드입니다.

## 주요 기능

### 1. AI 기능 테스트
- 키워드 추출 정확성 검증
- 질문 생성 품질 평가
- AI 응답 파싱 안정성 확인

### 2. 폴백 시스템 테스트
- AI 서비스 실패 시 폴백 동작
- 기본 키워드/질문 제공 확인
- 서비스 연속성 보장

### 3. 성능 및 안정성 테스트
- API 호출 최적화 검증
- 동시 요청 처리 능력
- 메모리 및 리소스 관리

## 테스트 케이스 구성

### 1. 키워드 추출 테스트
#### test_extract_keywords_success()
- 정상적인 키워드 추출 검증
- 5-10개 키워드 개수 확인
- 기술 관련 키워드 품질 평가

#### test_extract_keywords_with_various_texts()
- 다양한 포트폴리오 텍스트 처리
- 프로그래밍 언어별 키워드 추출
- 프로젝트 유형별 키워드 분석

#### test_extract_keywords_empty_text()
- 빈 텍스트 입력 처리
- 적절한 오류 처리 확인
- 폴백 키워드 제공 검증

#### test_extract_keywords_long_text()
- 긴 텍스트 처리 능력
- 텍스트 길이 제한 동작
- 핵심 키워드 추출 정확성

### 2. 질문 생성 테스트
#### test_generate_questions_success()
- 정상적인 질문 생성 검증
- 기술 3개 + 행동 2개 구성 확인
- 질문 품질 및 관련성 평가

#### test_generate_questions_with_company()
- 회사명 포함 질문 생성
- 개인화된 질문 내용 확인
- 회사 특성 반영 검증

#### test_generate_questions_various_keywords()
- 다양한 키워드 조합 처리
- 키워드별 맞춤 질문 생성
- 질문 다양성 확인

#### test_generate_questions_fallback()
- AI 실패 시 폴백 질문 제공
- 기본 질문 품질 확인
- 서비스 연속성 보장

### 3. JSON 파싱 테스트
#### test_extract_json_valid_response()
- 정상 JSON 응답 파싱
- 코드 블록 제거 기능
- 구조화된 데이터 추출

#### test_extract_json_malformed_response()
- 잘못된 JSON 형식 처리
- 파싱 오류 안전 처리
- None 반환 확인

#### test_extract_json_with_code_blocks()
- ```json 코드 블록 처리
- 마크다운 형식 응답 파싱
- 정확한 JSON 추출

### 4. API 호출 테스트
#### test_call_llm_success()
- Solar LLM API 정상 호출
- 인증 헤더 설정 확인
- 응답 데이터 처리

#### test_call_llm_authentication_failure()
- 인증 실패 처리
- 401 오류 응답 처리
- 적절한 오류 로깅

#### test_call_llm_timeout()
- API 타임아웃 처리
- 네트워크 지연 시뮬레이션
- 안전한 오류 복구

#### test_rate_limiting()
- API 호출 간격 제어
- 요청 빈도 제한 준수
- 동시 요청 관리

### 5. 프롬프트 관리 테스트
#### test_load_keyword_prompts()
- 키워드 추출 프롬프트 로드
- JSON 파일 파싱 확인
- 기본값 폴백 처리

#### test_load_question_prompts()
- 질문 생성 프롬프트 로드
- 템플릿 변수 처리
- 프롬프트 품질 검증

#### test_prompt_template_formatting()
- 프롬프트 템플릿 포맷팅
- 변수 치환 정확성
- 특수 문자 처리

### 6. 오류 처리 테스트
#### test_api_key_missing()
- API 키 누락 시 처리
- 환경 설정 오류 처리
- 폴백 시스템 동작

#### test_network_error_handling()
- 네트워크 오류 처리
- 연결 실패 시 복구
- 재시도 메커니즘

#### test_invalid_response_handling()
- 잘못된 API 응답 처리
- 예상치 못한 데이터 형식
- 안전한 오류 복구

## 테스트 데이터 관리

### 1. 샘플 포트폴리오 텍스트
- 다양한 기술 스택 포함
- 프로젝트 설명 및 경험
- 실제 포트폴리오 패턴 반영

### 2. 모킹 응답 데이터
- Solar LLM API 응답 시뮬레이션
- 다양한 성공/실패 케이스
- 실제 응답 패턴 반영

### 3. 기대 결과 데이터
- 키워드별 예상 추출 결과
- 질문 유형별 기대 구조
- 품질 평가 기준

## AI 품질 평가 메트릭

### 1. 키워드 추출 품질
- 기술 관련성 점수
- 키워드 다양성 측정
- 중복 키워드 비율

### 2. 질문 생성 품질
- 질문 유형 분포 확인
- 개인화 수준 평가
- 실용성 점수

### 3. 응답 일관성
- 동일 입력 대비 일관성
- 품질 변동성 측정
- 안정성 지표

## 성능 테스트

### 1. 응답 시간 측정
- 키워드 추출 시간
- 질문 생성 시간
- 전체 파이프라인 시간

### 2. 리소스 사용량
- 메모리 사용 패턴
- CPU 사용률 모니터링
- 네트워크 대역폭

### 3. 동시성 테스트
- 다중 요청 처리
- 리소스 경합 상황
- 스레드 안전성

## 테스트 실행 방법

### 1. 기본 실행
```bash
# 전체 LLM 테스트 실행
pytest tests/test_llm_processor.py

# 키워드 추출 테스트만
pytest tests/test_llm_processor.py -k "keyword"

# 질문 생성 테스트만
pytest tests/test_llm_processor.py -k "question"
```

### 2. 품질 평가 포함
```bash
# AI 품질 메트릭 포함 실행
pytest tests/test_llm_processor.py --quality-metrics

# 성능 테스트 포함
pytest tests/test_llm_processor.py --performance
```

## 테스트 환경 설정

### 1. API 키 관리
- 테스트 전용 API 키 사용
- 실제 API 호출 최소화
- 모킹 우선 사용

### 2. 비동기 테스트 설정
- pytest-asyncio 플러그인
- 이벤트 루프 관리
- 타임아웃 설정

### 3. 외부 의존성 격리
- httpx 모킹
- API 응답 시뮬레이션
- 네트워크 격리

## 지속적 품질 관리

### 1. 품질 기준 모니터링
- AI 응답 품질 추적
- 성능 지표 모니터링
- 사용자 피드백 반영

### 2. 테스트 데이터 업데이트
- 새로운 기술 트렌드 반영
- 실제 사용 패턴 분석
- 테스트 케이스 확장

### 3. 프롬프트 최적화
- 프롬프트 성능 평가
- A/B 테스트 수행
- 지속적 개선
