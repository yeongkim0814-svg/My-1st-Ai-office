# RetroForge 경쟁 제품 조사 (Phase 0-3) — 예비 조사(불완전)

> 조사일: 2026-10-16 / 작성: Claude / Issue #17
> **상태: 예비 조사.** 기능·가격·라이선스·렌더러 표기는 정리했지만 **구매자 후기와 이슈를 읽지 못했다.** Phase 0-3이 요구하는 후기 조사는 끝나지 않았고(Issue #17은 열어 둔다), 3절의 미충족 문제는 근거가 없는 가설이다.
> **이 조사의 사실은 모두 검색 결과 요약(상품 페이지·Godot 스토어 문구의 인용 포함)이며, 상품 페이지를 직접 열어 확인한 것이 없다.** 이 세션의 네트워크가 itch.io 등에 접근하지 못했다.
> 가격은 검색 결과의 표시값이며 **만료된 세일가나 번들 할인가가 섞여 있다.** 같은 제품의 가격이 출처마다 달라 신뢰하지 않는다(10~12번). 가격 책정 전에 각 페이지에서 **정가와 단품 가격**을 직접 확인한다.

## 확인 수준 표기

| 표기 | 뜻 |
|---|---|
| ○ | 검색 결과가 상품·스토어 페이지 문구를 인용했다 |
| △ | 요약만 있고 원문 확인 불가, 또는 출처끼리 다름 |
| ✕ | 찾지 못했다 |

## 1. 경쟁 제품 표

| # | 제품 | 가격·라이선스 | 핵심 기능 | 렌더러·버전 | 확인 |
|---|---|---|---|---|---|
| 1 | **PSX Godot Shader** (fcidade) | 무료(자율 지불), **CC0** | 정점 스냅(떨림 옵션), 아핀 매핑, 15비트 색, 디더링, 브라우저 뷰어 | **Compatibility·Mobile·Forward+ 모두**, Godot 4.6에서 시험 | ○ ([스토어](https://store.godotengine.org/asset/fcidade/psx-godot-shader/)) |
| 2 | **PSX Look Free** (heyheythere) | 무료, **CC BY 4.0** | 정점 스냅, 아핀 텍스처. 플러그인 없이 GDScript+셰이더만. **브라우저 데모** | **Godot 4.3~4.7, 모든 렌더러, 데스크톱·모바일·웹** 시험이라고 표기 | ○ ([Asset Library](https://godotengine.org/asset-library/asset/5493)) |
| 3 | **PSX Look** (heyheythere, 유료) | **$5.99** | 정점 스냅, 아핀, 240p 해상도, 디더링, 15비트 색, **프리셋 10개**. Godot 4와 Unity용 | 유료판의 렌더러 정보 ✕ | △ (번들 목록 문구) |
| 4 | **PSX Visuals - GD4 Port** (scolastico) | 무료, **MIT** | 정점 스냅, 아핀, 안개, 화면 공간 디더링, 전역 셰이더 변수, **런타임 머티리얼 자동 변환(선택)** | Godot 4.1 이상. 버전 표기가 2.0.0과 2.1.3으로 다름 | △ ([Asset Library](https://godotengine.org/asset-library/asset/4687)) |
| 5 | **PS1 / PSX Visuals** (snotbane) | 무료, **Unlicense** | 정점 스냅, 정점 안개, 아핀, 구로 셰이딩, 비트 깊이 감소와 디더링 | Godot 4.0, v1.5.0 | △ ([GitHub](https://github.com/snotbane/psx_visuals)) |
| 6 | **godot-psx** (AnalogFeelings) | 무료, **MIT** | 소규모 셰이더 모음, 디더링 | Godot 4.0. 구로 셰이딩이 4.x에서 깨져 있다고 저자가 경고 | △ ([GitHub](https://github.com/AnalogFeelings/godot-psx)) |
| 7 | **godot-psx-style-demo** (MenacingMecha) | 무료(데모 프로젝트) | 정점 스냅, 아핀, 색 깊이, 디더링, 안개. 수동 설정 | Godot 4.x, 브라우저 데모 | △ ([GitHub](https://github.com/MenacingMecha/godot-psx-style-demo)) |
| 8 | **Ultimate Retro Shader Collection** (zorochase) | 가격 ✕ (무료로 표기한 결과가 있음) | 정점 스냅, 아핀, N64 3점 필터, 거리 텍스처 LOD, 안개. 편집기 스크립트가 전역 변수를 추가 | Godot 4 | △ ([itch](https://zorochase.itch.io/ultimate-retro-shader-collection-for-godot)) |
| 9 | **Retro Shaders Pro for Godot** (Daniel Ilett) | **최소 $15.99** | PS1 아핀·정점 스냅, N64 필터, CRT/VHS 후처리, 픽셀화, 텍셀 정렬 조명 | **모든 렌더러, 단 텍셀 정렬 조명은 Compatibility에서 제대로 안 됨.** Godot 4.5+만 보증 | ○ ([itch](https://danielilett.itch.io/retro-shaders-pro-for-godot)) |
| 10 | **HorrorScreenFX** (asago) | 표시 가격 상충: 검색 결과는 $7.99(세일 $5.99), 검토 의견은 $4.99(세일 $1.99). **직접 확인 필요** | 공포 풀스크린 효과 프리셋, 런타임 제어, GDScript API | Godot 4.x | △ ([itch](https://asago.itch.io/horrorscreenfx)) |
| 11 | **Retro Screen FX** (inkharbor) | 검색 결과는 번들 할인 적용 $4.96, 검토 의견은 정가 $8(세일 $6). **번들 할인가를 단품 가격으로 쓰면 안 됨, 직접 확인 필요** | 후처리 셰이더 9종, 프리셋 37개, 드롭인 레이어 노드 | Godot 4.7 | △ |
| 12 | **Retro Screen FX** (heyheythere) | 검색 결과는 번들·론칭 세일가 $2.99, 검토 의견은 현재 $3.49. **직접 확인 필요** | CRT·VHS·게임보이 프리셋 12종, 2D·3D | Godot 4 | △ |
| 13 | Pixel Dither / Color Dither | 무료, CC0 | 팔레트 디더링 | Godot 4 | △ |
| 14 | Godot 4 Shader Pack (munchkin-jonesy), Retro Horror FX Toolkit (rastalr) | 계획서 초안은 각각 $4.99 | 초안은 "셰이더 13개 + 데모", "화면 효과 4종·프리셋 12종" | - | **이번 조사에서 찾지 못함 ✕** (GPT 초안의 인용) |

## 2. 눈에 띈 사실

1. **PSX 룩의 핵심 효과(정점 스냅, 아핀, 디더링, 안개)는 무료·허용적 라이선스 제품으로 이미 충분히 제공된다**(1, 2, 4, 5, 6번).
2. **"웹과 모바일에서도 동작" 주장은 무료 제품이 이미 한다.** PSX Look Free와 PSX Godot Shader가 모든 렌더러와 웹을 시험했다고 표기하고 브라우저 데모를 제공한다. 계획서가 차별화 후보로 둔 "웹·Android 환경"은 선점되어 있다.
3. **"무료 Lite + 유료 Pro" 구조도 이미 쓰인다.** PSX Look(무료판과 유료판), inkharbor의 번들(13개 도구 중 11개에 무료 Lite). 우리의 판매 구조는 차별점이 아니다.
4. **가격대는 대략 한 자릿수 달러 중반에서 $15.99까지 넓다고 보인다.** 유사 기능 묶음(3번)이 $5.99이고, 후처리까지 묶은 상위 제품(9번)이 최소 $15.99다. 후처리 제품(10~12번)의 정확한 가격은 위 표대로 불확실하다. $9.99는 그 사이에 있지만 위 사실 1~2를 이길 이유가 필요하다.
5. **공개된 한계 표기가 있다.** 9번은 텍셀 정렬 조명이 Compatibility에서 안 된다고 밝혔고, 6번은 구로 셰이딩이 깨졌다고 밝혔다. 버전 보증 범위도 4.0, 4.1+, 4.3~4.7, 4.5+로 제각각이다.
6. **성능 수치(프레임 시간)를 공개한 제품을 이번 조사에서는 찾지 못했다 ✕.** 다만 상품 페이지를 직접 읽지 못했으므로 "없다"가 아니라 "확인하지 못했다"이다.

## 3. 미충족 문제 (근거가 약함)

구매자·사용자의 불만을 직접 확인한 근거는 **찾지 못했다 ✕.** 후기, 이슈, 포럼 글을 읽을 수 없었고, 검색으로는 Android 성능이나 떨림 문제를 다룬 글이 나오지 않았다. 아래는 공개된 한계 표기에서 추정한 **가설**일 뿐이다.

| 가설 | 근거 | 약점 |
|---|---|---|
| 버전·렌더러별로 무엇이 되고 안 되는지 한눈에 알기 어렵다 | 제품마다 보증 범위가 4.0, 4.1+, 4.3~4.7, 4.5+로 다르다(사실 5) | 구매자가 이것에 돈을 낼지는 증거 없음 |
| 효과를 켰을 때 성능 비용을 알 수 없다 | 성능 수치를 공개한 제품을 못 찾음(사실 6) | 못 찾은 것이지 없는 것이 아님 |
| 여러 제품을 이어 붙이는 설정 부담이 있다 | 후처리와 PSX 머티리얼이 제품별로 나뉘어 있고 전역 변수 설정이 제각각 | 3번과 4번이 이미 한 줄 변환·자동 변환을 표방 |

## 4. 차별화 한 줄 후보와 깨지는 지점

| 후보 | 깨지는 지점 |
|---|---|
| A. "웹·Android 환경 전용 PSX 툴킷" | 1, 2번이 이미 모든 렌더러·웹을 시험했다고 표기하고 브라우저 데모가 있다. 무료이고 CC0·CC BY다 |
| B. "프로젝트 전체 룩을 한 곳에서 관리하는 프리셋과 도크" | 3번(프리셋 10개), 4번(자동 변환), 9번(통합 후처리)이 이미 있다. 도크는 P1이라 첫 버전에 없다 |
| C. "실측 성능표와 버전·렌더러 호환 매트릭스를 함께 파는 신뢰성" | 경쟁품에서 공개 사례를 못 찾았다. 다만 구매자가 이것에 돈을 낸다는 증거가 없고, 실측에는 여러 장비가 필요하다(Phase 0-6, 시험 장비 한계) |
| D. "PSX와 CRT·VHS·N64 후처리를 한 묶음" | 9번이 $15.99로 이미 한다 |

## 5. 판정 (예비)

**차별화 한 줄: 약함 (현재 근거로는 적을 수 없음).** 이 판정이 의존하는 근거는 **기능·라이선스·렌더러 표기**(사실 1~3)이고, 후기는 아직 반영하지 않았다.

- A, B, D는 이미 무료 또는 유료 제품이 한다. C만 비어 보이지만 **수요 증거가 없고 검증 비용이 크다.**
- 핵심 효과가 무료·CC0·MIT로 풍부해서, 같은 효과를 $9.99로 파는 것은 구매자에게 지불 이유가 약하다. 이는 Court의 유죄 사유 2(무료·저가 경쟁품 대비 수요 증거 없음)를 조사로 더 구체화한 결과다.
- 이 판정은 **상품 페이지·후기를 직접 읽지 못한 상태**의 예비 판정이다. 남은 조사(후기와 이슈 읽기, Issue #17 후속)를 네트워크 허용 새 세션에서 마친 뒤 확정하거나 바꾼다. 후기가 "충족되지 않은 문제"를 보여 주면 판정이 달라질 수 있다.

## 6. 다음 결정에 대한 의견 (사용자가 정함)

1. **현 계획 그대로 진행은 권하지 않는다.** 위 판정대로면 Phase 0의 "차별화 한 줄" 통과 조건을 못 채운다.
2. **후보 C를 싼 실험으로 검증**할 수 있다. 구현 없이 상품 페이지·후기를 읽고, Phase 0-4 구매자 대화에서 "이 정보에 돈을 낼지"만 묻는다. 비용은 사용자의 시간뿐이다.
3. **PIVOT 후보를 같은 방식으로 조사**한다(계획서 9절: 에셋 임포트·정리 도구, 테마 환경 패키지 등). 이 조사에는 "무엇이 실제로 팔리는가"를 볼 수 있는 itch.io 판매·후기 데이터가 필요하고, 네트워크 허용이 적용된 새 세션이 낫다.
4. 어느 쪽이든 **Court 재심(Phase 0-7) 전에 이 문서의 판정을 증거로 제출**한다. 재심은 시장 증거가 아니라는 원칙은 그대로다.

## 7. 출처 (검색에서 확인된 링크)

- PSX Godot Shader (fcidade, Godot Asset Store): https://store.godotengine.org/asset/fcidade/psx-godot-shader/
- PSX Look Free (Asset Library): https://godotengine.org/asset-library/asset/5493
- PSX Visuals - GD4 Port (Asset Library): https://godotengine.org/asset-library/asset/4687
- PS1 / PSX Visuals (snotbane): https://github.com/snotbane/psx_visuals
- godot-psx (AnalogFeelings): https://github.com/AnalogFeelings/godot-psx
- godot-psx-style-demo (MenacingMecha): https://github.com/MenacingMecha/godot-psx-style-demo
- Ultimate Retro Shader Collection (zorochase): https://zorochase.itch.io/ultimate-retro-shader-collection-for-godot
- Retro Shaders Pro for Godot (Daniel Ilett): https://danielilett.itch.io/retro-shaders-pro-for-godot
- HorrorScreenFX (asago): https://asago.itch.io/horrorscreenfx
- Godot 도구 13종 번들(포럼 글): https://forum.godotengine.org/t/13-godot-4-tools-for-shaders-vfx-and-game-feel-free-lites-included/145300
- Color Dither (Asset Library): https://godotengine.org/asset-library/asset/3036
