# Forky 프로젝트 AWS 서비스 활용 방안

## 현재 프로젝트 특성 분석

- **AI 기반 포트폴리오 분석 서비스**
- **PDF 처리 및 텍스트 추출**
- **실시간 면접 시뮬레이션**
- **사용자 데이터 저장 및 관리**

## 추천 AWS 서비스

### 1. 컴퓨팅 & 배포

#### **Amazon ECS (Elastic Container Service)** ⭐⭐⭐
```yaml
용도: Docker 컨테이너 기반 배포
장점:
  - FastAPI + React 앱을 컨테이너로 쉽게 배포
  - 자동 스케일링
  - 로드 밸런싱 내장
비용: 사용한 리소스만 과금
```

#### **AWS Lambda** ⭐⭐⭐
```yaml
용도: 서버리스 PDF 처리
장점:
  - PDF 업로드 시에만 실행 (비용 절약)
  - 자동 스케일링
  - 콜드 스타트 최소화
적용: PDF 전처리, 키워드 후처리
```

#### **Amazon EC2** ⭐⭐
```yaml
용도: 전통적인 서버 배포
장점: 완전한 제어권
단점: 관리 부담, 24시간 과금
```

### 2. 스토리지 & 파일 관리

#### **Amazon S3** ⭐⭐⭐
```yaml
용도: PDF 파일 및 결과 저장
기능:
  - 업로드된 PDF 파일 저장
  - 생성된 면접 결과 PDF 저장
  - 정적 웹사이트 호스팅 (React 앱)
  - CloudFront와 연동으로 CDN 구성
비용: 매우 저렴 (GB당 $0.023)
```

#### **Amazon EFS (Elastic File System)** ⭐
```yaml
용도: 컨테이너 간 파일 공유
적용: 여러 ECS 태스크 간 임시 파일 공유
```

### 3. 데이터베이스

#### **Amazon DynamoDB** ⭐⭐⭐
```yaml
용도: 사용자 세션 및 결과 저장
장점:
  - 서버리스, 자동 스케일링
  - 빠른 응답 속도
  - 사용량 기반 과금
데이터:
  - 사용자 세션 정보
  - 면접 결과 히스토리
  - 키워드 분석 결과
```

#### **Amazon RDS** ⭐⭐
```yaml
용도: 관계형 데이터 저장
적용: 복잡한 쿼리가 필요한 경우
단점: 24시간 과금
```

### 4. AI/ML 서비스

#### **Amazon Textract** ⭐⭐⭐
```yaml
용도: PDF 텍스트 추출 (현재 외부 API 대체)
장점:
  - 높은 정확도
  - 표, 양식 인식 가능
  - AWS 네이티브 통합
비용: 페이지당 과금
```

#### **Amazon Comprehend** ⭐⭐
```yaml
용도: 키워드 추출 및 감정 분석
기능:
  - 핵심 구문 추출
  - 기술 용어 식별
  - 텍스트 분류
```

#### **Amazon Bedrock** ⭐⭐⭐
```yaml
용도: 면접 질문 생성 (현재 외부 API 대체)
장점:
  - Claude, Llama 등 다양한 모델
  - AWS 네이티브 통합
  - 보안 및 컴플라이언스
```

### 5. API & 통합

#### **Amazon API Gateway** ⭐⭐⭐
```yaml
용도: API 관리 및 보안
기능:
  - API 키 관리
  - 요청 제한 (Rate Limiting)
  - CORS 설정
  - 모니터링 및 로깅
```

#### **AWS AppSync** ⭐⭐
```yaml
용도: GraphQL API (실시간 기능)
적용: 실시간 면접 진행 상황 업데이트
```

### 6. 보안 & 인증

#### **Amazon Cognito** ⭐⭐⭐
```yaml
용도: 사용자 인증 및 관리
기능:
  - 회원가입/로그인
  - 소셜 로그인 (Google, GitHub)
  - JWT 토큰 관리
  - 사용자 프로필 저장
```

#### **AWS Secrets Manager** ⭐⭐
```yaml
용도: API 키 및 민감 정보 관리
적용: 외부 API 키 안전한 저장
```

### 7. 모니터링 & 로깅

#### **Amazon CloudWatch** ⭐⭐⭐
```yaml
용도: 애플리케이션 모니터링
기능:
  - 로그 수집 및 분석
  - 메트릭 모니터링
  - 알람 설정
  - 대시보드 구성
```

#### **AWS X-Ray** ⭐⭐
```yaml
용도: 분산 추적 및 성능 분석
적용: API 호출 체인 추적
```

### 8. 콘텐츠 전송

#### **Amazon CloudFront** ⭐⭐⭐
```yaml
용도: CDN (Content Delivery Network)
기능:
  - React 앱 전역 배포
  - 빠른 로딩 속도
  - DDoS 보호
```

## 권장 아키텍처

### 최소 비용 구성 (스타트업)
```yaml
Frontend: S3 + CloudFront
Backend: Lambda + API Gateway
Database: DynamoDB
AI: Bedrock (또는 기존 외부 API 유지)
Storage: S3
Monitoring: CloudWatch (기본)
```

### 확장 가능한 구성 (성장 단계)
```yaml
Frontend: S3 + CloudFront
Backend: ECS Fargate + ALB
Database: DynamoDB + RDS (필요시)
AI: Textract + Bedrock
Storage: S3
Auth: Cognito
Monitoring: CloudWatch + X-Ray
```

### 엔터프라이즈 구성 (대규모)
```yaml
Frontend: S3 + CloudFront + WAF
Backend: EKS + ALB
Database: Aurora Serverless + DynamoDB
AI: SageMaker + Bedrock
Storage: S3 + EFS
Auth: Cognito + IAM
Monitoring: CloudWatch + X-Ray + Config
```

## 비용 예상 (월 기준)

### 최소 구성 (1000 사용자/월)
- S3: $5
- Lambda: $10
- DynamoDB: $15
- API Gateway: $10
- CloudFront: $5
- **총합: ~$45/월**

### 확장 구성 (10000 사용자/월)
- ECS Fargate: $50
- S3: $20
- DynamoDB: $50
- RDS: $30
- CloudFront: $15
- **총합: ~$165/월**

## 구현 우선순위

### Phase 1 (즉시 적용 가능)
1. **S3** - 파일 저장 및 정적 호스팅
2. **CloudFront** - CDN 구성
3. **CloudWatch** - 기본 모니터링

### Phase 2 (단기)
1. **ECS** - 컨테이너 배포
2. **DynamoDB** - 사용자 데이터 저장
3. **API Gateway** - API 관리

### Phase 3 (중장기)
1. **Cognito** - 사용자 인증
2. **Textract** - PDF 처리 개선
3. **Bedrock** - AI 모델 통합

## 결론

**가장 추천하는 서비스들:**
1. **S3 + CloudFront** - 정적 호스팅 및 CDN
2. **ECS Fargate** - 컨테이너 기반 배포
3. **DynamoDB** - 사용자 데이터 저장
4. **CloudWatch** - 모니터링
5. **Cognito** - 사용자 인증 (향후)

이 구성으로 시작하면 비용 효율적이면서도 확장 가능한 아키텍처를 구축할 수 있습니다.