#!/usr/bin/env python3
"""PR 규칙 검사 (알림 전용, 병합을 막지 않는다). Issue #11.

검사 로직은 순수 함수로 두고(네트워크 없이 시험 가능), 입출력은 main()에 모은다.
PR 본문·브랜치명·Issue 본문은 신뢰하지 않는 입력이므로 셸에 넘기지 않고 이 스크립트에서만 처리한다.
"""
import html
import json
import os
import re
import sys
import urllib.request

MARKER = "<!-- pr-rules-check -->"
PROTECTED = ["docs/protocol/", "agents/", ".github/"]
PROTECTED_FILES = ["AGENTS.md", "CLAUDE.md", "GEMINI.md"]
SLUG = r"[0-9A-Za-z가-힣._-]+"


def parse_issue_paths(body):
    """Issue 본문의 '### 수정 가능 경로' 섹션 줄들을 경로 목록으로 돌려준다."""
    paths, on = [], False
    for line in (body or "").splitlines():
        if line.startswith("### "):
            on = line.strip() == "### 수정 가능 경로"
            continue
        if on:
            p = re.sub(r"^\s*[-*]\s+", "", line).strip().strip("`").strip()
            if p:
                paths.append(p)
    return paths


def parse_prefix(agent_md):
    """agents/<이름>.md의 '## 브랜치 접두어' 섹션에서 첫 `접두어/`를 읽는다."""
    on = False
    for line in (agent_md or "").splitlines():
        if line.startswith("## "):
            on = line.strip() == "## 브랜치 접두어"
            continue
        if on:
            m = re.search(r"`([0-9A-Za-z_-]+)/`", line)
            if m:
                return m.group(1)
    return None


def _res(id_, level, message):
    return {"id": id_, "level": level, "message": message}


def check_branch(branch, prefixes):
    if branch.startswith("ccr-"):
        return _res("branch", "note", f"세션 브랜치 `{branch}`: 규약 형식이 아니지만 위반으로 보지 않는다.")
    m = re.fullmatch(rf"([0-9A-Za-z_-]+)/(\d+)-{SLUG}", branch)
    if m and m.group(1) in prefixes:
        return _res("branch", "ok", f"브랜치명 `{branch}` 형식이 맞다.")
    return _res("branch", "fail", f"브랜치명 `{branch}`이 `<접두어>/<이슈번호>-슬러그` 형식이 아니다 (접두어: {', '.join(prefixes)}).")


def find_closes(body):
    m = re.search(r"\bcloses\s+#(\d+)", body or "", re.IGNORECASE)
    return int(m.group(1)) if m else None


def check_closes(number, issue, auto_generated=False):
    if number is None:
        if auto_generated:
            return _res("closes", "review", "자동 생성 본문이라 `Closes #N`이 없다. 연결된 Issue를 사람이 확인해야 한다.")
        return _res("closes", "fail", "본문에 `Closes #N`이 없다.")
    if issue is None:
        return _res("closes", "fail", f"`Closes #{number}`의 Issue를 찾을 수 없다.")
    return _res("closes", "ok", f"`Closes #{number}`가 있고 Issue가 존재한다.")


def _is_protected(path):
    return path in PROTECTED_FILES or any(path.startswith(p) for p in PROTECTED)


def _covered(path, declared):
    for d in declared:
        if d.endswith("/"):
            if path.startswith(d):
                return True
        elif path == d:
            return True
    return False


def check_scope(files, declared):
    if not declared:
        return _res("scope", "fail", "Issue에 '수정 가능 경로'가 없거나 읽을 수 없다.")
    out = [f for f in files if not _is_protected(f) and not _covered(f, declared)]
    if out:
        return _res("scope", "fail", "Issue의 수정 가능 경로 밖의 파일: " + ", ".join(f"`{f}`" for f in out))
    return _res("scope", "ok", "보호 경로를 제외한 변경 파일이 모두 수정 가능 경로 안에 있다.")


def check_protected(files, declared):
    touched = [f for f in files if _is_protected(f)]
    if not touched:
        return _res("protected", "ok", "보호 경로를 건드리지 않았다.")
    bad = [f for f in touched if not _covered(f, declared)]
    if bad:
        return _res("protected", "fail", "Issue가 선언하지 않은 보호 경로 변경: " + ", ".join(f"`{f}`" for f in bad))
    return _res("protected", "ok", "보호 경로 변경이 Issue에 선언되어 있다.")


def run_checks(pr):
    results = [check_branch(pr["branch"], pr["prefixes"])]
    number = find_closes(pr["body"])
    results.append(check_closes(number, pr["issue"], pr.get("auto_generated", False)))
    if pr["issue"] is None:
        results.append(_res("scope", "skip", "연결된 Issue가 없어 건너뛰었다."))
        results.append(_res("protected", "skip", "연결된 Issue가 없어 건너뛰었다."))
    else:
        declared = parse_issue_paths(pr["issue"].get("body", ""))
        results.append(check_scope(pr["files"], declared))
        results.append(check_protected(pr["files"], declared))
    return results


ICON = {"ok": "✅", "fail": "⚠️", "note": "ℹ️", "review": "🔎", "skip": "⏭️"}


def render_comment(results):
    lines = [
        MARKER,
        "### PR 규칙 검사 (알림)",
        "이 검사는 알림용이며 병합을 막지 않는다. 판단은 검토자와 사용자가 한다.",
        "",
    ]
    for r in results:
        msg = html.escape(r["message"], quote=False).replace("@", "@​")
        lines.append(f"- {ICON.get(r['level'], '•')} **{r['id']}**: {msg}")
    return "\n".join(lines) + "\n"


# --- 입출력 (네트워크) ---------------------------------------------------------

def _api(method, url, token, data=None):
    req = urllib.request.Request(url, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    body = None
    if data is not None:
        body = json.dumps(data).encode()
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, body, timeout=30) as resp:
        return json.load(resp)


def _paged(url, token):
    page, items = 1, []
    while True:
        chunk = _api("GET", f"{url}{'&' if '?' in url else '?'}per_page=100&page={page}", token)
        items.extend(chunk)
        if len(chunk) < 100:
            return items
        page += 1


def load_prefixes(agents_dir="agents"):
    prefixes = []
    for name in sorted(os.listdir(agents_dir)):
        if name.endswith(".md") and not name.startswith("_"):
            with open(os.path.join(agents_dir, name), encoding="utf-8") as f:
                p = parse_prefix(f.read())
            if p:
                prefixes.append(p)
    return prefixes


def main():
    token = os.environ["GH_TOKEN"]
    repo = os.environ["GITHUB_REPOSITORY"]
    number = int(os.environ["PR_NUMBER"])
    api = f"https://api.github.com/repos/{repo}"
    pr = _api("GET", f"{api}/pulls/{number}", token)
    files = [f["filename"] for f in _paged(f"{api}/pulls/{number}/files", token)]
    body = pr.get("body") or ""
    closes = find_closes(body)
    issue = None
    if closes is not None:
        try:
            issue = _api("GET", f"{api}/issues/{closes}", token)
            if "pull_request" in issue:
                issue = None
        except urllib.error.HTTPError:
            issue = None
    info = {
        "branch": pr["head"]["ref"],
        "body": body,
        "files": files,
        "issue": issue,
        "prefixes": load_prefixes(),
        "auto_generated": "created automatically by Jules" in body,
    }
    text = render_comment(run_checks(info))
    comments = _paged(f"{api}/issues/{number}/comments", token)
    mine = [c for c in comments if c["body"].startswith(MARKER) and c["user"]["type"] == "Bot"]
    if mine:
        _api("PATCH", f"{api}/issues/comments/{mine[0]['id']}", token, {"body": text})
    else:
        _api("POST", f"{api}/issues/{number}/comments", token, {"body": text})
    print(text)


if __name__ == "__main__":
    sys.exit(main())
