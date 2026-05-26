# Skill: token-model-parser

**Layer:** 0 (Foundation — always active during parse step)

**Purpose:** Governs how to interpret a verbal token description and translate it into a complete, accurate TokenModel YAML.

---

## Parsing Principles

**Map everything you can infer, flag everything you can't.**
Do not leave fields blank when a reasonable inference is possible. Do not invent values when they are genuinely unknown — set to `unknown` and create an I-05 finding.

**Treat optimistic framing as a signal, not data.**
Token descriptions are often marketing documents. "We have a sustainable treasury" → check the numbers. "Community-owned" → check the actual distribution table. "Real yield" → check whether revenue is exogenous. Don't transcribe claims — evaluate and categorize them.

**When in doubt about archetypes, assign all that apply.**
A token can be simultaneously governance + real-yield + ve-token. Being thorough here determines which knowledge files are loaded and which failure patterns apply.

---

## Field Extraction Rules

### supply.initial_circulating
If not stated: estimate from the distribution. Community/airdrop + ecosystem emissions typically available at TGE. Team/investor amounts are typically locked. A reasonable estimate: `community_pct + (ecosystem_pct × 0.20)` percent of total supply at TGE. Flag as I-05.

### supply.emission_rate_annual_pct
If a staking APY is stated but emission rate is not:
```
approximate_emission_rate ≈ staking_APY × estimated_staking_rate
```
Example: 25% APY with estimated 30% staking rate → 25% × 0.30 = 7.5% annual emission of circulating supply. Flag as I-05.

### economics.treasury.monthly_burn_usd
If not stated, use stage-based estimates (flag as I-05):
- concept: $50–100K/month
- testnet: $100–300K/month
- mainnet-early: $300K–1M/month
- mainnet-mature: $500K–3M/month

### vesting fields
If description says "standard vesting" without detail: do not assume; set to unknown and ask one clarifying question in the same response. If description says "TGE unlock" for any insider category: cliff_months = 0, duration_months = 0.

### utility.staking.reward_source
Map description language:
- "emissions-funded staking" → "inflation"
- "fee revenue shared with stakers" → "protocol-revenue"
- "combination of emissions and fees" → "mixed"
- "staking rewards from our treasury" → "inflation" (treasury drawdown = inflation proxy)
- unspecified → "unknown"

### economics.annual_revenue_usd
Extract any stated protocol revenue figure (trading fees, borrowing fees, liquidation revenue, etc.). If the description states a TVL and fee rate, estimate: `annual_revenue ≈ tvl × fee_rate × volume_to_tvl_ratio` (use 0.3 as default volume/TVL for DEXs, 0.5 for perps, 1.0 for lending). If revenue is genuinely unknown, set to -1 and flag I-05. Do not confuse "fee revenue" with "staking APY paid" — the latter is a cost, not income.

### economics.fee_rate_bps
Convert any stated fee percentage to basis points (1% = 100 bps). If multiple fee tiers exist (e.g., Uniswap 0.05/0.30/1.00%), record the primary or most-used tier. If no fee applies (pure governance token), set to -1.

### economics.value_accrual_to_token
This is the most important field for detecting C-03 (Ponzi) and M-01 (no value accrual). Read the full description and ask: what would a rational investor hold this token for? Governance rights alone with no economic stake = no value accrual. Inflationary staking rewards = circular (you hold to earn more tokens, which dilute the value of tokens you hold).

Map description language to schema values:
- "Fees distributed directly to stakers/holders" → `direct-distribution`
- "Protocol buys back and burns tokens" → `buyback-and-burn`
- "Fees go to the treasury" → `treasury-accumulation`
- "veToken holders receive trading fees" → `ve-token-fees`
- "No fee mechanism" or governance-only → `none`
- Combination of above → `mixed`
- Unclear → `unknown`

### token.archetypes — upgrade triggers
Always check for these combos even if not explicit:
- Mentions "vote-escrowed" OR "lock for boost" OR "lock for voting power" → add `ve-token`
- Mentions "protocol fee distribution" OR "real yield" OR "fee sharing" → add `real-yield`
- Has a separate stable/utility token alongside a governance token → add `dual-token`
- Supply automatically adjusts based on price or other signal → add `rebasing`

---

## Clarifying Questions Protocol

Ask clarifying questions in one batch, before parsing, when ANY of these fields are missing:
1. Investor vesting schedule (cliff + duration)
2. Treasury composition (% stablecoins vs. native)
3. Governance timelock duration
4. Staking reward source split (% from emissions vs. fees)
5. Whether a stablecoin in the system uses the native token as collateral

Do not proceed without at least attempting to gather these. If the user says "proceed with what you have," set unknown fields and create I-05 findings.

---

## Red Flags During Parsing

If you encounter these patterns in the description, immediately note them (they will be formal findings in Step 4, but notice them now):

| Pattern in description | Likely finding |
|---|---|
| "Our stablecoin is backed by [native token]" | C-01 |
| "No lockup for team/investors" or "available at TGE" | C-02 |
| "APY of X%/year" with no revenue source mentioned | C-03 or C-07 |
| "Governance executes immediately after vote" | C-05 |
| "Emissions over 100% in year 1" | C-06 |
| "All treasury is in [token]" | H-05 |
| "Team cliff is X months" where X < 12 | H-01 |

Noting these during parsing keeps you alert and ensures you don't miss them in Step 4.
