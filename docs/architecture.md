# 구조도

```mermaid
flowchart TD
    Internet["🌐 Internet"]
    IGW["Internet Gateway\n(infra-igw)"]
    VPC["VPC\n10.0.0.0/16"]
    Subnet["Public Subnet\n10.0.1.0/24\n(ap-northeast-2a)"]
    SG["Security Group (infra-sg)\nHTTP 80: 0.0.0.0/0\nSSH 22: 내 IP만"]
    EC2["EC2 (t2/t3.micro)\nNginx 실행 중\nPublic IP: 퍼블릭IP"]
    RT["Route Table\n0.0.0.0/0 → IGW"]

    Internet -->|"HTTP 80"| IGW
    IGW --> VPC
    VPC --> RT
    RT --> Subnet
    Subnet --> SG
    SG --> EC2

    style Internet fill:#D6EAF8,stroke:#1A5276
    style IGW fill:#F5EEF8,stroke:#8E44AD
    style VPC fill:#FFF8EE,stroke:#FF9900
    style Subnet fill:#EBF5FB,stroke:#147EBA
    style SG fill:#FDEDEC,stroke:#E74C3C
    style EC2 fill:#EAFAF1,stroke:#229954
    style RT fill:#FDF2F8,stroke:#8E44AD
```

## 트래픽 흐름 설명

1. **Internet** → HTTP(80) 요청 발생
2. **Internet Gateway** → VPC 진입점. VPC에 Attached 상태여야 동작.
3. **Route Table** → `0.0.0.0/0`을 IGW로 라우팅. Public Subnet에 연결됨.
4. **Public Subnet** → Public IP가 할당된 EC2 인스턴스 위치.
5. **Security Group** → 인바운드 HTTP(80) 허용(`0.0.0.0/0`), SSH(22)는 내 IP만.
6. **EC2 (Nginx)** → 요청 수신 후 HTTP 200 응답 반환.
