# services/llm_processor.py - Solar LLM 처리

## 역할
Solar LLM API와 연동하여 키워드 추출과 면접 질문 생성을 담당하는 핵심 AI 처리 서비스입니다.

## 주요 기능

### 1. Solar LLM API 연동
- ChatGPT 호환 형식의 API 호출
- Bearer 토큰 기반 인증
- 비동기 HTTP 통신으로 성능 최적화
- 요청 간격 제어로 API 제한 준수

### 2. 키워드 추출 서비스
- 포트폴리오 텍스트에서 5-10개 기술 키워드 자동 추출
- 프롬프트 엔지니어링으로 정확도 향상
- JSON 형식 응답 파싱 및 검증
- 폴백 키워드 제공으로 서비스 안정성 확보

### 3. 면접 질문 생성 서비스
- 키워드 기반 맞춤형 질문 생성
- 기술면접 3개 + 행동면접 2개 균형 구성
- 회사명을 고려한 개인화된 질문
- 각 질문에 대한 평가 가이드 포함

### 4. 견고한 오류 처리
- API 호출 실패 시 폴백 시스템
- JSON 파싱 오류 처리
- 텍스트 길이 제한 및 전처리
- 상세한 로깅으로 디버깅 지원

## 클래스 구조

### LLMProcessor
메인 LLM 처리 클래스

#### 주요 메서드
- `extract_keywords(text)`: 키워드 추출
- `generate_questions(text, keywords, company_name)`: 질문 생성
- `_call_llm(system_prompt, user_prompt, max_tokens)`: LLM API 호출
- `_extract_json(text)`: 응답에서 JSON 추출
- `_wait_rate_limit()`: API 호출 간격 제어

## 키워드 추출 과정
1. **텍스트 전처리**: 길이 제한 및 정제
2. **프롬프트 구성**: 키워드 추출 전용 프롬프트 로드
3. **LLM 호출**: Solar API로 키워드 추출 요청
4. **응답 파싱**: JSON 형식에서 키워드 목록 추출
5. **결과 검증**: 키워드 개수 제한 (최대 10개)
6. **폴백 처리**: 실패 시 기본 키워드 제공

## 질문 생성 과정
1. **입력 검증**: 텍스트, 키워드, 회사명 확인
2. **프롬프트 구성**: 질문 생성 전용 프롬프트 로드
3. **컨텍스트 구성**: 포트폴리오, 키워드, 회사 정보 통합
4. **LLM 호출**: 면접 질문 생성 요청
5. **응답 파싱**: JSON에서 질문 목록 추출
6. **구조 검증**: 질문 형식 및 필수 필드 확인
7. **폴백 처리**: 실패 시 기본 질문 제공

## API 호출 최적화
- **Rate Limiting**: 1초 간격으로 API 호출 제한
- **타임아웃 관리**: 30초 타임아웃 설정
- **토큰 제한**: 키워드 500토큰, 질문 6500토큰
- **Temperature**: 0.3으로 일관된 결과 생성

## JSON 응답 처리
- 코드 블록 (```json) 자동 제거
- JSON 경계 자동 탐지
- 파싱 오류 시 안전한 폴백
- 응답 구조 검증

## 프롬프트 관리
- 외부 JSON 파일로 프롬프트 관리
- 시스템 프롬프트와 사용자 프롬프트 분리
- 템플릿 기반 동적 프롬프트 구성
- 프롬프트 로드 실패 시 기본값 제공

## 폴백 시스템

### 키워드 폴백
기본 제공 키워드: JavaScript, Python, React, Node.js, Git

### 질문 폴백
- 기술면접 3개: 기술 스택, 문제 해결, 버전 관리
- 행동면접 2개: 팀워크, 회사 기여 의지
- 회사명 반영한 개인화된 질문

## 설정 및 환경변수
- `UPSTAGE_API_KEY`: Solar LLM API 키
- `UPSTAGE_MODEL`: 사용할 모델명 (solar-pro2)
- `API_TIMEOUT`: API 호출 타임아웃
- `MAX_TEXT_LENGTH`: 텍스트 최대 길이
- `MAX_OUTPUT_TOKENS`: 출력 토큰 제한
- `RATE_LIMIT_INTERVAL`: API 호출 간격

## 사용 예시
```python
processor = LLMProcessor()

# 키워드 추출
keywords = await processor.extract_keywords(portfolio_text)

# 질문 생성
questions = await processor.generate_questions(
    portfolio_text, 
    keywords["keywords"], 
    "네이버"
)
```

## 의존성
- httpx: 비동기 HTTP 클라이언트
- json: JSON 데이터 처리
- asyncio: 비동기 처리 및 타이밍
- logging: 로깅 시스템
- config: 환경설정 관리
