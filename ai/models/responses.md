# models/responses.py - Pydantic 응답 모델

## 역할
API 엔드포인트에서 반환하는 응답 데이터의 구조를 정의하고 일관성을 보장하는 Pydantic 모델들을 관리합니다.

## 주요 기능

### 1. 응답 구조 표준화
- 모든 API 응답에 일관된 형식 제공
- 성공/실패 상태, 메시지, 데이터를 명확히 구분
- 클라이언트에서 예측 가능한 응답 처리 가능

### 2. 타입 안전성
- 응답 데이터의 타입 보장
- IDE 자동완성 및 타입 체크 지원
- 런타임 데이터 검증

### 3. API 문서 자동 생성
- OpenAPI 스키마에 응답 예시 자동 포함
- Swagger UI에서 응답 구조 시각화

## 기본 모델

### BaseResponse
모든 응답의 기본 구조
- `success: bool` - 요청 성공 여부
- `message: str` - 응답 메시지

## 기능별 응답 모델

### DocumentParseResponse
문서 파싱 API 응답
- BaseResponse 상속
- `content: Optional[str]` - 추출된 텍스트 내용

### KeywordResponse
키워드 상세 정보 모델
- `tech: str` - 기술명
- `category: str` - 기술 카테고리
- `reason: str` - 선택 이유

### KeywordExtractResponse
키워드 추출 API 응답
- BaseResponse 상속
- `keywords: Optional[List[str]]` - 추출된 키워드 목록
- `detailed_keywords: Optional[List[KeywordResponse]]` - 상세 키워드 정보
- `is_fallback: bool` - 폴백 사용 여부
- `fallback_reason: Optional[str]` - 폴백 사용 이유

### QuestionResponse
면접 질문 모델
- `id: str` - 질문 고유 ID
- `type: str` - 질문 유형 (technical/behavioral)
- `text: str` - 질문 내용
- `explanation: str` - 평가 가이드

### QuestionGenerateResponse
질문 생성 API 응답
- BaseResponse 상속
- `questions: Optional[List[QuestionResponse]]` - 생성된 질문 목록
- `is_fallback: bool` - 폴백 사용 여부
- `fallback_reason: Optional[str]` - 폴백 사용 이유

### ProcessCompleteResponse
완전 처리 파이프라인 응답
- BaseResponse 상속
- `document_content: Optional[str]` - 문서 내용
- `keywords: Optional[List[str]]` - 키워드 목록
- `detailed_keywords: Optional[List[KeywordResponse]]` - 상세 키워드
- `questions: Optional[List[QuestionResponse]]` - 질문 목록
- `keyword_fallback: bool` - 키워드 폴백 여부
- `question_fallback: bool` - 질문 폴백 여부
- `fallback_reasons: Optional[List[str]]` - 폴백 이유 목록

## 응답 예시
```json
{
    "success": true,
    "message": "Keywords extracted successfully",
    "keywords": ["React", "Node.js", "JavaScript"],
    "is_fallback": false,
    "fallback_reason": null
}
```
