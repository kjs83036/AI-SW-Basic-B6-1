# B6-1 클라우드 웹 서비스 인프라 구축: CS 이론 및 실무 개념 학습 가이드

- **대상 과제**: AI/SW Basic — B6-1 클라우드 환경에서 웹 서비스 인프라 구축
- **위치**: `codyssey/antigravity/b6-1-2/`
- **목적**: 단순 AWS 조작(ClickOps)을 넘어, 인프라 배포 이면에 작동하는 핵심 CS 이론 및 실무 엔지니어링 원리 체화

---

## 1. 과제 성격 및 학습 방향성 (단일 개념형 vs 실무/통합형)

Codyssey / Antigravity 과정 내 과제들은 크게 **단일 개념 중심 과제**와 **실무/통합형 과제**로 구분됩니다.

| 구분 | 단일 개념 중심 과제<br>(1-1 리눅스, 2-1 파이썬, 3-1 자료구조, 5-1 DB) | 실무/통합형 과제<br>(4-1 웹 포트폴리오, 6-1 클라우드 인프라) |
| :--- | :--- | :--- |
| **핵심 목적** | 특정 기술 영역의 문법, 알고리즘 복잡도, 관계형 모델을 깊이 이해하고 정해진 입출력(단위 테스트) 만족 | 여러 단위 기술을 융합하여 **실제 외부에 노출되어 동작하는 완전한 라이브 시스템** 구축 |
| **동작 환경** | 로컬 샌드박스, 인메모리(In-Memory), 단일 프로세스/단일 파일 | 퍼블릭 인터넷, 브라우저 DOM, 외부 API, 클라우드 가상 머신(AWS Linux) |
| **평가 기준** | 코드의 정확성, 시간/공간 복잡도, 쿼리 정규화 | 아키텍처 정합성, 네트워크 패킷 흐름, 장애 해결(트러블슈팅), 운영/자원 수명주기 |

### 4-1(프론트엔드 실무)과 6-1(인프라 실무)의 구조적 대응

- **4-1 (클라이언트 실무 흐름)**: 사용자 이벤트 → DOM 조작 및 상태 갱신 → 외부 GitHub API 비동기 통신(로딩/성공/에러) → 반응형 UI 렌더링
- **6-1 (인프라 실무 흐름)**: VPC 네트워크 격리 → 서브넷/IGW 라우팅 → EC2/Nginx 웹 서버 프로비저닝 → 보안 그룹 방화벽 제어 → 외부 HTTP 검증 및 자원 정리

> 💡 **학습 핵심 포인트**:  
> 4-1 과제에서 단순 화면 구현보다 '이벤트-상태 흐름, 기술 선택 이유'가 중요하게 평가되듯, 6-1 과제 역시 단순 AWS 콘솔 클릭이 아니라 **"왜 이렇게 설정해야 정상 통신이 되는가"에 대한 CS 이론적 백그라운드**를 설명할 수 있어야 합니다.

---

## 2. 필수 컴퓨터 사이언스(CS) 핵심 이론

### ① 네트워크 계층 및 패킷 전달 (OSI 7 Layer & TCP/IP)

1. **L3 (네트워크 계층) - CIDR 및 서브넷팅 (Subnetting)**
   - **CIDR (Classless Inter-Domain Routing)**: 클래스(A/B/C) 기반 주소 낭비를 극복하기 위해 접두사 비트 길이(Prefix)로 네트워크/호스트를 분할합니다.
   - **서브넷 마스크 연산**: VPC 대역(`10.0.0.0/16`)은 앞 16비트가 네트워크 ID($2^{16} = 65,536$개 IP), Public Subnet(`10.0.1.0/24`)은 앞 24비트가 네트워크 ID($2^8 = 256$개 IP)로 논리적 망을 격리합니다.
   - **AWS 예약 IP 5개**: 각 서브넷의 `.0`(네트워크), `.1`(VPC 라우터), `.2`(DNS), `.3`(미래 예약), `.255`(브로드캐스트)는 AWS가 시스템용으로 예약하여 호스트에 할당 불가합니다.

2. **L4 (전송 계층) - TCP 3-Way Handshake & 포트(Port)**
   - 클라이언트와 Nginx 웹 서버 간 연결 수립 시 `SYN → SYN-ACK → ACK` 핸드셰이크를 거칩니다.
   - 포트 번호(HTTP 80, SSH 22)를 통해 운영체제 커널이 해당 목적지 소켓(Socket)을 사용하는 프로세스를 식별합니다.

3. **L7 (응용 계층) - HTTP 프로토콜**
   - 무상태성(Stateless)과 요청/응답 헤더 구조, HTTP 상태 코드(`200 OK`), `Server: nginx` 헤더 및 Keep-Alive 지속 연결 메커니즘을 이해합니다.

### ② 주소 변환 및 라우팅 (NAT & Routing Table)

1. **사설 IP (RFC 1918) vs 공인 IP (Public IP)**
   - 인터넷에서 직접 라우팅되지 않는 사설 IP 대역(`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`)을 내부망에 사용하고, 외부 통신 시 공인 IP와 매핑합니다.

2. **Internet Gateway(IGW)의 1:1 양방향 정적 NAT**
   - IGW는 단순한 라우터가 아니라, 퍼블릭 서브넷 인스턴스의 사설 IP와 공인 IP 간 주소 변환을 실시간으로 수행하는 1:1 양방향 정적 NAT 게이트웨이 역할을 합니다.

3. **디폴트 라우트(`0.0.0.0/0`) 및 최장 접두사 일치(LPM)**
   - 라우터는 패킷 전송 시 가장 구체적인(서브넷 마스크가 긴) 경로를 우선 선택하며, 로컬 VPC 대역 외의 모든 외부 인터넷 트래픽은 기본 경로인 `0.0.0.0/0 → IGW`를 통해 나갑니다.

### ③ 운영체제 및 웹 서버 아키텍처 (OS & Web Server)

1. **Nginx의 이벤트 기반 비동기 Non-blocking I/O**
   - Apache(프로세스/스레드 생성 모델)와 달리 Nginx는 단일 워커 프로세스 내에서 리눅스 `epoll` 시스템 콜을 이용한 이벤트 루프로 수만 개의 동시 접속을 효율적으로 처리합니다 (C10K 문제 해결).

2. **리눅스 서비스 관리 (systemd & daemon)**
   - 백그라운드 데몬 프로세스 제어(`systemctl start nginx`), 부팅 시 자동 시작 등록(`systemctl enable nginx`), 서비스 상태 추적(`systemctl status nginx`) 원리를 다룹니다.

3. **루프백 인터페이스 vs NIC 바인딩**
   - `curl http://localhost` (`127.0.0.1`)는 외부 네트워크 카드를 거치지 않고 OS 내부 루프백 인터페이스를 통해 웹 서버 데몬의 자체 동작 상태를 즉시 검증하는 방식입니다.

### ④ 암호학 및 인증 (Cryptography & SSH)

1. **비대칭키 암호화(RSA) 기반 SSH 핸드셰이크**
   - 서버에는 공개키(`authorized_keys`), 로컬 클라이언트에는 비밀키(`infra-keypair.pem`)를 보관하며, 비밀번호 전송 없이 전자서명 검증(Challenge-Response)을 통해 인증합니다.

2. **POSIX 파일 권한 및 보안 검증**
   - `chmod 400 infra-keypair.pem`(소유자 읽기 전용)을 설정하지 않으면 OpenSSH 클라이언트가 키 유출 위험으로 간주하고 연결을 강제 차단합니다.

---

## 3. 실무적 엔지니어링 개념 및 아키텍처 원칙

### ① 최소 권한 원칙(PoLP) 및 공격 표면(Attack Surface) 제어

- **최소 권한 원칙 (PoLP: Principle of Least Privilege)**:
  - 루트 계정을 봉인하고, 관리자 전체 권한(`AdministratorAccess`, `Action: *`) 대신 과제에 필요한 세부 권한(`AmazonEC2FullAccess`, `AmazonVPCFullAccess`)만 가진 IAM 사용자를 분리 생성합니다.
- **공격 표면 및 폭발 반경(Blast Radius) 축소**:
  - 65,535개 전체 포트 개방을 금지하고 웹 트래픽(HTTP 80)만 개방(`0.0.0.0/0`)하며, 관리용 SSH(22)는 관리자 공인 IP(`/32`)로 엄격히 제한하여 포트 스캐닝 및 Brute-force 공격을 차단합니다.
- **보안 그룹(Stateful) vs NACL(Stateless)**:
  - **보안 그룹**: 인스턴스(ENI) 레벨 방화벽, 상태 저장(Stateful) 방식으로 인바운드 허용 시 아웃바운드 응답 자동 통과, Allow 규칙만 지원.
  - **NACL**: 서브넷 레벨 방화벽, 상태 비저장(Stateless) 방식으로 인바운드/아웃바운드 규칙 각각 필요, Allow 및 Deny 규칙 순차 평가.

### ② 고가용성(High Availability) 및 SPOF 리스크

- **단일 실패 지점 (SPOF: Single Point of Failure)**:
  - 단일 AZ(`ap-northeast-2a`) 및 단일 EC2 구성은 데이터센터 장애 시 서비스 전체 중단을 유발합니다.
- **Multi-AZ 아키텍처 트레이드오프**:
  - 실무에서는 2개 이상의 AZ에 서브넷을 이중화하고 상단에 ALB(Application Load Balancer)를 배치하여 고가용성($SLA = 1 - (1-0.995)^2 = 99.9975\%$)을 확보합니다.

### ③ 클라우드 FinOps 및 유휴 자원(Zombie Resource) 관리

- **유휴 비용 누수 방지**:
  - EC2 인스턴스를 중지(Stopped)해도 연결된 EBS 볼륨 스토리지는 지속 과금되며, 인스턴스에 연결되지 않은 탄력적 IP(EIP)는 시간당 페널티 요금이 부과됩니다.
- **종속성 기반 리소스 정리 순서**:
  $$\text{EC2 종료} \rightarrow \text{EBS 삭제 / EIP 릴리스} \rightarrow \text{IGW Detach 및 삭제} \rightarrow \text{Subnet / RT 삭제} \rightarrow \text{SG / VPC 삭제}$$

### ④ 체계적인 6단계 트러블슈팅 프레임워크

$$\text{증상(Symptom)} \rightarrow \text{원인 가설(Hypothesis)} \rightarrow \text{검증(Verification)} \rightarrow \text{조치(Mitigation)} \rightarrow \text{결과(Result)} \rightarrow \text{재발 방지(Action Items)}$$

- **실무 빈출 트러블슈팅 사례**:
  1. **SSH Connection Timeout**: 보안 그룹 22번 소스 IP 불일치, 퍼블릭 IP 할당 누락, 서브넷 라우팅 테이블 누락.
  2. **Web Request Timeout**: 보안 그룹 80번 규칙 누락, IGW Detached 상태, Nginx 데몬 미실행.
  3. **IAM AccessDenied**: VPC 생성 시 `AmazonVPCFullAccess` 누락.

---

## 4. 핵심 요약 매핑 표

| 영역 | 핵심 CS 이론 | 실무 적용 구성 요소 | 실무 핵심 검증 포인트 |
| :--- | :--- | :--- | :--- |
| **네트워크** | CIDR, 서브넷팅, 1:1 양방향 NAT, 디폴트 라우트 | VPC, Public Subnet, IGW, Route Table | CIDR 충돌 방지, `0.0.0.0/0` → IGW 경로 연결 |
| **서버 & OS** | 비동기 논블로킹 I/O, systemd 데몬 관리, POSIX 권한 | EC2 Linux, Nginx, systemctl, chmod 400 | 로컬 루프백(`curl localhost`) 200 OK 확인 |
| **보안** | PoLP(최소 권한), Stateful 패킷 추적, RSA 비대칭키 | IAM 사용자/정책, Security Group, 키페어(.pem) | 루트 계정 미사용, SSH 포트(`/32`) 제한 |
| **아키텍처** | 가용성(SLA) 모델, SPOF 제거, 부하 분산 | Architecture Diagram, Multi-AZ & ALB | 단일 AZ의 한계 인지 및 확장 구조 설계 |
| **운영 / FinOps** | 리소스 종속성 제어, 유휴 자원 과금 방지 | 리소스 정리 체크리스트, Billing 대시보드 | EBS/EIP 등 잔여 자원 0건 확인 및 비용 누수 방지 |
