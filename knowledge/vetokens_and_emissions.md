# veTokens and Emissions

## Key Formulas

### Vote-Escrow Boost (Curve veCRV Model)

Lock weight (voting power):
```
veCRV = CRV_locked * (time_remaining / MAX_LOCK_TIME)
```
- `MAX_LOCK_TIME` = 4 years (Curve)
- Linear decay: veCRV decreases to 0 at lock expiry
- A 1-year lock on 1 CRV yields 0.25 veCRV

Liquidity mining boost multiplier:
```
boost = min(1, (user_liquidity / pool_liquidity) * (total_veCRV / user_veCRV) * 0.4) / 0.4
```
Simplified boost bound:
```
effective_boost = min(2.5x, 1 + 1.5 * (user_veCRV / total_veCRV) / (user_LP / total_LP))
```
- Minimum boost = 1x (no veCRV held)
- Maximum boost = 2.5x (sufficient veCRV relative to LP share)
- Boost clamp prevents whales from extracting unlimited advantage

Gauge weight vote allocation (weekly):
```
gauge_emissions_i = total_weekly_emissions * (votes_i / total_votes)
```

### Emission Decay Curves

**Exponential decay:**
```
E(t) = E_0 * r^t
```
- `r` = weekly/epoch decay factor (e.g., 0.99 per week ≈ 40% annual reduction)
- Circulating supply growth rate: `g(t) = E(t) / S(t)`, decreasing monotonically if `r < 1`

**Bitcoin-style halving:**
```
E(t) = E_0 / 2^floor(t / H)
```
- `H` = halving interval (epochs or blocks)
- Supply growth rate drops discontinuously at each halving; creates sell-pressure cliffs

**Polynomial decay:**
```
E(t) = E_0 / (1 + k*t)^n
```
- Slower long-run decay than exponential; higher tail inflation

**Circulating supply at time T (exponential):**
```
S(T) = S_0 + E_0 * (1 - r^T) / (1 - r)
```

**Terminal supply (exponential, r < 1):**
```
S_inf = S_0 + E_0 / (1 - r)
```

**Inflation rate at epoch t:**
```
inflation_rate(t) = E(t) / S(t)
```
Healthy range benchmark: < 5% annual inflation once protocol is mature (post year 2).

### Bribe Market Economics

Bribe efficiency ratio:
```
BER = USD_value_of_emissions_directed / USD_value_of_bribes_paid
```
- BER > 1: bribing is profitable for LPs/protocols (healthy incentive to participate)
- BER < 1: bribing is extractive relative to return; rational actors stop bribing
- Typical healthy range: BER 1.5–4x at protocol maturity

Vote-bribe equilibrium (competitive bribe market):
```
bribe_per_vote ≈ (gauge_emission_value * gauge_share) / total_votes_on_gauge
```
At Nash equilibrium, marginal bribe = marginal emission value captured.

---

## Core Principles

1. **Lock duration = alignment duration.** Voting power must decay proportionally to remaining lock time. Eternal or non-decaying locks (e.g., early Solidly) remove the time-preference signal entirely.

2. **Emissions must be gauge-voted, not fixed.** Static allocation favors insiders; gauge voting enables market-driven capital allocation, letting protocols compete for liquidity.

3. **Boost multipliers must be bounded.** Unbounded boosts allow whale dominance that destroys small-LP participation. Curve's 2.5x ceiling is the canonical bound.

4. **Decay rate must outpace new token unlock schedules.** If investor/team vesting unlocks add supply faster than emissions decay, net inflation accelerates mid-life. Model total token supply growth, not just emissions.

5. **Tail emissions should be non-zero but small.** Zero tail emissions collapse LP incentives post-emission; pure fee revenue requires massive TVL. Tail emission of 0.5–2% annual inflation preserves baseline LP incentive without hyperinflation.

6. **Bribing is only healthy when BER > 1 for the briber.** If protocol bribes exceed emission value returned, the protocol is subsidizing veToken holders with no liquidity depth benefit.

7. **veCRV-style model requires high TVL to function.** At low TVL, bribe markets are thin, vote manipulation is cheap, and small actors are priced out of meaningful boosts. Deploy ve-token mechanics only when TVL > $50M and token liquidity is deep.

8. **Front-loaded emissions accelerate bootstrapping but compress token price.** Front-loading (high E_0, steep decay) floods early supply; combine with high initial lock incentives to offset sell pressure.

9. **Emission schedules must be immutable or governed by time-locked governance.** Mutable emission parameters are a vector for governance attacks that inflate supply for extractive exits.

10. **Protocol revenue must eventually exceed emission cost.** Define the crossover epoch: when `fee_revenue_USD > emission_cost_at_market_price`. If no crossover is modeled within 4 years, the model is unsustainable.

---

## Failure Patterns

### Solidly / ve(3,3) Failure (Andre Cronje, 2022)

**Critical design flaws:**

1. **No lock decay.** vSOLID locks were permanent and non-decaying in early iterations. Voting power did not decrease over time, eliminating the long-term alignment incentive. Holders voted for their own pools perpetually with no cost.

2. **Emissions proportional to TVL, not locked supply.** Emissions scaled with protocol TVL, creating a reflexive loop: more TVL → more emissions → token dilution → TVL migration. Protocols raced to dump emissions rather than hold.

3. **Protocol-owned NFT voting.** Protocols received veNFT positions and directed 100% of votes to their own pools, concentrating emissions extraction with zero public bribe competition.

4. **No LP fee capture for veHolders.** In early Solidly, trading fees went to LPs rather than veHolders. This removed the core alignment mechanism of Curve (fees → veHolders → lock incentive).

5. **Mercenary protocol participation.** Protocols forked the code (Velodrome, Chronos, Thena, etc.) rather than locking SOLID. This fragmented liquidity and diluted bribe markets across forks.

### Velodrome Fixes (Optimism, 2022–present)

1. **Lock decay restored.** veVELO decays linearly to zero at lock expiry, identical to Curve. Restores time-alignment.

2. **Fees to veVELO holders, not LPs.** Trading fees from a gauge flow to veVELO voters who voted for that gauge. Direct correlation: vote for good pools → earn fees from those pools. Aligns voter interest with protocol health.

3. **Epoch-based voting resets.** Votes reset each epoch (weekly). Voters must actively re-vote, preventing passive extraction. Introduces ongoing governance engagement requirement.

4. **veNFT transferability.** Positions are transferable NFTs, enabling secondary market price discovery for locked positions without breaking the lock mechanic.

5. **Protocol-owned liquidity (POL) seeding.** Velodrome team seeded initial liquidity and locked large veVELO positions, bootstrapping the bribe market with sufficient depth before public launch.

6. **Team emissions vest over time.** Team allocation subject to same lock mechanics, not preferential unlock.

### Emission Hyperinflation Warning Signs

- Annual inflation rate > 100% in Year 1 with no corresponding TVL growth
- `S(t)` doubling faster than `TVL(t)`: token supply outpaces value captured
- Vesting cliff unlocks (team/investors) coinciding with emission peaks → combined dilution event
- Decay factor `r` > 0.999 per epoch (near-zero decay): essentially flat emissions forever
- Emission schedule has no defined terminal supply (unbounded)

### Mercenary Liquidity Pattern

- LPs hold zero protocol tokens; all yield immediately sold
- LP churn rate > 30% per epoch
- TVL correlation with token price > 0.9 (TVL leaves when price drops)
- No veToken lock ratio: locked supply / circulating supply < 10%

### Bribe Extraction (Unhealthy Bribe Market)

- BER < 1.0 sustained for > 3 epochs: bribers paying more than they receive
- Single actor controls > 40% of veToken votes: cartel pricing of gauge access
- Bribe-to-emission ratio growing quarter-over-quarter without TVL growth: rent extraction compressing protocol value
- Protocols bribing their own gauge with protocol treasury: circular value extraction

---

## Mitigations / Best Practices

**Lock mechanic:**
- Enforce linear decay on all voting power; no permanent locks
- Set MAX_LOCK_TIME between 2–4 years; shorter = lower alignment, longer = lower participation
- Allow lock extensions but not early unlocks without a penalty fee (e.g., 50% slash returned to veHolders)

**Emission schedule:**
- Define `E_0`, decay factor `r`, and `S_inf` before launch; publish as immutable parameters or require 6-month timelock to modify
- Target: Year-1 inflation < 80%, Year-2 < 40%, Year-3+ < 10%, tail < 2%
- Model combined dilution: emissions + investor vesting + team unlock on a single supply chart
- Include a "death spiral" stress test: what happens if token price drops 80% in month 3? Do emissions still incentivize enough TVL to generate fees?

**Bribe market health:**
- Require minimum lock duration to vote on gauges (e.g., 3-month minimum) to prevent flash-lock voting attacks
- Implement vote-weight caps per gauge (e.g., max 30% of emissions to a single pool) to prevent emission monopolization
- Publish BER metrics publicly each epoch; protocols and LPs should monitor this ratio

**Velodrome-pattern adoption checklist:**
- [ ] Fees accrue to veToken voters of the gauge that generated them (not all veHolders equally)
- [ ] Weekly vote resets with active re-vote required
- [ ] Decay-based lock weight, not permanent
- [ ] veNFT format for transferability
- [ ] Bribe marketplace with transparent on-chain BER visibility
- [ ] Team/investor positions subject to identical lock mechanics

**Emission guardrails:**
- Governance-adjustable emission rates should require: (a) supermajority (> 67% veToken vote), (b) 2-week timelock, (c) maximum adjustment of ±20% per epoch
- Hard-cap on weekly emissions as percentage of circulating supply (e.g., no single epoch can emit > 5% of current circulating supply)
- Automatic emission reduction trigger: if 30-day avg token price drops > 50% from ATH, apply an additional 0.5x multiplier to scheduled emissions

---

## Key Sources

- Curve Finance whitepaper — veCRV mechanism, boost formula, gauge weight voting (from training knowledge)
- Curve DAO source code — `VotingEscrow.vy`, `LiquidityGauge.vy` boost implementation (from training knowledge)
- Andre Cronje, "Solidly — the new AMM" (2022) — ve(3,3) original design post (from training knowledge)
- Velodrome Finance documentation and v2 architecture (2022–2023) — fee-to-voter mechanic, epoch resets (from training knowledge)
- Michael Egorov / Curve team — gauge controller design and bribe market emergence (from training knowledge)
- Votium, Hidden Hand protocol mechanics — bribe aggregator market structure and BER empirical data (from training knowledge)
- Delphi Digital, "The Curve Wars" research report (2021–2022) — Convex, Yearn gauge competition (from training knowledge)
- Token Engineering Commons — emission schedule modeling frameworks (from training knowledge)
