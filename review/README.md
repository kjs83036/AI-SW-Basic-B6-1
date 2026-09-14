# 코드 학습 문서 (초보자용 라인별 코드리뷰)

> 배경지식 없이 읽을 수 있는 워크스루 문서. 함수 하나씩 비유와 함께 설명.

## 읽는 순서

```
1. gen_architecture.md  → AWS 인프라 아키텍처 다이어그램을 그려 PDF로 저장하는 메인 파일
```

(의존 파일 없음 — 단일 파일 프로젝트)

## 파일별 한 줄 요약

| 파일 | 역할 | 핵심 개념 |
|------|------|-----------|
| [gen_architecture.md](./gen_architecture.md) | matplotlib로 AWS VPC/EC2/SG/IGW 구조도 그리기 → PDF 저장 | `FancyBboxPatch`, `rcParams`, `ax.annotate`, `try/finally` |

## 새 문법 사전 (이번 워크스루에서 추가)

| 문법/개념 | 설명 요약 | 처음 등장 |
|-----------|-----------|-----------|
| `matplotlib.rcParams` | 라이브러리 전역 설정 딕셔너리 | gen_architecture.md |
| `FancyBboxPatch` | 둥근 모서리 사각형 패치 클래스 | gen_architecture.md |
| `ax.annotate` | 화살표 + 텍스트 주석 그리기 | gen_architecture.md |
| `os.makedirs(exist_ok=True)` | 폴더 중복 생성 시 오류 무시 | gen_architecture.md |
| `try/except/finally` | finally는 예외 여부 무관 항상 실행 | gen_architecture.md |
| `plt.subplots()` | fig(전체 종이)와 ax(그림판) 동시 생성 | gen_architecture.md |
