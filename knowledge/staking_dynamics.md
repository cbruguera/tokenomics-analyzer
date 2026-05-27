# Staking Dynamics

## Key Formulas

### Ethereum Post-Merge Issuance
```
Annual_Issuance(S) ≈ 940.87 * sqrt(S)   [ETH/year, S in ETH]
APY(S) ≈ 940.87 / sqrt(S)
inflation_rate(S) ≈ 940.87 * sqrt(S) / total_supply
```
| S (ETH staked) | APY (approx) |
|---|---|
| 1M  | ~18.8% |
| 10M | ~5.9%  |
| 20M | ~4.2%  |
| 30M | ~3.4%  |

**Post-Dencun (EIP-4844, March 2024):** L2s shifted to blobs → EIP-1559 base fee burn dropped sharply. At ~34M ETH staked: gross issuance ~0.9% annual, net inflation ~0.18–0.23% after burn. ETH is not reliably deflationary post-Dencun. See `reference_benchmarks.md` for current figures.

### Staking Equilibrium
```
Rational equilibrium: r(s*) + π = c + γ
Steady-state ratio:   s* = [ r_0 / (c + γ - π) ]^2    [for r(s) = r_0 / sqrt(s)]
```
- `c` = opportunity cost; `γ` = liquidity premium; `π` = price appreciation expectation
- LSTs reduce `γ → 0`, pushing `s*` up; rising `π` increases `s*`; falling `π` collapses `s*`

### Real Yield Threshold
```
real_yield = protocol_revenue(t) / S   > 0   (self-sustaining)
Sustainable condition: fee_revenue_per_token >= issuance_per_token
```
Purely inflationary staking = zero-sum redistribution from non-stakers to stakers.

### Reflexivity Loop
```
APY(t)    = f(S(t), price(t))
inflow(t) = α * max(APY(t) - c, 0)
S(t+1)    = S(t) + inflow(t) - outflow(t)
price(t+1) = price(t) * g(circulating(t), demand(t))
```
Bear collapse: `price ↓ → π < 0 → unstaking → circ ↑ → sell pressure → price ↓`
Cascade trigger: `outflow(t) * price(t) > demand_depth(t)`

### Dynamic APY Controller (Cosmos-style)
```
APY(t+1) = APY(t) + k_p * (s_target - s(t))
```
Creates restoring force around `s_target` (typically 50–67%). Prevents over-staking and under-staking simultaneously.

---

## Key Thresholds

- Staking > 80% of supply: likely forced (lock-only with no liquid alternative) or artificially inflated; expect cascade when incentives change
- Staking < 20%: holders largely indifferent; security and velocity sinks both weak
- Single LST provider > 33% of stake: systemic concentration risk (governance capture + correlated slashing)
- Fixed nominal APY (regardless of staking ratio): no equilibrium; issuance scales linearly with S → Anchor/LUNA failure mode
- Unbonding delay < 7 days: high cascade risk; delay must exceed evidence submission window for slashing to deter attacks

| Delay   | Cascade Risk | Capital Efficiency | Slash Deterrence |
|---|---|---|---|
| < 24h   | Very High    | High               | Low              |
| 7 days  | Medium       | Medium             | Medium           |
| 21 days | Low          | Low                | High             |
| 28+ days| Very Low     | Very Low           | Very High        |
