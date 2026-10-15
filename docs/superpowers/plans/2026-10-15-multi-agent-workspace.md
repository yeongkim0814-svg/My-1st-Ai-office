# 멀티 에이전트 공동 작업 공간 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 설계 문서의 스캐폴드(규약·템플릿·에이전트 정의·진입 파일)를 레포에 만들고, main을 세우고, 라벨·브랜치 보호를 설정한다.

**Architecture:** 코드가 아니라 문서·설정 파일 묶음이다. 검증은 `scripts/check-scaffold.sh`(구조·일관성 검사)가 맡고, 이 스크립트를 먼저 작성해 실패를 확인한 뒤 파일을 채워 통과시킨다. 규약 본문은 `docs/protocol/`에만 쓰고 진입 파일은 얇게 유지한다.

**Tech Stack:** Markdown, GitHub Issue Forms(YAML), GitHub Actions(라벨 동기화 1개, 시크릿 없음), bash, python3+PyYAML(검사 스크립트용, 설치 확인됨)

**Spec:** `docs/superpowers/specs/2026-10-15-multi-agent-workspace-design.md`

## Global Constraints

- 규약 원본은 `docs/protocol/`에만 둔다. 진입 파일(`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`)은 각 20줄 이하.
- 진입 파일 본문은 "① `docs/protocol/README.md`를 먼저 읽는다 ② 자기 역할은 `agents/<이름>.md` ③ 작업은 Issue에서 시작한다"를 일반 문장으로 말한다. 임포트 문법에 의존하지 않는다.
- 브랜치명: `<에이전트>/<이슈번호>-슬러그`. 상태 라벨은 `status:*` 하나로만 표시한다.
- 상태 값: `ready`, `in-progress`, `review`, `changes-requested`, `done`, `blocked`.
- 병합은 사용자만 한다. main 직접 push 금지. 작성자≠검토자(Claude 포함).
- Issue 템플릿 "수정 가능 경로" 칸은 한 줄에 경로 하나, 필수 입력.
- 보호 경로: `docs/protocol/`, `agents/`, `.github/`, 진입 파일 3종.
- 레포 공개 여부 미확정 → 보안 규칙은 공개 레포 기준. 시크릿은 커밋하지 않는다.
- 문서 언어는 한국어. 커밋 메시지 끝에 세션 attribution 두 줄을 붙인다.

## Review Focus

1. 기본 브랜치가 `main`이 아님(현재 원격에 작업 브랜치만 있음) → Task 1이 main을 만들고 기본 브랜치를 바꾼다. PR의 base가 맞는지 확인.
2. 규약·템플릿이 `labels.yml`에 없는 라벨 이름을 참조 → 검사 스크립트가 교차 검증(Task 2의 check 5).
3. 진입 파일이 시간이 지나며 20줄을 넘어 규약이 복제됨 → check 3이 줄 수와 `docs/protocol/README.md` 참조를 강제.
4. Issue의 "수정 가능 경로"가 비었거나 형식이 틀림 → 템플릿 필수 입력 + check 4.
5. 에이전트가 진입 파일을 읽지 않는 환경(웹 앱) → 표준 지시문이 Issue 템플릿 안내와 `docs/protocol/README.md`에 모두 있어야 함(check 6).

---

### Task 1: main 브랜치 확립

현재 원격에는 `ccr-db18b917-hpg6xi`만 있다(빈 레포에서 처음 push한 브랜치라 기본 브랜치일 가능성이 높다). 스캐폴드 PR의 base가 필요하다.

**Files:** 없음(원격 브랜치 작업)

**Interfaces:**
- Produces: 원격 `main` 브랜치(설계 문서 커밋 `3feca6c` 지점)와 그것이 기본 브랜치라는 상태. 이후 모든 PR의 base.

- [ ] **Step 1: 기본 브랜치 확인** — 레포 정보에서 default branch 이름을 읽는다. Expected: `ccr-db18b917-hpg6xi`(다르면 그 이름을 기록하고 다음 단계의 지점을 맞춘다).
- [ ] **Step 2: `main` 생성** — 현재 HEAD(`3feca6c`)에서 `main`을 만든다(GitHub MCP `create_branch`).
- [ ] **Step 3: 기본 브랜치 변경 요청** — 이 단계는 사용자가 GitHub 웹에서 한다: Settings → Branches → Default branch를 `main`으로. 안내 문구를 사용자에게 전달하고 완료 확인을 받는다.
- [ ] **Step 4: 검증** — 레포 정보에서 default branch가 `main`인지 다시 확인. Expected: `main`.

### Task 2: 검사 스크립트 (먼저 실패시킨다)

**Files:**
- Create: `scripts/check-scaffold.sh`

**Interfaces:**
- Produces: `bash scripts/check-scaffold.sh` — 모든 검사 통과 시 종료 코드 0과 `OK: N checks passed`, 실패 시 실패한 check 번호·이유를 출력하고 종료 코드 1. 이후 모든 Task의 검증 명령.

- [ ] **Step 1: 스크립트 작성** — `set -euo pipefail`. 레포 루트에서 실행. 모든 check를 돌린 뒤 실패 목록을 모아 한 번에 출력. 검사 항목:
  1. 필수 파일 존재: `AGENTS.md CLAUDE.md GEMINI.md`, `.github/ISSUE_TEMPLATE/task.yml`, `.github/ISSUE_TEMPLATE/config.yml`, `.github/pull_request_template.md`, `.github/labels.yml`, `.github/workflows/sync-labels.yml`, `docs/protocol/{README,lifecycle,handoff,conflicts}.md`, `agents/{_template,claude,codex,gemini}.md`, `docs/decisions/README.md`, `projects/.gitkeep`
  2. YAML 파싱: `task.yml`, `config.yml`, `labels.yml`, `sync-labels.yml`을 `python3 -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))"`로 파싱.
  3. 진입 파일 3종: 각 20줄 이하이고 문자열 `docs/protocol/README.md`를 포함.
  4. `task.yml`의 `body` 중 id가 `paths`인 항목이 `validations.required: true`이고 label에 "한 줄에 경로 하나"를 포함.
  5. 교차 검증: `docs/`, `agents/`, `.github/ISSUE_TEMPLATE/`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`에서 `` `(agent|status|type):[a-z-]+` `` 형태로 언급된 모든 라벨이 `labels.yml`의 name 목록에 존재(설계 문서 `docs/superpowers/`는 제외).
  6. 표준 지시문 문자열 `AGENTS.md를 읽고 Issue #`가 `docs/protocol/README.md`와 `.github/ISSUE_TEMPLATE/task.yml` 양쪽에 존재.
  7. `agents/` 아래 `_template.md`를 제외한 각 파일이 필수 섹션 헤딩 `## 강점`, `## 맡기지 말 일`, `## 쓰기 허용 경로`, `## 브랜치 접두어`, `## 기동 방법`, `## 관찰 기록`을 모두 포함(`_template.md`도 동일).
  8. 시크릿 의심 패턴(`AIza[0-9A-Za-z_-]{20,}`, `sk-[A-Za-z0-9]{20,}`, `ghp_[A-Za-z0-9]{20,}`)이 추적 파일에 없음.
- [ ] **Step 2: 실행해 실패 확인** — Run: `bash scripts/check-scaffold.sh; echo "exit=$?"`. Expected: check 1 실패(파일 없음) 목록 출력, `exit=1`.
- [ ] **Step 3: 커밋** — `git add scripts/check-scaffold.sh` / `git commit -m "test: 스캐폴드 검사 스크립트 추가(실패 상태)"`.

### Task 3: 규약 문서 (`docs/protocol/`, `docs/decisions/`)

**Files:**
- Create: `docs/protocol/README.md`, `lifecycle.md`, `handoff.md`, `conflicts.md`, `docs/decisions/README.md`, `projects/.gitkeep`

**Interfaces:**
- Consumes: 설계 문서 §3~§6, §9의 수명주기·충돌 규칙·표준 지시문.
- Produces: 라벨 이름 체계 `agent:claude|codex|gemini`, `status:ready|in-progress|review|changes-requested|done|blocked`, `type:feature|refactor|fix|docs` (Task 4·5·6이 이 이름을 그대로 사용). 표준 지시문 `AGENTS.md를 읽고 Issue #N을 수행하라.` 인수인계 메모 형식(handoff.md).

- [ ] **Step 1: `README.md`** — 한 장 요약: 흐름 7단계, 라벨 체계, 표준 지시문(위 문자열 정확히), 각 문서로의 링크, "규약 수정은 해당 Issue로만"을 포함.
- [ ] **Step 2: `lifecycle.md`** — 설계 §4의 7단계를 규칙 형태로(필수 항목, 상태 전이 표, blocked 처리, Claude 두 모드와 우선순위, 구독으로 깨어나는 방식). 토큰·컨텍스트 3층(§5)을 "Issue는 자기완결형, 규모(S·M·L)와 예산 메모, 한 세션 안에 끝나는 크기" 지침으로 포함.
- [ ] **Step 3: `handoff.md`** — PR 보고 양식 항목(요약 / 변경 파일 / 검증 결과 / 가정·미해결)의 작성 규칙과 반려 기준("확인했다"만 쓴 검증 결과는 반려, 실행 못 한 것은 "미실행"). 세션 중단 시 Issue 댓글용 인수인계 메모 양식(완료한 것 / 남은 것 / 막힌 점 / 다음 한 걸음) 포함.
- [ ] **Step 4: `conflicts.md`** — 설계 §6의 11개 규칙을 번호 그대로, 보호 경로 목록 포함.
- [ ] **Step 5: `docs/decisions/README.md`** — ADR 작성법 5줄(제목, 날짜, 맥락, 결정, 결과)과 첫 항목 후보 목록(`lane:direct` 검토). `projects/.gitkeep`은 빈 파일.
- [ ] **Step 6: 검증** — Run: `bash scripts/check-scaffold.sh`. Expected: check 1의 `docs/protocol/*`, `docs/decisions`, `projects` 관련 실패가 사라지고, 나머지 실패는 Task 4~6 대상 파일뿐.
- [ ] **Step 7: 커밋** — `git add docs projects` / `git commit -m "docs: 협업 규약(protocol) 추가"`.

### Task 4: GitHub 템플릿과 라벨

**Files:**
- Create: `.github/ISSUE_TEMPLATE/task.yml`, `.github/ISSUE_TEMPLATE/config.yml`, `.github/pull_request_template.md`, `.github/labels.yml`, `.github/workflows/sync-labels.yml`

**Interfaces:**
- Consumes: Task 3의 라벨 이름 체계와 표준 지시문.
- Produces: `labels.yml`(라벨 name/color/description 목록 13개: agent 3 + status 6 + type 4), Issue Form 필드 id `type, size, goal, paths, done, verify, depends, budget`.

- [ ] **Step 1: `labels.yml`** — 위 13개 라벨. 각 항목 `name`, `color`(6자리 hex, 그룹별 동일 계열), `description`.
- [ ] **Step 2: `task.yml`** — Issue Form. 필드: `type`(dropdown: feature/refactor/fix/docs), `size`(dropdown: S/M/L), `goal`(textarea, 필수), `paths`(textarea, 필수, label에 "수정 가능 경로 (한 줄에 경로 하나)"), `done`(textarea, 필수), `verify`(textarea, 필수), `depends`(input, 선택, 예 `#12`), `budget`(textarea, 선택). 상단 `markdown` 블록에 표준 지시문 `AGENTS.md를 읽고 Issue #N을 수행하라.`와 핵심 규칙 3줄(브랜치명, 경로 제한, 검증 결과 첨부)을 넣는다.
- [ ] **Step 3: `config.yml`** — `blank_issues_enabled: false`.
- [ ] **Step 4: `pull_request_template.md`** — `Closes #` 줄과 handoff.md의 4항목 헤딩(요약 / 변경 파일 / 검증 결과 / 가정·미해결)과 "자기 PR은 자기가 검토하지 않음" 체크박스.
- [ ] **Step 5: `sync-labels.yml`** — 트리거 `workflow_dispatch`와 `push`(branches: main, paths: `.github/labels.yml`). `permissions: issues: write, contents: read`. `actions/checkout@v4` 후, `labels.yml`을 읽어 각 라벨에 `gh label create "$name" --color "$color" --description "$desc" --force`를 실행(`GH_TOKEN: ${{ github.token }}`). 시크릿 사용 없음.
- [ ] **Step 6: 검증** — Run: `bash scripts/check-scaffold.sh`. Expected: check 2, 4, 5(템플릿 범위)와 `.github` 관련 check 1 통과. 남은 실패는 `agents/`와 진입 파일.
- [ ] **Step 7: 커밋** — `git add .github` / `git commit -m "feat: Issue/PR 템플릿과 라벨 정의, 라벨 동기화 워크플로 추가"`.

### Task 5: 에이전트 정의

**Files:**
- Create: `agents/_template.md`, `agents/claude.md`, `agents/codex.md`, `agents/gemini.md`

**Interfaces:**
- Consumes: Task 3·4의 라벨 이름과 표준 지시문.
- Produces: 각 파일이 헤딩 `## 강점`, `## 맡기지 말 일`, `## 쓰기 허용 경로`, `## 브랜치 접두어`, `## 기동 방법`, `## 관찰 기록`을 가짐. 브랜치 접두어 `claude/`, `codex/`, `gemini/`.

- [ ] **Step 1: `_template.md`** — 위 6개 헤딩과 각 헤딩 아래 한 줄 작성 가이드, 상단에 "새 에이전트 추가 4단계(이 파일 복사 → 진입 파일 → `agent:<이름>` 라벨 → 브랜치 접두어)".
- [ ] **Step 2: `claude.md`** — 지휘/구현 두 모드와 우선순위(지휘 먼저), 자기 PR 자기 검토 금지, 사용자가 세션을 열어 시작하고 PR 구독으로 검토 이벤트를 받는다는 기동 방법. 강점은 "가설"이라고 명시.
- [ ] **Step 3: `codex.md`, `gemini.md`** — 기동 방법: Gemini는 "Jules 웹 앱에서 레포 연결 후 표준 지시문 입력, 보조 리뷰어로 Gemini Code Assist 앱(`/gemini review`)", Codex는 "웹/클라우드에서 레포 연결 후 표준 지시문 입력". 강점은 가설, 관찰 기록은 빈 표 헤더만(날짜 / Issue / 규약 준수 / 범위 이탈 / 검증의 정직성).
- [ ] **Step 4: 검증** — Run: `bash scripts/check-scaffold.sh`. Expected: check 7 통과. 남은 실패는 진입 파일 3종뿐.
- [ ] **Step 5: 커밋** — `git add agents` / `git commit -m "docs: 에이전트 정의와 등록 양식 추가"`.

### Task 6: 진입 파일과 전체 통과

**Files:**
- Create: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`

**Interfaces:**
- Consumes: Task 3의 `docs/protocol/README.md` 경로와 Task 5의 `agents/<이름>.md`.

- [ ] **Step 1: `AGENTS.md`(공통)** — 20줄 이하: 이 레포가 다중 에이전트 협업 공간이라는 한 줄, ① `docs/protocol/README.md`를 먼저 읽는다 ② 자기 역할은 `agents/<이름>.md` ③ 작업은 Issue에서 시작하고 Issue에 없는 일은 하지 않는다, 선언된 수정 가능 경로 밖은 건드리지 않는다.
- [ ] **Step 2: `CLAUDE.md`** — 20줄 이하: `AGENTS.md`를 먼저 읽으라는 문장, 역할은 `agents/claude.md`, 지휘 처리가 구현보다 우선.
- [ ] **Step 3: `GEMINI.md`** — 20줄 이하: `AGENTS.md`를 먼저 읽으라는 문장, 역할은 `agents/gemini.md`.
- [ ] **Step 4: 전체 검증** — Run: `bash scripts/check-scaffold.sh; echo "exit=$?"`. Expected: `OK: 8 checks passed`, `exit=0`.
- [ ] **Step 5: 커밋** — `git add AGENTS.md CLAUDE.md GEMINI.md` / `git commit -m "docs: 에이전트 진입 파일 추가"`.

### Task 7: 보고와 사용자 설정 (PR 포함)

**Interfaces:**
- Consumes: Task 1의 `main`, Task 2~6의 커밋이 쌓인 `ccr-db18b917-hpg6xi`.

- [ ] **Step 1: 브랜치 push** — `git push -u origin ccr-db18b917-hpg6xi`.
- [ ] **Step 2: PR 생성** — base `main`, head `ccr-db18b917-hpg6xi`. 본문에 변경 요약과 `bash scripts/check-scaffold.sh` 출력 첨부. **사용자의 명시적 승인 후에만 생성한다.**
- [ ] **Step 3: 사용자 설정 안내** (사용자가 태블릿 GitHub 웹에서 수행, 각 단계 완료 확인):
  1. PR 병합.
  2. Actions 탭 → `sync-labels` → Run workflow(라벨 13개 생성). 확인: Issues → Labels에 13개.
  3. Settings → Branches → `main` 보호 규칙: Require a pull request before merging 체크, 직접 push 차단.
  4. Jules/Codex에서 레포 연결 확인.
- [ ] **Step 4: 첫 시험 Issue 작성** — 설계 §9의 smoke test Issue를 템플릿에 맞춰 작성: 수정 가능 경로 `projects/_smoke/hello-jules.md`, 담당 `agent:gemini`. 사용자가 Jules에 표준 지시문으로 지시하고, 결과를 관찰 항목 5개 기준으로 `agents/gemini.md` 관찰 기록에 남긴다(별도 PR).
