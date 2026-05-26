# Fee Economics & Protocol Unit Economics

Load this file when: a real-yield token is present, fee-sharing is described, or assessing revenue sustainability.

---

## Revenue Taxonomy

| Revenue Type | How Earned | Example Protocols |
|---|---|---|
| **Trading fees** | % of swap volume (fixed or dynamic) | Uniswap (0.05–1%), Curve (0.04%), GMX (0.05–0.1%) |
| **Borrowing/lending fees** | Interest rate on borrowed assets (utilization-based) | Aave, Compound, MakerDAO stability fees |
| **Liquidation fees** | % of collateral seized during liquidation | Aave (5–15%), MakerDAO (13%) |
| **Perpetuals/derivatives fees** | Opening fee + funding rate + close fee | GMX, dYdX, Synthetix |
| **Stablecoin minting fees** | Stability fee on CDP minting | MakerDAO (variable by collateral type) |
| **Protocol-owned yield** | Interest on treasury assets (RWA, lending) | MakerDAO/Sky (~$300–500M annual, 2024) |
| **Sequencer revenue** | L2 sequencer margin: user gas paid minus L1 settlement cost | Optimism, Arbitrum |
| **Restaking/validation fees** | AVS operator fees, restaking service commissions | EigenLayer operators |
| **Subscription/access fees** | Fixed periodic payments for protocol access | Rare; some institutional DeFi |

---

## Key Metrics & Formulas

### Fee Coverage Ratio (FCR)

The single most important sustainability metric. Measures whether fee revenue covers the dilution cost to non-stakers.

```
FCR = annual_fee_revenue / inflation_cost

inflation_cost = circulating_supply × token_price × annual_inflation_rate
```

| FCR | Interpretation |
|---|---|
| FCR > 2.0 | Strong real yield — fees substantially exceed dilution |
| FCR 1.0–2.0 | Real yield — fees cover inflation; sustainable |
| FCR 0.5–1.0 | Partially subsidized — inflation partially funded by issuance |
| FCR < 0.5 | Dilutive — staking rewards primarily inflationary; unsustainable long-term |
| FCR = 0 | No fee revenue — pure inflation token; zero durable demand basis |

Maps to: `economics.annual_revenue_usd`, `supply.emission_rate_annual_pct`, `utility.staking.reward_source`

### Revenue Yield on TVL

```
revenue_yield_pct = (annual_revenue_usd / tvl_usd) × 100
```

Benchmarks (2024–2025):
| Protocol Type | Typical Revenue/TVL | Notes |
|---|---|---|
| Lending (Aave, Compound) | 2–5% | Scales with utilization rate |
| DEX (Uniswap v3, Curve) | 0.5–3% | Highly dependent on volume/TVL ratio |
| Perps/Derivatives (GMX) | 10–20% | High-risk/high-return activity |
| Algorithmic stablecoin | 0.5–2% | Low if collateral is on-chain |
| Protocol-owned RWA yield | 3–6% | Matches real-world interest rates |

**Minimum viable:** Revenue/TVL < 0.5% annually indicates the protocol is a fee-extracting thin layer over underlying yield — not a durable revenue model.

### Revenue-to-FDV Ratio (P/F ratio, analogous to P/E)

```
P/F = fully_diluted_valuation / annual_revenue_usd
```

| P/F Ratio | Interpretation |
|---|---|
| < 10x | Cheap on revenue; likely undervalued or high risk |
| 10–50x | Reasonable for early-stage DeFi protocol |
| 50–200x | Growth-stage pricing; dependent on revenue expansion thesis |
| > 200x | Speculative; revenue does not justify valuation |
| ∞ (no revenue) | Pure speculation; no fundamental basis |

Note: P/F is only meaningful when fee revenue actually accrues to token holders. If fees go to LPs only (Uniswap pre-fee-switch), the token has no claim on revenue regardless of protocol volume.

### Breakeven TVL

Minimum TVL needed for fee revenue to cover token inflation at current rates:

```
tvl_breakeven = inflation_cost / (fee_rate × volume_to_tvl_ratio)
```

Where `volume_to_tvl_ratio` is the daily volume/TVL (typically 0.05–0.5 for DEXs, 0.3–1.0 for perps).

---

## Value Accrual Mechanisms

How fees reach token holders determines whether the token captures protocol value. Map to `economics.value_accrual_to_token`.

| Mechanism | Token Effect | Strength | Risk |
|---|---|---|---|
| **Direct distribution** | Fee yield paid directly to stakers/holders | Strong — immediate cash flow | Requires sustained revenue; taxable event |
| **Buyback-and-burn** | Protocol buys token on open market; burns it | Deflationary; benefits all holders | Requires sustained revenue; subject to slippage; governance can redirect |
| **veToken fee distribution** | Fees distributed to vote-escrow holders | Aligns incentives with long-term holders | Creates two-tier system; non-lockers get no yield |
| **Treasury accumulation** | Fees grow the treasury | Indirect — treasury backs token value | Token has no direct claim; treasury can be misused |
| **LP incentivization** | Fees boosted back to LPs | Improves liquidity | Does not benefit token holders; circular if own-token LPs |
| **None / redirected** | Fees go to team or are unused | No token value accrual | Critical flaw — see M-01 red flag |

---

## Fee Distribution Design Patterns

### Pattern 1: Split distribution (GMX model)
```
fee_revenue split:
  → 70% to GLP liquidity providers (as ETH/AVAX)
  → 30% to staked GMX (as ETH/AVAX)
```
Analysis: Token holders receive real yield in ETH, not native token. Avoids circular value extraction. GLP holders bear counterparty risk and earn higher share.

### Pattern 2: veToken fee routing (Curve model)
```
fee_revenue split:
  → 50% to veCRV holders (as 3CRV)
  → 50% to LPs in respective pools
+ gauge emissions directed by veCRV votes
```
Analysis: Locks incentivize long-term alignment. Fee yield to veCRV is modest (~1–5% APY historically) but consistent. Governance over emissions amplifies value of veCRV.

### Pattern 3: Buyback-and-burn (MakerDAO/Sky model)
```
stability_fee_revenue
  → MakerDAO DSS Flap auction
  → Protocol buys MKR on open market
  → MKR is burned
```
Analysis: Token supply decreases proportional to revenue. At $300–500M annual revenue, MKR burn is substantial. Risk: governance can redirect fees (and has, historically).

### Pattern 4: Fee switch (Uniswap model)
```
Pre-switch: 100% of trading fees → LPs
Post-switch: (100 - x)% → LPs, x% → UNI holders/treasury
```
Analysis: Fee switch activation is a major catalyst but creates LP-holder tension. Uniswap fee switch was fully activated December 2025. When auditing tokens with a "planned fee switch," treat it as unrealized until on-chain governance passes.

---

## Benchmarks (as of 2026-05-25)

| Protocol | Annual Revenue | Revenue/TVL | Token P/F | Value Accrual |
|---|---|---|---|---|
| MakerDAO/Sky | ~$400M | ~6% | ~15–25x | Buyback-and-burn (MKR) |
| GMX | ~$50–100M | ~15–20% | ~20–40x | Direct (ETH to stakers) |
| Uniswap | ~$500M–1B | ~0.5–1% | ~50–150x | ve-fee post Dec 2025 |
| Curve | ~$50–80M | ~2–4% | ~30–60x | veCRV fees + crvUSD interest |
| Aave | ~$150–300M | ~2–3% | ~20–50x | Treasury + stkAAVE rewards |
| Lido | ~$100–200M | ~0.5% | ~40–80x | LDO treasury, no direct yield |

Cross-reference with `reference_benchmarks.md` for current figures; the above represents 2024–2025 range estimates.

---

## 10 Core Principles

1. **FCR < 1.0 means staking rewards are a tax on non-stakers.** Any staking yield not backed by fee revenue is pure inflation — a transfer from non-stakers to stakers, not value creation.

2. **Fee revenue without value accrual to the token is irrelevant to token value.** A protocol generating $500M/year in fees that all go to LPs provides zero fundamental backing for its governance token.

3. **Revenue concentration is fragile.** A protocol deriving >80% of revenue from one product, one chain, or one market condition (bull) has effectively no revenue model under adverse conditions.

4. **Volume/TVL ratio is the revenue multiplier.** Two protocols with equal TVL can have 10× different revenue if one has higher capital efficiency (v3 style) or higher-fee activity (perps vs. stablecoin swaps).

5. **Fee rate optimization is non-trivial.** Raising fees reduces volume (elasticity varies by product). Optimal fee rate maximizes `fee_rate × volume(fee_rate)`. Too high, and LPs leave; too low, and revenue is insufficient.

6. **The P/F ratio compresses as protocols mature.** Early-stage DeFi trades at 100–300x revenue (growth pricing); mature protocols trade at 10–50x. Auditing a new protocol at 500x P/F requires a very specific growth thesis.

7. **Buyback-and-burn is only as strong as governance's commitment to it.** MakerDAO redirected surplus buffer to RWA before burning MKR in some periods. A buyback mechanism that governance can override is not a guaranteed floor.

8. **veToken fee yield is real but modest without Curve-scale TVL.** At $100M TVL and 50% fee share, veCRV-style mechanics generate ~1–3% fee APY. Protocols launching ve-token mechanics at low TVL will have uncompetitively low real yield, forcing them to compensate with inflation — defeating the purpose.

9. **Fee switches are political events, not technical ones.** Activating a fee switch that LP providers were not expecting can trigger LP flight. Design fee switches with LP notice periods and graduated activation.

10. **Real yield must be denominated in non-native token to avoid circularity.** Paying staking rewards in ETH or USDC is real yield. Paying in the protocol's own token is inflation renamed.

---

## Red Flag Patterns (reference to red_flags_master.md)

These map to existing flags — use fee_economics.md as analytical depth when a flag triggers:

| Pattern | Maps To | Diagnostic |
|---|---|---|
| FCR = 0 (no revenue at all) | M-01 (no value accrual) | Check `economics.annual_revenue_usd` and `value_accrual_to_token` |
| FCR < 0.5 with staking yield > 20% | H-07 (unsustainable APY) | Inflation cost >> fee revenue |
| Revenue > 80% from one source | M-11 (single revenue source) | Check `protocol_revenue_sources` list |
| Fee accrues to LPs only, not token | M-01 (no value accrual) | `value_accrual_to_token = none` |
| Fee switch "planned" but not live | I-01 (assumption noted) | Treat as zero revenue for grading |
| P/F > 200x with no revenue growth thesis | M-10 (overvaluation risk) | Flag in competitive analysis |

---

## Key Sources

- GMX fee distribution and esGMX mechanics — protocol docs (from training knowledge + reference_benchmarks.md)
- Curve Finance fee distribution (3CRV to veCRV) — protocol docs and `vetokens_and_emissions.md`
- MakerDAO stability fee and MKR burn mechanism — MakerDAO forum and governance history (from training knowledge)
- Uniswap fee switch governance (Proposal 43, activated December 2025) — from training knowledge
- Token Terminal — P/F ratio methodology and DeFi revenue benchmarks (from training knowledge)
- DeFiLlama fees dashboard — revenue/TVL data methodology (from training knowledge)
