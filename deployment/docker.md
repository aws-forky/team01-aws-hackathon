# Docker Configuration

## 역할
Forky 애플리케이션의 컨테이너화 및 배포 설정을 관리합니다.

## 컨테이너 구성

### 1. Backend Container
- Base Image: python:3.11-slim
- FastAPI 애플리케이션 실행
- 의존성 설치 및 환경 설정
- 포트 8000 노출

### 2. Frontend Container
- Base Image: node:18-alpine
- React 애플리케이션 빌드 및 서빙
- Nginx 정적 파일 서버
- 포트 80 노출

### 3. Nginx Container
- 리버스 프록시 설정
- SSL 터미네이션
- 정적 파일 서빙
- 로드 밸런싱

## Docker Compose 구성

### 서비스 정의
- `backend`: FastAPI 서버
- `frontend`: React 애플리케이션
- `nginx`: 리버스 프록시
- `redis`: 캐싱 (선택사항)

### 네트워크 설정
- 내부 네트워크로 서비스 간 통신
- 외부 포트 노출 최소화
- 보안 그룹 설정

### 볼륨 마운트
- 로그 파일 영구 저장
- 설정 파일 외부 관리
- 업로드 파일 임시 저장

## 환경별 설정

### Development
- 핫 리로드 지원
- 디버그 모드 활성화
- 로컬 볼륨 마운트

### Production
- 최적화된 빌드
- 보안 설정 강화
- 헬스체크 설정
- 자동 재시작 정책

## 배포 스크립트
- 빌드 자동화
- 환경 변수 설정
- 컨테이너 오케스트레이션
- 롤링 업데이트
