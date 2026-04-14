# masterboard — 프로젝트 컨텍스트

> ⚠️ **0순위 필독:** `~/Desktop/Projects/WORKFLOW_RULES.md` (모든 프로젝트 공통 마스터 규칙)
> 이 파일은 masterboard 프로젝트의 핵심 컨텍스트입니다.
> **최종 업데이트: 2026-04-14**

---

## 프로젝트 개요

- **역할:** 모든 프로젝트(salarykorea, maxout 등)의 메인 허브 / 포트폴리오
- **위치:** `~/Desktop/Projects/masterboard/`
- **기술:** HTML + CSS + Vanilla JS (단일 페이지, 빌드 없음)
- **데이터 소스:** `project-data.json` (단일 진실 소스, .js와 항상 동기화)

---

## 주요 파일

| 파일 | 역할 |
|-----|------|
| `index.html` | 메인 허브 / 포트폴리오 (프로젝트 카드, 타임라인) |
| `project-masterboard.html` | 전체 작업 현황 (카테고리별 필터링) |
| `maxout-board.html` | 맥스아웃 앱 전용 마스터보드 (Phase별) |
| `blog-upload-board.html` | 블로그 업로드 현황 |
| `project-data.js` | 메인 데이터 파일 (브라우저에서 로드) |
| `project-data.json` | 데이터 백업 (.js와 동일 내용) |

---

## 데이터 동기화 규칙

- `project-data.js`와 `project-data.json`은 **항상 동일한 내용** 유지
- 작업 추가/완료 시 두 파일 모두 업데이트
- 각 프로젝트의 PROJECT_CONTEXT 파일과도 동기화 (양방향)

---

## 맥스아웃 카테고리 색상

- icon: 💪
- bg: rgba(249,115,22,0.12)
- color: #fb923c
- badgeBg: #7c2d12
- task id 범위: w1~w19 (현재), 추가 시 w20~

---

## 진행 중인 카테고리

- 사이트 / 블로그 / SEO / 도구 / 수익화 / 전략 / 부동산 (salarykorea 계열)
- 맥스아웃 (maxout)

---

> **읽기 순서:** WORKFLOW_RULES.md → 이 파일(PROJECT_CONTEXT.md)
