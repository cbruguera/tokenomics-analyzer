# Red Flags Master Checklist

The weakness scanner runs this list top-to-bottom against every parsed TokenModel.
Each entry is a binary check: triggered (finding) or not triggered (pass).
**YAML Fields** column specifies exactly which model fields to inspect.
Severity determines the grade impact per `scoring_rubric.md`.

> **This file is the single source of truth for both flag definitions and evaluation rules.**
> Do not maintain a separate field-to-flag mapping. When adding a new flag, add the YAML fields column here.

---

## CRITICAL

| # | Check | Trigger Condition | YAML Fields to Inspect |
|---|---|---|---|
| C-01 | Endogenous collateral | Stablecoin/peg backed by protocol's own token at any % | `token.archetypes`, `economics.value_accrual_to_token`, `additional_notes` |
| C-02 | No lockup for insiders | Team AND investor tokens both have cliff=0 AND duration=0 | `vesting.team.cliff_months`, `vesting.team.duration_months`, `vesting.investors.cliff_months`, `vesting.investors.duration_months` |
| C-03 | Ponzi structure | Staking/yield funded by new entrant capital AND zero external protocol revenue | `economics.protocol_revenue_sources`, `utility.staking.reward_source`, `economics.value_accrual_to_token` |
| C-04 | Death spiral conditions | ≥6 of 10 conditions on death spiral checklist triggered simultaneously | Run Step 4b checklist from `failure_postmortems.md` |
| C-05 | Governance flash loan attack | No snapshot delay AND no timelock → governance executable in same tx as vote | `utility.governance.timelock_days`, `utility.governance.voting_mechanism`, `additional_notes` |
| C-06 | Hyperinflation + no sink | Annual emission >100% of circulating supply AND no burn AND no staking lock | `supply.emission_rate_annual_pct`, `supply.burn_mechanism`, `utility.staking.enabled`, `economics.velocity_sinks` |
| C-07 | Fabricated APY | APY >1000% annualized with no verifiable external revenue | `economics.value_accrual_to_token`, `economics.protocol_revenue_sources`, `additional_notes` |
| C-08 | Zero exogenous collateral | Algorithmic stablecoin with 0% exogenous (non-native) collateral | `token.archetypes`, `economics.value_accrual_to_token`, `additional_notes` |

**Critical evaluation notes:**
- **C-01**: Hybrid collateral still triggers (e.g., 60% USDC + 40% native = triggered). Only pure exogenous collateral passes.
- **C-02**: If vesting is mentioned but schedule unknown, create I-05 (not C-02). C-02 requires confirmed zero vesting.
- **C-03**: Requires BOTH missing revenue AND inflation-funded staking. A protocol with even one real revenue source (fees, subscriptions, interest) does not trigger C-03.
- **C-05**: Snapshot.org off-chain vote with on-chain timelock enforcement = NOT C-05 (but may be H-07). No timelock + no snapshot delay = C-05.

---

## HIGH

| # | Check | Trigger Condition | YAML Fields to Inspect |
|---|---|---|---|
| H-01 | Short team cliff | Team vesting cliff < 12 months | `vesting.team.cliff_months` |
| H-02 | Cliff bomb | Single unlock event >10% of circulating supply at cliff date | `vesting.team.cliff_months`, `distribution.team_pct`, `supply.initial_circulating`, `vesting.investors.*` |
| H-03 | Insider concentration | Team + investor allocation combined >40% of total supply | `distribution.team_pct`, `distribution.investors_pct` |
| H-04 | Pure inflationary staking | Staking yield 100% from new token emission, 0% from protocol revenue | `utility.staking.reward_source`, `economics.protocol_revenue_sources` |
| H-05 | No stablecoin reserves | Treasury 0% stablecoins, 100% native token | `economics.treasury.composition` |
| H-06 | Short runway | Treasury runway <12 months at current burn rate | `economics.treasury.size_usd`, `economics.treasury.monthly_burn_usd` |
| H-07 | No governance timelock | Timelock absent or <24 hours | `utility.governance.timelock_days` |
| H-08 | Whale quorum | Single entity can reach quorum with <5% of total supply | `utility.governance.quorum_pct`, `distribution.*` |
| H-09 | Weak algorithmic stablecoin | Partial-collateral stablecoin with exogenous collateral <80% | `token.archetypes`, `economics.value_accrual_to_token`, `additional_notes` |
| H-10 | Emission front-load | Year-1 emission >80% of initial circulating supply | `supply.emission_rate_annual_pct`, `supply.initial_circulating` |
| H-11 | Single utility (substitutable) | Token has only one use case AND it is easily substituted by ETH/USDC | `utility.use_cases`, `economics.demand_drivers` |
| H-12 | Thin peg liquidity | Protocol DEX liquidity <10% of outstanding stablecoin/pegged asset supply | `economics.treasury.size_usd`, `additional_notes` |
| H-13 | Team vesting < product timeline | Team fully vested before protocol reaches stated milestones | `vesting.team.duration_months`, `additional_notes`, `token.launch_stage` |
| H-14 | Subsidized staking yield | >50% of staking yield funded by finite reserve drawdown (not revenue) | `utility.staking.reward_source`, `economics.treasury.size_usd`, `additional_notes` |

**High evaluation notes:**
- **H-02 calculation**: `cliff_unlock = (allocation_pct/100) × total_supply`; `circulating_at_cliff = initial_circulating + (emission_monthly × cliff_months)`; trigger if `cliff_unlock / circulating_at_cliff > 0.10`. Check team and investor cliffs separately and combined.
- **H-03**: Include advisors in the insider count if not broken out separately. Exclude: ecosystem fund, community treasury, public sale, LP incentives.
- **H-06 calculation**: `runway_months = treasury_size_usd / monthly_burn_usd`. If burn rate unknown, estimate by launch stage: concept $75K/mo, testnet $200K/mo, mainnet-early $650K/mo, mainnet-mature $1.5M/mo. Flag estimate as I-05.
- **H-08**: Trigger if any single distribution category (e.g., team alone at 25%) exceeds quorum threshold, OR if top-3 combined categories can reach quorum without community participation.
- **Do not double-trigger H-03 + M-02**: use H-03 (>40%) or M-02 (30–40%), not both. Same rule applies to H-06/M-07, H-10/M-06, H-14/M-12.

---

## MEDIUM

| # | Check | Trigger Condition | YAML Fields to Inspect |
|---|---|---|---|
| M-01 | Governance token no value accrual | Governance token with no fee capture, no buyback, no burn, no yield | `token.archetypes`, `economics.value_accrual_to_token`, `utility.fee_payment.fee_sink` |
| M-02 | Elevated insider allocation | Team + investor allocation 30–40% of total supply | `distribution.team_pct`, `distribution.investors_pct` |
| M-03 | Majority inflationary staking | Staking yield 50–99% from inflation, <50% from protocol revenue | `utility.staking.reward_source`, `economics.protocol_revenue_sources` |
| M-04 | Unbounded supply | No defined terminal supply or hard cap | `supply.uncapped`, `supply.emission_schedule` |
| M-05 | veToken deployed too early | Vote-escrow mechanics launched at TVL <$50M | `token.archetypes`, `economics.treasury.size_usd` |
| M-06 | Heavy front-loaded emissions | Year-1 emission 40–80% of initial circulating supply | `supply.emission_rate_annual_pct`, `supply.initial_circulating` |
| M-07 | Marginal treasury runway | Treasury runway 12–18 months at current burn | `economics.treasury.size_usd`, `economics.treasury.monthly_burn_usd` |
| M-08 | No governance delegation | No delegation mechanism in token-weighted governance | `utility.governance.voting_mechanism`, `additional_notes` |
| M-09 | Validator/LP cartel risk | Top-3 validators or stakers control >50% of stake/voting weight | `distribution.*`, `additional_notes` |
| M-10 | Low governance timelock | Governance timelock 24–48 hours (present but low) | `utility.governance.timelock_days` |
| M-11 | Single revenue dependency | 100% of protocol revenue from a single product or chain | `economics.protocol_revenue_sources` |
| M-12 | Reserve-subsidized yield | 20–50% of yield funded by reserve drawdown | `utility.staking.reward_source`, `economics.treasury.size_usd` |
| M-13 | No on-chain treasury visibility | Treasury not readable on-chain; no public dashboard | `economics.treasury.composition`, `additional_notes` |
| M-14 | Bribe market at thin TVL | veToken bribe market at TVL <$100M with <3 competing protocols | `token.archetypes`, `economics.treasury.size_usd`, `additional_notes` |

**Medium evaluation notes:**
- **M-03 vs H-04**: If reward_source = "mixed" and split is unknown, estimate by stage: pre-revenue → assume 90% inflation (→ H-04); early mainnet with stated fees → assume 65% inflation (→ M-03); mature protocol → check if below 50% before triggering M-03.
- **M-04**: Trigger if `supply.uncapped == true` OR if `emission_schedule` has no defined endpoint and no decay curve with a calculable terminal supply.

---

## LOW

| # | Check | Trigger Condition | YAML Fields to Inspect |
|---|---|---|---|
| L-01 | Undocumented emission schedule | No public supply chart or emission model | `supply.emission_schedule`, `supply.emission_rate_annual_pct` |
| L-02 | Short unbonding period | Staking unbonding period <7 days (bank-run vulnerable) | `utility.staking.unbonding_period_days` |
| L-03 | No formal risk disclosures | Team documentation acknowledges no economic risks | `risks_stated_by_team` |
| L-04 | Quorum not specified | Governance quorum threshold absent | `utility.governance.quorum_pct` |
| L-05 | No circuit breakers | No mention of automated protections for stress scenarios | `additional_notes`, `economics.value_accrual_to_token` |
| L-06 | Missing benchmark comparison | No comparable protocols named | `competitive.comparable_protocols` |
| L-07 | Treasury composition undisclosed | Treasury exists but asset breakdown not available | `economics.treasury.composition` |
| L-08 | Marginal governance timelock | Timelock 48–96 hours — functional but below 7-day standard | `utility.governance.timelock_days` |
| L-09 | Circular revenue | Protocol fees denominated in native token (self-referential) | `economics.protocol_revenue_sources`, `utility.fee_payment.fee_sink` |
| L-10 | Single price oracle | No redundant oracle or TWAP fallback | `additional_notes` |

**Low evaluation notes:**
- **L-09**: `fee_sink = "burned"` is NOT circular revenue. Circular only if fees are collected AND redistributed as native token yield to stakers, making the "revenue" denominated in the same asset it's meant to value.

---

## INFORMATIONAL

| # | Check | Trigger Condition | YAML Fields to Inspect |
|---|---|---|---|
| I-01 | Revenue source not diversified | Single revenue source — not yet a risk but worth monitoring | `economics.protocol_revenue_sources` |
| I-02 | Vesting not on-chain verifiable | Vesting described but no on-chain contract address | `vesting.notes`, `additional_notes` |
| I-03 | Governance participation unknown | No historical or projected voter turnout data | `utility.governance.*`, `additional_notes` |
| I-04 | No incident response plan | No documented process for peg defense, governance emergency, treasury stress | `additional_notes`, `risks_stated_by_team` |
| I-05 | Schema field missing | Required TokenModel field could not be determined; assumption made | Any required field set to `unknown` |

---

## Cross-Reference

| Domain | Primary Checks | Knowledge File |
|---|---|---|
| Stablecoin / peg | C-01, C-08, H-09, H-12 | `failure_postmortems.md`, `failure_postmortems_2024.md` |
| Staking & emissions | C-06, H-04, H-10, H-14, M-03 | `staking_dynamics.md`, `vetokens_and_emissions.md` |
| Governance | C-05, H-07, H-08, M-08, M-09 | `governance_attacks.md` |
| Treasury | H-05, H-06, M-07, M-13 | `treasury_design.md` |
| Vesting & distribution | C-02, H-01, H-02, H-03, M-02 | `token_archetypes.md` |
| Value accrual | C-03, C-07, M-01, M-11 | `token_velocity.md`, `token_archetypes.md` |
