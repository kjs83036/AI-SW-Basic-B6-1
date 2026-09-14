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


if __name__ == "__main__":
    main()
