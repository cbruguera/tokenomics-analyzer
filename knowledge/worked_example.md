# Worked Audit Example

This file calibrates the expected depth, format, and reasoning for audit findings and reports.
Read this before writing any audit report. Use the quality of findings and fix proposals here as your standard.

---

## Example Token: AgroFi Protocol (AGRO)

**Description (input as received):**

> AgroFi is a DeFi lending protocol on Ethereum that lets farmers tokenize agricultural commodities as collateral to borrow USDA, our native stablecoin. USDA is backed by a mix of AGRO tokens (our governance token) and USDC — roughly 60/40 at launch. AGRO holders vote on interest rate parameters and treasury usage. We have a total supply of 500 million AGRO tokens. The team gets 25%, investors get 20%, and the rest goes to ecosystem and community. Team tokens unlock after 3 months with a 2-year vest. There's a treasury with about $8M currently, mostly in AGRO. Monthly burn is roughly $400K. Staking AGRO gives 25% APY — we'll fund this from emissions initially and hopefully fees later. No timelock on governance yet — we're moving fast. Governance requires 5% quorum.

---

## Parsed TokenModel (YAML)

```yaml
token:
  name: AgroFi Protocol
  symbol: AGRO
  tagline: DeFi lending protocol using tokenized agricultural commodity collateral
  archetypes: [governance, dual-token]
  chain: Ethereum
  launch_stage: mainnet-early

supply:
  total_supply: 500000000
  uncapped: false
  initial_circulating: 50000000    # estimated: ecosystem/community release at TGE
  emission_schedule: linear-inflation
  emission_rate_annual_pct: 15     # estimated from 25% APY staking with ~30% staking rate
  burn_mechanism: none
  burn_rate_estimate: none described

distribution:
  team_pct: 25
  investors_pct: 20
  ecosystem_pct: 35
  community_pct: 15
  treasury_pct: 5
  other_pct: 0
  notes: Team and investor vesting described; ecosystem/community partially at TGE

vesting:
  team:
    cliff_months: 3
    duration_months: 24
  investors:
    cliff_months: unknown
    duration_months: unknown
  ecosystem:
    cliff_months: 0
    duration_months: 12
  notes: Investor vesting not specified in description

utility:
  use_cases: [governance, collateral, staking]
  staking:
    enabled: true
    reward_source: mixed        # stated "emissions initially, fees later"
    lock_period_days: 0
    slashing: false
    unbonding_period_days: unknown
  governance:
    enabled: true
    voting_mechanism: token-weighted
    quorum_pct: 5
    timelock_days: 0
    proposal_threshold: unknown
  fee_payment:
    enabled: false
    fee_sink: unknown

economics:
  protocol_revenue_sources:
    - interest on commodity-collateralized loans (USDA borrowing rate)
  value_accrual_to_token: staking rewards (initially inflationary); governance rights
  demand_drivers: [staking yield, governance, USDA stablecoin collateral requirement]
  velocity_sinks: [staking]
  treasury:
    size_usd: 8000000
    composition: native-only          # "mostly in AGRO"
    monthly_burn_usd: 400000

competitive:
  comparable_protocols: [MakerDAO, Aave, Synthetix]
  differentiation: commodity collateral specialization

risks_stated_by_team: []
additional_notes: USDA stablecoin backed 60% AGRO / 40% USDC. No circuit breakers described.
```

---

## Step 4a: Red Flags Scan

### [CRITICAL-01] C-01 — Endogenous Collateral

**Severity:** Critical
**Category:** Stablecoin / Peg Mechanics

**Description:**
USDA, the protocol's own stablecoin, is backed 60% by AGRO — the same governance token it governs. This creates a circular dependency: AGRO's value depends on USDA's market cap (utility demand) while USDA's backing depends on AGRO's price. Under stress, both assets fall simultaneously, making full redemption impossible — precisely the Terra/LUNA failure mode. At peak USDA demand, AGRO price could be high. The moment USDA redemptions accelerate, AGRO must be minted to cover redemptions, which inflates AGRO supply and crashes its price, destroying more USDA backing in a reinforcing loop.

**Evidence:**
`additional_notes: "USDA stablecoin backed 60% AGRO / 40% USDC"` — endogenous collateral ratio of 60%, far exceeding any safe threshold. Only the 40% USDC portion provides genuine backing.

**Fix Proposal:**
Eliminate AGRO as USDA collateral entirely. Replace with exogenous assets only: USDC, ETH, wBTC, or approved commodity tokens. Target 100% exogenous collateral ratio. If a phased approach is required, hard-code a minimum CR of 100% exogenous collateral in the smart contract, governance-immutable for at least 12 months post-launch. Additionally implement a mint rate limiter (max 0.5% of USDA supply per hour) to prevent bank run acceleration.

---

### [CRITICAL-02] C-05 — Governance Flash Loan Attack

**Severity:** Critical
**Category:** Governance

**Description:**
Governance has no timelock. Any proposal that passes can be executed in the same transaction or immediately after voting. Combined with token-weighted voting and no snapshot delay described, an attacker can borrow AGRO on a flash loan, reach 5% quorum (25M tokens on 500M total supply), pass a malicious proposal directing the $8M treasury, and return the loan — all within one Ethereum transaction. The 5% quorum threshold is achievable at current AGRO prices for a fraction of the treasury value.

**Evidence:**
`utility.governance.timelock_days = 0` and `utility.governance.quorum_pct = 5`. Flash loan attack cost: 5% × 500M × market_price vs. $8M treasury. At any AGRO price below $0.32, the attack is free after repaying the flash loan.

**Fix Proposal:**
1. Deploy a 48-hour minimum timelock immediately; migrate to 7-day timelock before any treasury exceeds $5M.
2. Add a voting snapshot delay of at least 1 block (Compound Governor-style) so votes are counted from balances at proposal creation, not execution.
3. Increase proposal threshold to 1% of total supply (5M AGRO) to raise the cost of spam proposals.
4. Consider time-weighted voting (arxiv.org/abs/2505.00888) for treasury proposals above $1M.

---

### [HIGH-01] H-01 — Short Team Cliff

**Severity:** High
**Category:** Vesting / Distribution

**Description:**
The team's 3-month cliff is substantially below the 12-month minimum required for Grade A and well below the industry standard of 12 months. A 3-month cliff means team members can exit with 8.3% of their allocation (3/24 of vesting duration in linear schedule) three months after TGE — before the protocol has demonstrated any sustained traction. This misaligns the team's financial incentives with long-term protocol health.

**Evidence:**
`vesting.team.cliff_months = 3` — trigger threshold is < 12 months.

**Fix Proposal:**
Extend team cliff to minimum 12 months. Maintain 24-month (or extend to 36-month) total vesting duration. Enforce via an on-chain vesting contract deployed at TGE with no discretionary unlock capability. Consider adding a 12-month performance milestone trigger as an additional gate beyond calendar-based vesting.

---

### [HIGH-02] H-03 — Insider Concentration

**Severity:** High
**Category:** Distribution / Concentration

**Description:**
Team (25%) + investors (20%) = 45% insider allocation, exceeding the 40% High threshold and approaching the Grade F disqualifier at 60%. With 45% of supply controlled by insiders with relatively short vesting, selling pressure post-vesting could persistently suppress token price. A 45% insider allocation also means insiders can approach governance quorum (5% of 500M = 25M) with their team allocation alone (125M AGRO), raising plutocracy and governance capture risk.

**Evidence:**
`distribution.team_pct = 25`, `distribution.investors_pct = 20` → insider total = 45% > 40% threshold.

**Fix Proposal:**
Reduce insider allocation. Target: team ≤ 15%, investors ≤ 15%, combined ≤ 28%. Reallocate excess to community treasury, ecosystem grants, or public sale. If current cap table is fixed by legal agreements, compensate by extending vesting to 48 months and increasing cliff to 18 months to slow market impact. Separately implement a governance cap: no single address or identifiable affiliate group may hold > quorum_pct of voting power through any multi-sig or proxy arrangement.

---

### [HIGH-03] H-05 — No Stablecoin Reserves

**Severity:** High
**Category:** Treasury

**Description:**
The $8M treasury is "mostly in AGRO" — the protocol's own token. This provides no real USD runway guarantee: if AGRO price falls 80% (routine in bear markets), the treasury collapses to $1.6M, providing only 4 months of runway. A treasury denominated in native tokens is not a treasury — it is a circular claim on protocol success. A protocol that fails needs fiat/stable reserves to continue operations during exactly the period when the token price has declined.

**Evidence:**
`economics.treasury.composition = "native-only"`, `economics.treasury.size_usd = 8000000`, `economics.treasury.monthly_burn_usd = 400000` → stated 20-month runway becomes 4-month runway at −80% AGRO price.

**Fix Proposal:**
Immediately diversify treasury: sell sufficient AGRO on-market or via OTC to establish a minimum 18-month stablecoin/ETH reserve ($7.2M at current burn rate). Target treasury composition: 60% stablecoins, 20% ETH, 20% AGRO (for governance operations only). Governance-ratify a Treasury Diversification Policy that prohibits the stablecoin component falling below 12 months of operational burn.

---

### [HIGH-04] H-06 — Short Treasury Runway (Stress-Adjusted)

**Severity:** High
**Category:** Treasury

**Description:**
Nominal runway is 20 months ($8M / $400K). However, with treasury held in native token (AGRO), stress-adjusted runway at −80% price = 4 months. Even at nominal values, 20 months is below the 24-month threshold for Grade A. If AGRO staking rewards must be funded from treasury during a bear market (when protocol revenue from loans will also decline), burn rate could increase to $600K–$800K/month, collapsing even the nominal runway to 10–13 months.

**Evidence:**
`treasury.size_usd = 8000000`, `treasury.monthly_burn_usd = 400000`, `treasury.composition = "native-only"`. Stress-adjusted: $8M × 0.20 (80% decline) = $1.6M / $400K = 4 months.

**Fix Proposal:**
See H-05 fix (diversify). Additionally, publish a monthly treasury report on-chain showing: (a) stablecoin balance, (b) native token balance at market price, (c) real runway in months, (d) monthly burn rate trend. Governance vote required if real runway drops below 12 months.

---

### [MEDIUM-01] M-01 — Governance Token No Value Accrual (Partial)

**Severity:** Medium
**Category:** Value Accrual

**Description:**
AGRO governance rights currently provide no fee capture, no burn, no dividends, and no buyback mechanism. Staking provides yield, but it is funded by inflation — this is not value accrual to existing holders, it is dilution of non-stakers. A pure governance token with inflationary staking rewards has no fundamental value floor beyond speculation on future utility. The team states fees may fund staking "later" but no mechanism, timeline, or trigger condition is specified.

**Evidence:**
`economics.value_accrual_to_token = "staking rewards (initially inflationary); governance rights"` — no fee distribution, buyback, or burn mechanism described.

**Fix Proposal:**
Define and commit to a fee switch timeline: "from month 12 onwards, 30% of USDA borrowing fees are distributed to AGRO stakers in USDC." Hard-code the distribution contract at launch (even if rates start at 0%) so the mechanism exists and is governance-upgradeable but not eliminable.

---

### [MEDIUM-02] M-04 — Unbounded Supply Risk

**Severity:** Medium
**Category:** Supply

**Description:**
The emission schedule is described as linear inflation with no defined terminal supply reduction or sunset. At 15% annual inflation on a 500M token supply, ~75M new AGRO tokens are minted per year. Over 5 years, circulating supply grows from ~50M to ~425M — an 8.5× increase in float — requiring equivalent demand growth to maintain price. No halving, decay curve, or emission sunset is specified.

**Evidence:**
`supply.emission_rate_annual_pct = 15`, `supply.burn_mechanism = "none"`, no decay or halving specified in description.

**Fix Proposal:**
Implement exponential decay on emissions: `E(t) = E_0 × 0.85^t` (15% annual reduction in emission rate). Alternatively, define a 4-year emission budget with a hard stop, transitioning to protocol-fee-only rewards by year 5. Publish a supply chart showing total supply at years 1, 2, 3, 5, 10 alongside projected protocol revenue to demonstrate feasibility.

---

### [LOW-01] L-02 — Unbonding Period Unknown

**Severity:** Low
**Category:** Staking

**Description:**
Staking unbonding period is not specified. If instant or less than 7 days, this is a bank-run vulnerability: stakers can exit simultaneously during a stress event, creating rapid circulating supply increases that accelerate price decline.

**Evidence:**
`utility.staking.unbonding_period_days = unknown`.

**Fix Proposal:**
Specify and implement a minimum 7-day unbonding period. Recommend 14 days for a lending protocol where oracle-delayed liquidations could create concentrated unstaking pressure.

---

### [INFORMATIONAL-01] I-02 — Investor Vesting Not Specified

**Severity:** Informational
**Category:** Missing Information

**Description:**
Investor vesting schedule was not provided in the description. Audit assumption: treated as unknown for flag evaluation. H-02 (cliff bomb) analysis used team cliff only. If investors have a short cliff or no vesting, this would trigger additional High findings.

**Evidence:**
`vesting.investors.cliff_months = unknown`, `vesting.investors.duration_months = unknown`.

**Action Required:**
Provide investor vesting schedule. If investors have cliff < 12 months, trigger H-01 (investor variant). If cliff unlock creates combined event > 10% of circulating supply, trigger H-02.

---

### [INFORMATIONAL-02] I-04 — No Incident Response Plan

**Severity:** Informational
**Category:** Operational

**Description:**
No documentation of emergency procedures for USDA depeg, mass redemptions, treasury depletion, or governance attacks. For a protocol with an algorithmic stablecoin and a known flash loan governance vulnerability, this is an operational gap.

**Fix Proposal:**
Publish an incident response runbook covering: (1) USDA peg deviation > 2% — who has authority to invoke emergency pause and how; (2) governance attack — multi-sig emergency veto procedure; (3) treasury < 3-month runway — escalation and communication protocol.

---

## Step 4b: Death Spiral Count

Checking all 10 conditions from `failure_postmortems.md`:

| # | Condition | Status | Evidence |
|---|---|---|---|
| 1 | Collateral is endogenous | ✅ TRIGGERED | USDA 60% backed by AGRO |
| 2 | Backing MC < liability MC | ⚠️ Unknown | USDA supply not stated |
| 3 | Yield is subsidized, not earned | ✅ TRIGGERED | Staking funded by emissions, "fees later" |
| 4 | APY > 50% with no sustainable source | ❌ Not triggered | 25% APY < 50% threshold |
| 5 | Peg deviation > 1% for > 24h | ❌ Not triggered | Pre-launch; no history |
| 6 | Treasury runway < 60 days | ❌ Not triggered | Nominal 20 months (but stress-adjusted: 4 months is concerning) |
| 7 | No mint/burn rate limiter | ✅ TRIGGERED | No rate limiter described for USDA mint/burn |
| 8 | Protocol liquidity < 10% of supply | ⚠️ Unknown | DEX liquidity for USDA not stated |
| 9 | Top-10 holders control > 40% of collateral | ✅ TRIGGERED | Team (25%) + investors (20%) = 45% |
| 10 | Demand driver is single internal yield product | ✅ TRIGGERED | Primary AGRO demand driver is inflationary staking yield |

**Death Spiral Score: 5 conditions triggered** (2 unknown — if condition 2 or 8 triggers, score becomes 6–7 → C-04 Critical finding)

---

## Step 4c: Grade Assignment

**Check F disqualifiers first:**
- ≥3 Critical findings? → 2 Critical (C-01, C-05) — not yet F
- Ponzi structure (C-03)? → Not triggered (protocol has external revenue: loan interest)
- Death spiral ≥6? → 5 confirmed, 2 unknown. If either unknown triggers → F. Flag as conditional.
- No lockup at all (C-02)? → Not triggered (vesting exists, just short cliff)
- 100% inflationary staking + no burn + no demand + no revenue? → Not fully triggered (has loan interest revenue)
- Governance flash loan? → C-05 triggered → **F disqualifier applies**

**→ Grade: F (automatic disqualifier: C-05 governance flash loan risk)**

*If timelock were present (hypothetically removing C-05): grade would be C — 2 Critical findings, 4 High findings, 2 Medium findings, death spiral score 5.*

---

## Expected Report Executive Summary

```markdown
## Executive Summary

**Overall Grade: F**

| Severity | Count |
|---|---|
| Critical | 2 |
| High | 4 |
| Medium | 2 |
| Low | 1 |
| Informational | 2 |

The AgroFi Protocol token model is not economically viable in its current form and should not launch.

The automatic Grade F disqualifier is triggered by the absence of any governance timelock (C-05): 
with a 5% quorum requirement and no execution delay, the $8M treasury is extractable via flash 
loan in a single Ethereum transaction. Separately, USDA's 60% endogenous AGRO collateral (C-01) 
replicates the Terra/LUNA death spiral architecture — under redemption stress, AGRO must be minted 
to cover USDA, collapsing its own price and the stablecoin's backing simultaneously. Five of ten 
death spiral conditions are confirmed triggered with two more dependent on undisclosed liquidity data.

The model has one meaningful strength: genuine protocol revenue from commodity loan interest, which 
provides a foundation for sustainable real yield once governance and collateral design are corrected.
```

---

## Quality Standards Demonstrated Above

**Do:**
- Cite the exact YAML field and value in every Evidence section
- Calculate the numeric consequence (4-month stress-adjusted runway, 45% insider sum, etc.)
- In Fix Proposals: name the specific contract, parameter, timeline, and threshold
- In the death spiral count: show the check-by-check reasoning
- In grade assignment: show the F disqualifier check before grade bands

**Don't:**
- Write "the team allocation is high and could cause sell pressure" — show the math and trigger
- Write "consider adding a timelock" — specify the minimum duration, the governance contract type, and when it must be in place relative to launch
- Skip ambiguous fields — create I-05 findings and state your assumption explicitly
- Inflate severity — a short unbonding period alone is Low, not High
