# AWS Deployment

## 역할
AWS 클라우드 환경에서의 Forky 배포 및 인프라 관리를 담당합니다.

## AWS 서비스 구성

### 1. Compute Services
- **ECS Fargate**: 컨테이너 오케스트레이션
- **Application Load Balancer**: 트래픽 분산
- **Auto Scaling**: 자동 확장/축소
- **CloudWatch**: 모니터링 및 로깅

### 2. Storage Services
- **S3**: 정적 파일 저장 (업로드된 PDF)
- **CloudFront**: CDN 및 캐싱
- **EFS**: 공유 파일 시스템 (선택사항)

### 3. Security Services
- **IAM**: 권한 관리
- **Secrets Manager**: API 키 보안 저장
- **WAF**: 웹 애플리케이션 방화벽
- **Certificate Manager**: SSL/TLS 인증서

### 4. Networking
- **VPC**: 가상 프라이빗 클라우드
- **Subnets**: 퍼블릭/프라이빗 서브넷
- **Security Groups**: 방화벽 규칙
- **Route 53**: DNS 관리

## 배포 아키텍처

### High Availability 구성
```
Internet → CloudFront → ALB → ECS Fargate (Multi-AZ)
                              ↓
                         S3 (File Storage)
```

### 보안 구성
- 프라이빗 서브넷에 백엔드 배치
- 퍼블릭 서브넷에 로드 밸런서 배치
- API 키는 Secrets Manager에서 관리
- WAF로 악성 트래픽 차단

## CI/CD 파이프라인

### GitHub Actions
- 코드 푸시 시 자동 빌드
- Docker 이미지 ECR 푸시
- ECS 서비스 자동 업데이트
- 테스트 자동 실행

### 배포 전략
- Blue-Green 배포
- 롤링 업데이트
- 헬스체크 기반 트래픽 전환
- 롤백 자동화

## 모니터링 및 알림
- CloudWatch 메트릭 수집
- 로그 중앙화 관리
- 에러 알림 설정
- 성능 대시보드
