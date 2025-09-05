# routers/keywords.py - 키워드 추출 엔드포인트

## 역할
포트폴리오 텍스트에서 Solar LLM을 사용하여 기술 스택 키워드를 자동으로 추출하는 API 엔드포인트를 제공합니다.

## 주요 기능

### 1. AI 기반 키워드 추출
- Solar LLM을 활용한 지능형 키워드 분석
- 포트폴리오 텍스트에서 5-10개의 핵심 기술 키워드 추출
- 기술 스택의 중요도와 관련성을 고려한 선별

### 2. 텍스트 전처리
- 입력 텍스트 검증 및 정제
- 최대 길이 제한으로 API 효율성 확보
- 빈 텍스트 및 유효하지 않은 입력 필터링

### 3. 폴백 시스템
- AI 서비스 실패 시 기본 키워드 제공
- 서비스 중단 없는 안정적인 응답 보장
- 폴백 사용 여부 및 이유 명시

## API 엔드포인트

### POST /api/v1/keywords/extract
**요청**
- Content-Type: application/json
- Body: KeywordExtractRequest
  - `text: str` - 키워드를 추출할 포트폴리오 텍스트

**응답**
- KeywordExtractResponse 모델
- 추출된 키워드 목록
- 상세 키워드 정보 (선택적)
- 폴백 사용 여부 및 이유

## 키워드 추출 과정
1. 입력 텍스트 검증 및 전처리
2. Solar LLM에 키워드 추출 프롬프트 전송
3. AI 응답에서 JSON 형식 키워드 파싱
4. 키워드 개수 제한 (최대 10개)
5. 실패 시 폴백 키워드 반환

## 사용 예시
```bash
curl -X POST "http://localhost:4700/api/v1/keywords/extract" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "React와 Node.js를 사용한 웹 애플리케이션 개발..."
     }'
```

## 응답 예시
```json
{
    "success": true,
    "message": "Keywords extracted successfully",
    "keywords": ["React", "Node.js", "JavaScript", "Express", "MongoDB"],
    "detailed_keywords": [],
    "is_fallback": false,
    "fallback_reason": null
}
```

## 폴백 키워드
AI 추출 실패 시 제공되는 기본 키워드:
- JavaScript
- Python  
- React
- Node.js
- Git

## 오류 처리
- 400: 텍스트 내용이 비어있음
- 500: 내부 서버 오류 (LLM 처리 실패)

## 의존성
- LLMProcessor 서비스 클래스
- KeywordExtractRequest/Response 모델
- 키워드 추출 프롬프트 템플릿
