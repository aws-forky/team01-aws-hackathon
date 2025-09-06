# API Documentation

## 역할
백엔드 API의 상세한 엔드포인트 명세와 사용법을 설명합니다.

## API 엔드포인트

### 1. 파일 업로드
```
POST /api/upload
Content-Type: multipart/form-data
```
- 요청: PDF 파일
- 응답: 파일 ID, 추출된 텍스트, 메타데이터
- 에러: 파일 형식 오류, 크기 초과

### 2. 키워드 추출
```
POST /api/extract-keywords
Content-Type: application/json
```
- 요청: 추출된 텍스트
- 응답: 기술 키워드 목록, 우선순위, 카테고리
- 에러: AI API 오류, 텍스트 분석 실패

### 3. 질문 생성
```
POST /api/generate-questions
Content-Type: application/json
```
- 요청: 키워드 목록, 회사 정보
- 응답: 질문 목록, 모범답안, 질문 타입
- 에러: 질문 생성 실패, Fallback 적용

### 4. 회사 목록
```
GET /api/companies
```
- 응답: 지원 가능한 회사 목록, 특징, 기술 스택

### 5. 헬스체크
```
GET /health
```
- 응답: 서버 상태, 버전 정보

## 응답 형식
- 성공: `{"success": true, "data": {...}}`
- 실패: `{"success": false, "error": "...", "code": "..."}`

## 에러 코드
- `FILE_TOO_LARGE`: 파일 크기 초과
- `INVALID_FILE_TYPE`: 지원하지 않는 파일 형식
- `AI_API_ERROR`: AI API 호출 실패
- `PARSING_ERROR`: 문서 파싱 오류
- `GENERATION_ERROR`: 질문 생성 실패
