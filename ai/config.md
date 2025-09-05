# config.py - 환경설정 중앙 관리

## 역할
애플리케이션의 모든 환경 설정을 중앙에서 관리하는 설정 모듈입니다. 환경변수를 타입 안전하게 로드하고 기본값을 제공합니다.

## 주요 기능

### 1. 환경변수 로드
- `python-dotenv`를 사용하여 `.env` 파일에서 환경변수 자동 로드
- 시스템 환경변수와 `.env` 파일 모두 지원

### 2. 타입 안전한 설정 클래스
- `@dataclass` 데코레이터로 타입 힌트가 있는 설정 클래스 정의
- 각 설정값에 대한 기본값 제공으로 안정성 확보

### 3. 설정 카테고리

#### Upstage API 연결 설정
- `upstage_api_key`: Upstage API 인증 키
- `upstage_base_url`: API 베이스 URL (기본: https://api.upstage.ai)
- `upstage_model`: 사용할 Solar LLM 모델명 (기본: solar-pro2)

#### 성능 최적화 설정
- `api_timeout`: API 호출 타임아웃 (기본: 30초)
- `max_text_length`: 텍스트 최대 길이 제한 (기본: 2000자)
- `max_output_tokens`: LLM 출력 토큰 최대 개수 (기본: 6500)
- `rate_limit_interval`: API 호출 간격 제어 (기본: 1.0초)

### 4. 전역 설정 인스턴스
- `settings` 객체를 통해 애플리케이션 전체에서 설정값 접근 가능
- 싱글톤 패턴으로 일관된 설정 보장

## 사용 예시
```python
from config import settings

# API 키 사용
headers = {"Authorization": f"Bearer {settings.upstage_api_key}"}

# 타임아웃 설정
async with httpx.AsyncClient(timeout=settings.api_timeout) as client:
    response = await client.post(url, data=data)
```

## 환경변수 파일 (.env)
```
UPSTAGE_API_KEY=your_actual_api_key_here
UPSTAGE_MODEL=solar-pro2
API_TIMEOUT=30
MAX_TEXT_LENGTH=2000
MAX_OUTPUT_TOKENS=6500
RATE_LIMIT_INTERVAL=1.0
```
