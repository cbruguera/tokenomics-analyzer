# Token Model Submission Guide

This guide is for teams preparing their token model for analysis. The more precisely you answer the questions below, the more concrete and actionable your audit results will be. Vague inputs produce vague findings; specific inputs produce specific ones.

---

## How to Submit

You can describe your token model in plain prose, structured bullet points, a spreadsheet, a whitepaper excerpt, or any combination. The analyzer will parse what you provide into a structured model before running the analysis.

**One rule:** do not omit information because it makes the model look worse. Gaps are always flagged as findings, and a flagged known weakness is more useful than a hidden unknown one.

---

## The Six Questions That Drive the Analysis

Every audit is organized around six questions. Answer them as completely as you can.

---

### Q1 — Who gets the tokens, and when?

Provide the full allocation table and vesting schedule for every category.

**What to include:**
- Allocation percentages per category (team, investors, ecosystem/grants, community/airdrop, treasury, public sale)
- For each insider category (team, investors, advisors): cliff in months, then vesting duration in months
- Whether vesting is enforced on-chain or administered manually
- Any tokens unlocked at TGE (Token Generation Event) — state the percentage explicitly

**Example of a complete answer:**
> Total supply: 100,000,000 tokens. Team: 20% — 12-month cliff, 36-month linear vesting, on-chain. Investors (seed): 15% — 6-month cliff, 24-month linear. Investors (series A): 10% — 3-month cliff, 18-month linear. Ecosystem incentives: 30% — 0% at TGE, released monthly at 1%/month over 30 months. Community/airdrop: 10% — 100% at TGE. Treasury: 15% — no vesting; held in multi-sig, governance-controlled. Public sale (IDO): 0% remaining post-launch.

**Common gaps that block analysis:**
- "Standard vesting" — not specific enough; provide actual months
- "Investor terms vary" — provide the worst-case (shortest cliff) and average
- Not stating whether any portion unlocks at TGE

---

### Q2 — What is the total supply trajectory?

Describe how the token supply changes over time.

**What to include:**
- Hard cap (or state explicitly if uncapped)
- Emission schedule type: fixed, linear inflation, exponential decay, halving, dynamic, or none
- Annual emission rate as a percentage of total supply (at launch, and how it changes)
- Burn mechanism (if any): transaction-fee burn, buyback-and-burn, manual governance, none
- If you have a token that automatically adjusts supply (rebasing), describe the mechanism and trigger

**Example of a complete answer:**
> Hard cap: 500,000,000 tokens. At launch, ~120M tokens will be circulating (24%). Ecosystem emissions add ~2% of total supply per year for 5 years, then decay to 0. A 0.3% transaction fee is split: 50% burned, 50% to treasury. No rebasing. The burn rate at current projected volume would be ~0.8% of supply annually, making the net emission approximately +1.2%/year in years 1–5.

**Common gaps that block analysis:**
- Not distinguishing emissions from unlocks (vesting unlocks ≠ new token issuance)
- Stating staking APY without stating where the rewards come from (new issuance? existing treasury? protocol revenue?)
- "Dynamic emissions" without describing the adjustment mechanism and bounds

---

### Q3 — Why would anyone hold this token?

Describe every concrete reason a rational actor would want to acquire and hold this token rather than immediately sell it.

**What to include:**
- What utility functions the token serves (fee payment, staking, governance, collateral, access/gating, work token)
- If staking: lock period, unbonding period, reward source (new emissions vs. protocol revenue), slashing conditions
- If the token is required for protocol access (not just optional): describe the requirement
- Velocity sinks: mechanisms that lock or remove tokens from active circulation

**Example of a complete answer:**
> Holding use cases: (1) Required for validator staking — validators must stake a minimum of 10,000 tokens to participate; rewards are sourced from 50% of protocol fees, not new emissions. (2) Governance — 1 token = 1 vote on parameter changes; proposals require 100,000 tokens. (3) Fee discount — stakers get a 30% discount on platform fees. Lock period: 90 days minimum; unbonding: 14 days. No slashing.

**Common gaps that block analysis:**
- "Governance" listed as the only use case with no economic stake attached
- "Staking rewards" listed without stating whether rewards come from inflation or protocol revenue
- Describing token utility in aspirational terms ("will be used for...") — flag these as not-yet-live

---

### Q4 — How does the protocol generate value, and who captures it?

This is the most important question for assessing long-term sustainability.

**What to include:**
- All revenue sources: trading fees, borrowing fees, liquidation fees, subscription fees, etc.
- Fee rate(s) as a specific percentage or basis points
- Where fees go: burned, distributed to stakers, accumulated in treasury, split between these
- Annualized revenue estimate in USD (current or projected at stated assumptions)
- If the protocol has TVL, state it — combined with fee rate it lets us estimate revenue
- Explicit statement of whether token staking yields are funded by protocol revenue, new token issuance, or both

**Example of a complete answer:**
> Revenue: 0.30% swap fee on all trades. At $50M average daily volume, that's ~$54M/year. Fee distribution: 50% to stakers (pro-rata by staked balance), 30% buyback-and-burn, 20% treasury. Staking rewards are entirely fee-sourced — no inflation component.

**Common gaps that block analysis:**
- "High APY" staking described with no stated revenue source — this is the single most common red flag and almost always triggers a critical finding
- Confusing "fees paid out as staking rewards" with "protocol revenue" — if fees come in as Token A and go out as Token B (or as more of the same token), the economics are different
- No USD estimate provided — even a rough order-of-magnitude helps calibrate sustainability

---

### Q5 — Who governs the system, and with what checks?

**What to include:**
- Voting mechanism: token-weighted, quadratic, conviction, ve-token, off-chain (Snapshot), multisig
- Quorum requirement (% of circulating supply that must vote for a proposal to pass)
- Timelock: delay between a vote passing and it being executable on-chain (in days)
- Proposal threshold: minimum tokens required to submit a proposal
- Emergency controls: who can pause contracts, upgrade proxies, or override governance? Under what conditions?
- Whether smart contracts are upgradeable, and how upgrades are gated

**Example of a complete answer:**
> Token-weighted on-chain voting (OpenZeppelin Governor). Quorum: 4% of circulating supply. Proposal threshold: 50,000 tokens (~0.05% of supply). 48-hour voting period + 72-hour timelock before execution. Protocol multisig (3-of-5) can pause contracts in emergencies; pause lasts max 14 days before requiring governance approval to extend. Contracts are upgradeable via transparent proxy; upgrades require passing a governance vote with the standard timelock.

**Common gaps that block analysis:**
- Governance described but timelock not mentioned — this is a security-critical detail
- "We use Snapshot" — Snapshot is off-chain; if the result isn't enforced by an on-chain timelock, it provides weaker guarantees
- Emergency multisig described without stating who holds the keys or what the threshold is

---

### Q6 — What resources does the protocol have to survive adversity?

**What to include:**
- Treasury total value in USD at time of submission
- Treasury composition: how much is in the native token vs. stablecoins vs. other assets
- Monthly operational burn rate (team salaries, infrastructure, audits, marketing)
- Implied runway at current burn (in months)
- Whether the protocol has Protocol-Owned Liquidity (POL) and its USD value
- Any revenue already covering operational costs (and what % of burn is covered)

**Example of a complete answer:**
> Treasury: $12M total. Composition: 40% USDC, 30% ETH, 30% native token (valued at $0.15/token). Monthly burn: ~$400K (team 12 FTE + infrastructure + audits). Runway: ~22 months at current burn if stables+ETH only (conservative estimate). Protocol-owned liquidity: $800K in USDC/TOKEN LP. Current fee revenue: ~$120K/month, covering ~30% of burn.

**Common gaps that block analysis:**
- Stating treasury size without composition — a $10M treasury that is 100% native tokens is very different from one that is 60% stablecoins
- Not stating burn rate — without it, runway cannot be calculated
- "We have runway" without a number

---

## Additional Context That Improves Analysis

Beyond the six core questions, include the following if applicable:

**Comparable protocols:** Name 2–3 protocols with similar mechanics. This enables quantitative benchmarking against live data.

**Novel mechanisms:** If your token has a mechanism that doesn't have a common name (custom bonding curve, novel liquidity bootstrapping, unique fee distribution), describe it in plain language. Novel mechanisms get narrative analysis rather than checklist scoring.

**Risks you've already identified:** List known weaknesses or tensions in the design. This is not a trap — the analysis will surface these regardless, and acknowledging them upfront signals design maturity and helps calibrate the fix proposals.

**What's not live yet:** Clearly distinguish between live mechanics and planned future mechanics. Planned mechanics cannot be analyzed as if they exist.

---

## Format Tips

**Numbers over narratives.** "Substantial treasury" is not analyzable. "$8M, 60% stablecoins, $300K/month burn" is.

**Percentages over descriptions.** "Team has a small allocation" → state the percentage. "Most tokens are in community hands" → state the distribution table.

**Specificity on timing.** "Tokens unlock gradually" → state the cliff and vesting duration. "Emissions decrease over time" → state the schedule and the rate at each stage.

**Be direct about unknowns.** If you don't have a number yet (e.g., revenue is pre-launch), say so explicitly. The analyzer handles unknowns gracefully — it will flag them as informational and make conservative assumptions. What it cannot handle is a stated number that is aspirational rather than actual.

---

## What the Analysis Produces

Given a complete model, the audit delivers:
- A parsed structured model (YAML) that serves as the canonical reference for all findings
- A scored findings list: Critical / High / Medium / Low / Informational with specific fix proposals
- Python simulations: supply schedule, price distribution under Monte Carlo, sensitivity heatmap, and stress scenarios (bear market, flash crash, revenue collapse)
- A grade (A–F) with justification
- A full written report covering system dynamics, equilibrium conditions, viable operating ranges, and an optimization roadmap

The quality of all of these scales directly with the completeness of the input.

---

## Submission Checklist

Before submitting, confirm you've addressed each item:

- [ ] Full allocation table with percentages summing to 100%
- [ ] Vesting schedule for team and investors (cliff months + duration months)
- [ ] Hard cap or explicit statement that supply is uncapped
- [ ] Emission rate as a % of supply per year, and how it changes
- [ ] Burn mechanism described (or explicitly stated as none)
- [ ] All utility use cases listed, including which are live vs. planned
- [ ] Staking reward source stated (inflation / protocol revenue / mixed)
- [ ] Revenue sources listed with fee rates
- [ ] Annualized revenue estimate in USD
- [ ] How revenue flows to token holders (burn, distribution, treasury, none)
- [ ] Governance mechanism with timelock duration and quorum %
- [ ] Treasury size in USD with composition breakdown
- [ ] Monthly operational burn rate
- [ ] Any novel mechanisms described in plain language
- [ ] Explicit flag on what is live vs. planned
