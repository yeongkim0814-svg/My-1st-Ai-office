# Gemini

## 강점
초기 가설이며 관찰 기록으로 갱신한다.

- Jules를 통한 비동기 구현 작업 (가설).
- Gemini Code Assist 앱을 통한 PR 보조 리뷰.

## 맡기지 말 일
- 자기가 쓴 PR의 검토 (자기 검토 금지).
- 규약 파일(`docs/protocol/`, `agents/`, `.github/`, 진입 파일) 수정. 허점은 Issue로 제안한다.
- 병합.

## 쓰기 허용 경로
Issue가 선언한 경로뿐이다.

## 브랜치 접두어
`gemini/` → `gemini/<이슈번호>-슬러그`

## 기동 방법
- **구현**: Jules 웹 앱에서 이 레포를 연결한 뒤 표준 지시문을 입력한다.

  > AGENTS.md를 읽고 Issue #N을 수행하라.

- **보조 리뷰**: Gemini Code Assist GitHub 앱을 설치하면 PR이 열릴 때 자동으로 검토한다. PR 댓글에 `/gemini review`를 달아 수동으로 호출할 수도 있다.
- **자동 기동 (B단계)**: `run-gemini-cli` GitHub Action으로 `@gemini-cli` 멘션 기동. 도입 전 보안 규칙(소유자·협업자 멘션만 허용, 최소 권한)을 적용한다.

Jules가 `AGENTS.md`를 읽는지, 지정한 브랜치명 형식을 지키는지는 첫 시험(`projects/_smoke/`)에서 확인하고 아래 관찰 기록에 남긴다.

## 관찰 기록

| 날짜 | Issue | 규약 준수 | 범위 이탈 | 검증의 정직성 |
|---|---|---|---|---|
| 2026-10-15 | #2 | 준수 (AGENTS.md 및 계획/수명주기 준수) | 없음 (선언된 경로만 수정) | 정직함 (check-scaffold.sh 및 read_file로 검증) |
