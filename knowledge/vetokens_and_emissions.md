# veTokens and Emissions

## Key Formulas

### Vote-Escrow Lock Weight (Curve veCRV model)
```
veCRV = CRV_locked * (time_remaining / MAX_LOCK_TIME)
```
- MAX_LOCK_TIME = 4 years; linear decay to 0 at expiry
- 1-year lock on 1 CRV = 0.25 veCRV

### Liquidity Mining Boost (Curve)
```
effective_boost = min(2.5x, 1 + 1.5 * (user_veCRV / total_veCRV) / (user_LP / total_LP))
```
- Minimum boost = 1× (no veCRV); Maximum boost = 2.5× (sufficient veCRV relative to LP share)
- Bound prevents unlimited whale advantage

### Gauge Weight → Emission Share
```
gauge_emissions_i = total_weekly_emissions * (votes_i / total_votes)
```

### Emission Decay Curves
```
Exponential decay:   E(t) = E_0 * r^t          (r ≈ 0.99/week = ~40% annual reduction)
Bitcoin halving:     E(t) = E_0 / 2^floor(t/H)  (H = halving interval)
Terminal supply:     S_inf = S_0 + E_0 / (1 - r)
Inflation rate:      inflation(t) = E(t) / S(t)
```
Healthy inflation benchmark: < 5% annual once mature (post year 2).

### Bribe Market Efficiency
```
BER = USD_value_of_emissions_directed / USD_value_of_bribes_paid
```
- BER > 1: bribing profitable for LPs/protocols
- BER 1.5–4×: healthy range at protocol maturity
- BER < 1: bribers subsidizing veToken holders; rational actors stop bribing

---

## Key Thresholds and Benchmarks

- Annual inflation > 100% in Year 1 with no TVL growth → hyperinflation warning
- Decay factor r > 0.999/epoch (near-flat emissions) → perpetual dilution
- Combined team/investor unlocks coinciding with emission peaks → compounded dilution event
- veToken lock ratio < 10% of circulating supply → mercenary liquidity (no alignment)
- TVL < $50M: ve-token bribe markets too thin to function; deploy ve-mechanics only above this
- Single actor > 40% of veToken votes: cartel pricing of gauge access
- Target emission schedule: Year-1 < 80%, Year-2 < 40%, Year-3+ < 10%, tail 0.5–2%

---

## Protocol Version Notes

**Curve v2 (CryptoSwap, 2021+):** veCRV boost and gauge weight voting apply identically to v2 pools. AMM invariant differs but ve-mechanics are identical.

**crvUSD (May 2023):** Interest revenue from crvUSD lending flows to the Curve DAO fee distributor — adds protocol revenue independent of trading fees. Materially increased CRV's real yield characteristics.

**CRV emission cut (August 2025):** CRV annual inflation rate reduced to ~5.02%. Use current rates from `reference_benchmarks.md` when projecting gauge emissions.

---

## Velodrome Pattern Checklist (ve(3,3) fixes)

Velodrome fixed Solidly's design flaws (non-decaying locks, no fee-to-voter routing). When evaluating ve-token designs, verify:

- [ ] Fees accrue to veToken voters of the gauge that generated them (not all veHolders equally)
- [ ] Weekly vote resets — active re-vote required each epoch
- [ ] Decay-based lock weight, not permanent/non-decaying
- [ ] veNFT format for secondary market transferability
- [ ] Team/investor positions subject to identical lock mechanics
- [ ] Minimum lock duration to vote on gauges (prevents flash-lock attacks)
- [ ] Per-gauge emission cap (e.g., max 30% of total emissions to one pool)
