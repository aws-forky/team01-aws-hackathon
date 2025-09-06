# Frontend Services

## 역할
백엔드 API와의 통신 및 클라이언트 사이드 비즈니스 로직을 처리합니다.

## 주요 서비스

### 1. API Service
- Axios 기반 HTTP 클라이언트
- 백엔드 API 엔드포인트 호출
- 요청/응답 인터셉터 설정
- 에러 처리 및 재시도 로직
- 타임아웃 및 취소 기능

### 2. File Service
- 파일 업로드 처리
- 파일 검증 (크기, 형식)
- 업로드 진행률 추적
- 드래그앤드롭 이벤트 처리
- 파일 미리보기 기능

### 3. PDF Service
- jsPDF를 활용한 PDF 생성
- html2canvas로 HTML을 이미지 변환
- 질문/답안 레이아웃 최적화
- 다운로드 및 저장 기능
- 인쇄 친화적 포맷팅

### 4. Storage Service
- 로컬 스토리지 관리
- 세션 데이터 저장
- 사용자 설정 저장
- 임시 데이터 캐싱
- PWA 오프라인 데이터

### 5. Analytics Service
- 사용자 행동 추적
- 페이지 뷰 및 이벤트 로깅
- 성능 메트릭 수집
- 에러 리포팅
- A/B 테스트 지원

## API 엔드포인트
- `POST /api/upload` - 파일 업로드
- `POST /api/extract-keywords` - 키워드 추출
- `POST /api/generate-questions` - 질문 생성
- `GET /api/companies` - 회사 목록 조회

## 특징
- TypeScript 타입 안전성
- 비동기 처리 (async/await)
- 에러 바운더리 연동
- 로딩 상태 관리
- 캐싱 및 최적화
