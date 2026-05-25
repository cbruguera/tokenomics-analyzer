# Token Velocity

## Key Formulas

### MV = PQ (Quantity Theory of Money applied to tokens)
| Symbol | Definition | Notes |
|--------|-----------|-------|
| M | Token supply (circulating) | Fixed or algorithmically scheduled |
| V | Velocity — average number of times a token changes hands per period | V = (Total on-chain transaction volume) / M |
| P | Price level of the service denominated in the token | Fiat price of one unit of the service |
| Q | Quantity of services/goods exchanged via the token per period | Real throughput of the network |

**Derived token price:**
```
P_token = (P * Q) / (M * V)
```
Or equivalently, the implied market cap:
```
Market Cap = P * Q / V
```

**Key implication:** Holding GDP (P×Q) constant, a doubling of V halves the market cap. Token price is inversely proportional to velocity.

### Velocity from on-chain data
```
V = Annual on-chain transaction volume (USD-equivalent) / Average circulating market cap
```
Bitcoin historical V ≈ 3–7×/year. Stablecoins (USDC, USDT) V > 50×/year. High-utility "gas" tokens can exceed 100×/year in theory.

### Hold-Time / Velocity Relationship
```
V = 1 / Average_hold_time_in_years
```
If average hold time = 3 days → V ≈ 122. If average hold time = 1 year → V = 1.

### Sink-Adjusted Velocity
```
V_effective = (M_circulating / M_total) * V_raw
```
Where M_circulating = M_total − M_locked (staked, escrowed, burned).

---

## Core Principles

1. **Velocity is the dominant value driver in MV=PQ models.** Given any fixed GDP (P×Q), a 10× increase in V destroys 90% of token value. Protocol designers must treat velocity as a first-class design variable.

2. **Pure medium-of-exchange tokens have a fundamental value floor near zero.** (Pfeffer, 2017) If a token's only use is to pay for a service and users can acquire it instantly on a DEX, rational actors hold the minimum balance needed — driving M_effective → 0 and V → ∞.

3. **Utility ≠ value accrual.** (Samani, 2018) A token can mediate $10B of annual transactions yet have a market cap of $100M if V = 100. High utility and high token value are only correlated when sinks exist that reduce velocity.

4. **The "hot potato" problem.** If there is no incentive to hold a token beyond immediate use, all participants minimize hold time. Each actor rationally passes the token as fast as possible, creating a reflexive velocity spiral.

5. **Substitutability amplifies velocity.** If multiple tokens or fiat on-ramps can substitute for the native token (e.g., protocol accepts USDC as well as native token), demand for the native token collapses and V for the remaining holders spikes.

6. **Monetary premium requires speculation discount.** (Burniske) Tokens can command a premium beyond their utility value only if speculators expect future price appreciation. This premium is unstable and cannot be relied upon in a valuation model.

7. **PQ growth does not automatically increase token price.** Network growth raises P×Q but if V scales proportionally (more users transact, not hold), price is unchanged. Sinks must scale with GDP for token price to appreciate.

8. **Velocity is bounded by block throughput.** Technical transaction-per-second limits create an implicit cap on V independent of demand.

---

## Failure Patterns

### 1. The Velocity Trap (canonical case)
- **Condition:** Token required to pay for service; users buy immediately before use, sell immediately after receiving.
- **Mechanism:** Minimum viable hold time approaches one block (~seconds to minutes). V → (seconds per year / seconds per block).
- **Consequence:** Market cap ≈ (daily GDP × ~1 day holding period). For a $1B/year network with 1-day average hold: Market Cap ≈ $2.7M.
- **Examples:** Early Golem (GNT), Basic Attention Token at launch, most 2017-era ICO utility tokens.

### 2. Reflexive Sell Pressure From Staking Emissions
- **Condition:** Protocol mints staking rewards; stakers sell rewards to cover operating costs or realize yield.
- **Mechanism:** Inflation increases M; yield farmers immediately sell rewards → V for reward tokens is near-maximum.
- **Consequence:** Nominal APY is misleading; real value of staked position erodes unless buy-side demand grows faster than emissions.
- **Examples:** Numerous DeFi protocols 2020–2022 (OHM forks, high-emission yield farms).

### 3. Staking Without Demand Constraint
- **Condition:** Staking locks tokens but the locked supply is not tied to productive use or scarcity of a real resource.
- **Mechanism:** Locking M_locked reduces circulating supply but P×Q doesn't increase proportionally → P_token inflated beyond real GDP, creating a bubble.
- **Consequence:** When staking incentives decline, M_locked unlocks, circulating supply jumps, price collapses. Not a true sink.
- **Examples:** Pure "stake-to-earn" tokens with no underlying demand for the service.

### 4. Circular/Recursive Token Demand
- **Condition:** Token demand is driven primarily by other participants wanting to stake/speculate, not by service consumers.
- **Mechanism:** GDP (P×Q) is mostly denominated in the token itself (staking rewards, governance payouts) rather than external value.
- **Consequence:** Reflexive collapse when external demand dries up; MV=PQ GDP numerator shrinks and V has no floor.
- **Examples:** Ponzi-structured "ecosystem" tokens; early DeFi governance tokens with no fee switch.

### 5. Competing On-Ramp Suppression
- **Condition:** CEX listings, fiat pairs, or stablecoin substitution routes allow users to sidestep the native token.
- **Mechanism:** GDP transacted through non-native paths does not appear in token V numerator (on-chain volume) but reduces demand for the native token.
- **Consequence:** On-chain V appears low (false signal of health) while actual token demand is structurally undermined.

### 6. Governance Token Value Illusion
- **Condition:** Governance rights are non-transferable in practical terms (quorum rules, time locks) and the protocol has no fee switch.
- **Mechanism:** MV=PQ GDP = $0 because no cash flows are governed; token value rests entirely on option value of future fee switch.
- **Consequence:** Token price is a pure speculation on governance activation; fundamental value = 0 until fee switch activates.
- **Examples:** Early UNI, COMP before fee discussions; most DAO governance tokens.

### 7. Pfeffer's "No Store of Value" Argument
- **Condition:** Token has no store-of-value use case; protocol is not a sovereign monetary network; another token (BTC) already dominates monetary premium.
- **Mechanism:** In equilibrium, rational actors hold the minimum token balance for utility purposes. M_effective → 0, or V → ∞.
- **Consequence:** Utility tokens converge toward zero value in a competitive, rational market. Only protocols that win a "winner-take-all" monetary use case can sustain value.

---

## Mitigations / Best Practices

### Against the Velocity Trap
| Design Choice | Mechanism | Tradeoff |
|--------------|-----------|----------|
| **Protocol fee payable only in native token** | Forces transient demand at minimum | Competitive disadvantage vs. stablecoin fee protocols |
| **Mandatory minimum stake to access service** | Users must hold a balance proportional to usage | Friction; UX degradation |
| **Time-weighted fee discounts** | Reward longer holding with lower fees | Requires careful calibration to avoid gaming |
| **Work tokens** (Juels & Bresnahan model) | Service providers must stake tokens as collateral; stake size ∝ work volume | Effective only when provider collusion risk is real |

### Sink Mechanisms (ranked by effectiveness)
1. **Burn-on-use (deflationary):** Portion of every transaction fee is burned. Reduces M permanently. BNB model. V is unchanged but M shrinks → price appreciation if P×Q grows.
   - Formula: `dM/dt = -burn_rate * Volume`. Effective when Volume growth outpaces new issuance.
2. **Staking for access rights:** Token locked to receive a right (e.g., validator slot, premium tier). Reduces circulating M without creating sell pressure if unlock periods are long (≥1 year).
   - Rule of thumb: need ≥20–30% of circulating supply locked to meaningfully impact velocity.
3. **Governance escrow with vote-locking:** veToken model (Curve veCRV). Lock duration 1–4 years; voting power ∝ lock time. Creates strong time-preference sink.
   - Observed effect on Curve: ~50% of CRV locked at any given time, materially reducing effective V.
4. **Protocol-owned liquidity using buyback-and-lock:** Treasury buys tokens on open market, locks in LP. Reduces float without inflationary issuance.
5. **Fee redistribution to stakers:** Stakers earn protocol revenue (not new issuance). Incentivizes holding without increasing M. Only effective when protocol generates real fees.

### Against Staking-Emission Reflexivity
- Cap annual emission to ≤ projected real fee revenue within 2–3 years.
- Implement emission decay schedules (halving or linear reduction).
- Separate "security budget" (validator rewards) from "growth budget" (LP incentives); sunset growth budget on a fixed timeline.

### Against Governance Token Value Illusion
- Commit to a fee switch activation date or milestone in governance docs.
- Structure fees so a fraction accrues to a DAO treasury immediately (even if small), establishing real cash-flow GDP.
- Use time-lock contracts to make future fee activation credible.

### Quantitative Velocity Benchmarks
| V Range | Interpretation | Design Status |
|---------|---------------|---------------|
| V < 1 | Tokens held >1 year on average; strong store-of-value behavior | Healthy |
| 1 ≤ V ≤ 10 | Moderate velocity; acceptable for large-cap networks | Acceptable |
| 10 < V ≤ 50 | High velocity; strong sinks required to sustain valuation | Concerning |
| V > 50 | Approaching stablecoin-level velocity; near-zero fundamental value | Critical |

- Bitcoin (2020–2024): V ≈ 3–6. ETH: V ≈ 8–15. USDC/USDT: V > 50.
- Any token with V > 20 and no active burn or staking sink should be flagged as a velocity trap candidate.

### Protocol Design Checklist (velocity-focused)
- [ ] Is there at least one sink locking ≥20% of circulating supply?
- [ ] Does staking yield derive from fees, not new issuance?
- [ ] Is the burn rate sufficient to offset new emissions under base-case growth?
- [ ] Does the GDP (P×Q) include only external, non-circular demand?
- [ ] Is V < 20 under stress-test assumptions (GDP −50%, sinks −30%)?
- [ ] Is there a credible fee switch or cash-flow mechanism in the governance roadmap?

---

## Key Sources

1. **Burniske, Chris** — "Cryptoasset Valuations" (Medium, 2017).
   https://medium.com/@cburniske/cryptoasset-valuations-ac83479ffca7
   Primary application of MV=PQ to token valuation; defines V for cryptoassets; introduces current utilization ratio.

2. **Burniske, Chris & Tatar, Jack** — *Cryptoassets: The Innovative Investor's Guide to Bitcoin and Beyond* (McGraw-Hill, 2017).
   Full treatment of MV=PQ, current utilization ratio (CUR), and discounted utility model for token price.

3. **Pfeffer, John** — "An Institutional Investor's Take on Cryptoassets" (2017, v6 final).
   https://s3.eu-west-2.amazonaws.com/john-pfeffer/An+Institutional+Investor%27s+Take+on+Cryptoassets+v6.pdf
   Argues utility tokens trend toward zero in rational equilibrium; only monetary store-of-value tokens (BTC) can sustain non-trivial value.

4. **Samani, Kyle** — "New Models for Utility Tokens" (Multicoin Capital, 2018).
   https://multicoin.capital/2018/02/13/new-models-for-utility-tokens/
   Defines velocity traps; catalogs sink mechanisms (staking, burn, work tokens, gamification); introduces the concept of hold-time engineering.

5. **Samani, Kyle** — "On Value Capture at Layers 1 and 2" (Multicoin Capital, 2019).
   Extension of velocity analysis to L1 vs. L2 value accrual; fat protocol thesis critique.

6. **Evans, Alex** — "A Monetary Policy for Crypto" (Placeholder VC, 2019).
   Academic extension: formalizes velocity as a function of holding incentive structure; introduces "velocity-adjusted" GDP model.

7. **Juels, Ari & Bresnahan, Timothy** — Work token model formalization.
   Referenced in Samani (2018); work tokens as a theoretically sound sink: providers stake to earn the right to perform work, creating demand proportional to service volume.

8. **Davarpanah, A. et al.** — Academic critiques of MV=PQ applied to tokens (2019–2022).
   Key critique: MV=PQ assumes velocity is exogenous and stable; in token systems, V is endogenous and responds reflexively to price, invalidating naive valuations.

9. **Curve Finance veCRV documentation** — Empirical case study for vote-escrow sink model.
   https://curve.readthedocs.io/dao-vecrv.html

10. **BNB Whitepaper / Binance Quarterly Burn Reports** — Empirical case study for burn-on-use deflation.
    https://www.binance.com/en/blog/ecosystem/bnb-auto-burn-explained-421499824684903302
