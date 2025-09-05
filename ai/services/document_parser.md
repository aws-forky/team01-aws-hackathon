# services/document_parser.py - Upstage 문서파싱 연동

## 역할
Upstage Document Parser API와 연동하여 다양한 형식의 문서에서 텍스트를 추출하는 핵심 비즈니스 로직을 담당합니다.

## 주요 기능

### 1. Upstage API 연동
- Document Parser API 호출 및 응답 처리
- Bearer 토큰 기반 인증 처리
- multipart/form-data 형식으로 파일 전송
- 비동기 HTTP 클라이언트 (httpx) 사용

### 2. 다양한 문서 형식 지원
- PDF 문서 파싱
- Microsoft Word (DOCX) 처리
- 이미지 파일 (JPG, PNG 등) OCR 처리
- 텍스트 파일 (TXT, MD, JSON) 직접 처리

### 3. 견고한 오류 처리
- API 호출 실패 시 폴백 처리
- 네트워크 타임아웃 관리 (60초)
- 파싱 결과 검증 및 후처리
- 상세한 로깅으로 디버깅 지원

### 4. 응답 데이터 처리
- API 응답에서 HTML 콘텐츠 추출
- 중첩된 JSON 구조 탐색
- 원시 JSON 응답 감지 및 폴백 처리
- 텍스트 품질 검증

## 클래스 구조

### DocumentParser
메인 문서 파싱 클래스

#### 주요 메서드
- `parse_document(file_content, filename)`: 메인 파싱 메서드
- `_extract_content(result)`: API 응답에서 콘텐츠 추출
- `_fallback_extraction(file_content, filename)`: 폴백 처리

## 처리 과정
1. **파일 검증**: 파일 존재 및 형식 확인
2. **API 호출**: Upstage Document Parser 요청
3. **응답 처리**: JSON 응답에서 HTML 콘텐츠 추출
4. **품질 검증**: 추출된 텍스트 품질 확인
5. **폴백 처리**: API 실패 시 대안 처리

## 폴백 시스템
API 실패 시 다음과 같은 폴백 처리:
- TXT/MD 파일: UTF-8 디코딩
- JSON 파일: 구조화된 텍스트 변환
- 기타 파일: 텍스트 추출 시도
- 최소 길이 검증 (10자 이상)

## 설정 및 환경변수
- `UPSTAGE_API_KEY`: API 인증 키
- `UPSTAGE_BASE_URL`: API 베이스 URL
- API 타임아웃: 60초 (고정)

## 사용 예시
```python
parser = DocumentParser()
content = await parser.parse_document(file_bytes, "portfolio.pdf")
```

## 오류 처리
- 네트워크 오류: 폴백 처리로 전환
- 인증 실패: 로그 기록 후 폴백
- 파싱 실패: 파일 형식별 대안 처리
- 빈 결과: ValueError 발생

## 로깅
- 파싱 실패 시 상세 오류 로그
- 폴백 사용 시 경고 로그
- API 응답 상태 추적

## 의존성
- httpx: 비동기 HTTP 클라이언트
- json: JSON 데이터 처리
- logging: 로깅 시스템
- config: 환경설정 관리
