# Forky 자동화 워크플로우

## 전체 시스템 플로우

```mermaid
graph TD
    A[사용자 PDF 업로드] --> B[파일 검증]
    B --> C[Document Parser API]
    C --> D[텍스트 추출 & HTML 정제]
    D --> E[키워드 추출 API]
    E --> F[기술 키워드 분류]
    F --> G[회사 선택]
    G --> H[질문 생성 API]
    H --> I[면접 질문 표시]
    I --> J[PDF 결과 다운로드]
```

## 상세 워크플로우

### 1. 파일 업로드 & 처리 워크플로우

```mermaid
sequenceDiagram
    participant U as 사용자
    participant F as Frontend
    participant B as Backend
    participant D as Document Parser API
    
    U->>F: PDF 파일 업로드
    F->>B: POST /api/upload
    B->>B: 파일 검증 (크기, 타입)
    B->>B: 임시 파일 저장
    B->>D: POST /api/v1/documents/parse
    D-->>B: HTML 형태 텍스트 반환
    B->>B: HTML 태그 제거 & 정제
    B-->>F: 추출된 텍스트 반환
    F->>F: 상태 저장 (extractedText)
```

### 2. 키워드 추출 워크플로우

```mermaid
sequenceDiagram
    participant F as Frontend
    participant B as Backend
    participant K as Keyword Extract API
    
    F->>B: POST /api/extract-keywords
    Note over F,B: {text: "포트폴리오 텍스트"}
    B->>K: POST /api/v1/keywords/extract
    K-->>B: 키워드 문자열 배열
    B->>B: 카테고리 자동 분류
    Note over B: language|framework|tool|database|cloud
    B->>B: 중요도 순서별 할당
    B-->>F: 구조화된 키워드 객체 배열
    F->>F: 상태 저장 (keywords)
```

### 3. 질문 생성 워크플로우

```mermaid
sequenceDiagram
    participant F as Frontend
    participant B as Backend
    participant Q as Question Generate API
    
    F->>B: POST /api/generate-questions
    Note over F,B: {keywords, company, text}
    B->>Q: POST /api/v1/questions/generate
    Q-->>B: 질문 객체 배열
    Note over Q,B: {id, type, text, explanation}
    B->>B: 응답 구조 매핑
    Note over B: text→question, explanation→answer
    B-->>F: 표준화된 질문 배열
    F->>F: 상태 저장 (questions)
    F->>F: 면접 페이지로 이동
```

## 데이터 플로우

### 상태 관리 플로우

```mermaid
stateDiagram-v2
    [*] --> Upload: 시작
    Upload --> KeywordExtract: PDF 업로드 완료
    KeywordExtract --> CompanySelect: 키워드 추출 완료
    CompanySelect --> QuestionGenerate: 회사 선택
    QuestionGenerate --> Interview: 질문 생성 완료
    Interview --> Result: 면접 완료
    Result --> [*]: PDF 다운로드
    
    Upload: extractedText 저장
    KeywordExtract: keywords 배열 저장
    CompanySelect: selectedCompany 저장
    QuestionGenerate: questions 배열 저장
    Interview: answers 배열 저장
    Result: 최종 결과 생성
```

### API 호출 체인

```mermaid
graph LR
    A[PDF Upload] --> B[Document Parser]
    B --> C[Text Processing]
    C --> D[Keyword Extract]
    D --> E[Category Mapping]
    E --> F[Company Selection]
    F --> G[Question Generate]
    G --> H[Response Mapping]
    H --> I[Interview Display]
```

## 에러 처리 워크플로우

```mermaid
flowchart TD
    A[API 호출] --> B{응답 성공?}
    B -->|Yes| C[데이터 검증]
    B -->|No| D[HTTP 에러 처리]
    
    C --> E{데이터 유효?}
    E -->|Yes| F[정상 처리]
    E -->|No| G[데이터 에러 처리]
    
    D --> H[에러 메시지 표시]
    G --> H
    F --> I[다음 단계 진행]
    H --> J[사용자 재시도]
```

## 자동화 스크립트 예시

### CI/CD 파이프라인

```yaml
# .github/workflows/deploy.yml
name: Deploy Forky
on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Test Backend
        run: |
          cd backend
          pip install -r requirements.txt
          python -m pytest
      - name: Test Frontend
        run: |
          cd frontend
          npm install
          npm test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to AWS
        run: |
          # AWS 배포 스크립트
          docker build -t forky .
          docker push $ECR_REGISTRY/forky:latest
```

### 개발 환경 자동 설정

```bash
#!/bin/bash
# setup.sh - 개발 환경 자동 설정

echo "🚀 Forky 개발 환경 설정 시작..."

# 백엔드 설정
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 프론트엔드 설정
cd ../frontend
npm install

# 환경 변수 설정
cp backend/.env.example backend/.env
echo "✅ 개발 환경 설정 완료!"
```

## 모니터링 워크플로우

```mermaid
graph TD
    A[API 호출] --> B[로그 수집]
    B --> C[메트릭 생성]
    C --> D[대시보드 업데이트]
    
    E[에러 발생] --> F[알림 발송]
    F --> G[자동 복구 시도]
    G --> H{복구 성공?}
    H -->|Yes| I[정상 상태 복원]
    H -->|No| J[수동 개입 요청]
```

## 성능 최적화 자동화

```mermaid
flowchart LR
    A[성능 측정] --> B[병목 지점 식별]
    B --> C[자동 스케일링]
    C --> D[캐시 최적화]
    D --> E[리소스 조정]
    E --> F[성능 재측정]
    F --> A
```

이 워크플로우를 통해 Forky 시스템의 전체적인 자동화 프로세스를 이해하고 관리할 수 있습니다.