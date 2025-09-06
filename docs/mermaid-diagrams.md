# Forky 워크플로우 Mermaid 다이어그램

## 1. 전체 시스템 플로우

```mermaid
graph TD
    A[사용자 PDF 업로드] --> B[파일 검증]
    B --> C{검증 성공?}
    C -->|Yes| D[Document Parser API]
    C -->|No| E[에러 메시지]
    D --> F[텍스트 추출 & HTML 정제]
    F --> G[키워드 추출 API]
    G --> H[기술 키워드 분류]
    H --> I[회사 선택 페이지]
    I --> J[사용자 회사 선택]
    J --> K[질문 생성 API]
    K --> L[면접 질문 표시]
    L --> M[사용자 답변 입력]
    M --> N[PDF 결과 생성]
    N --> O[다운로드 완료]
    E --> A
```

## 2. API 호출 시퀀스 다이어그램

```mermaid
sequenceDiagram
    participant U as 사용자
    participant F as Frontend
    participant B as Backend
    participant D as Document Parser
    participant K as Keyword API
    participant Q as Question API
    
    U->>F: PDF 업로드
    F->>B: POST /api/upload
    B->>D: POST /documents/parse
    D-->>B: HTML 텍스트
    B-->>F: 추출된 텍스트
    
    F->>B: POST /extract-keywords
    B->>K: POST /keywords/extract
    K-->>B: 키워드 배열
    B-->>F: 구조화된 키워드
    
    U->>F: 회사 선택
    F->>B: POST /generate-questions
    B->>Q: POST /questions/generate
    Q-->>B: 질문 객체들
    B-->>F: 매핑된 질문들
    F-->>U: 면접 시뮬레이션
```

## 3. 상태 관리 플로우

```mermaid
stateDiagram-v2
    [*] --> Upload: 앱 시작
    Upload --> Processing: PDF 업로드
    Processing --> KeywordExtract: 텍스트 추출 완료
    KeywordExtract --> CompanySelect: 키워드 추출 완료
    CompanySelect --> QuestionGenerate: 회사 선택
    QuestionGenerate --> Interview: 질문 생성 완료
    Interview --> Result: 답변 완료
    Result --> [*]: PDF 다운로드
    
    Processing --> Upload: 처리 실패
    KeywordExtract --> Upload: 키워드 추출 실패
    QuestionGenerate --> CompanySelect: 질문 생성 실패
```

## 4. 데이터 플로우 다이어그램

```mermaid
flowchart LR
    A[PDF 파일] --> B[파일 검증]
    B --> C[Document Parser]
    C --> D[HTML 텍스트]
    D --> E[텍스트 정제]
    E --> F[키워드 추출]
    F --> G[카테고리 분류]
    G --> H[중요도 할당]
    H --> I[회사 선택]
    I --> J[질문 생성]
    J --> K[응답 매핑]
    K --> L[면접 질문]
    
    style A fill:#e1f5fe
    style L fill:#e8f5e8
    style C fill:#fff3e0
    style F fill:#fff3e0
    style J fill:#fff3e0
```

## 5. MVC 아키텍처 다이어그램

```mermaid
graph TB
    subgraph "Frontend (View)"
        V1[UploadPage]
        V2[CompanyPage]
        V3[InterviewPage]
        V4[ResultPage]
        V5[Components]
    end
    
    subgraph "Backend (Controller)"
        C1[/api/upload]
        C2[/api/extract-keywords]
        C3[/api/generate-questions]
        C4[/api/companies]
    end
    
    subgraph "Services & Models"
        S1[DocumentParserService]
        S2[AIService]
        S3[FileService]
        M1[Keyword Model]
        M2[Question Model]
        M3[Company Model]
    end
    
    subgraph "External APIs"
        E1[Document Parser API]
        E2[Keyword Extract API]
        E3[Question Generate API]
    end
    
    V1 --> C1
    V2 --> C2
    V2 --> C4
    V3 --> C3
    
    C1 --> S1
    C2 --> S2
    C3 --> S2
    C4 --> M3
    
    S1 --> E1
    S2 --> E2
    S2 --> E3
    
    S1 --> M1
    S2 --> M2
```

## 6. 에러 처리 플로우

```mermaid
flowchart TD
    A[API 호출] --> B{HTTP 상태}
    B -->|200| C[응답 데이터 검증]
    B -->|4xx| D[클라이언트 에러]
    B -->|5xx| E[서버 에러]
    B -->|Timeout| F[타임아웃 에러]
    
    C --> G{데이터 유효성}
    G -->|Valid| H[정상 처리]
    G -->|Invalid| I[데이터 에러]
    
    D --> J[에러 메시지 표시]
    E --> J
    F --> J
    I --> J
    
    J --> K[사용자 재시도 옵션]
    K --> A
    
    H --> L[다음 단계 진행]
    
    style H fill:#e8f5e8
    style J fill:#ffebee
```

## 7. CI/CD 파이프라인

```mermaid
gitgraph
    commit id: "Initial"
    branch develop
    checkout develop
    commit id: "Feature A"
    commit id: "Feature B"
    checkout main
    merge develop
    commit id: "Release v1.0"
    
    branch hotfix
    checkout hotfix
    commit id: "Bug Fix"
    checkout main
    merge hotfix
    commit id: "Release v1.0.1"
```

```mermaid
flowchart LR
    A[Git Push] --> B[GitHub Actions]
    B --> C[코드 검사]
    C --> D[테스트 실행]
    D --> E[빌드]
    E --> F[Docker 이미지]
    F --> G[AWS 배포]
    G --> H[Health Check]
    H --> I[배포 완료]
    
    C --> J[실패 시 알림]
    D --> J
    E --> J
    G --> J
    
    style I fill:#e8f5e8
    style J fill:#ffebee
```

## 8. 성능 모니터링 플로우

```mermaid
graph TD
    A[사용자 요청] --> B[로드 밸런서]
    B --> C[백엔드 서버]
    C --> D[외부 API]
    
    C --> E[로그 수집]
    D --> F[응답 시간 측정]
    E --> G[메트릭 생성]
    F --> G
    
    G --> H[대시보드]
    G --> I{임계값 초과?}
    I -->|Yes| J[알림 발송]
    I -->|No| K[정상 모니터링]
    
    J --> L[자동 스케일링]
    L --> M[리소스 증설]
```

## 사용법

1. **Mermaid Live Editor**: https://mermaid.live/
2. **GitHub**: 마크다운 파일에 직접 삽입
3. **VS Code**: Mermaid 확장 프로그램 설치
4. **Notion, Obsidian**: Mermaid 지원 도구 사용

각 다이어그램 코드를 복사해서 위 도구들에 붙여넣으면 시각적인 다이어그램으로 렌더링됩니다.