# salarykorea 2026-04-14 — AI 내성 레이어 공통 컴포넌트 구현 + income-tax 파일럿 적용

> 작업 시간: 저녁 세션
> 분류: #기능추가 #구현 #파일럿
> 프로젝트: salarykorea

## 📌 오늘 한 일

### 1) 공통 CSS 컴포넌트 추가 (`common.css`)
- 파일 끝에 "AI 내성 레이어" 섹션(약 200줄) 추가.
- **`.trust-badge`** — 상단 검증 배지 (초록 알약). 도트 + "2026년 개정 세법 기준 · 최종 업데이트 YYYY.MM.DD · ⓘ".
- **`.result-actions` + `.ra-btn`** — 결과 카드 아래 저장/공유 버튼 그룹. PDF · 이미지 · 링크복사 · 인쇄.
- **`.ra-toast`** — 복사·저장 후 피드백 토스트.
- **`.sources-footer`** — 하단 출처 박스 (법령/고시 링크, 경고 노트, changelog).
- **`@media print`** — 인쇄 시 nav/광고/article-card 숨김, 결과 영역 흑백 테두리로 재스타일.

### 2) `trust-layer.js` 신규 작성 (루트 경로)
- html2canvas + jsPDF를 **버튼 클릭 시점 lazy-load**. 페이지 초기 로딩 영향 0.
- `TrustLayer.bind({ targetId, actionsId, filename, shareParams })` API.
- 기능: `saveAsPDF` · `saveAsImage` · `copyShareURL`(clipboard + execCommand fallback) · `print` · `toast`.
- 긴 결과도 여러 페이지로 분할 저장하는 간단한 페이지 분할 로직 포함.

### 3) 파일럿 페이지: `income-tax.html` 패치
- **Trust Badge**: 페이지 제목 바로 아래 삽입.
- **captureTarget div**로 resultHero + detailCard + bookkeepingCard 감싸기 → PDF/이미지 저장 대상 지정.
- **Result Actions** 버튼 그룹을 result-col 내부, 캡처 영역 밖에 배치.
- **Sources Footer** 섹션 추가 — 소득세법 55조, 업종별 경비율 고시, 인적공제 기준, 기장의무 구분의 4개 출처 명시 + 주의 노트 + changelog.
- **공유 링크 복원 로직** 추가: `?income=...&type=...&rate=...&dependents=...&prepaid=...` URL 파라미터로 오면 입력값 자동 채움 후 자동 계산 실행.
- **계산 완료 시점**에 `TrustLayer.show('resultActions')` 호출로 저장 버튼 등장.

### 4) 컨텍스트·마스터보드 반영
- `PROJECT-CONTEXT.md` — #11·#12·#13 상태 ✅ 완료로 갱신 (t29는 "배포 후 실제 작동 검증 대기"로 세분화).
- `masterboard/project-data.json` — t28·t29 `done: true`.

## 🤔 결정 사항

- **lazy-load 선택**: html2canvas(~200KB) + jsPDF(~300KB)를 defer로도 초기 로드하지 않음. 버튼 클릭 시점에만 CDN에서 가져오도록 해서 애드센스 승인 심사 중인 지금 **페이지 속도(LCP, FID)** 영향 없게.
- **captureTarget 범위**: Kakao 공유 버튼(.action-row)과 Result Actions는 **캡처 영역 밖**에 두어서 저장된 PDF/이미지에 버튼이 찍히지 않도록.
- **공유 링크 형태**: 세션 고유 URL이 아니라 **쿼리 파라미터로 평문 인코딩**. 서버 없이도 작동 + 사용자가 URL 보고 이해 가능.
- **checkbox 상태(세액감면)는 공유 파라미터에서 제외**: 파라미터 개수가 너무 많아지면 링크 지저분해서 MVP에서는 핵심 5개(income, type, rate, dependents, prepaid)만.
- **"검증 방법" anchor**: `about.html#verification` 으로 링크. 해당 섹션은 아직 작성 안 됨 → 후속 작업으로 about.html에 verification 섹션 추가 필요.
- **"ChatGPT 프롬프트 섹션" 공격적 옵션은 의도적으로 제외** — 3축 효과를 깨끗하게 측정하기 위해 변수 분리.

## 🐛 문제와 해결 과정

- 초기 기획 문서(`docs/ai-resistance/components.md`)에서는 `trust-layer.js`를 `<script defer>`로만 불러왔는데, 실제 구현 시 **bind를 DOMContentLoaded에서 실행**해야 확실히 동작. 스크립트 태그만 defer로 두고 초기화는 이벤트 리스너로 분리.
- html2canvas가 result-hero의 그라디언트 배경을 정확히 렌더 못 할 가능성이 있어서 `backgroundColor: "#FFFFFF"` 옵션 + `scale: 2`로 해상도 보정. 실제 배포 후 첫 저장 결과에서 확인 필요.

## 🔍 검증 결과 (로컬)

- 파일 수정/생성 확인:
  - `common.css` 1034줄 → 약 1230줄 (AI 내성 섹션 추가)
  - `trust-layer.js` 신규 (약 220줄)
  - `income-tax.html` 총 3개 구역 패치(배지·캡처래퍼+액션·출처푸터) + 스크립트 2개 블록 추가
- 코드 일관성 확인:
  - `<div id="captureTarget">` 1개 ↔ `</div><!-- /#captureTarget -->` 1개 일치
  - `resultActions` 참조 3곳(HTML, show 호출, bind 설정) 모두 동일 id
- **배포 후 검증 체크리스트** (git push → GitHub Pages 반영 후):
  1. 로컬↔원격 파일 일치
  2. income-tax 페이지 로딩 정상 (console 에러 없음)
  3. Trust Badge 렌더링 확인
  4. 계산 실행 → Result Actions 버튼 등장
  5. PDF 저장 → 파일 다운로드 + 내용 정상
  6. 이미지 저장 → PNG 다운로드 + 결과 카드 정상
  7. 링크 복사 → 클립보드 값 확인
  8. 복사된 링크로 재접속 → 입력값 자동 복원 + 자동 계산
  9. 인쇄 미리보기 → nav·광고 숨김, 결과만 깔끔
  10. Sources Footer 링크 4개 정상 동작

## 📅 다음에 할 일

- **즉시**: 현태님이 git push → 배포 후 위 10항목 체크리스트 실행.
- **검증 후 OK**:
  - (a) `about.html#verification` 섹션 작성 (우리의 검증 방식 설명)
  - (b) 메인 계산기 14개 페이지에 동일 레이어 롤아웃 — 템플릿화해서 페이지당 20~30분
- **검증 후 이슈**:
  - html2canvas가 그라디언트/이모지 못 그리면 result-hero를 캡처 전용 모드로 일시 교체하는 로직 추가
- **중기**: PDF 기획안 v2 리라이트 ("긴 글" → "가이드 50% + 워크시트 50%" 구조)

## 💭 느낀 점

- 기획 문서를 먼저 쓴 덕분에 구현이 **매우 빠르고 흔들림 없이** 진행됐다. components.md의 HTML/CSS 스펙을 그대로 common.css에 옮기기만 하면 됐음 — 계획이 곧 시간을 산다는 말의 실제 사례.
- `captureTarget` 래퍼를 만든 것이 의외로 설계의 핵심. 이걸로 "PDF/이미지에 찍힐 것"과 "찍히지 말아야 할 UI 컨트롤"을 깔끔하게 분리. 롤아웃 시 다른 페이지도 같은 패턴으로 찍어낼 수 있음.
- lazy-load는 단순한 최적화를 넘어, **애드센스 심사 중인 지금 속도 지표를 지키는 방어 장치**. 승인 심사 기간에 로딩이 느려지는 건 재앙이므로 이게 합리적.
- 공유 링크에 입력값을 쿼리로 심는 건 서버 없이 가능한 가장 낮은 비용의 "상태 보존" 솔루션. AI 채팅이 줄 수 없는 것 — **"이 계산을 다시 열어볼 수 있음"**.
