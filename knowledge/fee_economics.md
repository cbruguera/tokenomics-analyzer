# Fee Economics

Load when: real-yield token, fee-sharing, or assessing revenue sustainability.

## Revenue Taxonomy

| Revenue Type | How Earned | Example Protocols |
|---|---|---|
| Trading fees | % of swap volume | Uniswap (0.05–1%), Curve (0.04%), GMX (0.05–0.1%) |
| Borrowing/lending | Interest on borrowed assets (utilization-based) | Aave, Compound, MakerDAO stability fees |
| Liquidation fees | % of collateral seized | Aave (5–15%), MakerDAO (13%) |
| Perpetuals/derivatives | Opening fee + funding rate + close fee | GMX, dYdX, Synthetix |
| Protocol-owned yield | Interest on treasury assets (RWA, lending) | MakerDAO/Sky (~$300–500M annual, 2024) |
| Sequencer revenue | L2 sequencer margin: user gas minus L1 settlement cost | Optimism, Arbitrum |

---

## Key Metrics

### Fee Coverage Ratio (FCR) — primary sustainability metric
```
FCR = annual_fee_revenue / inflation_cost
inflation_cost = circulating_supply × token_price × annual_inflation_rate
```
| FCR     | Interpretation |
|---|---|
| > 2.0   | Strong real yield |
| 1.0–2.0 | Real yield — fees cover inflation; sustainable |
| 0.5–1.0 | Partially subsidized |
| < 0.5   | Dilutive — rewards primarily inflationary |
| 0       | No fee revenue — pure inflation token |

### Revenue Yield on TVL
```
revenue_yield_pct = (annual_revenue_usd / tvl_usd) × 100
```
| Protocol Type | Typical Revenue/TVL | Notes |
|---|---|---|
| Lending (Aave, Compound) | 2–5% | Scales with utilization |
| DEX (Uniswap v3, Curve)  | 0.5–3% | Volume/TVL dependent |
| Perps/Derivatives (GMX)  | 10–20% | High-risk/high-return |
| Protocol-owned RWA yield | 3–6% | Matches real-world rates |

**Minimum viable:** Revenue/TVL < 0.5% annually = fee-extracting thin layer, not a durable model.

### Revenue-to-FDV (P/F ratio)
```
P/F = fully_diluted_valuation / annual_revenue_usd
```
| P/F     | Interpretation |
|---|---|
| < 10×   | Cheap on revenue; high risk or undervalued |
| 10–50×  | Reasonable for early-stage DeFi |
| 50–200× | Growth-stage pricing; revenue expansion required |
| > 200×  | Speculative; no fundamental basis |
| ∞       | Pure speculation |

P/F only meaningful when fees actually accrue to token holders (not LPs only).

---

## Value Accrual Mechanisms

| Mechanism | Token Effect | Strength | Risk |
|---|---|---|---|
| Direct distribution | Fee yield to stakers/holders | Strong — immediate cash flow | Requires sustained revenue |
| Buyback-and-burn | Protocol buys on market; burns | Deflationary; benefits all holders | Governance can redirect |
| veToken distribution | Fees to vote-escrow holders | Aligns long-term holders | Non-lockers get no yield |
| Treasury accumulation | Fees grow treasury | Indirect | Token has no direct claim |
| None / redirected | Fees go to team or unused | No value accrual | Critical flaw — M-01 |

---

## Protocol Benchmarks (2024–2025 range)

| Protocol | Annual Revenue | Revenue/TVL | P/F   | Value Accrual |
|---|---|---|---|---|
| MakerDAO/Sky | ~$400M        | ~6%         | 15–25× | Buyback-and-burn (MKR) |
| GMX          | ~$50–100M     | ~15–20%     | 20–40× | Direct (ETH to stakers) |
| Uniswap      | ~$500M–1B     | ~0.5–1%     | 50–150× | ve-fee post Dec 2025 |
| Curve        | ~$50–80M      | ~2–4%       | 30–60× | veCRV fees + crvUSD |
| Aave         | ~$150–300M    | ~2–3%       | 20–50× | Treasury + stkAAVE |
| Lido         | ~$100–200M    | ~0.5%       | 40–80× | LDO treasury; no direct yield |

Cross-reference with `reference_benchmarks.md` for current figures.
