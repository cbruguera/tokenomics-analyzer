# Staking Dynamics

## Key Formulas

### Ethereum Post-Merge Issuance (Consensus Layer)

Base reward per validator (per epoch):
```
base_reward = effective_balance * BASE_REWARD_FACTOR
              / integer_sqrt(total_active_balance) / BASE_REWARDS_PER_EPOCH
```
Where:
- `BASE_REWARD_FACTOR = 64` (EIP-1971 / Altair)
- `BASE_REWARDS_PER_EPOCH = 4`
- `effective_balance` = validator balance capped at 32 ETH (in Gwei)
- `total_active_balance` = sum of all active validator effective balances (in Gwei)

Annual issuance as a function of total ETH staked `S`:
```
Annual_Issuance(S) ≈ 940.87 * sqrt(S)   [ETH/year, S in ETH]
```
Approximate APY for a validator:
```
APY(S) ≈ 940.87 / sqrt(S)
```
Reference points (pre-EIP-4844 era, no MEV):
| S (ETH staked) | APY (approx) |
|---------------|--------------|
| 1,000,000     | ~18.8%       |
| 10,000,000    | ~5.9%        |
| 20,000,000    | ~4.2%        |
| 30,000,000    | ~3.4%        |

Key property: issuance scales as `sqrt(S)`, so APY is inversely proportional to `sqrt(S)` — a deliberate design choice to penalize over-staking and maintain security without excessive inflation.

Annual inflation rate:
```
inflation_rate(S) ≈ 940.87 * sqrt(S) / total_supply
```
At 120M ETH supply and 30M ETH staked: ~0.5% annual issuance (partially offset by EIP-1559 burns).

**Post-Dencun adjustment (EIP-4844, March 2024):** Dencun introduced blob transactions, which move L2 data posting from expensive calldata to cheap, ephemeral blobs. L2s immediately shifted to blobs, sharply reducing calldata fees and therefore EIP-1559 base fee burn. Net result: ETH net issuance turned positive (inflationary) in most post-Dencun periods. As of mid-2026, with ~34M ETH staked, gross issuance is ~0.9% annually but net inflation is ~0.18–0.23% after burn — lower burn than pre-Dencun during high-activity periods, higher when L2 activity is low. When auditing protocols that benchmark against ETH's "deflationary" narrative, note this shift: ETH is not reliably deflationary post-Dencun. See `reference_benchmarks.md` for current figures.

### General Staking Equilibrium Model

Let:
- `r(s)` = nominal staking APY as function of staking ratio `s = S/Supply`
- `c` = opportunity cost of staking (risk-free rate or liquid DeFi yield)
- `γ` = liquidity premium (compensation for lock-up / illiquidity)
- `π` = expected price appreciation of the token

Rational staking equilibrium condition:
```
r(s*) + π = c + γ
```
Steady-state staking ratio `s*` solves:
```
s* = [ r_0 / (c + γ - π) ]^2     [for issuance curves of the form r(s) = r_0 / sqrt(s)]
```
Where `r_0` is the issuance coefficient (e.g., ~940.87/Supply for Ethereum).

Implications:
- Rising token price expectation `π` increases `s*` (more staking as speculation rises)
- Falling opportunity cost `c` increases `s*`
- Liquid staking tokens (LSTs) reduce `γ → 0`, pushing `s*` up dramatically
- When `π < 0` (bear market), `s*` collapses unless `r(s)` is sufficiently high

### Real Yield Threshold

Define:
- `protocol_revenue(t)` = fees, MEV, or other non-inflationary income per period
- `staking_rewards(t)` = total issuance to stakers per period

Real yield staking (self-sustaining):
```
real_yield = protocol_revenue(t) / S   >  0
```
Purely inflationary staking (dilutive):
```
real_yield = 0,   all rewards = new token issuance
```
Break-even / real yield threshold condition:
```
protocol_revenue(t) >= staking_rewards(t)
⟺  fee_yield(s) >= inflation_rate(s)
```
If this condition fails, non-stakers subsidize stakers via dilution. Sustainability requires:
```
fee_revenue_per_token >= issuance_per_token
```

### Reflexivity Loop Equations

Define a discrete-time system:
```
APY(t)        = f(S(t), price(t))          -- reward rate given staked amount
inflow(t)     = α * max(APY(t) - c, 0)     -- new staking driven by yield attractiveness
S(t+1)        = S(t) + inflow(t) - outflow(t)
circ(t)       = total_supply - S(t)        -- circulating supply
price(t+1)    = price(t) * g(circ(t), demand(t))  -- price as function of supply/demand
```
Where `α` is staking sensitivity coefficient and `g(·)` is a price discovery function.

Positive reflexivity (bull loop):
```
price ↑ → π ↑ → s* ↑ → circ ↓ → price ↑  (self-reinforcing)
```
Negative reflexivity (bear collapse):
```
price ↓ → π < 0 → unstaking → circ ↑ → sell pressure → price ↓
```
Unstaking cascade trigger: when sell pressure from unlocked tokens exceeds buy demand:
```
outflow(t) * price(t) > demand_depth(t)  →  cascade
```

---

## Core Principles

1. **Issuance-curve shape determines equilibrium staking ratio.** Concave curves (sqrt, log) self-regulate — higher staking lowers per-validator APY, stabilizing at `s*`. Linear issuance (fixed APY regardless of staking) has no equilibrium and maximizes inflation pressure.

2. **Real yield is the only durable staking incentive.** Inflationary rewards are a zero-sum redistribution from non-stakers to stakers. Sustainable staking models must route protocol revenue (fees, MEV, liquidations) to stakers.

3. **Liquid staking eliminates the liquidity premium.** LSTs (e.g., stETH) collapse `γ → 0` in the equilibrium condition, pushing `s*` to near 100% of supply. This can starve DeFi liquidity and create systemic concentration risk.

4. **Lock periods and unbonding delays are reflexivity dampeners.** They introduce friction in the `inflow/outflow` terms, preventing cascading unstaking during price drops. Optimal unbonding delay trades off security (longer = safer) vs. capital efficiency (shorter = more staking).

5. **Slashing is a non-linear risk term.** Expected validator return = `APY - P(slash) * slash_penalty`. Slashing risk reduces effective APY and deters marginal stakers, keeping staking ratio from approaching 100%.

6. **Dynamic APY (target-rate mechanisms) is more stable than fixed issuance.** Setting a target staking ratio `s_target` and adjusting rewards accordingly (e.g., Cosmos-style) creates a restoring force: `APY ↑` when `s < s_target`, `APY ↓` when `s > s_target`.

7. **Unbonding delay must exceed the time needed to detect and prove validator misbehavior.** For slashing to deter attacks, the unbonding window must be longer than the evidence submission window.

8. **Staking concentration risk increases with protocol age.** Large staking pools compound rewards faster in absolute terms; anti-concentration mechanisms (e.g., Ethereum's effective balance cap) limit per-validator advantage.

---

## Failure Patterns

### 1. Inflationary Ponzi Collapse
**Condition:** `protocol_revenue << staking_rewards` (no real yield; pure dilution)

Mechanism:
- Early stakers earn high APY funded by minting
- New stakers dilute total issuance per validator → APY falls
- APY attractiveness falls → staking inflow stops
- Existing stakers exit → unlock pressure → token price falls
- Falling price destroys staking incentive entirely → full unwind

Diagnostic signal: staking reward yield consistently > fee burn rate with no path to fee growth.

### 2. Reflexivity Collapse (Unbonding Cascade)
**Condition:** `price drop → mass unstaking → sell pressure exceeds market depth`

Trigger sequence:
1. Token price drops X% (external shock or narrative change)
2. `π < 0` → staking no longer covers opportunity cost
3. Validators initiate unbonding en masse
4. Unbonded tokens hit market → price drops further
5. Positive feedback until new equilibrium or near-zero

Amplified by: short unbonding periods, no slashing risk, high staking ratio (more tokens to unlock).

### 3. Fixed-APY Death Spiral
**Condition:** Protocol guarantees fixed nominal APY (e.g., 20%) regardless of staking ratio

Mechanism:
- Fixed APY means issuance scales linearly with `S`
- More stakers → more issuance → more inflation → token devalues
- Real yield = `nominal_APY - inflation_rate` → approaches 0 or negative
- Stakers must continuously compound just to maintain real value
- Classic example: Anchor Protocol (UST/LUNA) — 20% fixed yield required unsustainable subsidies

Ponzi condition formally: `d(issuance)/d(S) > 0` with no corresponding `d(revenue)/d(S) > 0`.

### 4. Liquid Staking Concentration Risk
**Condition:** Single LST provider captures >33% of total stake

Risk: Protocol-level governance capture; correlated slashing events; systemic depeg of LST → mass redemption → liquidity crisis.

### 5. Compounding Inequality / Rich-Get-Richer
**Condition:** No effective balance cap or validator limit per entity

Large validators compound faster in absolute ETH terms; staking ratio concentrates over time; security model degrades as minority of actors controls majority of stake.

---

## Mitigations / Best Practices

### Dynamic APY with Target Staking Ratio
Implement a PID-style controller (analogous to Cosmos Hub):
```
APY(t+1) = APY(t) + k_p * (s_target - s(t))
```
Where `k_p` is the proportional gain. Sets a restoring force around `s_target` (e.g., 67%).

Advantages: prevents both over-staking (excessive inflation) and under-staking (security degradation).

### Unbonding Delay Design
- Minimum unbonding: `max(evidence_window, 1 epoch)`
- Recommended range: 7–28 days for PoS chains
- Ethereum uses ~27 hours (exit queue) + no forced unbonding (voluntary exit only)
- Tradeoff table:

| Delay     | Cascade Risk | Capital Efficiency | Slash Deterrence |
|-----------|-------------|-------------------|-----------------|
| <24h      | Very High   | High              | Low             |
| 7 days    | Medium      | Medium            | Medium          |
| 21 days   | Low         | Low               | High            |
| 28+ days  | Very Low    | Very Low          | Very High       |

### Real Yield Mandate
- Route a defined % of protocol fees directly to stakers (e.g., EIP-1559 tips, DEX fees)
- Target: `fee_yield(s) >= 50% of total staking APY` before launch
- Track `protocol_revenue / market_cap` (P/E equivalent) as sustainability metric

### Slashing Parameter Design
- Correlation penalty: slash amount scales with number of validators slashing simultaneously → deters coordinated attacks
- Ethereum: `slash_penalty = balance/32 + correlated_penalty * (3 * num_slashed / total_validators)`
- Minimum penalty deters individual negligence; correlation penalty deters Sybil attacks

### Anti-Reflexivity Circuit Breakers
- Rate-limit unbonding: cap total unbonding per epoch (e.g., max 1% of stake per day)
- Dynamic unbonding: extend unbonding periods automatically when net outflow exceeds threshold
- Reserve buffers: protocol-owned liquidity to absorb initial sell pressure during unwind

### Lock Period Incentives (Lock-Up Premium)
Tiered APY by lock duration:
```
APY(lock_duration) = base_APY * (1 + lock_premium * lock_duration / max_duration)
```
Attracts long-term stakers, reduces short-term reflexivity, reduces circulating supply volatility.

### Emission Schedule Design
- Decreasing issuance schedule: `emission(t) = emission_0 * decay^t`
- Ensures inflation rate falls over time regardless of staking ratio
- Prevents perpetual dilution in absence of revenue growth

---

## Key Sources

- Ethereum Consensus Specification (EIP-1971 / Altair): https://github.com/ethereum/consensus-specs/blob/dev/specs/altair/beacon-chain.md
- Ethereum Issuance Post-Merge overview: https://ethereum.org/en/roadmap/merge/issuance/
- Vitalik Buterin, "Serenity Design Rationale": https://notes.ethereum.org/@vbuterin/serenity_design_rationale
- ethresear.ch — "Calculating Stake Yields and Inflation": https://ethresear.ch/t/calculating-stake-yields-and-inflation/14841
- Cosmos Hub staking target-rate mechanism: https://github.com/cosmos/cosmos-sdk/blob/main/x/mint/README.md
- Lido / LST concentration risk analysis: https://dune.com/lido/lido-staking-stats
- Anchor Protocol post-mortem (fixed APY failure): https://cryptorisks.substack.com/p/anchor-protocol
- "Real Yield" framework — Token Terminal: https://tokenterminal.com/resources/articles/real-yield
- Tarun Chitra, "Competitive Equilibria Between Staking and On-chain Lending" (2020): https://arxiv.org/abs/2001.00919
- Vitalik Buterin, "On Staking Pool Concentration": https://notes.ethereum.org/@vbuterin/staking_pool_concentration
