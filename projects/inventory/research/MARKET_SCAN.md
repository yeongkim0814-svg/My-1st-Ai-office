# 인벤토리 에셋 경쟁·수요 예비 조사

> 조사일: 2026-10-17 / 작성: Claude / Issue #25
> **예비 조사이며 수요 증거가 아니다.** 아래 결론은 시장 증거에 의한 판정이 아니라, 공개 페이지에서 읽은 가격·기능·신호로 세운 판단이다.
> 사용자의 프로토타입은 보지 않았다(Issue B 담당). 그래서 "우리 제품이 무엇을 더 하는가"는 비교하지 못했다.

## 확인 수준 표기

| 표기 | 뜻 |
|---|---|
| ◎ | 이 세션이 원문을 직접 받았다 (Godot Asset Library API, raw 소스 파일, itch.io 상품 페이지 HTML) |
| ○ | 이 세션이 페이지를 열었으나 **요약 도구(WebFetch)를 거친 값**이다. 원문 대조는 하지 않았다 |
| △ | 검색 결과 요약만 봤다 |
| ✕ | 찾지 못했다 |

"판매 신호"(다운로드·판매량·리뷰 수)는 대부분 페이지에 **표시되지 않는다.** 표시되지 않는 것은 "없음"이 아니라 "미확인"이다.

## 접근 상황

| 호스트 | 결과 |
|---|---|
| godotengine.org/asset-library (API) | 열림 |
| raw.githubusercontent.com | 열림 (일부 파일 404) |
| itch.io 검색·태그 목록 | 열림. 상품 페이지는 연속 요청 시 **429**(요청 제한)가 나서 일부만 직접 받음 |
| store.godotengine.org | 열림 (검색 페이지는 받았으나 인벤토리 유료 상품은 찾지 못함 ✕) |
| assetstore.unity.com | 상품 페이지만 열림. 검색 화면은 동적이라 목록을 얻지 못함 |
| github.com 직접(curl) | **403** (WebFetch로는 일부 열림) |
| api.github.com, godotassetlibrary.com | **403** |

GitHub 별 수·마지막 커밋 같은 값은 `github.com`이 막혀 있어 WebFetch 요약에만 의존했다.

## 1. 경쟁 제품 표

가격은 조사일 표시값이며 세일가가 섞였을 수 있다. "갱신"은 페이지가 보여 준 값이고, "N일 전"은 조사일 기준 상대 표기를 날짜로 환산하지 않았다.

| # | 제품 (제작자) | 가격·라이선스 | 기능 | 판매·평가 신호 | 갱신 | 출처 | 확인 |
|---|---|---|---|---|---|---|---|
| 1 | **GLoot** (pkish) — Godot 4.4+ | 무료, MIT | 격자 제약(크기 가진 아이템), **90° 회전**, 무게 제약, 직렬화/역직렬화, 기본 UI 컨트롤. 아이템 크기는 직사각형이며 소스에서 다각형·불규칙 모양 처리는 찾지 못함. 중첩 컨테이너는 확인 못함 | GitHub 별 985, 포크 46 (○). Asset Library 평점 표시 없음 | Asset Library 3.0.1 (2025-05-01), master의 plugin.cfg는 3.0.2 | [Asset Library](https://godotengine.org/asset-library/asset/1368), [grid_constraint.gd](https://raw.githubusercontent.com/peter-kish/gloot/master/addons/gloot/core/constraints/grid_constraint.gd), [GitHub](https://github.com/peter-kish/gloot) | ◎ 기능·라이선스 / ○ 별 수 |
| 2 | **Wyvernbox** (don-tnowe) | 무료, MIT | 기본·격자(아이템이 직사각형 칸 점유)·제한·화폐 인벤토리, 제작, 상점, 단축 조작(Shift-클릭 이동, 우클릭 분할). README에 회전 언급 없음 | 신호 ✕ | 1.3.14 (2025-06-22) | [Asset Library](https://godotengine.org/asset-library/asset/1919), [README](https://raw.githubusercontent.com/don-tnowe/godot-wyvernbox-inventory/master/README.md) | ◎ |
| 3 | **GBIS – Grid Base Inventory System** (cabbage0211) | 무료, MIT | MVC식 분리, 저장·불러오기, 클릭·빠른 이동·사용·분할 입력, 인벤토리 간 이동. 모양·회전·멀티플레이는 페이지에서 확인 못함 | GitHub 별 76, 포크 12 (○) | 2.2.1 (2025-08-21) | [Asset Library](https://godotengine.org/asset-library/asset/4128), [GitHub](https://github.com/Cabbage0211/grid-base-inventory-system) | ◎ 버전·라이선스 / ○ 나머지 |
| 4 | **Modular Inventory** (alvlp) | 무료, MIT (Codeberg 저장소) | 드래그앤드롭, 핫바, 아이템 로직 스크립팅, 우클릭 1개 집기, 스크롤로 수량 조절, Shift-클릭 빠른 이동 | 신호 ✕ | 2.0.0 (2026-06-30) | [Asset Library](https://godotengine.org/asset-library/asset/5186) | ◎ |
| 5 | **Grid Inventory Lite / Grid Inventory** (Godot_Forge) | Lite 무료(MIT), **PRO $6.99** | Lite: 슬롯 격자 드래그 이동·교환. PRO: 스택, 개수 표시, 병합, 툴팁, 저장 연동, Godot 4.3~4.6, 약 250줄, 상업 라이선스 포함. **회전·다칸 아이템 언급 없음** (슬롯 격자) | 평점·판매 ✕ | Lite 1.0.0 (2026-06-21) | [itch PRO](https://godot-forge.itch.io/grid-inventory-godot), [Asset Library Lite](https://godotengine.org/asset-library/asset/5285) | ◎ |
| 6 | **Inventory Kit** (heyheythere) | **최소 $7.99** (Godot 4 번들 $14.99 프로모션, 2D 번들 58종 $39.99 표기) | 격자, **90° 회전**, 상자·장비 인형 이동, 저장·불러오기(평문 데이터), Godot 4.3~4.7, 재배포 금지 | 평점·다운로드 표시 없음 | 조사 시 "4일 전 갱신, 11일 전 게시" | [itch](https://heyheythere.itch.io/inventory-kit) | ○ |
| 7 | **Inventory Kit Free** (heyheythere, 샘플) | 무료 표기로 보임 (목록에서 가격 파싱 안 됨) | "끌기·쌓기·합치기 격자 인벤토리 샘플". 6번 페이지는 무료판을 언급하지 않음 | ✕ | ✕ | [itch](https://heyheythere.itch.io/inventory-kit-free) | △ (검색 목록 제목만) |
| 8 | **Diablo/RE4 스타일 인벤토리** (Martin Senges) — 제품명에 타사 게임 이름이 들어 있음 | **최소 $10** | 90° 회전, 아이템별 가로·세로 칸 크기, 호버 애니메이션. 마우스만 지원(게임패드·키보드 질문에 "마우스만" 답변). 저장·무게·멀티플레이 언급 없음. 재배포 금지 | 평점·다운로드 없음, 댓글 2개 | 출시 2024-04-13, 버그픽스 2024-09-21 | [itch](https://martin-senges.itch.io/diablo-resident-evil-4-style-inventory-system-godot-4) | ○ |
| 9 | **Inventory System for Godot 4** (inkharbor) | **최소 $8** (론칭 세일, 13종 번들 $54.56) | 격자 UI, 드래그앤드롭, 스택, 인벤토리 간 이동, 상자, JSON 저장(`to_dict`/`from_dict`), Godot 4.3+. **회전·무게·멀티플레이는 "포함 안 함"** | 평점 없음 | 조사 시 "1일 전 갱신, 7일 전 게시" | [itch](https://inkharbor.itch.io/inventory-kit) | ○ |
| 10 | **Inventory System – No-Code RPG Items** (selodev) | **$4.99**, 무료 Lite 있음 | 스택, 무게, 핫바, 툴팁, 컨테이너 종류별 데이터 계층, 에디터 독 | 평점 5.0 (1개) | 2026-10-13 | [itch](https://selodev.itch.io/godot-inventory-system) | ◎ |
| 11 | **Godot 4 2D Inventory & Crafting** (SeiyaMob) | **$3.99** | 고정 슬롯 격자, 스택, 드래그, 제작, JSON 저장 | 평점 5.0 (2개) | 게시 2026-10-08 | [itch](https://seiyamob.itch.io/godot-4-2d-inventory-crafting-system-modular-template) | ◎ |
| 12 | **Storage System – Godot 4.4** (mm4rk3t) | **최소 $2.99**, 재배포 금지 | 자동 스택·정렬, "모두 줍기", 동적 격자 생성, 잠긴 아이템 | 신호 ✕ | ✕ | [itch](https://mm4rk3t.itch.io/storage-system-godot-4) | ○ |
| 13 | **Inventory System Pro** (Ishihara, **Unity**) | **$19** | 격자, **가변 크기·사용자 정의 모양**, 드래그 유효성 표시, 스택, JSON 저장, 소스 포함 | 평점 없음 | 게시 2026-09-29 | [itch](https://ishiharaworks.itch.io/inventory-system-pro) | ◎ |
| 14 | **Inventory Framework PRO** (smack_gds, **Unity**) | **$30** | 포럼 글: 불규칙 모양, 회전, 보관함·상점·제작대 데모, JSON 저장 | 즐겨찾기 104, 제목 옆 "(3)"(평점 수인지 불확실) | v3.1, 2026-10-07 | [Asset Store](https://assetstore.unity.com/packages/tools/gui/inventory-framework-pro-319294), [포럼](https://discussions.unity.com/t/50-new-release-inventory-framework-pro-ui-toolkit/1668571) | ○ |
| 15 | **Grid Inventory System** (Developers Hub, **Unity**) | **$39.99** | 설명란이 비어 있어 기능 확인 못함 | 즐겨찾기 40, "평점 부족" | v2.2.0, 2026-06-29 | [Asset Store](https://assetstore.unity.com/packages/2d/gui/grid-inventory-system-276772) | ○ |
| 16 | **Action RPG Inventory** (**Unity**) | **$5** | 설명란 비어 있음. 검색 요약은 "회전 가능한 격자"라고 함(△) | 즐겨찾기 8, "평점 부족" | 2020-10-12 | [Asset Store](https://assetstore.unity.com/packages/tools/integration/action-rpg-inventory-180555) | ○ 가격·날짜 / △ 기능 |
| 17 | **UInventoryGrid** (Two TV Games, **Unity**) | **$20** | 격자, 드래그앤드롭, 스택·분할, **회전**, 아이템 설명 | 신호 ✕ | ✕ | [itch](https://twotvgames.itch.io/unity3d-uinventorygrid) | ◎ |

**시장 규모를 가늠한 숫자**

- Godot Asset Library에서 `inventory`로 검색하면 10건이고 전부 무료·MIT였다 (◎, API 응답). 단 **이 숫자는 시장 신호로 쓰지 않는다**: 구 Asset Library는 무료·오픈소스만 받는 곳이라(`projects/retroforge/research/sales-channels.md`) 유료 상품이 애초에 없고, `godot_version=4.3` 필터 때문에 4.4 이상 전용 에셋과 이전 버전용이 빠졌을 수 있다. 시장 크기나 무료·유료 비율을 추정하려면 필터 없는 중복 제거 교차 집계가 필요하며 이번에는 하지 않았다(✕).
- itch.io에서 `Godot`+`inventory` 태그의 도구는 **10건**이고 가격은 $1.35~$8, 어느 상품에도 평점·리뷰 수가 표시되지 않았다 (○).
- itch.io `grid inventory` 검색의 첫 화면(약 55건, 엔진 혼합)에서 Godot용 유료 상품은 $2.99~$10대, RPG Maker·Unity용은 $2.99~$20대로 보였다 (◎, 가격은 목록 값).

## 2. 무료 vs 유료 기능 경계와 빈자리 후보

### 무료가 이미 하는 일

GLoot(MIT, 별 985)이 **격자 + 90° 회전 + 무게 제약 + 직렬화 + 기본 UI**를 제공한다(1번). Wyvernbox는 다칸 점유 격자·제작·상점까지 한다(2번). 즉 "회전되는 격자 인벤토리 + 저장"은 **무료 오픈소스가 이미 충족**한다. 이 경계가 유료 제품 가격($3~$10)을 눌러 놓는 가장 큰 요인으로 보이지만, 구매자가 무엇 때문에 유료를 사는지는 후기를 읽지 못해 확인하지 못했다 ✕.

### 유료 Godot 제품이 얹는 것 (페이지 문구 기준)

완성된 UI 위젯과 데모, 상업 라이선스 명시, 에디터 편의(독·프리셋), 장비 인형·상자 같은 **즉시 쓸 수 있는 패키지**(5, 6, 9, 10번). 회전을 내세우는 유료 Godot 제품은 6번과 8번 둘이며, 그중 8번은 마우스 전용이다.

### Unity에는 있고 Godot 쪽에서는 찾지 못한 기능

**사용자 정의·불규칙 모양**은 Unity 제품(13, 14번)이 내세운다. Godot 쪽에서 이를 내세운 상품은 이번 조사에서 찾지 못했다. 다만 이는 "Godot에 없다"의 증거가 아니라 **찾지 못했다**(✕)이다. 이름 없는 GitHub 저장소나 itch 미노출 상품이 있을 수 있다.

### 빈자리 후보 (0~4개, 모두 가설)

| 후보 | 근거 | 깨지는 지점 |
|---|---|---|
| A. **불규칙 모양(다각형) 아이템 + 회전** | Unity 제품 둘이 내세움(13, 14번). GLoot 격자 소스에서 다각형 처리를 찾지 못함. 유료 Godot 상품 중 내세운 곳 못 찾음 | 구매자가 직사각형 이상의 모양을 원한다는 증거가 없다. 격자 퍼즐 방식은 구현이 단순해 무료 포크가 금방 생길 수 있다 |
| B. **키보드·게임패드로 격자 탐색** | 8번이 "마우스만"이라고 답함. 1~7번은 확인 못함 | 조사한 제품 대부분의 입력 방식을 확인하지 못했다. 모르는 사이 이미 지원할 수 있다 |
| C. **서버 권위 검증·멀티플레이 안전성** | 9번이 "포함 안 함"으로 적음. 나머지 상품은 언급이 없다 | 구현·검증 비용이 크고(서버 시험 환경), 구매자 수요 증거가 없다. 6만 원 목표에 비해 작업량이 과하다 |
| D. **엔진 비종속(웹/TypeScript) 모듈** | 이번 조사는 Godot·Unity 위주였고 npm·웹 라이브러리는 **조사하지 않았다** | **미확인**: 웹 쪽 경쟁은 아직 모른다. 결정 근거로 쓰지 못한다 |

## 3. 월 6만 원에 필요한 판매 건수

`projects/retroforge/research/net_revenue.py`의 가정을 그대로 썼다(환율 1,400원/달러, itch 수수료 10%, 한국 PayPal 4.4%+$0.30, 비관은 미국 원천징수 30% 추가, 낙관은 카드 2.9%+$0.30). 이 값들은 RetroForge 문서와 같은 **가정이며 공식 문서로 확인된 값이 아니다.** 목표만 월 순수익 60,000원으로 바꿨다. itch.io 외 판매처(Godot 스토어, Unity Asset Store)의 수수료는 **미확인**이라 계산하지 않았다.

실행: `net_revenue.py`의 `net_usd`와 `SCENARIOS`를 import해서 계산했다(PR 검증 결과 참조).

| 가격 | A 기준 (1건 순수익 → 월 필요 건수) | B 비관 | C 낙관 |
|---|---|---|---|
| $4.99 | $3.97 (5,560원) → **11건** | $2.47 (3,464원) → 18건 | $4.05 (5,665원) → 11건 |
| $6.99 | $5.68 (7,957원) → **8건** | $3.59 (5,021원) → 12건 | $5.79 (8,104원) → 8건 |
| $7.99 | $6.54 (9,155원) → **7건** | $4.14 (5,799원) → 11건 | $6.66 (9,323원) → 7건 |
| $9.99 | $8.25 (11,552원) → **6건** | $5.25 (7,356원) → 9건 | $8.40 (11,762원) → 6건 |

해석(판단):

1. **필요 건수 자체는 작다.** 월 6~18건이면 된다. 계산만으로는 달성 불가능한 목표가 아니다.
2. **문제는 그 건수가 매달 지속되는지다.** 신규 에셋은 출시 직후에 몰리고 이후 줄어드는 경향이 일반적이라고 알려져 있지만, 이 레포 안에는 그 곡선의 근거가 없다(미확인). 월 6만 원은 "1년에 약 72~216건"이라는 뜻이다(A 기준 $7.99 약 84건, B 비관 $4.99 약 216건).
3. **신호가 약하다.** 비슷한 유료 Godot 인벤토리 상품 중 평점이 표시된 것은 10, 11번 둘뿐이고 각각 1개, 2개다(둘 다 게시 10일 이내의 신제품). 나머지는 평점·판매 수를 보여 주지 않는다. 판매가 있다는 증거도, 없다는 증거도 얻지 못했다. 무료·MIT 제품이 여럿 있고(1~4번, 모두 Asset Library 등록분이라 무료만 보이는 곳이라는 점에 유의) 가장 큰 무료 제품(GLoot)이 회전·무게·저장을 이미 한다.
4. 가격은 Godot용이 $2.99~$10, Unity용이 $5~$40으로 보인다. Godot에서 $9.99는 조사한 가장 비싼 축(8번 $10)과 같은 수준이다.

## 4. 상표·저작권 주의와 홍보 문구 후보

**피할 것**

- 특정 게임 이름·로고·아이콘·UI 스크린샷: 제품명, 태그, 설명, 썸네일, 데모 아이템 아이콘 모두. 8번은 제품명에 타사 게임 두 개를 넣었는데, 이는 우리가 따라 할 선례가 아니라 해당 제작자가 스스로 지는 위험으로 본다.
- 블록 퍼즐 게임의 이름(상표). 대신 "퍼즐 맞추기식", "다칸 아이템"처럼 일반 표현을 쓴다.
- 데모에 쓰는 아이템 그림은 직접 만들거나 CC0·사용 허가가 확인된 것만 쓴다. 다른 상품의 아이콘 팩을 가져오지 않는다.
- 경쟁 제품 코드·README를 복사하지 않는다. 무료 MIT 코드를 참고하더라도 라이선스 고지를 따른다(법률 자문은 아니다).

**일반 표현 홍보 문구 후보** (사실 주장은 구현·시험이 끝난 뒤에만 쓴다)

- "회전하고 겹치지 않게 맞춰 넣는 격자 인벤토리" / "A grid inventory where multi-cell items rotate and fit like puzzle pieces."
- "생존·탐색 게임을 위한 가방 정리 시스템" / "A pack-and-manage inventory for survival and loot-driven games."
- "저장·불러오기와 게임패드 조작을 포함" — **포함이 확인된 경우에만**.
- "Godot 4.x 버전별 시험 결과 표 제공" — 시험한 뒤에만.

## 5. 결론

**보류.**

근거

1. 계산상 필요 건수는 월 6~18건으로 작다(3절).
2. 그러나 **유료 수요의 증거를 얻지 못했다.** 평점이 표시된 유사 유료 상품은 둘뿐이고 각각 1~2개이며, 판매·다운로드는 어디에도 보이지 않는다. 증거가 약한 것이지 수요가 없다는 증거는 아니다.
3. 핵심 기능(격자, 회전, 무게, 저장)은 무료 MIT 제품(GLoot)이 이미 제공하고 가격대는 $3~$10에 몰려 있다. 같은 기능으로는 유료 전환의 이유가 약하다.
4. 빈자리 후보(2절 A~C)는 모두 근거가 약한 가설이고, D(웹/엔진 비종속)는 조사하지 않았다.
5. 중단까지는 아니다. 필요 건수가 작고, 후보 A(불규칙 모양)가 Godot 쪽 빈자리일 가능성이 남아 있으며, 지출이 없는 조사이기 때문이다.

**반증 조건** (이 사실이 나오면 판단이 뒤집힌다)

| 방향 | 조건 |
|---|---|
| 진행으로 | 유사 유료 Godot 인벤토리 상품의 공개 판매 신호(예: 평점 수십 개 이상, 판매 건수 공개, 번들 판매 순위)가 확인된다. 또는 Issue B가 감사한 프로토타입이 후보 A(불규칙 모양+회전)나 B(게임패드)를 이미 구현한 상태이고, 이것이 GLoot과 6·8번에 없는 것으로 확인된다. 또는 D(웹) 쪽에서 경쟁이 거의 없고 수요 신호가 있는 것이 확인된다 |
| 중단으로 | 프로토타입이 GLoot(회전·무게·저장)이 이미 하는 범위를 넘지 못한다. 또는 Godot에서 불규칙 모양을 내세우는 상품·오픈소스가 이미 있고 무료다. 또는 판매처 수수료가 3절 가정보다 훨씬 커서 필요 건수가 수 배로 늘어난다 |

## 6. 확인하지 못한 항목

| 항목 | 이유 |
|---|---|
| 모든 상품의 다운로드·판매 수 | itch.io가 공개하지 않거나 페이지에 없음 |
| 구매자 후기·이슈 | 후기를 읽지 못함. 대부분 상품에 후기가 표시되지 않음 |
| GLoot 최신 릴리스·마지막 커밋 날짜 | `github.com`이 직접 접근 403, `api.github.com` 403. 별·포크는 WebFetch 요약값(○) |
| GLoot 중첩 컨테이너·불규칙 모양 지원 여부 | 소스 일부(`grid_constraint.gd`, `inventory.gd`)만 확인했고 전체 저장소는 보지 못함. 일부 파일에서 해당 문자열이 없었다는 것뿐이다 |
| Godot 스토어(store.godotengine.org)의 유료 인벤토리 상품 | 검색 화면에서 인벤토리 상품을 찾지 못함. 없다는 증거는 아님 |
| 웹·npm·TypeScript 인벤토리 라이브러리 | 이번 조사 범위 밖(Godot·Unity 위주). 후보 D의 근거 없음 |
| Unity Asset Store 수수료, Godot 스토어 수수료 | 공식 문서를 확인하지 못함. 3절은 itch.io 가정만 사용 |
| itch.io 상품 페이지 일부 원문 | 429로 받지 못함 (heyheythere 무료판, 일부 목록 상품). 6, 8, 9, 12번은 요약 도구를 거친 값(○) |
| 신규 에셋의 판매 감소 곡선 | 레포 안에 근거 없음 |
| 사용자의 프로토타입과의 비교 | Issue B의 범위 |
