#!/usr/bin/env bash
# 협업 스캐폴드 구조·일관성 검사. 레포 어디서 실행해도 루트 기준으로 동작한다.
set -uo pipefail
cd "$(git rev-parse --show-toplevel)"

FAILS=()
CHECKS=12
fail() { FAILS+=("check $1: $2"); }

# 1. 필수 파일 존재
REQUIRED=(
  AGENTS.md CLAUDE.md GEMINI.md
  .github/ISSUE_TEMPLATE/task.yml .github/ISSUE_TEMPLATE/config.yml
  .github/pull_request_template.md .github/labels.yml
  .github/workflows/sync-labels.yml
  docs/protocol/README.md docs/protocol/lifecycle.md
  docs/protocol/handoff.md docs/protocol/conflicts.md
  agents/_template.md agents/claude.md agents/codex.md agents/gemini.md
  docs/decisions/README.md projects/.gitkeep
)
for f in "${REQUIRED[@]}"; do
  [ -f "$f" ] || fail 1 "missing file: $f"
done

# 2. YAML 파싱
for f in .github/ISSUE_TEMPLATE/task.yml .github/ISSUE_TEMPLATE/config.yml \
         .github/labels.yml .github/workflows/sync-labels.yml; do
  [ -f "$f" ] || continue
  python3 -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" "$f" 2>/dev/null \
    || fail 2 "invalid YAML: $f"
done

# 3. 진입 파일: 20줄 이하 + 규약 README 참조
for f in AGENTS.md CLAUDE.md GEMINI.md; do
  [ -f "$f" ] || continue
  [ "$(wc -l < "$f")" -le 20 ] || fail 3 "$f exceeds 20 lines"
  grep -q 'docs/protocol/README.md' "$f" || fail 3 "$f does not reference docs/protocol/README.md"
done

# 4. Issue 템플릿의 paths 필드: 필수 + 형식 안내
if [ -f .github/ISSUE_TEMPLATE/task.yml ]; then
  python3 - <<'PY' || fail 4 "task.yml paths field must be required and say '한 줄에 경로 하나'"
import yaml, sys
d = yaml.safe_load(open(".github/ISSUE_TEMPLATE/task.yml"))
for b in d.get("body", []):
    if b.get("id") == "paths":
        ok = b.get("validations", {}).get("required") is True \
             and "한 줄에 경로 하나" in b.get("attributes", {}).get("label", "")
        sys.exit(0 if ok else 1)
sys.exit(1)
PY
fi

# 5. 문서가 언급하는 라벨이 labels.yml에 정의되어 있는가
if [ -f .github/labels.yml ]; then
  DEFINED=$(python3 -c "import yaml; print('\n'.join(l['name'] for l in yaml.safe_load(open('.github/labels.yml'))))" 2>/dev/null)
  SCAN=()
  for p in docs/protocol docs/decisions agents .github/ISSUE_TEMPLATE AGENTS.md CLAUDE.md GEMINI.md; do
    [ -e "$p" ] && SCAN+=("$p")
  done
  if [ ${#SCAN[@]} -gt 0 ]; then
    while IFS= read -r ref; do
      grep -qxF "$ref" <<<"$DEFINED" || fail 5 "label referenced but not defined: $ref"
    done < <(grep -rhoE '`(agent|status|type):[a-z-]+`' "${SCAN[@]}" 2>/dev/null | tr -d '`' | sort -u)
  fi
fi

# 6. 표준 지시문: README에 있고, Issue 템플릿에서는 제출되는 본문(markdown 타입 제외)에 있어야 한다
grep -qF 'AGENTS.md를 읽고 Issue #' docs/protocol/README.md 2>/dev/null \
  || fail 6 "standard instruction missing in docs/protocol/README.md"
if [ -f .github/ISSUE_TEMPLATE/task.yml ]; then
  python3 - <<'PY' || fail 6 "standard instruction must be inside a submitted (non-markdown) field of task.yml"
import yaml, sys, json
d = yaml.safe_load(open(".github/ISSUE_TEMPLATE/task.yml"))
ok = any(b.get("type") != "markdown" and "AGENTS.md를 읽고 Issue #" in json.dumps(b, ensure_ascii=False)
         for b in d.get("body", []))
sys.exit(0 if ok else 1)
PY
fi

# 7. 에이전트 파일의 필수 섹션
for f in agents/*.md; do
  [ -f "$f" ] || continue
  for h in '## 강점' '## 맡기지 말 일' '## 쓰기 허용 경로' '## 브랜치 접두어' '## 기동 방법' '## 관찰 기록'; do
    grep -qF "$h" "$f" || fail 7 "$f missing heading: $h"
  done
done

# 8. 시크릿 의심 패턴 (이 스크립트 자신은 제외)
if git ls-files -z --cached --others --exclude-standard \
   | grep -zv '^scripts/check-scaffold.sh$' \
   | xargs -0 grep -IlE 'AIza[0-9A-Za-z_-]{20,}|sk-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}' 2>/dev/null | grep -q .; then
  fail 8 "possible secret found in tracked files"
fi

# 9. 워크플로 안전: sync-labels의 run 단계는 shell: bash(pipefail), pull_request_target 금지
if [ -f .github/workflows/sync-labels.yml ]; then
  python3 - <<'PY' || fail 9 "sync-labels.yml run steps must set 'shell: bash'"
import yaml, sys
d = yaml.safe_load(open(".github/workflows/sync-labels.yml"))
steps = [s for j in d["jobs"].values() for s in j["steps"] if "run" in s]
sys.exit(0 if steps and all(s.get("shell") == "bash" for s in steps) else 1)
PY
fi
if grep -rlE 'pull_request_target' .github/workflows 2>/dev/null | grep -q .; then
  fail 9 "pull_request_target is not allowed in workflows (public repo)"
fi

# 10. 진입 파일·규약 본문에 특정 에이전트 목록을 박지 않는다 (에이전트 추가 시 본문이 바뀌지 않도록)
HARD=$(grep -rnE 'agent:(claude|codex|gemini)|agents/(claude|codex|gemini)\.md' AGENTS.md docs/protocol 2>/dev/null)
[ -z "$HARD" ] || fail 10 "hard-coded agent names in protocol/entry: $(echo "$HARD" | head -1)"

# 11. 공개 레포: 신뢰할 수 없는 입력 규칙이 AGENTS.md와 README에 있어야 한다
for f in AGENTS.md docs/protocol/README.md; do
  [ -f "$f" ] && { grep -qF '소유자·협업자' "$f" || fail 11 "untrusted-input rule (소유자·협업자) missing in $f"; }
done

# 12. 문서 우선순위·지휘자용 문서 표시·관찰 기록 작성 주체 (Issue #4)
grep -qF '다른 모든 문서보다 우선' AGENTS.md 2>/dev/null \
  || fail 12 "AGENTS.md must state that the Issue's editable paths override every other document"
grep -qF 'docs/superpowers/' AGENTS.md 2>/dev/null \
  || fail 12 "AGENTS.md must say docs/superpowers/ is for the conductor and is not followed"
grep -qF '지휘자용' docs/superpowers/README.md 2>/dev/null \
  || fail 12 "docs/superpowers/README.md must exist and say it is conductor-only (지휘자용)"
for f in agents/_template.md docs/protocol/handoff.md; do
  grep -qF '관찰 기록은 지휘자가 쓴다' "$f" 2>/dev/null \
    || fail 12 "$f must say '관찰 기록은 지휘자가 쓴다'"
done

if [ ${#FAILS[@]} -gt 0 ]; then
  printf 'FAIL: %s\n' "${FAILS[@]}"
  exit 1
fi
echo "OK: $CHECKS checks passed"
