# Backend Services

## 역할
비즈니스 로직을 처리하고 외부 API와의 통신을 담당합니다.

## 주요 서비스

### 1. Document Parser Service
- Upstage Document Parser API 연동
- PDF 파일을 텍스트로 변환
- OCR 없이 고품질 텍스트 추출
- 메타데이터 제거 및 텍스트 정제

### 2. AI Service
- Upstage Solar LLM Pro2 API 연동
- 프롬프트 엔지니어링 적용
- 키워드 추출 및 질문 생성
- Chain-of-Thought 방식 구현

### 3. Keyword Extraction Service
- 포트폴리오 텍스트 분석
- 기술 스택 식별 및 분류
- 시장 수요 기반 우선순위 결정
- 2024-2025 채용 트렌드 반영

### 4. Question Generation Service
- 개인화된 기술 질문 생성
- 회사별 특화 질문 커스터마이징
- 행동 질문 및 상황 질문 포함
- Fallback 시스템 (AI 실패 시 기본 질문)

### 5. File Service
- 파일 업로드 처리
- 임시 파일 관리
- 파일 검증 및 보안 체크
- 지원 형식 확인 (PDF)
