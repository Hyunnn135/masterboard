# [masterboard] 2026-04-18 — Phase 3: 프로젝트 상세 템플릿 + devlog 자동 인덱싱 (3/4)

> 작업 시간: 저녁 세션
> 분류: #리팩토링 #스키마 #UI리디자인 #자동화

## 📌 오늘 한 일

**Phase 3: `project.html` 단일 템플릿 신규 작성.** `?slug=xxx` 쿼리 분기로 4개 프로젝트(salarykorea/maxout/nudge/realestate)를 한 파일로 커버. 구성:

- **Hero 헤더** — 아이콘·이름·oneLiner·Phase 타임라인(currentPhase 하이라이트)·메트릭(진행률, Now/Next/Later/Done 카운트)·linkedDocs 칩. `status==='paused'` 면 PAUSED 배지 + 헤더 왼쪽 accent bar에 프로젝트 themeColor 적용 (CSS 변수 `--accent` / `--accent-bg` 런타임 주입).
- **Status 아코디언 5단** — Now(🔴) / Next(🟡) / Later(⚪) / Done(✅) / Archived(📦). Now·Next는 기본 펼침, 나머지는 접힘. Now·Next·Later 는 카드형(priority 색 border-left, phase/tags/createdAt chip, notes 블록), Done·Archived 는 컴팩트 리스트(제목 + completedAt 날짜) — 완료 태스크가 화면을 잠식하지 않도록 밀도 분리.
- **프로젝트별 devlog 섹션** — `window.DEVLOG_INDEX` (후술) 에서 `project===slug` 필터링 후 최대 15개. salarykorea 는 별도로 `blog-upload-board.html` 링크 chip 노출.
- **404 대응** — slug 없거나 유효하지 않은 경우 "프로젝트를 찾을 수 없습니다" 화면.

**devlog 자동 인덱싱 도입.** Phase 2 에서 index.html 의 Recent devlog 가 하드코딩으로 남아있던 부채를 해소:

- `update-devlog-index.py` 작성 — `devlog/*.md` 를 스캔해서 파일명(`YYYY-MM-DD-{project}[-N].md`)과 h1 첫 줄에서 date/project/title 추출. `#`, `[project]`, date, `—/–/-` 구분자를 벗겨 깔끔한 title 만 남기는 `clean_title()` 로직 추가 (기존 devlog들이 표준 템플릿을 완전히 안 따르는 경우도 흡수 — 예: `# Nudge 2026-04-17 — ...`).
- 출력 2종: `devlog/index.json`(외부/사람용, 기존 포맷 유지) + `devlog/index.js`(브라우저용, `window.DEVLOG_INDEX = [...]`).
- 기존 index.json 은 10개였는데 실제 파일 19개 → 9개 누락 상태. 스크립트 실행 후 19/19 정합.
- idempotent 확인: 스크립트 재실행 시 출력 byte-exact 동일.

**index.html 하드코딩 제거.** Phase 2 의 `// TODO(Phase 3 이후)` 주석 붙어있던 Recent devlog 3개 하드코딩 블록을 `window.DEVLOG_INDEX` 기반 동적 렌더로 교체. 이제 devlog 추가 시 `python3 update-devlog-index.py` 한 번만 돌리면 index.html + project.html 양쪽이 자동 반영.

## 🤔 결정 사항

- **프로젝트별 HTML 파일 4개 대신 단일 `project.html`** — salarykorea/maxout/nudge 각각 전용 보드(`project-masterboard.html` 등)를 두던 기존 구조는 프로젝트 추가 시마다 HTML 복제를 유발. 템플릿 + 쿼리 분기로 전환하니 데이터만 바꾸면 새 프로젝트 카드 + 상세가 즉시 생성됨. Phase 4에서 구 보드 4개 삭제 예정.
- **Done/Archived 만 컴팩트 리스트, Now/Next/Later 는 카드형** — "난잡함"의 주 원인 중 하나가 완료 태스크 40여 개가 진행 중 태스크와 같은 밀도로 섞여 있던 것. 상태별로 정보 밀도 자체를 차등화 해서, 첫 화면에서 "지금 할 것"의 인지 비용을 낮춤.
- **devlog 인덱스는 빌드 스크립트 방식** — 브라우저에서 `readdir` 불가, fetch 는 file:// 에서 CORS. 간단히 Python 스크립트 1회 실행 → `index.js` (JSONP 스타일) 생성 → `<script>` 로 로드. 새로운 빌드 도구 없이 Python stdlib 만으로 충분.
- **`blog-upload-board.html` 는 별도 페이지로 유지 (Phase 4에서 재검토)** — 흡수하려면 65개 포스트 데이터 이관 + 위젯 재작성 필요. project.html 의 salarykorea 헤더에 링크 chip 만 노출하고 실제 흡수는 Phase 4 또는 그 이후로 이월.

## 🐛 문제와 해결 과정

- devlog h1 title 파싱 초기 정규식(`^#\s*\[([^\]]+)\]\s*\d{4}-\d{2}-\d{2}\s*[—–-]\s*(.+?)$`)이 엄격해서 nudge 파일들 중 `# Nudge 2026-04-17 — ...` 처럼 `[project]` 대괄호 없이 쓴 케이스가 폴백으로 흘러가 title 이 `"Nudge 2026-04-17 — ..."` 통째로 들어감. `clean_title()` 로 교체 — leading `#`, `[...]`, `project` literal, date, `—/–/-` 를 순차 벗기고 남은 걸 title 로. 재실행 시 8개 nudge 엔트리 모두 정상화.

## 🔍 검증 결과 (배포 시)

- 로컬↔원격 일치 여부: _(push 후 확인)_
- 실제 작동 확인: _(4개 slug 각각 project.html 열어 헤더·5아코디언·devlog 섹션 렌더 확인 필요. 404 케이스 `project.html?slug=없음` 도 확인)_
- Phase 3 검증 스크립트: 24/24 체크 통과 (파일 구조·devlog 인덱스 정합·4 프로젝트 시뮬·하드코딩 제거·idempotent).

## 📅 다음에 할 일

- **Phase 4: 구 보드 제거 + 문서 갱신**
  - 삭제: `project-masterboard.html`, `maxout-board.html`, `nudge-board.html` (3개 — 모두 `project-data.js` 참조하지만 project.html 로 대체됨)
  - `blog-upload-board.html` 은 salarykorea 블로그 업로드 워크플로 전용이라 존치 or 재검토
  - 레거시 필드(`text/done/tag/tagColor`) 제거 후 데이터 크기 15~20% 감축 검증
  - `PROJECT_CONTEXT.md` 갱신 — 단일 진실 소스 + project.html 템플릿 구조 반영
  - `README.md` (있다면) 또는 신규 생성으로 devlog 인덱스 빌드 프로세스 문서화

## 💭 느낀 점

- **단일 템플릿 + 쿼리 분기** 는 정적 사이트에서 의외로 저렴한 패턴이었음. React/Vue 없어도 URL 상태와 전역 데이터 하나만 있으면 "프로젝트 추가 = 데이터 한 줄 추가" 까지 압축 가능.
- devlog 자동 인덱싱을 Phase 1에서 미루고 Phase 2 와 Phase 3 세션 사이에 9개 devlog 가 index.json 에 빠진 상태로 남아있었던 게 바로 "부채는 쌓인다"의 실증 사례. 자동화 가치가 가장 큰 지점은 실제로 현재 고장나 있는 곳이라는 평범한 교훈 재확인.
- Phase 3 를 1세션에 끝낼 수 있었던 건 Phase 1~2 에서 데이터 레이어(`project-data.json` schema v2)를 단단하게 잡아둔 덕. 스키마에 `status`/`priority`/`phase`/`tags` 같은 구조적 필드가 이미 있으니 뷰 하나 새로 추가하는 게 "필드 조합만 바꾸는 일" 이 됨.
