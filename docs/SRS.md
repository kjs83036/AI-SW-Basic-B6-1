# 소프트웨어 요구사항 명세서 (SRS: B6-1 클라우드 웹 서비스 인프라 구축)

## 1. 개요
본 문서는 **B6-1 클라우드 환경에서 웹 서비스 인프라 구축** 과제에 대한 세부 요구사항 명세서이다. AWS 기반 격리 네트워크 구성, 컴퓨팅/웹 서버 프로비저닝, 보안그룹/IAM 접근제어 적용 및 검증을 목표로 한다.

## 2. 기능 요구사항 (Functional Requirements)

| 요구사항 ID | 항목 | 상세 설명 |
| :--- | :--- | :--- |
| **FR-61-01** | VPC 네트워크 구성 | AWS 서울 리전(`ap-northeast-2`) 내 VPC 1개, Public Subnet 1개, Internet Gateway 연결 |
| **FR-61-02** | 라우팅 테이블 설정 | Route Table에 `0.0.0.0/0 → Internet Gateway` 경로를 설정하여 인터넷 연결 보장 |
| **FR-61-03** | EC2 및 웹서버 | Public Subnet 내 EC2 1대(t2.micro/t3.micro, Ubuntu/Amazon Linux, 8~10GiB EBS) 배포 및 Nginx 설치 (`curl http://localhost` 200 OK 응답) |
| **FR-61-04** | 접근 제어 (SG) | HTTP(80) `0.0.0.0/0` 허용, SSH(22) 개인 IP만 허용, `0.0.0.0/0` 대상 전체 포트 허용 규칙 금지 |
| **FR-61-05** | 최소 권한 IAM | 루트 계정 미사용, 필수 최소 권한을 가진 IAM 사용자 생성 (Admin 권한 금지) |
| **FR-61-06** | 산출물 및 정리 | - 아키텍처 다이어그램 (`docs/architecture.pdf`)<br>- 외부 접속 증거 (`docs/access-result.md`)<br>- 트러블슈팅 보고서 (`docs/troubleshooting.md`)<br>- 리소스 정리 체크리스트 (`docs/cleanup-checklist.md`) |

## 3. 제약사항 및 개발 환경
- **환경**: AWS 프리 티어 범위 준수, ap-northeast-2 리전
- **정리**: 실습 종료 후 자원 즉시 삭제 및 Billing 대시보드 검증
