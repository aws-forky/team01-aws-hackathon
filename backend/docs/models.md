# Data Models

## 역할
API 요청/응답 스키마와 데이터 구조를 정의합니다.

## 주요 모델

### 1. Request Models
- `FileUploadRequest` - 파일 업로드 요청 스키마
- `KeywordExtractionRequest` - 키워드 추출 요청 스키마
- `QuestionGenerationRequest` - 질문 생성 요청 스키마

### 2. Response Models
- `UploadResponse` - 파일 업로드 응답 (파일 ID, 추출된 텍스트)
- `KeywordResponse` - 키워드 추출 응답 (키워드 목록, 우선순위)
- `QuestionResponse` - 질문 생성 응답 (질문 목록, 모범답안)

### 3. Data Models
- `Portfolio` - 포트폴리오 정보 (텍스트, 메타데이터)
- `Keyword` - 기술 키워드 (이름, 카테고리, 중요도)
- `Question` - 면접 질문 (질문, 답안, 타입, 난이도)
- `Company` - 회사 정보 (이름, 특징, 기술 스택)

### 4. Enum Types
- `QuestionType` - 질문 유형 (기술, 행동, 상황)
- `DifficultyLevel` - 난이도 (초급, 중급, 고급)
- `KeywordCategory` - 키워드 분류 (언어, 프레임워크, 도구)

## 특징
- Pydantic 기반 타입 안전성
- 자동 검증 및 직렬화
- OpenAPI 스키마 자동 생성
- 상세한 필드 설명 및 예시
