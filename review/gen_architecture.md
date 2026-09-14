# gen_architecture.py 라인별 워크스루

> AWS 인프라 아키텍처 다이어그램을 matplotlib로 그려 PDF로 저장하는 파일.

---

## 1. 모듈 독스트링 + 임포트

```python
"""
아키텍처 다이어그램 생성기
VPC/Subnet/IGW/EC2/SG 구성 요소와 외부 트래픽 흐름을 PDF로 출력한다.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import matplotlib

# Windows 한글 폰트 설정
matplotlib.rcParams["font.family"] = "Malgun Gothic"
matplotlib.rcParams["axes.unicode_minus"] = False
```

### 한 줄씩 설명

| 줄/구문 | 코드 | 설명 |
|---------|------|------|
| 임포트 | `import os` | 파일/폴더 조작용 표준 라이브러리 |
| 임포트 | `import matplotlib.pyplot as plt` | 그래프 캔버스 도구. `plt`라는 별명으로 줄여 씀 |
| 임포트 | `import matplotlib.patches as mpatches` | 도형(사각형·타원) 그리기 도구 모음 |
| 임포트 | `from matplotlib.patches import FancyBboxPatch` | 모서리가 둥근 사각형 클래스만 꺼냄 |
| 임포트 | `import matplotlib` | 전역 설정(`rcParams`)을 건드리려고 본체를 따로 임포트 |
| 설정 | `matplotlib.rcParams["font.family"] = "Malgun Gothic"` | matplotlib 전체 기본 폰트를 맑은 고딕으로 지정 |
| 설정 | `matplotlib.rcParams["axes.unicode_minus"] = False` | 음수 부호`-`가 네모(`□`)로 깨지는 현상 방지 |

> 💡 **배경지식: rcParams**
>
> matplotlib는 전역 설정값을 `rcParams`라는 딕셔너리에 보관한다. 열쇠(key)로 설정 항목을 지정하고, 값을 대입하면 이후 모든 그래프에 적용된다.
> ```python
> matplotlib.rcParams["font.size"] = 14  # 모든 글자 기본 크기 14pt로
> ```
> 프로그램 맨 위에서 한 번만 설정하면 되는 "전체 기본값 조정판"이다.

---

## 2. draw_vpc(ax)

```python
def draw_vpc(ax):
    """VPC 외곽 박스와 레이블을 그린다."""
    vpc = FancyBboxPatch(
        (0.05, 0.08), 0.88, 0.78,
        boxstyle="round,pad=0.01",
        linewidth=2, edgecolor="#FF9900", facecolor="#FFF8EE", zorder=1
    )
    ax.add_patch(vpc)
    ax.text(0.09, 0.845, "VPC  (10.0.0.0/16)", fontsize=10,
            fontweight="bold", color="#FF9900", va="top", zorder=2)
```

### 한 줄씩 설명

| 줄/구문 | 코드 | 설명 |
|---------|------|------|
| 매개변수 | `ax` | matplotlib의 "그림판(Axes)". 도형과 글자를 붙이는 작업 공간 |
| 도형 생성 | `FancyBboxPatch((0.05, 0.08), 0.88, 0.78, ...)` | 좌하단 좌표 (0.05, 0.08), 너비 0.88, 높이 0.78인 둥근 사각형 생성 |
| 좌표계 | `0.05 ~ 0.93` | 0.0=왼쪽 끝, 1.0=오른쪽 끝인 상대 좌표(비율). 해상도 무관 |
| 스타일 | `boxstyle="round,pad=0.01"` | 모서리를 둥글게(round), 내부 여백(pad) 최소로 |
| 스타일 | `edgecolor="#FF9900"` | 테두리 색상. AWS 주황색 |
| 스타일 | `zorder=1` | 겹칠 때 그리는 순서. 숫자 작을수록 뒤에 깔림 (배경 역할) |
| 그리기 | `ax.add_patch(vpc)` | 만들어 둔 도형 객체를 실제 캔버스에 붙임 |
| 텍스트 | `ax.text(0.09, 0.845, "VPC ...", va="top", zorder=2)` | (0.09, 0.845) 위치에 VPC 레이블 텍스트 출력 |

### 역할 / 입출력 / 동작

- **역할**: VPC 외곽 테두리 상자와 CIDR 레이블을 캔버스에 그림
- **입력**: `ax` (matplotlib Axes 객체)
- **출력**: 없음 (ax에 직접 도형·텍스트 추가, 부작용)
- **동작**: ① 둥근 사각형 객체 생성 → ② 캔버스에 추가 → ③ 레이블 텍스트 추가

### 설계 의도 / 대안

- 좌표를 0~1 상대값으로 쓰면 그림 크기가 바뀌어도 비율이 유지됨
- 각 AWS 구성요소를 별도 함수로 분리해 관심사 구분. `main()`이 호출 순서만 제어

> 💡 **배경지식: FancyBboxPatch**
>
> matplotlib에서 도형을 그리려면 "패치(Patch)" 객체를 만든 뒤 캔버스에 `add_patch()`로 붙여야 한다. `FancyBboxPatch`는 모서리를 둥글게 깎은 사각형을 만드는 클래스다.
> ```python
> box = FancyBboxPatch((x, y), width, height, boxstyle="round,pad=0.02")
> ax.add_patch(box)  # 캔버스에 부착해야 비로소 보임
> ```
> 마치 스티커를 먼저 만들고(=객체 생성), 그 다음 종이에 붙이는(=add_patch) 두 단계다.

---

## 3. draw_components(ax)

```python
def draw_components(ax):
    """Public Subnet, EC2(Nginx), Security Group, Internet Gateway를 그린다."""
    # Public Subnet
    subnet = FancyBboxPatch(
        (0.12, 0.22), 0.68, 0.52,
        boxstyle="round,pad=0.01",
        linewidth=1.5, edgecolor="#147EBA", facecolor="#EBF5FB", zorder=2
    )
    ax.add_patch(subnet)
    ax.text(0.16, 0.72, "Public Subnet  (10.0.1.0/24)",
            fontsize=9, color="#147EBA", fontweight="bold", va="top", zorder=3)

    # Security Group (EC2 주변 점선 테두리)
    sg = FancyBboxPatch(
        (0.28, 0.30), 0.36, 0.32,
        boxstyle="round,pad=0.01",
        linewidth=1.5, edgecolor="#E74C3C", facecolor="#FDEDEC",
        linestyle="dashed", zorder=3
    )
    ax.add_patch(sg)
    ax.text(0.30, 0.60, "Security Group", fontsize=8,
            color="#E74C3C", va="top", zorder=4)
    ax.text(0.30, 0.565, "HTTP 80: 0.0.0.0/0", fontsize=7,
            color="#666666", va="top", zorder=4)
    ax.text(0.30, 0.540, "SSH 22: 내 IP만", fontsize=7,
            color="#666666", va="top", zorder=4)

    # EC2 (Nginx)
    ec2 = FancyBboxPatch(
        (0.33, 0.33), 0.26, 0.18,
        boxstyle="round,pad=0.01",
        linewidth=2, edgecolor="#229954", facecolor="#EAFAF1", zorder=4
    )
    ax.add_patch(ec2)
    ax.text(0.46, 0.44, "EC2 (Nginx)", fontsize=9,
            color="#229954", fontweight="bold", ha="center", va="center", zorder=5)
    ax.text(0.46, 0.375, "t2/t3.micro\nPublic IP: <퍼블릭IP>",
            fontsize=7.5, color="#555555", ha="center", va="center", zorder=5)

    # Internet Gateway
    igw = FancyBboxPatch(
        (0.33, 0.10), 0.26, 0.10,
        boxstyle="round,pad=0.01",
        linewidth=2, edgecolor="#8E44AD", facecolor="#F5EEF8", zorder=2
    )
    ax.add_patch(igw)
    ax.text(0.46, 0.152, "Internet Gateway",
            fontsize=9, color="#8E44AD", fontweight="bold",
            ha="center", va="center", zorder=3)
```

### 한 줄씩 설명

| 줄/구문 | 코드 | 설명 |
|---------|------|------|
| Subnet | `FancyBboxPatch((0.12, 0.22), 0.68, 0.52, ...)` | VPC 박스 안쪽에 더 작은 파란 서브넷 박스. zorder=2로 VPC 위에 쌓임 |
| SG 스타일 | `linestyle="dashed"` | Security Group은 방화벽 의미를 강조하려 점선(dashed) 테두리로 표현 |
| SG 텍스트 | `ax.text(..., "HTTP 80: 0.0.0.0/0", ...)` | 허용 포트 규칙 2줄을 별도 `ax.text()`로 추가 |
| EC2 위치 | `(0.33, 0.33)` | Security Group 박스(0.28~0.64) 안쪽에 중첩 배치 |
| EC2 텍스트 | `ha="center", va="center"` | 가로·세로 모두 중앙 정렬. 박스 중심에 텍스트 |
| IGW | `zorder=2` | Subnet 아래 배치 → VPC 안에 있지만 Subnet 밖에 있는 구성 요소임을 표현 |

### 역할 / 입출력 / 동작

- **역할**: VPC 내부의 4개 구성요소(Subnet, SG, EC2, IGW) 그리기
- **입력**: `ax` (matplotlib Axes 객체)
- **출력**: 없음 (ax 부작용)
- **동작**: ① Public Subnet → ② Security Group → ③ EC2 → ④ IGW 순으로 겹쳐 그림 (zorder로 레이어 순서 제어)

### 설계 의도 / 대안

- `zorder` 값을 1→5로 단계별로 높여 AWS 인프라의 포함 관계(VPC>Subnet>SG>EC2)를 레이어로 표현
- 구성 요소마다 색상 코드를 AWS 공식 색상에 맞춤(`#FF9900`=주황, `#147EBA`=파랑 등)

---

## 4. draw_traffic_flow(ax)

```python
def draw_traffic_flow(ax):
    """Internet → IGW → EC2 트래픽 흐름 화살표를 그린다."""
    # Internet 노드 (화면 최하단)
    ax.text(0.46, 0.025, "Internet", fontsize=10,
            color="#1A5276", fontweight="bold",
            ha="center", va="center",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#D6EAF8",
                      edgecolor="#1A5276", linewidth=1.5))

    # Internet → IGW
    ax.annotate(
        "", xy=(0.46, 0.10), xytext=(0.46, 0.058),
        arrowprops=dict(arrowstyle="->", color="#E67E22", lw=2)
    )
    ax.text(0.49, 0.078, "HTTP/HTTPS\n(80)", fontsize=7,
            color="#E67E22", va="center")

    # IGW → EC2
    ax.annotate(
        "", xy=(0.46, 0.33), xytext=(0.46, 0.20),
        arrowprops=dict(arrowstyle="->", color="#E67E22", lw=2)
    )
    ax.text(0.49, 0.26, "라우팅\n(RT)", fontsize=7,
            color="#E67E22", va="center")
```

### 한 줄씩 설명

| 줄/구문 | 코드 | 설명 |
|---------|------|------|
| 텍스트 박스 | `bbox=dict(boxstyle="round,pad=0.3", ...)` | `ax.text()`에 `bbox` 인자를 주면 텍스트 주위에 박스를 그려줌 |
| `dict()` 인자 | `dict(boxstyle="round,pad=0.3", facecolor=..., ...)` | `{}`와 동일하지만 키워드 인자로 써서 가독성 향상 |
| 화살표 | `ax.annotate("", xy=(0.46, 0.10), xytext=(0.46, 0.058), ...)` | 텍스트 없이(`""`) 화살표만 그림. `xytext`=시작점, `xy`=끝점 |
| 화살표 스타일 | `arrowprops=dict(arrowstyle="->", color=..., lw=2)` | `->` 일반 화살표, `lw=2` 선 굵기 2 |
| 레이블 | `ax.text(0.49, 0.078, "HTTP/HTTPS\n(80)", ...)` | 화살표 오른쪽에 프로토콜/포트 정보 별도 텍스트로 표시 |

### 역할 / 입출력 / 동작

- **역할**: 인터넷에서 서버까지의 트래픽 경로를 화살표로 시각화
- **입력**: `ax` (matplotlib Axes 객체)
- **출력**: 없음 (ax 부작용)
- **동작**: ① Internet 노드 텍스트 박스 → ② Internet→IGW 화살표+레이블 → ③ IGW→EC2 화살표+레이블

### 설계 의도 / 대안

- `ax.annotate()`는 화살표와 텍스트를 함께 그리는 함수지만, 여기서는 텍스트("")를 비워 화살표만 사용하고 텍스트는 `ax.text()`로 별도 배치해 위치 조정 자유도를 높임

> 💡 **배경지식: ax.annotate와 화살표**
>
> `ax.annotate(text, xy=끝점, xytext=시작점, arrowprops=...)` — `xy`가 화살촉이 향하는 목적지, `xytext`가 화살 꼬리(출발점)다.
> ```python
> ax.annotate("", xy=(0.5, 0.8), xytext=(0.5, 0.2),
>             arrowprops=dict(arrowstyle="->", color="red", lw=2))
> ```
> 마치 "여기서(xytext) 저기로(xy) 화살표 쏜다"고 읽으면 된다.

---

## 5. main()

```python
def main():
    """아키텍처 다이어그램을 생성하고 docs/architecture.pdf로 저장한다."""
    os.makedirs("docs", exist_ok=True)

    fig, ax = plt.subplots(figsize=(9, 7))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.set_title(
        "AWS 웹 서비스 인프라 아키텍처\n(서울 리전 ap-northeast-2)",
        fontsize=13, fontweight="bold", color="#2C3E50", pad=12
    )

    draw_vpc(ax)
    draw_components(ax)
    draw_traffic_flow(ax)

    # 범례
    legend_items = [
        mpatches.Patch(facecolor="#FFF8EE", edgecolor="#FF9900", label="VPC"),
        mpatches.Patch(facecolor="#EBF5FB", edgecolor="#147EBA", label="Public Subnet"),
        mpatches.Patch(facecolor="#FDEDEC", edgecolor="#E74C3C",
                       linestyle="dashed", label="Security Group"),
        mpatches.Patch(facecolor="#EAFAF1", edgecolor="#229954", label="EC2 (Nginx)"),
        mpatches.Patch(facecolor="#F5EEF8", edgecolor="#8E44AD", label="Internet Gateway"),
    ]
    ax.legend(handles=legend_items, loc="lower right",
              fontsize=8, framealpha=0.9, title="구성 요소")

    plt.tight_layout()
    out_path = os.path.join("docs", "architecture.pdf")
    try:
        fig.savefig(out_path, format="pdf", bbox_inches="tight")
        print(f"저장 완료: {out_path}")
    except IOError as e:
        print(f"오류: PDF 저장 실패 - {e}")
    finally:
        plt.close(fig)
```

### 한 줄씩 설명

| 줄/구문 | 코드 | 설명 |
|---------|------|------|
| 폴더 생성 | `os.makedirs("docs", exist_ok=True)` | `docs/` 폴더 생성. 이미 있으면 에러 대신 조용히 넘어감 |
| 캔버스 생성 | `fig, ax = plt.subplots(figsize=(9, 7))` | 9인치×7인치 캔버스(`fig`)와 그림판(`ax`)을 한 번에 생성 |
| 좌표 설정 | `ax.set_xlim(0, 1)` / `ax.set_ylim(0, 1)` | X·Y 범위를 0~1로 고정해 상대 좌표계 확보 |
| 축 숨김 | `ax.axis("off")` | X·Y 눈금선과 숫자 제거. 다이어그램에는 불필요 |
| 그리기 순서 | `draw_vpc → draw_components → draw_traffic_flow` | zorder가 낮은 것(배경)부터 호출 순서와 일치 |
| 범례 항목 | `mpatches.Patch(facecolor=..., label="VPC")` | 색상 정보만 담은 더미 패치. 실제 도형과 연결 없이 범례용으로만 사용 |
| 범례 배치 | `ax.legend(handles=legend_items, loc="lower right")` | 범례를 오른쪽 아래에 배치 |
| 여백 조정 | `plt.tight_layout()` | 제목·여백이 잘리지 않게 자동 여백 조정 |
| 저장 경로 | `os.path.join("docs", "architecture.pdf")` | OS에 맞는 경로 구분자로 `docs/architecture.pdf` 생성 |
| 저장 | `fig.savefig(out_path, format="pdf", bbox_inches="tight")` | PDF 포맷으로 저장. `bbox_inches="tight"` = 여백 최소화 |
| 예외 처리 | `except IOError as e` | 파일 쓰기 실패(디스크 꽉참, 권한없음 등) 시 오류 메시지 출력 |
| 정리 | `plt.close(fig)` | 메모리에서 그림 해제. `finally`로 저장 성공·실패 관계없이 항상 실행 |

### 역할 / 입출력 / 동작

- **역할**: 전체 흐름 조율. 캔버스 준비 → 도형 그리기 → PDF 저장
- **입력**: 없음
- **출력**: `docs/architecture.pdf` 파일
- **동작**: ① `docs/` 폴더 보장 → ② 캔버스 초기화 → ③ 세 그리기 함수 호출 → ④ 범례 추가 → ⑤ PDF 저장 → ⑥ 메모리 해제

### 설계 의도 / 대안

- `finally: plt.close(fig)` — 저장이 실패해도 메모리 누수를 막는 안전장치. 서버에서 반복 실행하면 `plt.close()` 빠뜨릴 시 메모리가 계속 쌓임

> 💡 **배경지식: exist_ok=True**
>
> `os.makedirs("폴더명")` 은 폴더가 이미 있으면 `FileExistsError`를 낸다. `exist_ok=True`를 추가하면 "이미 있어도 괜찮다"는 의미로 조용히 넘어간다.
> ```python
> os.makedirs("output", exist_ok=True)  # 있든 없든 안전하게 실행
> ```
> 스크립트를 여러 번 실행해도 두 번째부터 오류 없이 동작한다.

> 💡 **배경지식: try / except / finally**
>
> `finally` 블록은 예외가 발생했든 안 했든 **무조건** 실행된다. "청소" 코드를 넣는 자리다.
> ```python
> try:
>     파일_저장()       # 오류 날 수도 있음
> except IOError as e:
>     print("실패:", e) # 오류 났을 때
> finally:
>     자원_해제()       # 성공이든 실패든 항상
> ```
> 파일 닫기, 연결 끊기처럼 "반드시 정리해야 하는" 코드에 사용한다.

> 💡 **배경지식: plt.subplots와 fig/ax**
>
> `plt.subplots()`는 두 객체를 동시에 반환한다. `fig`(Figure)는 전체 종이, `ax`(Axes)는 그 위의 그림판이다.
> ```python
> fig, ax = plt.subplots(figsize=(너비인치, 높이인치))
> # fig: 저장·크기 담당   ax: 도형·텍스트 그리기 담당
> ```
> 포스터 용지(`fig`)에 그림 영역(`ax`)을 잡아놓는 구조다.

---

## 6. 진입점

```python
if __name__ == "__main__":
    main()
```

### 한 줄씩 설명

| 줄/구문 | 코드 | 설명 |
|---------|------|------|
| 진입점 | `if __name__ == "__main__":` | 이 파일을 직접 실행할 때만 `main()` 호출. 다른 파일이 임포트하면 실행 안 됨 |

(`__name__main__` 이미 전역 사전에 등록됨 — 💡 박스 생략)
