# 협업 규약 (한 장 요약)

이 레포는 여러 AI 에이전트(Claude, Codex, Gemini 등)와 사람이 GitHub로 함께 일하는 공간이다. **규약의 원본은 `docs/protocol/`이다.** 진입 파일(`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`)은 여기로 연결만 한다.

## 표준 지시문

사람이 에이전트를 띄울 때 이 문장을 그대로 쓴다.

> AGENTS.md를 읽고 Issue #N을 수행하라.

## 흐름

```
Issue 작성 → 배정 → 착수 → 작업 → PR 보고 → 검토 → 병합(사용자)
```

1. **작성**: 사용자(또는 Claude)가 Issue 템플릿으로 쓴다.
2. **배정**: Claude가 `agent:*` 라벨을 붙이고 `status:ready`로 바꾼다.
3. **착수**: 담당 에이전트가 착수 댓글을 달고 `<에이전트>/<이슈번호>-슬러그` 브랜치를 만든다. 상태는 `status:in-progress`.
4. **작업**: Issue가 선언한 수정 가능 경로 안에서만 수정한다. 막히면 멈추고 `status:blocked`로 바꾸고 질문한다.
5. **보고**: `Closes #N`이 들어간 PR을 연다. 양식은 [handoff.md](handoff.md).
6. **검토**: 작성자와 검토자는 다르다. 상태는 `status:review` → 통과하면 병합 대기, 아니면 `status:changes-requested`.
7. **병합**: 사용자만 병합한다. 병합 후 `status:done`.

## 라벨

| 그룹 | 값 |
|---|---|
| 담당 | `agent:claude`, `agent:codex`, `agent:gemini` |
| 상태 | `status:ready`, `status:in-progress`, `status:review`, `status:changes-requested`, `status:done`, `status:blocked` |
| 종류 | `type:feature`, `type:refactor`, `type:fix`, `type:docs` |

상태는 `status:*` 라벨 하나로만 표시한다.

## 문서 안내

- [lifecycle.md](lifecycle.md) — 단계별 규칙, 상태 전이, Claude의 두 모드, 토큰·컨텍스트 관리
- [handoff.md](handoff.md) — PR 보고 양식, 반려 기준, 인수인계 메모
- [conflicts.md](conflicts.md) — 충돌 방지 규칙 11개, 보호 경로

## 기본 원칙

- Issue에 없는 일은 하지 않는다.
- 규약 파일(`docs/protocol/`, `agents/`, `.github/`, 진입 파일)은 그것을 목표로 하는 Issue로만 고친다. 허점을 발견하면 Issue로 제안한다.
- 키·토큰·비밀번호는 커밋하지 않는다. 이 레포는 공개 레포다.
