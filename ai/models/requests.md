# models/requests.py - Pydantic 요청 모델

## 역할
API 엔드포인트로 들어오는 요청 데이터의 구조를 정의하고 검증하는 Pydantic 모델들을 관리합니다.

## 주요 기능

### 1. 데이터 검증
- 요청 데이터의 타입, 필수 필드, 형식 자동 검증
- 잘못된 데이터 형식 시 자동으로 HTTP 422 에러 반환
- 타입 힌트를 통한 IDE 지원 및 코드 안정성 확보

### 2. API 문서 자동 생성
- FastAPI가 Pydantic 모델을 기반으로 OpenAPI 스키마 자동 생성
- Swagger UI에서 요청 예시 및 필드 설명 제공

## 정의된 모델들

### KeywordExtractRequest
키워드 추출 API 요청 모델
- `text: str` - 키워드를 추출할 포트폴리오 텍스트 (필수)

### QuestionGenerateRequest  
질문 생성 API 요청 모델
- `text: str` - 포트폴리오 텍스트 (필수)
- `keywords: List[str]` - 추출된 기술 키워드 목록 (필수)
- `company_name: Optional[str]` - 지원 회사명 (선택)

### ProcessCompleteRequest
완전 처리 파이프라인 요청 모델
- `company_name: Optional[str]` - 지원 회사명 (선택)
- 파일은 multipart/form-data로 별도 처리

## 사용 예시
```python
# 키워드 추출 요청
{
    "text": "React와 Node.js를 사용한 웹 애플리케이션 개발 프로젝트..."
}

# 질문 생성 요청
{
    "text": "포트폴리오 전체 텍스트...",
    "keywords": ["React", "Node.js", "JavaScript", "Git"],
    "company_name": "네이버"
}
```

## 검증 기능
- 빈 문자열 검증
- 리스트 타입 검증
- 선택적 필드 처리
- 자동 타입 변환
