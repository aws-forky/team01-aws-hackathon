# routers/questions.py - 질문 생성 + 완전처리 엔드포인트

## 역할
키워드 기반 면접 질문 생성과 문서 파싱부터 질문 생성까지의 완전 자동화 파이프라인을 제공하는 API 엔드포인트입니다.

## 주요 기능

### 1. 맞춤형 면접 질문 생성
- 포트폴리오 텍스트와 키워드를 기반으로 한 개인화된 질문
- 기술면접 3개 + 행동면접 2개의 균형잡힌 구성
- 회사명을 고려한 맞춤형 질문 생성

### 2. 완전 자동화 파이프라인
- 파일 업로드 → 문서 파싱 → 키워드 추출 → 질문 생성
- 원스톱 서비스로 사용자 편의성 극대화
- 각 단계별 오류 처리 및 폴백 시스템

### 3. 견고한 오류 처리
- 각 처리 단계별 독립적인 오류 처리
- 부분 실패 시에도 가능한 결과 제공
- 폴백 사용 여부 및 이유 상세 추적

## API 엔드포인트

### POST /api/v1/questions/generate
개별 질문 생성 API

**요청**
- Content-Type: application/json
- Body: QuestionGenerateRequest
  - `text: str` - 포트폴리오 텍스트 (필수)
  - `keywords: List[str]` - 기술 키워드 목록 (필수)
  - `company_name: Optional[str]` - 지원 회사명 (선택)

**응답**
- QuestionGenerateResponse 모델
- 생성된 면접 질문 목록 (5개)
- 각 질문의 유형, 내용, 평가 가이드

### POST /api/v1/questions/process-complete
완전 자동화 파이프라인 API

**요청**
- Content-Type: multipart/form-data
- file: UploadFile (필수) - 포트폴리오 문서
- company_name: Optional[str] (선택) - 지원 회사명

**응답**
- ProcessCompleteResponse 모델
- 문서 내용, 키워드, 질문을 모두 포함
- 각 단계별 폴백 사용 여부 추적

## 질문 생성 과정
1. 입력 데이터 검증 (텍스트, 키워드)
2. 회사 정보 포함한 프롬프트 구성
3. Solar LLM으로 질문 생성 요청
4. JSON 응답 파싱 및 질문 구조화
5. 실패 시 폴백 질문 제공

## 완전 처리 파이프라인
1. **문서 파싱**: Upstage API로 텍스트 추출
2. **키워드 추출**: Solar LLM으로 기술 키워드 분석
3. **질문 생성**: 키워드 기반 면접 질문 생성
4. **결과 통합**: 모든 단계 결과를 하나의 응답으로 통합

## 사용 예시

### 질문 생성
```bash
curl -X POST "http://localhost:4700/api/v1/questions/generate" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "React 프로젝트 경험...",
       "keywords": ["React", "JavaScript", "Git"],
       "company_name": "네이버"
     }'
```

### 완전 처리
```bash
curl -X POST "http://localhost:4700/api/v1/questions/process-complete" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@portfolio.pdf" \
     -F "company_name=카카오"
```

## 응답 예시
```json
{
    "success": true,
    "message": "Questions generated successfully",
    "questions": [
        {
            "id": "tech_1",
            "type": "technical",
            "text": "React에서 상태 관리는 어떻게 하셨나요?",
            "explanation": "useState, useReducer 등의 이해도 확인"
        }
    ],
    "is_fallback": false,
    "fallback_reason": null
}
```

## 폴백 질문
AI 생성 실패 시 제공되는 기본 질문:
- 기술면접 3개: 기술 스택, 문제 해결, 버전 관리
- 행동면접 2개: 팀워크, 회사 기여 의지

## 오류 처리
- 400: 필수 데이터 누락 (텍스트, 키워드)
- 413: 파일 크기 초과 (완전 처리)
- 500: 내부 서버 오류

## 의존성
- DocumentParser, LLMProcessor 서비스
- 질문 생성 프롬프트 템플릿
- 관련 요청/응답 모델
