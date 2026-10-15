import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import pr_rules_check as m  # noqa: E402

PREFIXES = ["claude", "codex", "gemini"]
ISSUE_BODY = """### 목표
x

### 수정 가능 경로
scripts/check-scaffold.sh
scripts/tests/
docs/protocol/README.md

### 완료 조건
1. y
"""


class ParseIssuePaths(unittest.TestCase):
    def test_reads_lines_of_the_section_only(self):
        self.assertEqual(
            m.parse_issue_paths(ISSUE_BODY),
            ["scripts/check-scaffold.sh", "scripts/tests/", "docs/protocol/README.md"],
        )

    def test_missing_section_gives_empty(self):
        self.assertEqual(m.parse_issue_paths("### 목표\nx"), [])

    def test_strips_backticks_and_bullets_and_blank_lines(self):
        body = "### 수정 가능 경로\n- `a/b.md`\n\n* c/\n### 다음\n"
        self.assertEqual(m.parse_issue_paths(body), ["a/b.md", "c/"])


class FormHeading(unittest.TestCase):
    def test_reads_heading_generated_by_issue_form(self):
        # Issue 양식은 필드 label 전체를 제목으로 만든다
        body = "### 목표\nx\n\n### 수정 가능 경로 (한 줄에 경로 하나)\n\nscripts/a.py\nscripts/tests/\n\n### 완료 조건\n1. y"
        self.assertEqual(m.parse_issue_paths(body), ["scripts/a.py", "scripts/tests/"])

    def test_other_headings_with_similar_start_are_not_mixed(self):
        body = "### 수정 가능 경로 메모\nnot/a/path\n### 수정 가능 경로\nreal/path\n"
        self.assertEqual(m.parse_issue_paths(body), ["real/path"])


class Renames(unittest.TestCase):
    def test_collects_new_and_previous_names(self):
        api = [
            {"filename": "scripts/x.yml", "previous_filename": ".github/workflows/x.yml", "status": "renamed"},
            {"filename": "a.md", "status": "modified"},
        ]
        self.assertEqual(m.collect_files(api), ["scripts/x.yml", ".github/workflows/x.yml", "a.md"])

    def test_rename_out_of_protected_path_is_flagged(self):
        files = m.collect_files([{"filename": "scripts/x.yml", "previous_filename": ".github/workflows/x.yml"}])
        r = m.check_protected(files, ["scripts/"])
        self.assertEqual(r["level"], "fail")
        self.assertIn(".github/workflows/x.yml", r["message"])

    def test_no_duplicates(self):
        api = [{"filename": "a", "previous_filename": "a"}]
        self.assertEqual(m.collect_files(api), ["a"])


class BranchIssueMatch(unittest.TestCase):
    def pr(self, branch, body):
        return dict(
            branch=branch, body=body, files=["scripts/check-scaffold.sh"],
            issue={"body": ISSUE_BODY, "author_association": "OWNER"},
            prefixes=PREFIXES, auto_generated=False,
        )

    def test_mismatch_is_fail(self):
        by = {r["id"]: r for r in m.run_checks(self.pr("codex/99-work", "Closes #11"))}
        self.assertEqual(by["branch"]["level"], "fail")
        self.assertIn("99", by["branch"]["message"])
        self.assertIn("11", by["branch"]["message"])

    def test_match_is_ok(self):
        by = {r["id"]: r for r in m.run_checks(self.pr("codex/11-work", "Closes #11"))}
        self.assertEqual(by["branch"]["level"], "ok")

    def test_session_branch_never_mismatches(self):
        by = {r["id"]: r for r in m.run_checks(self.pr("ccr-abc", "Closes #11"))}
        self.assertEqual(by["branch"]["level"], "note")

    def test_branch_number_parser(self):
        self.assertEqual(m.branch_issue_number("claude/11-x"), 11)
        self.assertIsNone(m.branch_issue_number("ccr-abc"))
        self.assertIsNone(m.branch_issue_number("claude/x"))


class MarkdownSafety(unittest.TestCase):
    def test_code_strips_backticks_and_newlines(self):
        out = m.code("a`b\nc\r\td")
        self.assertNotIn("\n", out)
        self.assertNotIn("\r", out)
        self.assertEqual(out.count("`"), 2)  # 감싸는 두 개뿐

    def test_code_truncates_long_values(self):
        self.assertLessEqual(len(m.code("x" * 1000)), 210)

    def test_hostile_filename_cannot_inject_markdown(self):
        evil = "a`\n### 규약 위반 없음 ✅\n`b"
        r = m.check_scope([evil], ["scripts/"])
        text = m.render_comment([r])
        self.assertNotIn("\n### 규약 위반 없음", text)
        self.assertEqual(len([l for l in text.splitlines() if l.startswith("### ")]), 1)  # 제목은 우리 것 하나

    def test_hostile_branch_cannot_inject(self):
        r = m.check_branch("foo`\n- ✅ **x**: fake", PREFIXES)
        text = m.render_comment([r])
        self.assertNotIn("\n- ✅ **x**", text)


class ParsePrefixes(unittest.TestCase):
    def test_reads_prefix_from_agent_definition(self):
        text = "# X\n## 브랜치 접두어\n`codex/` → `codex/<이슈번호>-슬러그`\n## 기동 방법\n"
        self.assertEqual(m.parse_prefix(text), "codex")

    def test_none_when_missing(self):
        self.assertIsNone(m.parse_prefix("# X\n## 강점\n"))


class Branch(unittest.TestCase):
    def test_valid(self):
        r = m.check_branch("codex/6-hello-codex", PREFIXES)
        self.assertEqual(r["level"], "ok")

    def test_valid_korean_slug(self):
        self.assertEqual(m.check_branch("claude/11-검사-액션", PREFIXES)["level"], "ok")

    def test_unknown_prefix(self):
        self.assertEqual(m.check_branch("foo/6-x", PREFIXES)["level"], "fail")

    def test_missing_issue_number(self):
        self.assertEqual(m.check_branch("codex/hello", PREFIXES)["level"], "fail")

    def test_session_branch_is_note_only(self):
        self.assertEqual(m.check_branch("ccr-db18b917-hpg6xi", PREFIXES)["level"], "note")


class Closes(unittest.TestCase):
    def test_extracts_number(self):
        self.assertEqual(m.find_closes("Closes #12\n\nbody"), 12)

    def test_case_insensitive(self):
        self.assertEqual(m.find_closes("closes #3"), 3)

    def test_none(self):
        self.assertIsNone(m.find_closes("no link here #5"))

    def test_check_missing_is_fail(self):
        self.assertEqual(m.check_closes(None, None)["level"], "fail")

    def test_check_missing_for_auto_body_is_review(self):
        r = m.check_closes(None, None, auto_generated=True)
        self.assertEqual(r["level"], "review")

    def test_check_issue_not_found(self):
        self.assertEqual(m.check_closes(99, None)["level"], "fail")

    def test_check_ok(self):
        self.assertEqual(m.check_closes(99, {"body": ISSUE_BODY, "author_association": "OWNER"})["level"], "ok")


class Scope(unittest.TestCase):
    def test_all_inside(self):
        files = ["scripts/check-scaffold.sh", "scripts/tests/test_x.py"]
        self.assertEqual(m.check_scope(files, m.parse_issue_paths(ISSUE_BODY))["level"], "ok")

    def test_outside_is_fail_and_listed(self):
        r = m.check_scope(["README.md", "scripts/check-scaffold.sh"], m.parse_issue_paths(ISSUE_BODY))
        self.assertEqual(r["level"], "fail")
        self.assertIn("README.md", r["message"])
        self.assertNotIn("scripts/check-scaffold.sh", r["message"])

    def test_prefix_match_is_directory_boundary(self):
        # 'scripts/tests/' must not cover 'scripts/tests_other/x'
        r = m.check_scope(["scripts/tests_other/x"], ["scripts/tests/"])
        self.assertEqual(r["level"], "fail")

    def test_exact_file_does_not_cover_longer_name(self):
        r = m.check_scope(["projects/a.md.bak"], ["projects/a.md"])
        self.assertEqual(r["level"], "fail")

    def test_protected_exact_file_prefix_is_not_covered(self):
        r = m.check_protected(["docs/protocol/README.md.bak"], ["docs/protocol/README.md"])
        self.assertEqual(r["level"], "fail")

    def test_no_declared_paths_is_fail(self):
        self.assertEqual(m.check_scope(["a"], [])["level"], "fail")

    def test_protected_files_are_not_double_reported(self):
        r = m.check_scope([".github/x.yml", "other.txt"], ["docs/"])
        self.assertIn("other.txt", r["message"])
        self.assertNotIn(".github/x.yml", r["message"])


class Protected(unittest.TestCase):
    def test_declared_ok(self):
        r = m.check_protected(["docs/protocol/README.md"], ["docs/protocol/README.md"])
        self.assertEqual(r["level"], "ok")

    def test_undeclared_is_fail(self):
        r = m.check_protected([".github/workflows/x.yml"], ["scripts/"])
        self.assertEqual(r["level"], "fail")
        self.assertIn(".github/workflows/x.yml", r["message"])

    def test_entry_files(self):
        self.assertEqual(m.check_protected(["AGENTS.md"], [])["level"], "fail")
        self.assertEqual(m.check_protected(["GEMINI.md"], [])["level"], "fail")

    def test_no_protected_touched(self):
        self.assertEqual(m.check_protected(["projects/a.md"], [])["level"], "ok")

    def test_similar_name_not_protected(self):
        self.assertEqual(m.check_protected(["agentsX/a.md", "docs/protocolX/a"], [])["level"], "ok")


class Report(unittest.TestCase):
    def pr(self, **kw):
        base = dict(
            branch="claude/11-x",
            body="Closes #11",
            files=["scripts/check-scaffold.sh"],
            issue={"body": ISSUE_BODY, "author_association": "OWNER"},
            prefixes=PREFIXES,
            auto_generated=False,
        )
        base.update(kw)
        return base

    def test_all_ok(self):
        results = m.run_checks(self.pr())
        self.assertEqual([r["level"] for r in results], ["ok"] * 4)

    def test_comment_has_marker_and_is_advisory(self):
        text = m.render_comment(m.run_checks(self.pr(branch="foo/1-x")))
        self.assertTrue(text.startswith(m.MARKER))
        self.assertIn("알림", text)
        self.assertIn("병합을 막지 않", text)

    def test_exceptions_do_not_raise_fail(self):
        results = m.run_checks(self.pr(branch="ccr-abc", body="자동 생성", issue=None, auto_generated=True, files=[]))
        self.assertNotIn("fail", [r["level"] for r in results])

    def test_no_issue_skips_dependent_checks(self):
        results = m.run_checks(self.pr(body="nothing", issue=None))
        by = {r["id"]: r["level"] for r in results}
        self.assertEqual(by["closes"], "fail")
        self.assertEqual(by["scope"], "skip")
        self.assertEqual(by["protected"], "skip")

    def test_untrusted_issue_author_is_not_authority(self):
        issue = {"body": ISSUE_BODY, "author_association": "NONE"}
        results = m.run_checks(self.pr(issue=issue, files=["README.md"]))
        by = {r["id"]: r["level"] for r in results}
        self.assertEqual(by["closes"], "fail")
        self.assertEqual(by["scope"], "skip")
        self.assertEqual(by["protected"], "skip")

    def test_trusted_associations(self):
        for a in ("OWNER", "MEMBER", "COLLABORATOR"):
            issue = {"body": ISSUE_BODY, "author_association": a}
            self.assertEqual(m.run_checks(self.pr(issue=issue))[1]["level"], "ok", a)

    def test_missing_association_is_untrusted(self):
        issue = {"body": ISSUE_BODY}
        self.assertEqual(m.run_checks(self.pr(issue=issue))[1]["level"], "fail")

    def test_message_escapes_markdown_html(self):
        text = m.render_comment([{"id": "x", "level": "fail", "message": "<script>@user</script>"}])
        self.assertNotIn("<script>", text)


if __name__ == "__main__":
    unittest.main()
