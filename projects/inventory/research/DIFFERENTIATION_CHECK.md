# 인벤토리 차별 가설 검증 (H1~H4)

> 조사일: 2026-10-17 / 작성: Claude / Issue #29
> 선행 문서: `MARKET_SCAN.md`(Issue #25, PR #27), `PROTOTYPE_AUDIT.md`(Issue #26, PR #28). 둘 다 이 작성 시점에 main에 병합되지 않았다.
> **이 문서는 기능 중복 여부의 확인이다. 시장 수요 판정이 아니다.**
> 사용자의 프로토타입(`extraction-shooter-`)은 이번에 다시 열지 않았다. H1~H4는 Issue #29와 `PROTOTYPE_AUDIT.md`의 3절 설명을 그대로 가설로 썼다.

## 확인 수준 표기

| 표기 | 뜻 |
|---|---|
| ◎ | 이 세션이 원문(소스 파일, README, itch.io 페이지 HTML 설명문)을 직접 읽었다 |
| ○ | 요약 도구(WebFetch)를 거친 값 |
| △ | 검색 요약만 봄 |
| ✕ | 찾지 못했다 |

판정 용어: **있음 / 부분 / 없음 / 미확인.** 소스에서 "없음"은 *읽은 소스 안에서 해당 개념을 찾지 못했다*는 뜻이다(문자열 검색과 파일 읽기 기준). 설명문만 읽은 상품의 "없음"은 쓰지 않고 "미확인(설명문에 언급 없음)"으로 적었다.

## 가설 (Issue #29 원문)

- **H1** 컨테이너 아이템의 내부 그리드 (조끼·가방, 한 아이템에 여러 그리드)
- **H2** 수색: 아이템이 위에서부터 하나씩 공개, 중단 시 진행 중 아이템만 손실, 공개 전 선택·이동 불가
- **H3** 모든 변경이 명령 → 권한자 구조(실패 시 상태 불변, 롤백)로 서버 권한 전환이 가능한 설계
- **H4** 스태시 잠금, 저장 버전 마이그레이션

## 접근 상황과 방법

| 항목 | 결과 |
|---|---|
| `git clone --depth 1` (GIT_LFS_SKIP_SMUDGE=1) | **성공.** `github.com`의 공개 저장소는 이 방식으로 읽혔다. 아래 소스 판정은 모두 이 클론을 직접 읽은 것이다 |
| `github.com` 웹(WebFetch) | 열리지만 토픽·검색 화면이 **0건**을 돌려줬다. 로그인 없이 보이는 검색이 불완전할 수 있어 신뢰하지 않는다(4절) |
| itch.io 상품 페이지 | 연속 요청에서 429가 났다. 간격을 두고 다시 받아 **Inventory Kit, Inventory Kit Free, 5, 9, 10번 페이지 HTML은 모두 받았다** |
| itch.io 무료 파일 다운로드 | 이 세션에서는 `invalid key`로 막혀 받지 못했다. **사용자가 직접 내려받아 비공개 레포 `game-asset`에 올린 `inventory-kit-free-assets.zip`(245,853바이트)을 이 세션에서 풀어 소스를 읽었다.** zip 안에 Godot 프로젝트·애드온(`addons/inventory_kit/`, GDScript 7파일 1,215줄, 데모 포함), Unity 패키지 부분, PNG 22개, `LICENSE.txt`가 있었다 |
| Godot Asset Library API | 열림 |

클론한 커밋: GLoot `6b09b87` (master, 2026-07-14), GBIS `901410f`, expressobits `f716e2c`, Wyvernbox `f83080d`.

## 1. GLoot (peter-kish/gloot, MIT)

| 항목 | 값 | 근거 | 확인 |
|---|---|---|---|
| 마지막 커밋 | 2026-07-14 "Replace quad trees with occupancy maps (#313)", `6b09b87` | `git log -1` | ◎ |
| 최신 태그 | `v3.0.2` (커밋 2026-07-05). `git ls-remote --tags https://github.com/peter-kish/gloot`는 v1.0.1부터 v3.0.2까지 42개를 돌려준다(v2.4.0~v2.4.13, v3.0.0~v3.0.2 포함, 재확인 ◎). 가장 최신은 v3.0.2. GitHub "Release" 객체는 확인하지 못함 | `git ls-remote --tags`, `git log -1 v3.0.2` | ◎ 태그 / ✕ 릴리스 |
| 지원 버전 | Godot 4.4 이상 | [README.md:7](https://github.com/peter-kish/gloot/blob/6b09b87ac07a8536779ef1ab0fafc7e99830f948/README.md#L7) | ◎ |
| 버전 번호 불일치 | `plugin.cfg`는 3.0.2, Asset Library 항목은 3.0.1 (2025-05-01 수정일). **병기** | [plugin.cfg](https://github.com/peter-kish/gloot/blob/6b09b87ac07a8536779ef1ab0fafc7e99830f948/addons/gloot/plugin.cfg), [Asset Library](https://godotengine.org/asset-library/asset/1368) | ◎ |
| 구조 | `Inventory`는 Node, `InventoryItem`은 `RefCounted`. 제약(`GridConstraint`, `WeightConstraint`, `ItemCountConstraint`)을 붙여 조합 | [inventory.gd:3-4](https://github.com/peter-kish/gloot/blob/6b09b87ac07a8536779ef1ab0fafc7e99830f948/addons/gloot/core/inventory.gd#L3-L4), [inventory_item.gd:3-4](https://github.com/peter-kish/gloot/blob/6b09b87ac07a8536779ef1ab0fafc7e99830f948/addons/gloot/core/inventory_item.gd#L3-L4), [transition guide](https://github.com/peter-kish/gloot/blob/6b09b87ac07a8536779ef1ab0fafc7e99830f948/docs/gloot_2_to_3_transition_guide.md) | ◎ |

### H1~H4 판정 (GLoot)

| 가설 | 판정 | 근거 |
|---|---|---|
| **H1** 컨테이너 아이템 내부 그리드 | **없음** (소스 검색 기준) | 아이템은 `RefCounted`이고 인벤토리를 소유하는 필드가 없다(`inventory_item.gd`에서 `inventory` 참조는 자기가 속한 `_inventory`와 `get_inventory()`뿐, L38-L44, L116). 그리드는 인벤토리에 붙는 `GridConstraint` 하나가 한 인벤토리의 격자를 정한다. `nested`·`sub inventory`·`child inventory`·`bag`·`vest` 계열 문자열이 코어·문서·예제에서 해당 의미로 나오지 않았다(`parent`·`child` 히트는 Node 구조 코드뿐). 사용자 코드로 아이템 속성에 다른 인벤토리를 연결하는 것은 막혀 있지 않지만 **그런 기능이 제공되지는 않는다** |
| **H2** 수색·공개 | **없음** | `search`·`reveal`·`hidden`·`discover`·`loot table` 검색에서 의미 있는 히트가 없었다. `search` 히트는 `find_free_place` 설명(빈 칸 찾기)뿐이다([grid_constraint.gd:387](https://github.com/peter-kish/gloot/blob/6b09b87ac07a8536779ef1ab0fafc7e99830f948/addons/gloot/core/constraints/grid_constraint.gd#L387)). `progress` 히트는 용량 막대 UI다 |
| **H3** 명령→권한자, 롤백, 서버 권한 | **부분** (원자성 일부) / 명령·권한자·서버는 **없음** | 명령 객체·권한자 개념 없음(`command`, `authority`, `rpc`, `multiplayer` 검색 히트 없음. `undo`는 에디터 전용 `undoables.gd`로 직렬화 스냅샷을 되돌리는 편집기 기능). 다만 `InventoryItem.swap`은 중간 실패 시 두 아이템을 원래 위치로 되돌리고 `false`를 반환한다([inventory_item.gd:121-159](https://github.com/peter-kish/gloot/blob/6b09b87ac07a8536779ef1ab0fafc7e99830f948/addons/gloot/core/inventory_item.gd#L121-L159)). 이는 **연산 하나의 수동 복구**이지 모든 변경이 일관된 롤백을 갖는 구조가 아니다. `deserialize`는 `// TODO: Check return value`를 남기고 있다([inventory.gd:326 이하](https://github.com/peter-kish/gloot/blob/6b09b87ac07a8536779ef1ab0fafc7e99830f948/addons/gloot/core/inventory.gd#L326)) |
| **H4** 스태시 잠금, 저장 버전 마이그레이션 | **없음** | 직렬화 키는 `node_name`, `protoset`, `constraints`, `items` 넷이고 **버전 키가 없다**([inventory.gd:25-28](https://github.com/peter-kish/gloot/blob/6b09b87ac07a8536779ef1ab0fafc7e99830f948/addons/gloot/core/inventory.gd#L25-L28), [serialize L298-L312](https://github.com/peter-kish/gloot/blob/6b09b87ac07a8536779ef1ab0fafc7e99830f948/addons/gloot/core/inventory.gd#L298-L312)). 코어에서 `version` 문자열은 `plugin.cfg`뿐이다. 마이그레이션은 v2→v3 **사용자용 전환 안내 문서**이며 저장 데이터 변환 코드가 아니다. `lock`·`stash` 검색 히트 없음 |

GLoot이 **실제로 하는 것**(참고): 격자 제약과 90° 회전, 무게·개수 제약, 아이템 스택, 직렬화(딕셔너리), 인벤토리·슬롯·격자 UI 컨트롤, 에디터 도구. 즉 `MARKET_SCAN.md`의 1번 설명이 소스로 확인된다.

## 2. Inventory Kit Free / Inventory Kit (heyheythere, itch.io)

설명문 전체를 HTML에서 읽었고(◎), **무료판(Inventory Kit Free)은 사용자가 올린 zip의 GDScript 소스 7파일 1,215줄을 직접 읽었다(◎).** 유료판(Inventory Kit)의 소스는 받지 못했으므로 유료판의 H 판정은 설명문 기준이다.

| 항목 | Inventory Kit Free | Inventory Kit (유료) | 확인 |
|---|---|---|---|
| URL | [itch](https://heyheythere.itch.io/inventory-kit-free) | [itch](https://heyheythere.itch.io/inventory-kit) | ◎ |
| 가격 | 무료 | 최소 $7.99 (이전 조사와 같음) | ◎ |
| 라이선스 | **CC BY 4.0이라고 본문에 명시**: "use it in any game, commercial or not, change it and share it, as long as you credit it", 크레딧 문구 제공 | "unlimited commercial and non-commercial games. No attribution required. Don't resell or redistribute the items, skins or scripts themselves as an asset" | ◎ 주장 확인 (코드 파일의 라이선스 헤더는 못 봄 ✕) |
| 엔진·의존성 | Godot 4.3~4.7 "tested on both ends", Forward+·Mobile·Compatibility, 순수 GDScript, 플러그인·GDExtension 없음. Unity 6.3+ (UGUI, `com.unity.ugui`) | 동일 | ◎ |
| 갱신 기록 | "Updated 4 days ago", "Published 11 days ago". 파일 목록의 Unity 패키지는 `inventory-kit-free-1.0.1.unitypackage`인데 본문 설치 안내는 `...-1.0.0.unitypackage`라고 적어 **병기**(본문과 파일 목록이 다름). 변경 기록(devlog) 링크 없음 | "Updated 4 days ago", "Published 11 days ago". 본문은 `inventory-kit-1.0.0.unitypackage` | ◎ |
| 댓글 | HTML에 댓글 항목 0개 (로그인 안내 문구만) | 동일 | ◎ |
| 평점 | 표시 없음 | 표시 없음 | ◎ |
| 기능 목록 | 아이템이 칸 단위 발자국을 가짐, 끌기, 1/4 회전(R 또는 우클릭), 스택, 아이템 위에 놓아 교환·조합(레시피), Shift+클릭으로 상자로 이동, 정렬, "take all", 저장·불러오기("plain data"), 아이템·레시피 JSON. 16개 아이템과 판타지 스킨 | 위 + 장비 인형(슬롯 9개), 스킨 3종, 아이템 73개 | ◎ |
| 구조 단서 | `InventoryView`(화면)와 `InventoryGrid`(규칙만, "the rules alone, tested")를 나눔 | `InventoryGrid`·`Equipment` 규칙 분리 | ◎ |

### H1~H4 판정 (Inventory Kit Free / Kit)

| 가설 | 판정 | 근거 |
|---|---|---|
| H1 | **없음** (무료판 소스 ◎) | 항목은 `{id, count, pos, turned}` 사전 하나이고(`inventory_grid.gd:5`) 아이템이 자기 그리드를 갖는 필드가 없다. 데모의 배낭과 상자는 **별도의 `InventoryView` 인스턴스**를 나란히 놓은 것이며 `send_to`로 Shift+클릭 이동한다(README, `demo.gd`). 유료판은 설명문 기준 **미확인** |
| H2 | **없음** (무료판 소스 ◎) | `reveal`·`hidden`·`search` 검색에 소스 히트가 없다(`search`·`hidden`은 0건). 상자는 시작 내용물이 처음부터 모두 보이는 목록이다(`demo/demo.gd:10-23`의 시작 내용물 목록). 공개·중단 개념 없음. 유료판은 설명문에 언급 없음(미확인) |
| H3 | **부분** (무료판 소스 ◎) | `InventoryGrid`가 `RefCounted`로 규칙만 담고 화면과 분리돼 있다(`inventory_grid.gd:1-5`). `drop()`의 조합 실패와 `sort()` 실패는 `entries`를 되돌린다(`inventory_grid.gd:176-183` 부근, `sort`). 그러나 **명령 객체·권한자·이벤트·서버 개념은 없고**(`command`·`authority`·`rpc` 히트 0건), `swap`은 원본을 먼저 지운 뒤 놓는 방식이라 모든 변경이 일관된 롤백을 갖지는 않는다. 설명문의 "tested" 테스트 파일은 zip에 없어 확인하지 못함(✕) |
| H4 | **없음** (무료판 소스 ◎) | 저장은 `to_data()`/`from_data()`로 단순 배열을 주고받는다. **버전 키가 없고**, 불러올 때 카탈로그에 없거나 맞지 않는 항목은 **조용히 버린다**(보고 없음, `inventory_grid.gd` `from_data`). 스태시 잠금 개념 없음(`lock` 검색 히트는 `blockers()`라는 함수 이름뿐, 기능 아님) |

무료판 판정은 소스 검색(`reveal|search|hidden|nested|sub_inventor|container|rpc|authority|command|rollback|version|migrat|lock`)과 `inventory_grid.gd`, `item_hand.gd`, `item_catalogue.gd` 읽기에 근거한다. 검색 히트는 `blockers()`(칸 충돌 판정)와 `HBoxContainer`/`PanelContainer`(UI 노드) 이름뿐이었다. 유료판은 설명문 기준 장비 인형(슬롯 9개)을 더하는데 그 부분 소스는 읽지 못했다. 라이선스: zip의 `LICENSE.txt`가 CC BY 4.0과 크레딧 문구를 명시한다(◎).

## 3. MARKET_SCAN 5, 6, 9, 10번 상품 (설명문 기준)

6번은 위 2절의 Inventory Kit다. 나머지는 이번에 itch.io 페이지 HTML의 설명문 전체를 읽었다(◎). 소스는 읽지 못해 판정은 설명문 기준이다.

| # | 상품 | H1 | H2 | H3 | H4 | 근거 |
|---|---|---|---|---|---|---|
| 5 | Grid Inventory (Godot_Forge, $6.99) | 미확인(언급 없음) | 미확인(언급 없음) | 미확인(언급 없음) | 미확인(언급 없음) | [itch](https://godot-forge.itch.io/grid-inventory-godot). 슬롯 격자, 스택, 드래그, 신호, 약 250줄. Asset Library의 Lite 항목은 PRO가 "save integration"을 더한다고만 적음 |
| 9 | Inventory System for Godot 4 (inkharbor, $8) | 미확인(언급 없음) | 미확인(언급 없음). 단, "Not included"에 loot tables·weight·gamepad·multiplayer를 명시 | 미확인. "데이터 쪽(아이템·스택·장비·저장)은 UI와 분리"라고만 적음. 명령 구조 문구 없음 | **부분**. "versioned, migrates an older format, skips unknown ids and bad data without crashing, reports what it skipped"를 명시. 스태시 잠금 문구는 없음 | [itch](https://inkharbor.itch.io/inventory-kit) |
| 10 | Inventory System – No-Code RPG Items (selodev, $4.99) | 미확인(언급 없음) | 미확인(언급 없음) | 미확인(언급 없음) | 미확인. "save-ready", 별도 Save/Load 상품과 연동이라고만 적음 | [itch](https://selodev.itch.io/godot-inventory-system). 컨테이너 종류(상자 등)는 `container id` 설정이지 컨테이너 **아이템**이 아니다 |

→ 9번이 **저장 버전 마이그레이션**을 유료로 내세운다. H4의 "버전 마이그레이션" 절반은 새 사실이다. (`MARKET_SCAN.md`는 9번을 "JSON 저장"으로만 적었다.)

## 4. H2(수색·공개)를 구현한 오픈소스 저장소가 있는가

**방법**: Godot Asset Library 인벤토리 항목(`filter=inventory`, 버전 제한 없음)을 API로 받아 저장소가 공개된 것을 `git clone --depth 1` 하고, `search|reveal|discover|hidden|unidentified|searching`, `nested|sub_inventory|bag|vest|grids`, `command|authority|rollback|rpc|multiplayer|server`, `migrat|version|schema|locked|stash` 문자열을 검색해 히트 줄을 읽었다.

| 저장소 | 커밋일 | H1 | H2 | H3 | H4 |
|---|---|---|---|---|---|
| peter-kish/gloot | 2026-07-14 | 없음 | 없음 | 부분(swap 복구) | 없음 |
| Cabbage0211/grid-base-inventory-system (GBIS) | 2025-08-21 | 없음 (`item_grids_map`은 아이템이 차지한 **칸 좌표** 목록이지 내부 그리드가 아님. 컨테이너는 이름으로 구분되는 별도 데이터) [container_data.gd:16-17](https://github.com/Cabbage0211/grid-base-inventory-system/blob/901410f/addons/grid_base_inventory_system/core/model/container/container_data.gd#L16-L17) | 없음 | 없음 | 없음 |
| don-tnowe/godot-wyvernbox-inventory | 2026-01-27 | 없음 (`nested`는 중첩된 `ItemGenerator` 주석) | 없음 (`search`는 이름 검색 패턴·인스펙터 안내) | 없음 | 없음 (`save_state`·`load_state`·`to_dict`는 있으나 버전 키 못 찾음) |
| expressobits/inventory-system (C++ GDExtension; **`main`과 `addon` 브랜치가 다름**) | 2026-02-19 (`addon` 브랜치 `5d9a6f4` 포함) | 미확인 (README가 "Inventory with grids like RE4"를 완료로 표시. 컨테이너 아이템 여부는 소스 미열람) | 없음 | **부분** (`addon` 브랜치 ◎): `addons/inventory-system-demos/mp/`의 멀티플레이 데모가 `@rpc`, `multiplayer.is_server()`, `set_multiplayer_authority(1)`과 `SyncInventory` 노드를 쓴다. 이는 **Godot 멀티플레이 권한 + 동기화 노드** 방식이다. 명령 객체·롤백은 찾지 못했다 | 없음 | 없음 |
| seloc0des/godot-inventory-lite | 2026-10-13 | 없음 (`nested`는 에디터 독의 노드 탐색 주석) | 없음 | 없음 (`server`는 `TextServer`·`DisplayServer`) | 없음 (`migration`은 Lite→Pro **업그레이드 안내 문서**) |
| Menkos/inventory-forge | 2026-01-31 | 없음 | 없음 (`search`는 에디터 검색창) | 없음 | 부분이라기보다 **다른 종류**: 아이템 DB 편집기의 `validate_and_migrate()`와 JSON `"version": "1.0"`. 런타임 저장 데이터 마이그레이션인지는 읽지 못함 |
| Oen44/Godot-Inventory | 2026-07-15 | 없음 | 없음 | 없음 | 없음 |
| Rubonnek/inventory-manager | 2026-06-05 | 없음 | 없음 | 없음 | 없음 |
| adrianjpsantos/p0nni_inventory_system | 2025-10-21 | 없음 | 없음 | 없음 | 없음 |
| Ellyality-Godot-Hub/Ellyality-Inventory | 2025-09-18 | 없음 | 없음 | 없음 | 없음 |
| CiaNCI-Studio/InventoryToolkit | 2024-12-25 | 없음 | 없음 | 없음 | 없음 |
| godot-forge/grid-inventory-lite-godot | 2026-06-21 | 없음 | 없음 | 없음 | 없음 |

판정은 모두 ◎(클론 후 파일을 읽음). "없음"은 해당 문자열 검색과 위 히트 줄 읽기 기준이며, 파일을 한 줄씩 전부 읽은 것은 아니다(GLoot 제외 히트 확인 범위).

**읽지 못한 저장소**: `thunderplugins/inventory-for-godot-4`, `mdos-san/godot-inventory-system`, `Abab-bk/FlowerIventory`(클론이 인증 요구로 실패, 저장소 이동·삭제 가능성), `alvlp/modular-inventory`(Codeberg, 시도하지 않음), 그리고 Asset Library에 없는 GitHub 저장소 전체.

**GitHub 토픽·검색**: 요약 도구가 `topic:godot-inventory`에 "0 repositories", 검색 `godot inventory search reveal container loot`에 "0 results"를 돌려줬다(○). 로그인 없는 화면이 불완전할 수 있어 **"없다"의 근거로 쓰지 않는다.** 확인은 사용자가 로그인된 브라우저에서 아래 검색으로 하는 것이 정확하다.

- `https://github.com/search?q=topic%3Agodot-inventory&type=repositories`
- `https://github.com/search?q=godot+inventory+search+reveal&type=repositories`
- `https://github.com/search?q=godot+inventory+extraction&type=repositories`

### 4-2. CTIS (Cholopol Tetris Inventory System) — Codex 리뷰(P1)로 추가, 직접 확인

처음 조사에서 빠뜨린 무료 프로젝트다. Asset Library가 아니라 GitHub에만 있어 4절의 방법(Asset Library 목록)으로는 잡히지 않았다. 클론해서 README와 소스를 읽었다(◎).

| 항목 | 값 | 확인 |
|---|---|---|
| 저장소·라이선스 | `Cholopol/Cholopol-Tetris-Inventory-System`, **Apache-2.0**(`LICENSE` 파일), 마지막 커밋 2026-08-23 `15fe260` "v2.0.1", C# 파일 94개 | ◎ |
| 요구 사항 | **Godot 4.7+ .NET(Mono)와 .NET 8 SDK가 필요**하고, 별도 저장소의 DotPudica Framework·TetrisCoordLib 애드온 두 개에 의존한다(README 41행, 648행) | ◎ |
| 특징 | 임의 점집합(폴리오미노) 아이템, 4방향 회전, **"무한 중첩 컨테이너"**, 빠른 교환, 자동 정렬, 다중 슬롯 저장, 에디터 내장 데이터 편집기, 타르코프 풍 데모 UI | ◎ README |

| 가설 | 판정 | 근거 |
|---|---|---|
| **H1** 컨테이너 아이템 내부 그리드 | **있음** | README "Nested Containers & Tree Caching — Flat GUID Foreign-Key Model", `InventoryTreeCache`, "infinite nested containers". 중첩 구현 코드 자체는 줄 단위로 읽지 않았다 ○ |
| **H2** 수색·공개 | **없음** | `reveal|unidentified|searching|discover|hidden item` 검색에서 의미 있는 히트 없음(README의 "Discovery"는 오류 발견 시점 문맥) ◎ |
| **H3** 명령→권한자·롤백 | **있음 (서버 구현은 아님)** | 모든 변경이 불변 `InventoryCommand`(`CommandId` 멱등성, `ExpectedRevision` 낙관적 동시성)를 거치고 실패 시 트랜잭션 롤백("zero dirty state")이며 재생·되돌리기를 지원한다고 적었다(README 250-284행, 471-499행). **실제 서버/네트워크 코드는 읽지 못함**, README는 멀티플레이 복제를 "natively supporting"으로 표현 ○ |
| **H4** 스태시 잠금 / 저장 마이그레이션 | **부분** | 데모에 스태시 패널이 있다(`StashPanelVM`). README 목차에 "Save & Persistence — Wrapper Pattern and Version Migration"이 있으나 본문·코드는 읽지 않았다 ○. 스태시 잠금 개념은 코드 검색에서 못 찾음 |
| 테스트 | **미확인** | README는 "Core layer decoupled from Godot ... full test suites in seconds"라고 주장하지만 저장소에서 테스트 프로젝트 파일을 찾지 못했다(`find -iname '*test*'`는 `ShapeHitTest.cs`뿐) ✕ |

**의미**: H1, H3, H4(일부)는 **무료 오픈소스로 이미 존재한다.** 다만 **C#/.NET 8과 Godot 4.7 Mono 전용**이고 의존 프레임워크가 둘이다. GDScript만 쓰는 프로젝트에서는 쓸 수 없다. Godot 4.x의 C# 프로젝트는 웹 내보내기를 지원하지 않는다는 기록이 사용자 프로토타입 `docs/TECH.md`에 있으나(2차 자료), 4.7에서도 그런지는 **확인하지 못했다** ✕.

### 4-3. 보정 사항 (Codex 리뷰)

- **Asset Library 건수**: 내가 API(`filter=inventory`, `godot_version=any`)로 받은 값은 22건(전부 MIT)이었다. 리뷰어는 공식 웹 목록이 30건이고 내 목록에 없는 [Inventory Demo with bags and chests](https://godotengine.org/asset-library/asset/940)(Godot 3.4, MIT, "storage"·"bags"를 쓰는 Terraria풍 데모)가 있다고 지적했다. 내가 이 항목을 `asset/940` API로 직접 받아 존재와 설명문을 확인했다(◎). API 목록에는 나타나지 않았으므로 **건수는 재현되지 않는 값이며 시장 신호로 쓰지 않는다.** 이 항목은 Godot 3.4용 오래된 데모라 H1~H4 판정에는 쓰지 않았지만 "bags and chests"의 구현은 읽지 않았다 ✕.

### 4-4. Nested Inventories (CookieCherith0969, GDScript) — PR #27 리뷰(P1)로 추가, 직접 확인

Asset Library `godot_version=4.3` 필터 검색에서 빠져 있던 무료 애드온이다(Godot 4.5 전용이라 4.3 필터에 걸리지 않음).

| 항목 | 값 | 확인 |
|---|---|---|
| 출처 | [Asset Library 4628](https://godotengine.org/asset-library/asset/4628), 저장소 `CookieCherith0969/NestedInventories`, 커밋 `62ee2d0`(2026-01-02) | ◎ API, 클론 |
| 라이선스·버전 | **MIT**, Godot 4.5, 버전 1.0.1 | ◎ API |
| 언어·규모 | GDScript, `.gd` 6개, `.cs` 0개 | ◎ 클론 |
| 설명문(원문) | "A slot-based inventory system that supports **nesting containers inside other containers**, stacking items, **rotating items**, and **arbitrary item and inventory shapes**." | ◎ API |

| 가설 | 판정 | 근거 |
|---|---|---|
| H1 컨테이너 안 컨테이너 | **있음** (설명문 기준, 코드 줄 단위 검증 ✕) | 위 설명문 |
| H2 수색·공개 | **없음** | `reveal|hidden|search|discover|unidentified` 검색에서 의미 있는 히트 없음(`rotation` 주석 한 줄뿐) ◎ |
| H3 명령→권한자·롤백 | **없음** | `command|authority|rollback|revision|undo` 히트 없음 ◎ |
| H4 스태시 잠금 / 저장 마이그레이션 | **없음** | `version|migrat|lock` 히트 없음 ◎ |

**의미**: 이전 판단 "GDScript 쪽 무료 제품에는 H1(컨테이너 내부 그리드)이 없다"는 **틀렸다.** 작은(6파일) 애드온이지만 GDScript로 중첩과 불규칙 모양, 회전을 무료로 제공한다. 이 문서의 이전 문장 "GDScript 쪽에서는 못 찾음"을 이 절이 대체한다.

## 5. H1~H4 종합표

| 가설 | GLoot | Inventory Kit Free | 그 외 무료 저장소(읽은 11곳) | 유료(5, 9, 10번) | 종합 |
|---|---|---|---|---|---|
| H1 컨테이너 아이템 내부 그리드 | 없음 ◎ | 없음 ◎ (무료판 소스) | 없음 10곳 / 미확인 1곳(expressobits) / **있음 1곳: CTIS(4-2절)** | 미확인 | **무료로 존재한다**: CTIS(C#/.NET 전용)와 **Nested Inventories(GDScript, MIT, 4-4절)** |
| H2 수색·공개·중단 손실 | 없음 ◎ | 없음 ◎ (무료판 소스) | 없음 11곳, CTIS도 없음 ◎ | 미확인 | **읽은 모든 무료 제품에 없다.** 유일하게 일관된 빈자리. 단 유료 Kit·유료 5, 9, 10번 소스 미확인 |
| H3 명령→권한자·롤백·서버 권한 설계 | 부분 ◎ (swap 한 곳) | 부분 ◎ (조합·정렬 롤백, 규칙·화면 분리) | 없음 10곳 / 부분 1곳(expressobits 서버 권한 데모 ◎) / **있음 1곳: CTIS(불변 명령, 멱등, 리비전 검사, 트랜잭션 롤백)** | 미확인 | **무료로 존재한다(CTIS, C#/.NET 전용)**. GDScript 쪽은 부분 구현뿐 |
| H4 스태시 잠금 / 저장 버전 마이그레이션 | 없음 ◎ | 없음 ◎ (버전 키 없음, 맞지 않는 항목은 조용히 버림) | 없음 (Menkos 다른 종류) / **CTIS: 마이그레이션 주장 ○, 코드 미확인** | 9번 마이그레이션 **부분** | 마이그레이션은 CTIS·유료 9번이 내세움. 스태시 잠금은 못 찾음 |

## 6. 결론

**보류.** 이전 판정("진행")을 철회한다. 철회 사유는 4-2절의 CTIS(무료 Apache-2.0)가 H1, H3, H4 일부를 이미 구현했다는 사실이다.

Issue #29의 진행 조건("H2를 포함해 두 개 이상이 무료 제품에 없다")을 **다시 적용하면 충족하지 않는다.** 읽은 모든 무료 제품을 통틀어 일관되게 없는 것은 **H2(수색·공개) 하나**다.

근거

1. **H2는 어디에도 없다.** GLoot, Inventory Kit Free, 읽은 무료 저장소 11곳, CTIS 모두에서 찾지 못했다(소스 ◎). 일관된 빈자리는 이것 하나다.
2. **H1은 무료로 이미 있다**: CTIS(C#/.NET 전용, 4-2절)와 Nested Inventories(GDScript, MIT, 4-4절). **H3는 CTIS(C#)가 갖췄고** GDScript 쪽은 부분(GLoot swap 복구, Inventory Kit Free 조합·정렬 롤백, expressobits 서버 권한 데모)뿐이다.
3. 저장 버전 마이그레이션(H4의 절반)은 CTIS와 유료 9번이 내세운다.
4. 이 확인은 기능 중복이며 수요 증거가 아니다. `MARKET_SCAN.md`의 "유료 수요 증거 없음"은 그대로다.

### 좁혀진 가설 (이후 판단의 기준)

"익스트랙션 장르 구조 전체가 비어 있다"는 틀렸다. 남는 가설은 이렇다.

> **GDScript만으로 쓸 수 있고(.NET 불필요) 웹·모바일로 내보낼 수 있는 인벤토리에, 수색·공개(H2)와 명령 기반 롤백·권한자 구조(H3)를 함께 갖춘 것은 없다.** (컨테이너 중첩 H1은 Nested Inventories가 무료로 이미 제공하므로 차별점에서 제외한다.)

이 가설이 의미 있으려면 **세 가지가 확인돼야 한다.** 모두 아직 확인되지 않았다.
- 웹 내보내기 문제: Godot 4.7의 C# 프로젝트가 웹으로 내보내지는지. **리뷰어가 공식 4.7 문서(`list_of_features`)를 인용해 "Godot 4로 작성한 C# 프로젝트는 웹으로 내보낼 수 없다"고 지적했다.** 이 세션은 `docs.godotengine.org`가 429로 응답해 원문을 직접 읽지 못했다(✕). 맞다면 CTIS는 웹 대상에서 이미 제외되고 이 가설의 "웹으로 내보낼 수 있는"이 의미를 갖는다.
- GDScript 사용자 비중과 그중 이 구조를 원하는 사람이 있는지(수요).
- CTIS가 이미 GDScript 사용자에게 충분한 대안인지(예: 사용자가 .NET 설치를 꺼리는지).

### 반증 조건

| 방향 | 조건 |
|---|---|
| 중단으로 | Godot 4.7 C# 프로젝트가 웹·모바일로 내보내지고 CTIS가 그 용도로 이미 쓰인다. 또는 유료 Inventory Kit·유료 5, 9, 10번 소스 중 하나가 H2를 이미 갖췄다. 또는 H2를 구현한 공개 저장소가 나온다(읽지 못한 저장소 4곳, GitHub 전체 검색 미완) |
| 진행으로 | 좁혀진 가설의 세 항목이 긍정으로 확인된다. 특히 처음 보는 GDScript 사용자 1명 이상이 최소 데모(상자 수색 + 조끼·가방 이동)를 설명 없이 이해한다는 관찰 기록 |

### 남은 확인 항목

1. Godot 4.7 C# 웹 내보내기 상태: 리뷰어 인용(공식 문서)으로는 "불가"이고, 우리 쪽 직접 확인은 429로 실패했다. 문서 원문을 확인하면 이 항목은 닫힌다.
2. CTIS의 H4(마이그레이션) 코드와 중첩 구현, 테스트 존재 여부를 실제 소스로 읽기.
3. GitHub 검색 세 개 중 어느 것이 0건이었는지 사용자 확인(사용자 보고: "Your search did not match any repositories", 어느 검색인지 불명).

## 7. 확인하지 못한 항목

| 항목 | 이유 |
|---|---|
| 유료 Inventory Kit의 소스 | 유료라 받지 못함. 무료판 소스는 사용자가 올린 zip으로 읽음 |
| Inventory Kit Free 코드 파일 각각의 라이선스 헤더 | zip의 `LICENSE.txt`와 README의 CC BY 4.0 표기는 확인(◎). 각 `.gd` 파일 머리의 헤더는 없음 |
| 5, 9, 10번 상품 소스 | 유료. 설명문만 읽음 |
| GLoot GitHub Release 객체, 이슈·PR 목록 | 태그는 `ls-remote`로 확인했으나 Release 페이지·이슈는 보지 못함. 중첩·수색 기능 요청 이슈가 있는지 미확인 |
| `thunderplugins/inventory-for-godot-4`, `mdos-san/godot-inventory-system`, `Abab-bk/FlowerIventory`, Codeberg `alvlp/modular-inventory` | 클론 실패 또는 시도하지 않음 |
| Asset Library에 없는 GitHub 저장소, itch.io의 다른 무료 상품, Unity·웹 쪽 | 범위 밖. GitHub 토픽·검색은 요약 도구가 0건을 돌려줘 신뢰하지 않음 |
| expressobits의 컨테이너 아이템 여부, `main` 브랜치 C++ 코어 | `addon` 브랜치의 멀티플레이 데모(GDScript)는 읽었으나 C++ 코어는 컨테이너 아이템 구현 여부를 읽지 않음 |
| `MARKET_SCAN.md`의 Asset Library 건수 | 거기서 "10건"은 `godot_version=4.3` 필터를 건 값이다. 버전 제한 없이 API로 받으면 22건이었으나 리뷰어는 웹 목록이 30건이라고 한다(4-3절). **재현되지 않는 값이며 시장 신호로 쓰지 않는다.** 그 문서는 이 이슈의 수정 범위 밖이라 고치지 않았다 |
