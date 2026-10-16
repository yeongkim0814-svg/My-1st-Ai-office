#!/usr/bin/env python3
"""RetroForge 순수익·필요 판매 건수 계산. 가정은 아래 값을 고쳐서 다시 돌린다.

사용: python3 projects/retroforge/research/net_revenue.py
모든 수수료·환율·세율은 가정이며 공식 문서로 확인된 값이 아니다 (sales-channels.md 참고).
"""
import math

FX = 1400            # 원/달러 (가정)
TARGET = 1_000_000   # 목표 순이익 (원)
COSTS = (0, 300_000)  # 프로젝트 비용 가정 (원)

SCENARIOS = {
    "A 기준": dict(share=0.10, pct=0.044, fix=0.30, wh=0.0),   # itch 10% + 한국 PayPal 4.4%+$0.30
    "B 비관": dict(share=0.10, pct=0.044, fix=0.30, wh=0.30),  # A + 미국 원천징수 30%
    "C 낙관": dict(share=0.10, pct=0.029, fix=0.30, wh=0.0),   # 카드 2.9%+$0.30
}
PRICES = (7.99, 9.99, 12.99)
CONVERSIONS = (0.01, 0.03, 0.05)  # Lite 다운로드 → 유료 전환율 (가정)


def net_usd(price, share, pct, fix, wh):
    return (price - price * share - (price * pct + fix)) * (1 - wh)


def main():
    print(f"환율 {FX}원/달러, 목표 순이익 {TARGET:,}원")
    print("가격 | 시나리오 | 1건 순수익($) | (원) | 필요 건수(비용 " + " / ".join(f"{c:,}" for c in COSTS) + "원)")
    for p in PRICES:
        for name, kw in SCENARIOS.items():
            n = net_usd(p, **kw)
            won = n * FX
            need = [math.ceil((TARGET + c) / won) for c in COSTS]
            print(f"${p} | {name} | {n:.2f} | {won:,.0f} | {' / '.join(map(str, need))}")
    won = net_usd(9.99, **SCENARIOS["A 기준"]) * FX
    need = math.ceil(TARGET / won)
    print(f"\n$9.99 A 기준 {need}건에 필요한 Lite 다운로드:")
    for c in CONVERSIONS:
        print(f"  전환율 {c:.0%}: {math.ceil(need / c):,}건")


if __name__ == "__main__":
    main()
