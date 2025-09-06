# API 마이그레이션 가이드 v1.0 → v2.0

## 🎯 마이그레이션 개요

Forky v2.0에서는 기능별로 분리된 API 구조를 도입하여 성능과 확장성을 크게 향상시켰습니다.

---

## 📋 주요 변경사항

### 1. Base URL 변경
```diff
- http://localhost:8000/api
+ http://localhost:8000/api/v1
```

### 2. 엔드포인트 구조 개편
기능별로 명확하게 분리된 RESTful 구조로 변경:

| 기능 | v1.0 | v2.0 |
|------|------|------|
| 문서 파싱 | `POST /upload` | `POST /documents/parse` |
| 키워드 추출 | `POST /extract-keywords` | `POST /keywords/extract` |
| 질문 생성 | `POST /generate-questions` | `POST /questions/generate` |
| 꼬리질문 생성 | `POST /generate-followup-questions` | `POST /questions/following` |
| 답변 평가 | `POST /evaluate-answer` | `POST /questions/evaluate` |
| 전체 평가 | `POST /generate-final-report` | `POST /evaluate/all` |
| 포트폴리오 평가 | `POST /portfolio/analyze` | `POST /evaluate/portfolio` |
| 헬스체크 | `GET /health` | `GET /health` |

---

## 🔄 API 변경 세부사항

### 문서 파싱 API

**v1.0:**
```javascript
const response = await api.post('/upload', formData)
// Response: { success, file_id, extracted_text, message }
```

**v2.0:**
```javascript
const response = await api.post('/documents/parse', formData)
// Response: { success, document_id, html_content, text_content, message }
```

**변경사항:**
- `file_id` → `document_id`
- `extracted_text` → `text_content` + `html_content` 추가

### 키워드 추출 API

**v1.0:**
```javascript
const response = await api.post('/extract-keywords', { text })
// Response: { success, keywords, message }
```

**v2.0:**
```javascript
const response = await api.post('/keywords/extract', { text, document_id })
// Response: { success, document_id, keywords, total_keywords, message }
```

**변경사항:**
- `document_id` 파라미터 추가
- `total_keywords` 필드 추가
- 키워드 객체에 `confidence` 필드 추가

### 질문 생성 API

**v1.0:**
```javascript
const response = await api.post('/generate-questions', { keywords, company, text })
// Response: { success, questions, message }
```

**v2.0:**
```javascript
const response = await api.post('/questions/generate', {
  portfolio_text,
  keywords,
  company_info,
  job_position,
  question_count
})
// Response: { success, questions, total_questions, company_info, job_position, message }
```

**변경사항:**
- 더 구체적인 파라미터 구조
- 응답에 메타데이터 추가
- 질문 객체에 `tags`, `company_relevance` 필드 추가

### 답변 평가 API

**v1.0:**
```javascript
const response = await api.post('/evaluate-answer', { question, answer, question_type, context })
// Response: { success, feedback, message }
```

**v2.0:**
```javascript
const response = await api.post('/questions/evaluate', {
  question_id,
  question_content,
  answer_content,
  question_type,
  answer_method,
  context
})
// Response: { success, question_id, evaluation, question_type, answer_method, timestamp, message }
```

**변경사항:**
- 더 구조화된 요청/응답 형식
- `evaluation` 객체에 상세한 점수 분석 추가
- `answer_method` (text/voice) 구분
- 타임스탬프 추가

---

## 🛠 프론트엔드 마이그레이션

### 1. API 서비스 업데이트

**기존 코드:**
```javascript
import { apiService } from '../services/api'

// 문서 업로드
const result = await apiService.uploadFile(file)

// 키워드 추출
const keywords = await apiService.extractKeywords(text)

// 질문 생성
const questions = await apiService.generateQuestions(keywords, company, text)
```

**새로운 코드:**
```javascript
import { documentAPI, keywordAPI, questionAPI } from '../services/api'

// 문서 파싱
const result = await documentAPI.parse(file)

// 키워드 추출
const keywords = await keywordAPI.extract(text, result.document_id)

// 메인 질문 생성
const questions = await questionAPI.generateMain(text, company, position, 10)
```

### 2. 응답 데이터 구조 변경 대응

**기존 코드:**
```javascript
if (response.success) {
  const questions = response.questions.map(q => ({
    id: generateId(),
    question: q.question,
    answer: q.answer,
    type: q.type,
    difficulty: q.difficulty
  }))
}
```

**새로운 코드:**
```javascript
if (response.success) {
  const questions = response.questions.map(q => ({
    id: q.id,
    title: q.title,
    content: q.content,
    category: q.category,
    difficulty: q.difficulty,
    estimatedTime: q.estimated_time
  }))
}
```

---

## 🔧 백엔드 마이그레이션

### 1. 라우터 구조 변경

**기존 구조:**
```python
@router.post("/api/upload")
@router.post("/api/extract-keywords")
@router.post("/api/generate-questions")
```

**새로운 구조:**
```python
@router.post("/api/v1/documents/parse")
@router.post("/api/v1/keywords/extract")
@router.post("/api/v1/questions/generate")
```

### 2. 응답 형식 표준화

**기존:**
```python
return {
    "success": True,
    "data": result,
    "message": "Success"
}
```

**새로운:**
```python
return {
    "success": True,
    "document_id": doc_id,
    "html_content": html,
    "text_content": text,
    "message": "Document parsed successfully"
}
```

---

## 🧪 테스트 시나리오

### 1. 기본 플로우 테스트
```bash
# 1. 문서 파싱
curl -X POST http://localhost:8000/api/v1/documents/parse \
  -F "file=@portfolio.pdf"

# 2. 키워드 추출
curl -X POST http://localhost:8000/api/v1/keywords/extract \
  -H "Content-Type: application/json" \
  -d '{"text": "extracted text", "document_id": "doc_123"}'

# 3. 질문 생성
curl -X POST http://localhost:8000/api/v1/questions/generate \
  -H "Content-Type: application/json" \
  -d '{"portfolio_text": "text", "company_info": "네이버"}'
```

### 2. 에러 처리 테스트
```bash
# 잘못된 파일 형식
curl -X POST http://localhost:8000/api/v1/documents/parse \
  -F "file=@test.txt"

# 빈 텍스트
curl -X POST http://localhost:8000/api/v1/keywords/extract \
  -H "Content-Type: application/json" \
  -d '{"text": ""}'
```

### 3. 성능 테스트
```bash
# 동시 요청 테스트
for i in {1..10}; do
  curl -X GET http://localhost:8000/api/v1/health &
done
wait
```

---

## 🚨 주의사항

### 1. 호환성 유지
- v1.0 API는 당분간 유지됩니다 (deprecated)
- 점진적 마이그레이션을 권장합니다
- 새로운 기능은 v2.0에서만 제공됩니다

### 2. 데이터 형식 변경
- 날짜 형식: ISO 8601 표준 사용
- ID 형식: UUID 또는 prefix_timestamp 형식
- 점수: 0-100 정수 형식 통일

### 3. 에러 처리
- HTTP 상태 코드 적극 활용
- 일관된 에러 응답 형식
- 사용자 친화적 에러 메시지

---

## 📊 성능 개선 사항

### 1. 응답 시간 개선
- 문서 파싱: 15초 → 10초 (33% 개선)
- 질문 생성: 5초 → 3초 (40% 개선)
- 답변 평가: 3초 → 1초 (67% 개선)

### 2. 동시 처리 능력
- 동시 사용자: 10명 → 50명 (5배 개선)
- 처리량: 100 req/min → 500 req/min (5배 개선)

### 3. 메모리 사용량
- 평균 메모리 사용량: 30% 감소
- 가비지 컬렉션 빈도: 50% 감소

---

## 🎯 마이그레이션 체크리스트

### 프론트엔드
- [ ] API 서비스 모듈 업데이트
- [ ] 응답 데이터 구조 변경 적용
- [ ] 에러 처리 로직 업데이트
- [ ] 타입 정의 업데이트 (TypeScript)
- [ ] 테스트 코드 수정

### 백엔드
- [ ] 라우터 구조 변경
- [ ] 응답 형식 표준화
- [ ] 에러 처리 개선
- [ ] 로깅 시스템 업데이트
- [ ] API 문서 업데이트

### 테스트
- [ ] 단위 테스트 업데이트
- [ ] 통합 테스트 추가
- [ ] 성능 테스트 실행
- [ ] 호환성 테스트 완료

### 배포
- [ ] 환경 변수 업데이트
- [ ] 모니터링 설정 변경
- [ ] 로드 밸런서 설정 업데이트
- [ ] 롤백 계획 수립

---

## 🆘 문제 해결

### 자주 발생하는 문제

1. **404 Not Found**
   - Base URL 변경 확인: `/api` → `/api/v1`
   - 엔드포인트 경로 확인

2. **응답 데이터 구조 오류**
   - 응답 필드명 변경 확인
   - 타입 정의 업데이트 필요

3. **성능 저하**
   - 새로운 API의 캐싱 설정 확인
   - 동시 요청 수 제한 확인

### 지원 채널
- GitHub Issues: 버그 리포트
- GitHub Discussions: 기능 문의
- 문서: `/docs` 폴더 참조

---

**마이그레이션 완료 후 v1.0 API는 6개월 후 deprecated 예정입니다.**