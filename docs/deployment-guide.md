# AWS 배포 수행 가이드

> 모든 제약 사항(§7)을 준수하며 실제 AWS 콘솔에서 단계별로 수행한다.

---

## 사전 준비

| 항목 | 설정값 |
|------|--------|
| AWS 리전 | 서울 (`ap-northeast-2`) — **모든 단계에서 이 리전을 유지** |
| 계정 | 루트 계정 사용 금지 → IAM 사용자로만 접근 |
| 프리 티어 | 전 단계 프리 티어 범위 내 리소스만 사용 |

---

## 1단계. IAM 사용자 생성 (최소 권한)

> 루트 계정으로 최초 1회만 수행 후 즉시 IAM 사용자로 전환한다.

1. AWS 콘솔 → **IAM** → **사용자** → **사용자 생성**
2. 사용자 이름 예: `infra-practitioner`
3. **AWS Management Console 액세스** 활성화 → 사용자 지정 암호 설정
4. 권한 → **직접 정책 연결** → 아래 정책만 연결:

   | 정책 이름 | 이유 |
   |----------|------|
   | `AmazonEC2FullAccess` | EC2/SG/키페어 생성·관리 |
   | `AmazonVPCFullAccess` | VPC/Subnet/IGW/RouteTable 구성 |

   > ⚠️ `AdministratorAccess` **절대 부여하지 않는다.**  
   > ⚠️ S3, RDS 등 실습 무관 서비스 권한 부여하지 않는다.

5. 사용자 생성 후 콘솔 URL(예: `https://<계정ID>.signin.aws.amazon.com/console`) 기록
6. 이후 모든 단계를 **이 IAM 사용자로 로그인하여** 진행한다.

---

## 2단계. VPC 생성

1. **VPC** → **VPC 생성**
2. 설정:

   | 항목 | 값 |
   |------|----|
   | 이름 | `infra-vpc` |
   | IPv4 CIDR | `10.0.0.0/16` |
   | 테넌시 | 기본 |

3. **VPC 생성** 클릭 → VPC ID 기록

---

## 3단계. Public Subnet 생성

1. **서브넷** → **서브넷 생성**
2. 설정:

   | 항목 | 값 |
   |------|----|
   | VPC | 위에서 생성한 `infra-vpc` |
   | 서브넷 이름 | `public-subnet` |
   | 가용 영역 | `ap-northeast-2a` |
   | IPv4 CIDR | `10.0.1.0/24` |

3. 생성 후 **퍼블릭 IPv4 주소 자동 할당 활성화**:  
   서브넷 선택 → **작업** → **서브넷 설정 편집** → **퍼블릭 IPv4 주소 자동 할당 활성화** 체크

---

## 4단계. Internet Gateway 생성 및 VPC 연결

1. **인터넷 게이트웨이** → **인터넷 게이트웨이 생성**
2. 이름: `infra-igw` → 생성
3. 생성된 IGW 선택 → **작업** → **VPC에 연결** → `infra-vpc` 선택

---

## 5단계. Route Table 설정

1. **라우팅 테이블** → `infra-vpc`의 메인 라우팅 테이블 선택 (또는 새로 생성)
2. **라우팅** 탭 → **라우팅 편집** → **라우팅 추가**:

   | 대상 | 대상 유형 |
   |------|---------|
   | `0.0.0.0/0` | 인터넷 게이트웨이 → `infra-igw` |

3. **서브넷 연결** 탭 → **서브넷 연결 편집** → `public-subnet` 체크

---

## 6단계. Security Group 생성

1. **보안 그룹** → **보안 그룹 생성**
2. 기본 정보:

   | 항목 | 값 |
   |------|----|
   | 이름 | `infra-sg` |
   | 설명 | 웹서버 보안 그룹 |
   | VPC | `infra-vpc` |

3. **인바운드 규칙**:

   | 유형 | 프로토콜 | 포트 | 소스 | 이유 |
   |------|---------|------|------|------|
   | HTTP | TCP | 80 | `0.0.0.0/0` | 외부 웹 접속 |
   | SSH | TCP | 22 | **내 IP/32** | 관리 접속 (내 IP만) |

   > ⚠️ `0.0.0.0/0`에 포트 범위 `0-65535` 허용 규칙 **절대 추가하지 않는다.**

4. **아웃바운드 규칙**: 기본값 유지 (전체 허용)

---

## 7단계. 키페어 생성

1. **키페어** → **키페어 생성**
2. 설정:

   | 항목 | 값 |
   |------|----|
   | 이름 | `infra-keypair` |
   | 유형 | RSA |
   | 형식 | `.pem` (Linux/Mac) 또는 `.ppk` (Windows PuTTY) |

3. `.pem` 파일 다운로드 후 안전한 위치 보관 (재발급 불가)
4. 권한 설정 (Linux/Mac): `chmod 400 infra-keypair.pem`

---

## 8단계. EC2 인스턴스 생성

1. **EC2** → **인스턴스 시작**
2. 설정:

   | 항목 | 값 |
   |------|----|
   | 이름 | `infra-ec2` |
   | AMI | Ubuntu Server 26.04 LTS (또는 Ubuntu 24.04 LTS, Amazon Linux 2023) |
   | 인스턴스 유형 | `t2.micro` 또는 `t3.micro` (프리 티어) |
   | 키페어 | `infra-keypair` |
   | VPC | `infra-vpc` |
   | 서브넷 | `public-subnet` |
   | 퍼블릭 IP 자동 할당 | 활성화 |
   | 보안 그룹 | `infra-sg` |
   | 스토리지 | `gp3` 8GiB (기본값 유지) |

3. **인스턴스 시작** → 퍼블릭 IP 기록 (예: `x.x.x.x`)

---

## 9단계. Nginx 설치 및 실행

SSH로 인스턴스 접속 (Ubuntu 기본 계정: `ubuntu`):

```bash
ssh -i infra-keypair.pem ubuntu@<퍼블릭IP>
# (참고: Amazon Linux 2023일 경우 ec2-user@<퍼블릭IP>)
```

**Ubuntu 26.04 / 24.04 (기본 권장):**
```bash
# 1. 패키지 업데이트 및 Nginx 설치
sudo apt update -y
sudo apt install nginx -y

# 2. 우분투 기본 사이트 충돌 방지 및 /health 엔드포인트 구성
sudo rm -f /etc/nginx/sites-enabled/default
sudo bash -c 'cat << "EOF" > /etc/nginx/conf.d/health.conf
server {
    listen 80 default_server;
    server_name _;

    location / {
        root /var/www/html;
        index index.nginx-debian.html index.html;
    }

    location /health {
        access_log off;
        return 200 "OK\n";
        add_header Content-Type text/plain;
    }
}
EOF'

# 3. 문법 검사 및 서비스 리로드 (우분투는 apt 설치 시 자동 기동됨)
sudo nginx -t
sudo systemctl reload nginx
```

**참고 (Amazon Linux 2023 사용 시):**
```bash
sudo dnf update -y
sudo dnf install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
```

로컬 접속 확인:
```bash
curl http://localhost
curl http://localhost/health
# 기대 출력: Welcome to nginx! 포함 HTML 및 /health 200 OK
```

---

## 10단계. 외부 접속 확인

로컬 PC 또는 브라우저에서:

**방식 A (브라우저):**
```
http://<퍼블릭IP>
```
→ Nginx 기본 페이지("Welcome to nginx!") 표시 확인

**방식 B (curl /health):**
```bash
curl -v http://<퍼블릭IP>/health
# 기대: HTTP 200 또는 404 (Nginx 동작 중이면 응답 자체가 증거)
```

결과를 스크린샷으로 저장 → `docs/access-result.md`에 기록.

---

## 11단계. 리소스 정리 (과금 방지)

> 실습 완료 후 즉시 수행. 순서 준수.

1. EC2 인스턴스 → **종료(Terminate)** (Stopped가 아닌 Terminated)
2. EBS 볼륨 → 미사용 볼륨 삭제 확인 (EC2 종료 시 자동 삭제 설정이면 자동 처리됨)
3. Elastic IP → 할당했다면 **Release** (미사용 EIP도 과금)
4. Internet Gateway → VPC **Detach** 후 삭제
5. 서브넷 삭제
6. 라우팅 테이블 삭제 (메인 RT 외)
7. VPC 삭제
8. 키페어 삭제 (콘솔에서, 로컬 `.pem`도 삭제)
9. 보안 그룹 삭제
10. IAM 사용자 삭제 (선택: 재사용 계획 없으면 삭제)
11. **Billing Dashboard** 확인 → 과금 항목 없음 확인

`docs/cleanup-checklist.md` 체크리스트 항목과 1:1 대조하며 진행한다.

---

## 제약 사항 충족 확인표

| PDF 제약 | 충족 단계 | 비고 |
|----------|---------|------|
| 서울 리전 `ap-northeast-2` | 전 단계 | 콘솔 리전 항상 확인 |
| VPC 1개 생성 | 2단계 | `10.0.0.0/16` |
| Public Subnet 1개 | 3단계 | `10.0.1.0/24` |
| IGW VPC 연결 | 4단계 | |
| RT `0.0.0.0/0 → IGW` | 5단계 | |
| EC2 t2/t3.micro | 8단계 | 프리 티어 |
| EBS 8~10GiB | 8단계 | gp3 8GiB |
| 키페어 1개 | 7단계 | 안전 보관 |
| Nginx 설치·실행 | 9단계 | systemctl enable |
| `curl localhost` 200 | 9단계 | |
| HTTP 80: `0.0.0.0/0` | 6단계 | |
| SSH 22: 내 IP만 | 6단계 | |
| 전체 포트 규칙 금지 | 6단계 | |
| IAM 최소권한 | 1단계 | AdministratorAccess 금지 |
| 루트 계정 미사용 | 1단계 | IAM 사용자만 |
| 프리 티어 범위 | 전 단계 | |
| 실습 후 리소스 정리 | 11단계 | |
