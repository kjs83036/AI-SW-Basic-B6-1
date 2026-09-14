# 수동 검증 가이드

이 문서를 위에서 아래로 따라가면 모든 검증을 직접 재현할 수 있다.

---

## 0. 사전 준비

- **작업 폴더**: `E:\codyssey_claude\B6-1-2\output_클라우드환경에서웹서비스인프라구축`
- **실행 환경**: Python 3.x, matplotlib (`pip install matplotlib`)
- **AWS 환경**: IAM 사용자 로그인, 서울 리전(`ap-northeast-2`) 선택

---

## 1. 구현 실행 검증

### 1-1. 아키텍처 다이어그램 PDF 생성

- **목적**: `gen_architecture.py`가 PDF 제출 요건(`docs/architecture.pdf`)을 충족하는지 확인
- **실행**:
  ```bash
  cd output_클라우드환경에서웹서비스인프라구축
  python gen_architecture.py
  ```
- **기대 출력**:
  ```
  저장 완료: docs\architecture.pdf
  ```
- **확인 포인트**:
  - `docs/architecture.pdf` 파일 존재 (`ls docs/architecture.pdf`)
  - PDF 열었을 때 VPC·Subnet·IGW·EC2·SG 5종 박스 표시
  - `Internet → IGW → EC2` 화살표 및 포트 라벨 포함
  - 한글 텍스트 깨짐 없음(Malgun Gothic 폰트 적용)

### 1-2. 외부 접속 확인 (실제 배포 후)

- **목적**: EC2 Nginx에 외부 HTTP 접근 가능함을 확인
- **실행** (`docs/deployment-guide.md` 10단계 수행 후):
  ```bash
  curl -v http://<퍼블릭IP>/health
  ```
- **기대 출력**:
  ```
  < HTTP/1.1 200 OK
  < Server: nginx/...
  ```
- **확인 포인트**: HTTP 응답 수신, `Server: nginx` 헤더 포함

### 1-3. 인스턴스 내부 로컬 접속

- **목적**: Nginx가 정상 실행 중임을 EC2 내부에서 확인
- **실행** (SSH 접속 후):
  ```bash
  curl http://localhost
  ```
- **기대 출력**: Nginx 기본 페이지 HTML (200 OK)
- **확인 포인트**: 응답 본문에 `Welcome to nginx` 포함

---

## 2. 제약 충족 수동 확인

| PDF 제약 | 확인 방법 | 위치 |
|----------|---------|------|
| 서울 리전 `ap-northeast-2` | AWS 콘솔 상단 리전 확인 | 전 단계 |
| VPC `10.0.0.0/16` | VPC 콘솔 → CIDR 확인 | deployment-guide 2단계 |
| Public Subnet `10.0.1.0/24` | 서브넷 콘솔 → CIDR 확인 | deployment-guide 3단계 |
| RT `0.0.0.0/0 → IGW` | 라우팅 테이블 → 라우팅 탭 | deployment-guide 5단계 |
| HTTP 80 `0.0.0.0/0` | SG 인바운드 규칙 확인 | deployment-guide 6단계 |
| SSH 22 내 IP만 | SG 인바운드 규칙 소스 확인 | deployment-guide 6단계 |
| 전체포트 규칙 없음 | `grep "0-65535" gen_architecture.py` → 0건 | - |
| IAM AdministratorAccess 없음 | IAM → 사용자 → 권한 탭 확인 | deployment-guide 1단계 |
| t2/t3.micro | EC2 인스턴스 유형 확인 | deployment-guide 8단계 |
| EBS 8~10GiB | EC2 → 스토리지 탭 확인 | deployment-guide 8단계 |
| 키페어 1개 | EC2 → 키페어 목록 확인 | deployment-guide 7단계 |

---

## 3. 산출물 정합성 확인 (Step 9 결과 재현)

- [ ] `docs/architecture.pdf` 존재 + VPC/Subnet/IGW/EC2/SG 5종 포함
- [ ] `docs/access-result.md` 존재 + 접속 방식 명시
- [ ] `docs/troubleshooting.md` 존재 + 증상→원인→조치→결과 구조 1건 이상
- [ ] `docs/cleanup-checklist.md` 존재 + EC2/EBS/EIP/IGW/VPC/SG/키페어 항목 포함
- [ ] `docs/deployment-guide.md` 존재 + 모든 제약 사항 매핑
- [ ] `architecture.md` Mermaid 블록 포함
- [ ] `EXPLANATION.md` 함수별 "왜" 설명 + 제약-코드 매핑 표 포함
- [ ] `EXPLANATION.md` 선택과제 미수행 명시
- [ ] `README.md` 개요·실행법·파일목록·결과요약 포함
- [ ] 모든 산출물 한국어

---

## 4. codereview 결과 요약 (Step 6)

pal codereview를 `gen_architecture.py`에 대해 수행했다. 결과 요약:

| 지적 | 채택 여부 | 사유 |
|------|---------|------|
| 한글 폰트 누락(DejaVu Sans) | 채택 | `Malgun Gothic` 폰트로 수정, 한글 정상 렌더링 확인 |
| 하드코딩된 출력 경로 | 기각 | PDF §2.1 제출 구조(`docs/architecture.pdf`)가 고정 경로를 명시. 인자화 불필요 |
| `FancyArrowPatch` 미사용 임포트 | 채택 | 임포트 제거해 unused import 정리 |

> **사용자 확인 사항**: 위 지적 사항에 동의하지 않는 경우 `EXPLANATION.md` §제약-코드 매핑 표를 참조해 판단한다.

---

## 5. 종합 판정

아래 항목 전부 통과 시 과제 완료로 본다:

- [ ] `python gen_architecture.py` 실행 → `docs/architecture.pdf` 정상 생성
- [ ] PDF 포함 요소 5종 + 트래픽 흐름 육안 확인
- [ ] `docs/` 하위 제출 산출물 4종 모두 존재
- [ ] `docs/deployment-guide.md` 제약 전 항목 커버 확인
- [ ] 선택과제(HTTPS·Docker) 미수행 명시 확인
- [ ] 전체 산출물 한국어 확인
