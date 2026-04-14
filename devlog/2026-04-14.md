# [마스터보드] 2026-04-14 — 마스터 규칙 정립 + 프로젝트 명칭 전면 변경(dashboard→masterboard, workout→maxout)

> 작업 시간: 오전~오후
> 분류: #프로세스 #포트폴리오 #문서화 #리네이밍 #배포

## 📌 오늘 한 일

- `~/Desktop/Projects/WORKFLOW_RULES.md` 마스터 규칙 파일 신규 생성
  - 5대 핵심 지침을 항목별로 정리 (공통 적용·임의 수정 금지 / git push 프롬프트 / 로컬↔원격 검증 / 진행상황 양방향 연동 / devlog 포트폴리오화)
  - 매 세션 체크리스트 + 관련 파일 빠른 참조 표 포함
- 각 프로젝트 PROJECT_CONTEXT 파일 상단에 "0순위 필독: WORKFLOW_RULES.md" 포인터 추가
  - maxout/PROJECT_CONTEXT.md
  - salarykorea/PROJECT-CONTEXT.md
  - masterboard/PROJECT_CONTEXT.md (신규 작성)
- 모든 프로젝트의 `devlog/_TEMPLATE.md` 표준 템플릿 배포
  - maxout, salarykorea, masterboard 세 곳에 동일 구조로 세팅
  - 섹션: 오늘 한 일 / 결정 사항 / 문제와 해결 / 검증 결과 / 다음 할 일 / 느낀 점
- Claude 메모리에 마스터 규칙 0순위 항목 추가 (`feedback_workflow_rules.md` + `MEMORY.md` 인덱스 최상단)

## 🤔 결정 사항

- **마스터 규칙은 단일 파일(`WORKFLOW_RULES.md`)에 모은다.** 각 프로젝트 컨텍스트에 중복 작성하지 않고 0순위 포인터만 두어 단일 진실 소스 유지.
- **devlog 템플릿은 프로젝트별로 분리하되 구조는 동일하게.** 프로젝트 색깔(분류 태그)만 다르고 섹션은 통일 → 추후 masterboard에서 일괄 파싱하기 쉬움.
- **메모리는 보조, 파일이 주.** 진행상황은 메모리에만 저장하지 않고 반드시 전용 파일 + masterboard 데이터에 기록 (현태 지침 4번).

## 🔄 추가 작업 — 프로젝트 명칭 전면 변경

일반명사("dashboard", "workout") 사용으로 인한 의사소통 혼동을 막기 위해 고유명사로 통일.

- **dashboard / 대시보드 → masterboard / 마스터보드**
- **workout / 워크아웃 → maxout / 맥스아웃** (앱 이름으로도 사용 예정, "max out" = 최대치까지 짜낸다)
- **salarykorea / 월급연구소** → 그대로 유지

수행 작업:
- 로컬 폴더명 변경: `dashboard/`→`masterboard/`, `workout/`→`maxout/`
- 파일명 변경: `project-dashboard.html`→`project-masterboard.html`, `workout-dashboard.html`→`maxout-board.html`, `blog-upload-dashboard.html`→`blog-upload-board.html`, `workout/DASHBOARD.md`→`maxout/PROGRESS.md`
- 모든 텍스트 일괄 치환 (sed로 masterboard/, maxout/, WORKFLOW_RULES.md 일괄 처리)
- salarykorea/PROJECT-CONTEXT.md의 메타 참조만 갱신 (사이트 안 `.dashboard` CSS 클래스는 일반명사라 보존)
- 메모리 시스템 갱신: `project_workout.md`→`project_maxout.md` 신규, 기존은 deprecated stub, MEMORY.md 인덱스 갱신
- WORKFLOW_RULES.md 모든 명칭 갱신 (사용자 직접 추가 정리도 반영됨)

## 🔍 검증 결과

**1차 검증 (로컬, sed 직후):**
- 소스 파일 안의 dashboard/workout 잔존 참조 = 0건 (`.git/logs/`의 과거 커밋 메시지만 보존 — git 히스토리이므로 정상)
- 폴더 트리 정상: `masterboard/`, `maxout/`, `salarykorea/` 3개
- 파일명/내용 모두 일관성 있게 변경 확인

**2차 검증 (현태가 직접 push & 배포 후):**
- ✅ Git push 정상 완료
- ✅ 로컬 ↔ GitHub 파일 일치 확인
- ✅ 배포된 페이지 실제 작동 확인 (마스터보드 인덱스 / 카드 / 타임라인 / 하위 페이지 정상)

## 📅 다음에 할 일

- (선택) GitHub 저장소 이름을 `Hyunnn135/dashbord` → `Hyunnn135/masterboard`로 변경 (오타 + 명칭 일치). 그 후 `git remote set-url origin ...`로 로컬 remote 갱신
- (선택) maxout 폴더 git init + 별도 GitHub 저장소 생성 — 코드 작업 시작 시점에 결정
- masterboard/index.html 포트폴리오 타임라인에 자동으로 devlog 미리보기 표시하는 방안 (추후)

## 💭 느낀 점

- 프로젝트가 3개로 늘어난 시점에 규칙을 단일화한 건 적절한 타이밍. 매번 "이걸 어디에 적느냐"로 망설이는 비용이 사라짐.
- 일반명사를 고유명사로 바꾼 결정은 비용 대비 효과가 큼. 한 번의 대규모 리네이밍으로 앞으로 모든 대화의 모호성을 제거. "max out" 메타포가 진보적 과부하 컨셉과 자연스럽게 맞아떨어지는 것도 부수효과.
- "메모리 의존 금지, 파일이 주" 원칙은 대화 세션이 바뀌어도 흔들리지 않게 해주는 안전장치. 메모리는 인덱스 역할에 집중하고, 진실은 파일에서 읽도록.
- sed 일괄 치환은 빠르지만 위험. 사전에 영향 범위 grep으로 한 번 살펴본 게 결정적이었음 (salarykorea CSS `.dashboard` 클래스를 보호할 수 있었음).
