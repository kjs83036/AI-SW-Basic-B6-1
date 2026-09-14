# 통합 설명

## 과제 요약

AWS 서울 리전(`ap-northeast-2`)에서 프리 티어 범위 내 VPC·Public Subnet·Internet Gateway·EC2(Nginx)를 구성하고, 외부에서 HTTP로 접근 가능한 웹 서비스 인프라를 구축하는 실습 과제다. IAM 최소 권한 원칙과 보안 그룹 최소 허용 원칙을 준수해야 하며, 실습 완료 후 모든 리소스를 정리해 과금을 방지해야 한다. 최종 산출물은 아키텍처 다이어그램·외부 접속 증거·트러블슈팅 보고서·리소스 정리 체크리스트 4종이다.

---

## 선택과제 처리

선택과제 미수행. (PDF 명시 항목: 보너스 1 — HTTPS 적용, 보너스 2 — Docker 컨테이너 웹 서비스)

---

## 파일별 설명

### gen_architecture.py

#### 전체 설계 의도

PDF §2.1이 `docs/architecture.pdf`를 이미지(PNG) 또는 PDF로 제출하도록 명시했다. `draw.io`·AWS 콘솔 다운로드 같은 GUI 도구는 자동화가 불가능하므로, **matplotlib**으로 코드에서 직접 PDF를 생성하는 방식을 선택했다. 단일 파일(`gen_architecture.py`)로 유지해 의존성을 최소화했다.

대안으로 `reportlab`만으로 박스를 그리는 방식도 가능했으나, matplotlib의 `FancyBboxPatch` + `annotate`가 아키텍처 박스·화살표 표현에 더 직관적이어서 선택했다.

#### 함수: `draw_vpc(ax)`
- **역할**: VPC 외곽 박스(`10.0.0.0/16`)와 레이블을 그린다.
- **왜 이렇게 짰는가**: 가장 바깥 컨테이너를 먼저 그려야 Subnet·EC2 등 내부 요소가 시각적으로 중첩되게 표시된다. zorder=1로 설정해 내부 요소가 위에 렌더링되도록 했다.
- **대안 검토**: 단일 함수에 전부 넣을 수 있었으나, 구성 요소별 함수 분리가 수정 시 영향 범위를 좁혀 가독성에 유리했다.
- **충족하는 제약**: PDF §2.1 "VPC 구성 요소 포함" → `draw_vpc`에서 VPC 박스 표시

#### 함수: `draw_components(ax)`
- **역할**: Public Subnet, Security Group(점선), EC2(Nginx), Internet Gateway를 그린다.
- **왜 이렇게 짰는가**: SG를 별도 박스로 그리지 않고 EC2를 감싸는 점선 박스로 표현해, SG가 EC2 인스턴스에 연결된 논리적 관계를 직관적으로 나타냈다. SG 박스 내부에 인바운드 규칙(`HTTP 80: 0.0.0.0/0`, `SSH 22: 내 IP만`)을 텍스트로 표기해 다이어그램 하나로 보안 구성을 확인할 수 있도록 했다.
- **대안 검토**: SG를 범례로만 표기하는 방식도 있었으나, PDF 요구사항이 "Security Group 구성 요소 포함"을 명시해 시각적 표현이 적절했다.
- **충족하는 제약**: PDF §2.1 "VPC, Subnet, Internet Gateway, EC2, Security Group 구성 요소 포함"

#### 함수: `draw_traffic_flow(ax)`
- **역할**: `Internet → IGW → EC2` 트래픽 흐름 화살표와 Internet 노드를 그린다.
- **왜 이렇게 짰는가**: PDF §2.1이 "외부 → 서비스 트래픽 흐름 포함"을 명시했다. `ax.annotate`를 사용해 화살표 방향과 라벨(포트 번호, 라우팅 표기)을 함께 표시했다.
- **충족하는 제약**: PDF §2.1 "외부 → 서비스 트래픽 흐름 포함"

#### 함수: `main()`
- **역할**: 세 draw 함수를 호출하고 `docs/architecture.pdf`로 저장한다.
- **왜 이렇게 짰는가**: 출력 경로를 `docs/architecture.pdf`로 고정해 PDF §2.1 제출 구조(`docs/architecture.pdf`)와 1:1 매핑했다. `os.makedirs("docs", exist_ok=True)`로 폴더 선생성해 실행 순서 의존성을 제거했다.
- **충족하는 제약**: PDF §2.1 제출 구조 `docs/architecture.pdf`

---

## 제약-코드 매핑 표

| PDF 제약 | 충족 위치 |
|----------|---------|
| `docs/architecture.pdf` 제출 — VPC/Subnet/IGW/EC2/SG + 트래픽 흐름 | `gen_architecture.py` `draw_vpc` `draw_components` `draw_traffic_flow` |
| `docs/access-result.md` — 외부 접속 증거(방식 A 또는 B) | `docs/access-result.md` |
| `docs/troubleshooting.md` — 증상→원인→조치→결과 구조 1건 이상 | `docs/troubleshooting.md` (3건) |
| `docs/cleanup-checklist.md` — 리소스 정리 증명 | `docs/cleanup-checklist.md` |
| 서울 리전 `ap-northeast-2` | `docs/deployment-guide.md` 사전준비/전 단계 |
| VPC 1개 / Public Subnet 1개 | `docs/deployment-guide.md` 2단계·3단계 |
| IGW VPC 연결 | `docs/deployment-guide.md` 4단계 |
| Route Table `0.0.0.0/0 → IGW` | `docs/deployment-guide.md` 5단계 |
| EC2 프리 티어(t2/t3.micro), EBS 8~10GiB, 키페어 1개 | `docs/deployment-guide.md` 7단계·8단계 |
| Nginx 설치·실행, `curl localhost` 200 | `docs/deployment-guide.md` 9단계 |
| SG HTTP 80: `0.0.0.0/0` | `docs/deployment-guide.md` 6단계 / `gen_architecture.py:draw_components` |
| SG SSH 22: 내 IP만 | `docs/deployment-guide.md` 6단계 |
| 전체 포트(0-65535) 허용 규칙 금지 | `docs/deployment-guide.md` 6단계 주의 사항 |
| IAM 최소 권한(EC2+VPC만), AdministratorAccess 금지 | `docs/deployment-guide.md` 1단계 |
| 루트 계정 미사용 | `docs/deployment-guide.md` 1단계·사전준비 |
| 프리 티어 범위 내 | `docs/deployment-guide.md` 사전준비·8단계 |
| 실습 후 리소스 전부 정리 | `docs/cleanup-checklist.md` |

---

## 검증 결과

### gen_architecture.py 실행 검증

```
$ python gen_architecture.py
저장 완료: docs\architecture.pdf
```

- `docs/architecture.pdf` 39KB 생성 확인
- 필수 요소 5종(VPC·Subnet·IGW·EC2·SG) 박스 포함 ✅
- `Internet → IGW → EC2` 트래픽 흐름 화살표 포함 ✅
- Malgun Gothic 폰트 적용 → 한글 정상 렌더링 ✅

### pal codereview 결과

pal codereview 실패 없이 정상 수행됨. (상세 내용은 `MANUAL_VERIFICATION.md` §4 참조)

---

## 비고

실제 AWS 접속 스크린샷/퍼블릭 IP는 환경상 생성 불가 → `docs/access-result.md`에 플레이스홀더(`<퍼블릭IP>`) 처리. `docs/deployment-guide.md`의 단계별 가이드를 따라 실제 배포 후 해당 파일을 채운다.
