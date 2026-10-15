#!/usr/bin/env bash
# 협업 스캐폴드 구조·일관성 검사. 레포 어디서 실행해도 루트 기준으로 동작한다.
set -uo pipefail
cd "$(git rev-parse --show-toplevel)"

FAILS=()
CHECKS=8
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

# 6. 표준 지시문이 README와 Issue 템플릿 양쪽에 있는가
for f in docs/protocol/README.md .github/ISSUE_TEMPLATE/task.yml; do
  [ -f "$f" ] && { grep -qF 'AGENTS.md를 읽고 Issue #' "$f" || fail 6 "standard instruction missing in $f"; }
done

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
   | xargs -0 grep -IlE 'AIza[0-9A-Za-z_-]{20,}|sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}' 2>/dev/null | grep -q .; then
  fail 8 "possible secret found in tracked files"
fi

if [ ${#FAILS[@]} -gt 0 ]; then
  printf 'FAIL: %s\n' "${FAILS[@]}"
  exit 1
fi
echo "OK: $CHECKS checks passed"
