# 인벤토리 프로토타입 감사 (extraction-shooter-)

> 조사일: 2026-10-17 / 작성: Claude / Issue #26
> 대상: `yeongkim0814-svg/extraction-shooter-` (공개 저장소, 얕은 클론 1커밋 `4c88da9`). **읽기만 했고 아무것도 수정하지 않았다.**
> **테스트를 실행하지 못했다.** 이 세션에는 Godot가 없고 설치하지 않았다. 아래 "테스트 N개"는 `func test_` 개수를 센 값이지 통과 결과가 아니다.
> 이 문서는 코드와 문서를 읽고 쓴 것이다. 판단은 "판단"으로 표시했다.

## 먼저 알아야 할 점

사용자 설명은 "인벤토리 프로토타입을 만들었다가 폐기"였는데, 이 저장소는 **인벤토리만 있는 작은 프로토타입이 아니다.** Godot 4.7 익스트랙션 슈터 전체(GDScript 약 2만 1천 줄)이고 인벤토리는 그 핵심 부품이다. 어느 것이 "폐기된 것"인지는 확인하지 못했다(✕). 이 저장소가 폐기 대상이면 아래 평가는 "폐기된 코드의 재사용 가능성"이고, 아직 진행 중이면 "게임에서 떼어 내는 비용"이다.

## 1. 규모

| 구분 | 값 | 근거 |
|---|---|---|
| `scripts/` 전체 | 약 21,500줄 | `find scripts -name '*.gd'` |
| `scripts/core/` (순수 로직) | 약 4,190줄 | 인벤토리 503, 격자 204, 저장 369, 수색 127, 무기 조립 136 등 |
| `scripts/ui/inventory/` | 약 3,380줄 | 인벤토리 화면 1,074, 모딩 화면 735, 드롭 판정 281 등 |
| 테스트 함수 | 628개 (인벤토리 관련 3개 파일에 135개) | `func test_` 개수 (실행 ✕) |
| 로드맵 | M0~M5 완료 표시, M6 이후 완료 표시 없음 | `docs/PLAN.md` |
| 마지막 커밋 | 2026-10-09 | 얕은 클론이라 이력은 보지 못함 |

## 2. 구조 (판단: 좋은 쪽)

- **core / game / ui 계층 분리**가 규칙으로 문서화돼 있다(`docs/TECH.md` 4절). core는 `RefCounted` 순수 로직이고 Node·씬 트리를 부르지 않는다. 내가 확인한 범위(`grep`)에서 `scripts/core`에 `get_tree`·`Input`·`extends Node`는 없었다.
- **명령(Command) → 권한자(GameAuthority) → 결과+이벤트** 구조(`scripts/core/commands/`). 서버 권한으로 바꿀 수 있게 설계한 것으로 문서에 적혀 있다. **서버/멀티플레이 코드 자체는 없다** (`scripts/net` 없음, `rpc(` 없음).
- 모든 변경 연산이 **원자적**(실패 시 상태 불변)이라고 주석에 적혀 있고, 점유맵 불변식 검사 함수 `is_consistent()`가 있다.
- 한 파일이 1,000줄을 넘는 곳은 `inventory_screen.gd`(1,074줄) 하나다. 이 파일은 UI이며 재작성 후보다(판단).

## 3. 기능 목록

| 기능 | 상태 | 근거 파일 |
|---|---|---|
| 격자 배치·이동·삭제 (직사각형 다칸 아이템) | 있음 | `scripts/core/inventory/item_grid.gd` |
| 90° 회전 (아이템별 `can_rotate`) | 있음 | `item_grid.gd`, `scripts/core/items/item_def.gd` |
| 자동 배치 (행 우선, 두 방향) / 목표 칸 근처 배치 | 있음 | `item_grid.gd` `find_free_placement`, `find_nearest_placement` |
| 스택 병합·분할 | 있음 | `item_grid.gd` `merge`, `split`, `scripts/core/commands/split_stack_command.gd` |
| 컨테이너 아이템의 내부 그리드 (조끼·가방, 여러 그리드 가능) | 있음 | `item_def.gd` `grids`, `grid_offsets` |
| **컨테이너 안에 컨테이너 넣기** | **금지 (의도된 규칙)** | `inventory.gd` `_check_grid_target` → `NESTING_NOT_ALLOWED` |
| 장비 슬롯 (슬롯별 허용 카테고리) | 있음 | `scripts/core/equipment/equipment_slots.gd` |
| 스태시 잠금 (레이드 중) | 있음 | `inventory.gd` `stash_locked` |
| 월드 컨테이너 붙이기·떼기 (시체·상자) | 있음 | `inventory.gd` `attach_external`, `detach_external` |
| **수색: 아이템이 위에서부터 하나씩 공개, 중단 시 진행 중 아이템만 손실, 소음 발생** | 있음 | `scripts/core/search/search_state.gd`, `commands/search_container_command.gd` |
| 공개 전 아이템 `?` 표시, 선택·이동 불가 | 있음 | `scripts/ui/inventory/drop_resolver.gd`, `docs/TECH.md` 7절 |
| 가중치 루트 테이블 (시드 주입) | 있음 | `scripts/core/loot/loot_table.gd` |
| 저장·불러오기 + 버전 마이그레이션 | 있음 | `scripts/core/save/save_serializer.gd`, `save_migrations.gd` |
| 아이템 정의 데이터 | `ItemDef` 리소스 필드 있음. `data/` 폴더에는 `.tres`가 0개라 정의가 어디 있는지 **미확인** | `item_def.gd` |
| **무게 제한·이동 속도 연동** | **없음.** `ItemDef.weight` 필드만 있고 인벤토리 로직에서 쓰는 곳을 찾지 못함 | `item_def.gd:36` |
| 터치·마우스 드래그앤드롭 | 있음 | `scripts/ui/inventory/*`, `docs/TECH.md` 4절 |
| 키보드·게임패드 탐색 | **미확인.** UI 파일에 키 입력 처리 흔적은 있으나 격자 탐색 지원 여부는 읽지 못함 | `inventory_screen.gd` |
| 멀티플레이 동기화 | 없음 (설계만) | `docs/TECH.md` 5절 |
| 총기 부품 트리·호환성·스탯 | 있음 (인벤토리 크기에 영향) | `scripts/core/weapons/weapon_assembly.gd`, `scripts/ui/inventory/mod_screen.gd` |

## 4. 재사용을 막는 결합

`MARKET_SCAN.md`가 말한 "장르 전용 패키지"로 떼어 내려면 풀어야 할 것들이다 (판단 포함).

1. **무기가 아이템·저장에 섞여 있다.** `scripts/core/items`가 `WeaponAssembly`·`Magazine`을 참조하고, `save`와 `commands`도 무기 클래스를 쓴다(`grep` 집계). 무기를 빼면 저장·명령 코드를 고쳐야 한다.
2. **슈터 가정이 고정돼 있다.** 주머니 4개(`POCKET_COUNT`), 고정 장비 슬롯, "스태시/레이드" 개념, 사망 시 소실 규칙(`death_resolver.gd`)이 인벤토리 클래스에 들어 있다. 제품으로 팔려면 **설정 가능한 슬롯과 컨테이너**로 일반화해야 한다.
3. **UI가 게임 스타일에 묶여 있다.** 사용자가 말한 그래픽·디자인 문제가 있는 곳이다. 로직과 달리 UI는 판매 가치가 낮다고 보는 편이 안전하다(판단).
4. **저장소에 `LICENSE`가 없다.** 공개 저장소지만 라이선스를 명시하지 않았으므로, 소유자 본인이 새 제품에 쓰는 데는 문제가 없고 외부에 재배포하는 형태가 되려면 라이선스를 정해야 한다.

## 5. 소유권·라이선스 위험

| 항목 | 결과 | 근거 |
|---|---|---|
| 외부 에셋 기록 | 폰트 1개만 기록됨: Noto Sans KR, OFL-1.1 (약 10 MB) | `docs/ASSET_LICENSES.md` |
| 텍스처 | 자체 생성 스크립트로 만든 것으로 기록됨 (`tools/gen_*.py`) | `ASSET_LICENSES.md`, `assets/textures` |
| 3D 모델·오디오 | `assets/models` 4 KB, `assets/audio` 4 KB로 사실상 비어 있음 | `du` |
| AI 생성 이미지 | 무드보드용 이미지를 Higgsfield로 생성. **저장소에 이미지 없음**, 게임 에셋으로 쓰지 않는다고 적혀 있음. 쓰려면 상업 이용 조건 확인 필요 | `docs/MOODBOARD.md` |
| 서드파티 코드 | `addons/gut`(GUT, 라이선스 파일 `LICENSE.md` 있음) | `addons/gut/LICENSE.md` |
| 기법 참고 | "Abandoned Spaceship"(MIT) 방식을 참고했으나 코드·텍스처는 복사하지 않았다고 기록 | `ASSET_LICENSES.md` |
| 상표 | `Tarkov`, `Arena Breakout`, `Escape from` 문자열을 코드·문서·데이터에서 찾지 못함 | `grep -rniE` |
| 키·토큰 | 패턴 검색에서 해당 없음. 내보내기 프리셋에 keystore·password 문자열 없음 | `grep`, `export_presets.cfg` |
| 개인정보 | 학교·연령·연락처 패턴 검색에서 해당 없음 (검색 패턴 한계 있음) | `grep` |

**확인하지 못한 것**: 폰트 외 다른 서드파티 파일, 이미지 파일(`webp` 52개) 각각의 출처. `ASSET_LICENSES.md`에 없는 것은 모두 자체 제작이라는 뜻으로 읽었지만 하나하나 확인하지 않았다.

## 6. 판단

**추천: 부분 재사용 — 코어를 떼어 내 일반화하고, UI는 새로 만든다.**

근거

1. `MARKET_SCAN.md`에서 비교한 17개 상품의 페이지 기준으로, **수색(공개 순서·중단·소음), 컨테이너 내부 그리드, 스태시 잠금, 원자적 연산+롤백, 저장 마이그레이션, 권한자 구조**를 함께 갖춘 제품은 찾지 못했다(✕ 미확인이지 "없다"가 아니다). 이 저장소의 코어는 그 조합을 이미 구현하고 테스트(628 함수, 실행 ✕)로 고정해 둔 것으로 보인다. 처음부터 만드는 비용이 가장 큰 부분이다.
2. 사용자가 폐기 이유로 든 "구조·완성도"는 코어에서는 보이지 않았다. 문제는 **UI·그래픽·게임 결합** 쪽일 가능성이 높다(판단). 그 부분은 새로 만들면 된다.
3. 반대로, 이 코어는 **"제품"으로 만들려면 일반화가 필요**하다(4절 1~2번). 그 작업량이 큰 변수다.

작업량 구간 (판단, 불확실): **M** (몇 주). 불확실성: 무기·저장·명령의 결합을 얼마나 풀어야 하는지 미확인. `scripts/core/commands`의 15개 파일이 `GameAuthority`에 얼마나 묶여 있는지는 파일별로 읽지 않았다.

## 7. 반증 조건 (이 사실이 나오면 판단이 뒤집힌다)

| 방향 | 조건 |
|---|---|
| 재작성으로 | 코어를 떼어 낼 때 `GameAuthority`·`ItemInstance`가 무기·AI·레이드에 깊이 얽혀 있어서 떼어 내는 비용이 새로 쓰는 비용과 비슷하다 |
| 재작성으로 | 테스트를 실제로 돌렸더니 상당수가 실패하거나 Godot 4.7 전용 기능에 묶여 있다 (GLoot 등 경쟁 제품은 4.4+ 표기라 대상 버전 확인 필요) |
| 재사용(그대로)으로 | 사용자가 이 게임을 계속 만들 것이라 인벤토리를 제품으로 따로 떼지 않고 게임에 쓴다 — 이 경우 "제품화"는 별건이다 |
| 중단으로 | `MARKET_SCAN.md` 후속(GLoot 소스 전체 확인)에서 GLoot이 수색·컨테이너 구조를 이미 갖췄다고 확인된다 |

## 8. 확인하지 못한 항목

| 항목 | 이유 |
|---|---|
| 테스트 통과 여부 | Godot 미설치, 실행하지 않음 |
| 이 저장소가 폐기된 것인지 | 사용자 설명과 저장소 내용이 맞지 않음. 질문으로 남김 |
| 아이템 정의 데이터 위치 | `data/`에 `.tres` 없음 |
| 키보드·게임패드 격자 탐색 | UI 코드를 끝까지 읽지 않음 |
| `commands/`·`save/`의 무기 결합 정도 | 파일별로 읽지 않고 `grep` 집계만 봄 |
| UI 화면의 실제 모습 | 스크린샷을 보지 않음 (`docs/art`는 무드 참고 이미지 2장) |
| 이력·기여자 | 얕은 클론이라 이력 못 봄 |
| 이미지 52개의 출처 | 하나하나 확인하지 않음 |
