# Simulation Baselines

Default parameters for all cadCAD and Mesa simulations.
Override with values from the parsed TokenModel where available.

---

## Initial Conditions

| Parameter | Default | Source |
|---|---|---|
| Initial token price | $1.00 | Normalized for comparability |
| Initial circulating supply | From `supply.initial_circulating` | TokenModel |
| Initial treasury (USD) | From `economics.treasury.size_usd` | TokenModel |
| Initial staking rate | 20% of circulating supply | Use 40% if launch APY >15% |
| Initial protocol revenue (monthly) | From `economics.protocol_revenue_sources` | TokenModel |
| Initial TVL (if DeFi protocol) | 10× treasury size (estimate if unknown) | Heuristic |

---

## Time Horizon and Steps

| Parameter | Default |
|---|---|
| Simulation duration | 120 months (10 years) |
| Time step | 1 month |
| Monte Carlo paths | 1000 |
| Burn-in period (excluded from analysis) | 0 months |
| Reporting intervals | Monthly + annual aggregates |

---

## Scenario Definitions

| Scenario | Description | Demand growth | Price trajectory |
|---|---|---|---|
| **Base** | Moderate adoption | +20%/yr Y1–3, +10%/yr Y4+ | Follows demand with 80% vol |
| **Bull** | Strong adoption | +100%/yr Y1–2, +30%/yr Y3+ | Follows demand with 120% vol |
| **Bear** | Slow adoption | Flat Y1, −30% Y2, −50% Y3, flat thereafter | Follows demand |
| **Stress** | Severe shock | −80% demand over 6 months (starting month 12) | Shock −80% over 6 months |
| **Whale exit** | Insider unlock sell | Top vesting cliffs: 90% sold within 30 days of unlock | Supply shock + price impact |

All simulations run Base, Bear, and Stress by default. Bull and Whale Exit are optional.

---

## Monte Carlo Parameters

| Parameter | Default |
|---|---|
| Annual price volatility | 120% (crypto baseline) |
| Demand growth distribution | Log-normal, μ = base scenario rate, σ = 60% |
| Price ↔ demand correlation | 0.70 |
| Tail event: severe demand shock | 5% probability per year of −90% demand |
| Random seed (reproducible runs) | 42 |

**Percentile outputs:** P10, P25, P50, P75, P90 for price and circulating supply.

---

## Actor Distributions (Agent-Based Model)

| Actor Type | Default Share of Supply | Sell Behavior |
|---|---|---|
| Long-term holders (HODLers) | 30% | Hold unless price drops >70% from cost basis |
| Speculators | 25% | Momentum-following; exit on 30-day negative trend |
| Protocol users | 20% | Hold only for active utility; sell after use (high velocity) |
| Stakers / validators | 15% | Stake while APY > opportunity cost (default 5% annual) |
| Team / treasury | 10% | Sell 10% of newly vested tokens per quarter |

---

## Staking Dynamics Parameters

| Parameter | Default |
|---|---|
| Staking APY sensitivity | +1% staking rate per +0.5% APY above opportunity cost |
| Opportunity cost (baseline) | 5% annual (risk-free rate proxy) |
| Mass unstaking trigger | Price drop >40% in 30 days → 20% of staked supply unstakes |
| Unbonding period | From `utility.staking.unbonding_period_days` (default: 14 days) |
| Staking reward source split | From `utility.staking.reward_source` in TokenModel |

**Reflexivity loop (simulate explicitly):**
```
APY(t) = f(staking_rate(t), emission_rate(t), price(t))
staking_rate(t+1) = staking_rate(t) + sensitivity × (APY(t) - opportunity_cost)
circulating(t+1) = total_supply(t) - staked(t+1)
price(t+1) = f(circulating(t+1), demand(t+1))
```

---

## Stress Test Parameters

| Stress Scenario | Parameter | Default Value |
|---|---|---|
| Bear market price shock | Decline over 6 months | −80% from peak |
| Bear market demand shock | DAU/usage decline | −60% over 3 months |
| Liquidity shock | DEX liquidity drain | −70% over 1 month |
| Treasury stress | Native token component | −80%; stablecoins unchanged |
| Whale exit | Vesting cliff sell pressure | 90% of cliff unlock sold in 30 days |
| Governance attack cost | At stressed price | Recalculate: 51% of circulating × spot price |

---

## Emission Model Parameters

| Parameter | Default |
|---|---|
| Emission curve type | From `supply.emission_schedule` in TokenModel |
| If exponential decay: decay factor r | 0.99 per month (≈11% annual reduction) |
| If linear: annual amount | From `supply.emission_rate_annual_pct` |
| If halving: halving interval | 48 months (default) |
| Vesting unlock events | From `distribution.*` + `vesting.*` in TokenModel |

**Combined dilution model:** Plot emissions + all vesting unlocks on a single supply chart. Flag any month where combined new supply >5% of circulating supply as a "dilution event."

---

## Chart Output Requirements

Every simulation run must produce the following charts, saved to `analysis/<token-name>/`:

| Chart | Filename | Contents |
|---|---|---|
| Supply curve | `supply.png` | Total supply, circulating, staked, locked over time |
| Price percentiles | `price_bands.png` | P10/P25/P50/P75/P90 price over time |
| Treasury runway | `runway.png` | Months of runway remaining over time |
| Staking dynamics | `staking.png` | Staking rate, APY, and unstaking events over time |
| Death spiral triggers | `stress_triggers.png` | Which checklist conditions activate and when |
| Dilution events | `dilution.png` | Monthly new supply as % of circulating; flag events >5% |

All charts: 1200×800px, saved as PNG, labeled axes with units.
