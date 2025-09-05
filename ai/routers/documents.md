# routers/documents.py - 문서 파싱 엔드포인트

## 역할
파일 업로드를 받아 Upstage Document Parser API를 통해 텍스트를 추출하는 API 엔드포인트를 제공합니다.

## 주요 기능

### 1. 파일 업로드 처리
- `multipart/form-data` 형식의 파일 업로드 지원
- PDF, DOCX, 이미지 등 다양한 문서 형식 처리
- 파일 크기 제한 (50MB) 및 검증

### 2. 문서 파싱 API 연동
- Upstage Document Parser 서비스 호출
- 비동기 처리로 성능 최적화
- 파싱 결과에서 텍스트 내용 추출

### 3. 오류 처리 및 검증
- 파일 존재 여부 검증
- 파일 크기 초과 시 HTTP 413 에러
- 파싱 실패 시 적절한 에러 메시지 반환
- 로깅을 통한 디버깅 지원

## API 엔드포인트

### POST /api/v1/documents/parse
**요청**
- Content-Type: multipart/form-data
- file: UploadFile (필수) - 파싱할 문서 파일

**응답**
- DocumentParseResponse 모델
- 성공 시: 추출된 텍스트 내용 반환
- 실패 시: 에러 메시지와 상태 코드

## 지원 파일 형식
- PDF 문서
- Microsoft Word (DOCX)
- 이미지 파일 (JPG, PNG 등)
- 텍스트 파일 (TXT, MD)

## 사용 예시
```bash
curl -X POST "http://localhost:4700/api/v1/documents/parse" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@portfolio.pdf"
```

## 응답 예시
```json
{
    "success": true,
    "message": "Document parsed successfully",
    "content": "추출된 포트폴리오 텍스트 내용..."
}
```

## 오류 처리
- 400: 파일이 제공되지 않음
- 413: 파일 크기 초과 (50MB)
- 500: 내부 서버 오류 (파싱 실패)

## 의존성
- DocumentParser 서비스 클래스
- FastAPI UploadFile
- DocumentParseResponse 모델
