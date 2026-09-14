# 클라우드 환경에서 웹 서비스 인프라 구축

## 개요

AWS 프리 티어 범위 내에서 서울 리전(`ap-northeast-2`)에 VPC·Public Subnet·Internet Gateway·EC2(Nginx) 인프라를 구성하고, 외부 HTTP 접속이 가능한 웹 서비스를 배포하는 실습 과제다. IAM 최소 권한과 보안 그룹 최소 허용을 준수하며, 실습 후 모든 리소스를 정리한다.

---

## 실행 방법

### 아키텍처 다이어그램 PDF 생성

```bash
cd output_클라우드환경에서웹서비스인프라구축
python gen_architecture.py
# → docs/architecture.pdf 생성
```

> **사전 요건**: `pip install matplotlib`

### 실제 AWS 배포

`docs/deployment-guide.md`를 위에서 아래로 순서대로 수행한다.

---

## 파일 목록

| 파일 | 설명 |
|------|------|
| `gen_architecture.py` | 아키텍처 다이어그램 PDF 생성 스크립트 |
| `docs/architecture.pdf` | 아키텍처 다이어그램 (VPC/Subnet/IGW/EC2/SG + 트래픽 흐름) |
| `docs/access-result.md` | 웹 서비스 외부 접속 증거 (배포 후 채울 것) |
| `docs/troubleshooting.md` | 트러블슈팅 보고서 3건 |
| `docs/cleanup-checklist.md` | 리소스 정리 체크리스트 |
| `docs/deployment-guide.md` | 실제 AWS 배포 수행 가이드 (제약 전 항목 포함) |
| `architecture.md` | Mermaid 구조도 (인프라 흐름) |
| `EXPLANATION.md` | 코드리뷰 수준 통합 설명 |
| `MANUAL_VERIFICATION.md` | 수동 검증 가이드 |
| `README.md` | 본 문서 |

---

## 결과 요약

- `gen_architecture.py` 실행 → `docs/architecture.pdf` 39KB 정상 생성 (VPC/Subnet/IGW/EC2/SG 5종 + 트래픽 흐름 포함)
- `docs/` 하위 제출 산출물 4종 생성 완료 (아키텍처·접속증거·트러블슈팅·정리체크리스트)
- `docs/deployment-guide.md`에 모든 제약(IAM·SG·리전·리소스 규격) 매핑 포함
- 보너스 과제(HTTPS, Docker) 미수행
