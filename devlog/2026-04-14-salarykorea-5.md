# salarykorea 2026-04-14 — 계산기 3개 페이지 롤아웃 (AI 내성 레이어 확장)

> 작업 시간: 오후 세션 (4번째 연속 세션)
> 분류: #기능추가 #패턴확장 #수익화

## 📌 오늘 한 일

### 1. 파일럿 패턴을 3개 페이지로 확장

오전에 income-tax.html에서 검증된 AI 내성 레이어 풀패키지를 3개 계산기에 동일하게 적용했다. 파일럿 패턴이 신선할 때 확장하는 게 맞다고 판단해 같은 날 이어서 진행.

- **freelancer-tax.html** — 프리랜서 3.3% 세금 계산기
- **year-end-tax.html** — 연말정산 계산기
- **medical-tax.html** — 의료비 세액공제 계산기

### 2. 각 페이지 공통 작업 (파일럿 복제)

- `<div id="captureTarget">` 로 결과 영역(result-hero + breakdown-card) 래핑
- `<div class="capture-meta capture-only" id="captureMeta">` 삽입 (캡처 시에만 노출)
- `.result-actions` 4버튼 (PDF 저장 / 이미지 저장 / 링크 복사 / 인쇄) 추가
- `calculate()` 함수 끝에 captureMeta 채우는 코드 + `TrustLayer.show('resultActions')` 호출
- 파일 하단에 `trust-layer.js` 스크립트 태그 + `TrustLayer.bind({ ... })` 호출

### 3. 페이지별 captureMeta 맞춤 (입력 필드 구조가 달라서 페이지마다 다름)

- **freelancer-tax**: 월간 계약금액 · 연간 수입 · 필요경비율 · 소득유형(단순/기준) · 부양가족 · 원천징수액
- **year-end-tax**: 총급여 · 부양가족 · 자녀 세액공제 · 신용·체크카드 등 지출 합계 · 의료·교육·보험·기부·월세 합계 · 연금저축+IRP 합계 · 기납부세액
- **medical-tax**: 총급여 · 본인 의료비 · 65세↑·장애인 · 부양가족 의료비 · 난임시술비 · 실비보험 수령액 · 실비 차감 후 합계 · 최저사용액(3%)

### 4. 페이지별 references/disclaimer 카피라이팅

법령 조항 인용을 각 계산기 도메인에 맞춰 작성:

- **freelancer-tax**: 소득세법 제127조(원천징수의무) · 제129조(원천징수세율)
- **year-end-tax**: 소득세법 제47조(근로소득공제) · 제59조의2~59조의4(세액공제)
- **medical-tax**: 소득세법 제59조의4 제2항 (의료비 세액공제)

공통: 국세청 홈택스 안내 + 2026년 개정세법 해설 (기획재정부) + disclaimer.

### 5. 기존 saveImage() 로직 제거

year-end-tax와 medical-tax는 이전에 자체 구현한 단순 saveImage() 함수를 가지고 있었음 (html2canvas 직접 사용). 이는 trust-layer.js로 통합·대체되므로 함수 제거 + UI 버튼 위치도 결과 영역으로 통일. 기존 카카오 공유 버튼은 그대로 유지.

## 🤔 결정 사항

### 진행 방식: 전체 일괄 vs 단계별 → 단계별(②) 선택

사용자가 "계산기마다 입력 필드 구조가 달라서 captureMeta 내용도 페이지마다 다름 / 각 페이지의 references/disclaimer 카피라이팅 품질"을 먼저 검증하고 싶다는 이유로 ②(단계별, 3개 먼저) 선택. 타당한 판단 — 각 페이지마다 `cm-grid` 에 들어갈 필드가 6~8개 범위에서 달라졌고, references 법령도 계산 도메인마다 다름. 한번에 14개 하면 품질 편차 일어나기 쉬운 영역.

### medical-tax의 기존 `captureArea` 처리 → rename 결정

medical-tax.html에는 이미 `<div id="captureArea" style="display:none;">` 가 있었음. 파일럿과 ID 일관성을 위해 `captureTarget` 으로 rename (3군데 수정). rename 리스크 적고, 후속 유지보수 비용 큼.

### `display:none` 처리 방식

captureArea는 기존에 wrapper div에 `style="display:none"` 을 주고 calculate()에서 동적으로 'block'으로 바꿨음. 하지만 자식 요소(resultCard, breakdownCard)가 각각 `.show` 클래스로 제어되므로 wrapper의 display:none은 불필요. 제거해서 단순화.

## 🐛 문제와 해결 과정

### 3개 페이지 1차 검증 중 발견한 2개 이슈 (같은 세션에서 함께 수정)

**1. HTML 주석 이스케이프 버그** — `<!-- FAQ Section -->` 이 아니라 `<\!-- FAQ Section -->` 로 잘못 들어가 있어서 브라우저가 주석으로 인식 못 하고 텍스트로 렌더링됨. 웹 페이지에서도 인쇄에서도 `<!-- FAQ Section -->` 이라는 문자열이 그대로 보이는 증상. 원인은 과거 sed/셸 스크립트에서 `!` 를 이스케이프한 흔적으로 추정.

- 영향 범위: 11개 파일 (holiday-pay, income-tax, minimum-wage, insurance, salary-table, unemployment, silbi, retirement, index, freelancer-tax, medical-tax)
- 해결: 일괄 `sed -i 's/<\\!-- FAQ Section -->/<!-- FAQ Section -->/'` 로 11개 파일 한 번에 치환
- 검증: `grep -r '<\\!--' --include='*.html'` 결과 0건

**2. 인쇄 결과 중간 애매한 끊김 + 불필요한 영역 인쇄됨** — `window.print()` 가 페이지 전체를 인쇄하니 입력 폼, 하단 info-card, FAQ, 광고까지 다 찍히고 결과 영역이 중간에 페이지 넘김으로 잘림.

- 해결: `common.css` 의 `@media print` 블록을 대폭 강화
  - 숨김 대상 확대: `.page-header`, `.bottom-grid`, `.info-card`, `.faq-item`, `.ad-wrap`, `.result-placeholder`, `.trust-badge` 전부 `display: none`
  - 입력 컬럼 숨김: `.dashboard > div:first-child { display: none }` (모든 계산기가 입력→결과 2컬럼 구조라는 전제)
  - 캡처 전용 `captureMeta` 는 인쇄에는 표시 (+인쇄용 별도 스타일: 테두리/여백/cm-row 도트 구분선)
  - `result-hero`, `breakdown-card`, `sources-footer`, `step-row`, `b-item` 에 `page-break-inside: avoid` 추가
  - `@page { margin: 15mm }` 여백 통일
- 결과: 인쇄 시 입력 조건 요약 → 메인 결과 → 상세 내역 순으로 한 흐름으로 나오고 중간 끊김이 큰 블록 단위에서만 발생

## 🔍 검증 결과 (배포 전 — 로컬 검증 대기)

배포 전 로컬 검증 필요:

- [ ] freelancer-tax.html 로컬 열어서 계산 → PDF/이미지/링크/인쇄 4버튼 모두 작동 확인
- [ ] year-end-tax.html 동일
- [ ] medical-tax.html 동일
- [ ] 3개 페이지 captureMeta 출력 필드 노출 품질 확인
- [ ] references·disclaimer 문구 캡처 결과물에 잘 나오는지 확인

## 📅 다음에 할 일

### 즉시

- 3개 페이지 로컬 검증 후 → git push (salarykorea)
- 배포 후 실제 작동 확인

### 4/15~16

- 남은 10개 계산기 롤아웃: gift-tax, acquisition-tax, monthly-salary, salary-table, retirement, insurance, silbi, holiday-pay, unemployment, minimum-wage
- 3개 페이지 검증 결과를 반영해 captureMeta/references 템플릿 미세 조정

## 💭 느낀 점

파일럿 1개에서 3개로 확장하는 작업은 생각보다 가벼웠다. 이유는 명확한데 — `trust-layer.js`가 실제 로직을 모두 흡수하고 있어서 각 페이지에서는 **"어디를 캡처할지(targetId) + 어떤 입력을 보여줄지(captureMeta innerHTML) + 어떤 법령을 인용할지(references)"** 세 가지 설정만 결정하면 됐다. 공통 컴포넌트를 먼저 만들어둔 것의 비용 대비 편익이 이번 세션에서 확인됐다.

다만 captureMeta 채우는 로직이 각 페이지의 `calculate()` 함수 안에 복붙돼 들어가는 구조라, 14개 페이지로 확장하면 로직 변경 시 14군데를 고쳐야 하는 부담이 남음. 추후에 `TrustLayer.bind()` 옵션으로 captureMeta builder 함수를 받는 식으로 리팩터링할 여지는 있지만, 지금 단계에서는 페이지마다 너무 다른 입력 구조 때문에 오히려 각 페이지에 직접 적는 게 단순.

3번째 페이지(medical-tax)에서 기존 saveImage 함수가 이미 있었는데 제거하는 결정을 내리는 데 잠시 멈칫했다. 리팩터링은 항상 **"기존 동작을 그대로 둘까 / 새 패턴으로 대체할까"** 의 판단이 필요한데, 이번엔 trust-layer.js가 기존 saveImage의 상위 호환이고 패턴 일관성이 중요해서 대체로 갔다.
