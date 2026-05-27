# Token Velocity

## Key Formulas

### MV = PQ (Quantity Theory applied to tokens)
```
Market Cap = P * Q / V

P_token = (P * Q) / (M * V)
```
- M = circulating supply; V = velocity (times token changes hands/period)
- P = price level of service; Q = quantity of services exchanged
- Holding GDP (P×Q) constant: doubling V halves market cap

### Velocity Measures
```
V = Annual on-chain tx volume (USD) / Average circulating market cap
V = 1 / Average_hold_time_in_years     (3-day avg hold → V ≈ 122)
V_effective = (M_circulating / M_total) * V_raw
```

Reference: BTC V ≈ 3–7×/year; ETH V ≈ 8–15×; USDC/USDT V > 50×/year.

---

## Velocity Benchmarks

| V Range  | Interpretation | Design Status |
|---|---|---|
| V < 1    | Tokens held >1 year; strong store-of-value | Healthy |
| 1–10     | Moderate; acceptable for large-cap networks | Acceptable |
| 10–50    | High velocity; strong sinks required | Concerning |
| > 50     | Approaching stablecoin velocity; near-zero fundamental value | Critical |

Any token with V > 20 and no active burn or staking sink → flag as velocity trap candidate.

---

## Sink Mechanisms (ranked by effectiveness)

1. **Burn-on-use (deflationary):** `dM/dt = -burn_rate × Volume` — reduces M permanently.
   BNB model. Effective when volume growth outpaces issuance. No velocity change, but M shrinks.

2. **Staking for access rights:** Token locked for validator slot or premium tier.
   Rule of thumb: ≥20–30% of circulating supply must be locked to meaningfully impact velocity.

3. **Governance escrow (veToken):** 1–4 year locks with decaying voting power.
   Observed Curve effect: ~50% CRV locked at any given time → materially reduces effective V.

4. **Protocol-owned liquidity buyback-and-lock:** Treasury buys tokens, locks in LP.
   Reduces float without inflationary issuance.

5. **Fee redistribution to stakers:** Real fees (not new issuance) incentivize holding without increasing M.
   Only effective when protocol generates real fees.

---

## Critical Patterns

**Velocity trap:** Token required to pay for service; users buy immediately before use, sell immediately after.
Minimum viable hold ≈ one block. `Market Cap ≈ daily GDP × ~1 day`. For a $1B/year network: Market Cap ≈ $2.7M.

**Substitutability:** If protocol also accepts USDC/stablecoins, native token demand collapses and V for remaining holders spikes.

**Pure medium-of-exchange:** No store-of-value use case + users can acquire instantly on DEX → rational actors hold minimum balance → M_effective → 0, V → ∞. Fundamental value floor near zero (Pfeffer, 2017).
