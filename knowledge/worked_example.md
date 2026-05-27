# Worked Audit Example

Read this before writing any audit report. It calibrates the expected format, evidence depth, and reasoning standard.

---

## Finding Format — Required Structure

Every finding has exactly three parts:

```
### [SEVERITY-NN] Flag-ID — Title

**Severity:** Critical / High / Medium / Low / Informational
**Category:** Category name

**Description:**
What the problem is and WHY it matters economically. Not "this is risky" — explain the mechanism.
Cite the specific economic failure mode (e.g., "this replicates the Terra/LUNA death spiral architecture").

**Evidence:**
`yaml_field_name = value` — trigger condition met.
Calculate the numeric consequence. Example:
`distribution.team_pct = 25`, `distribution.investors_pct = 20`
→ insider total = 45% > 40% threshold

**Fix Proposal:**
Specific, implementable change with contract name, parameter value, timeline, and threshold.
Never write "consider adding a timelock." Write:
"Deploy a 48-hour minimum timelock to the Governor contract before launch. Migrate to 7-day timelock
before any treasury exceeds $5M. Snapshot voting weight at proposal-creation block (Compound Governor-style)."
```

Critical and High findings require Fix Proposals. Medium findings should have them when the fix is clear.

---

## Two Full Finding Examples

### [CRITICAL-01] C-01 — Endogenous Collateral

**Severity:** Critical
**Category:** Stablecoin / Peg Mechanics

**Description:**
USDA is backed 60% by AGRO — the same token it governs. This creates a circular dependency: AGRO's value depends on USDA demand while USDA's backing depends on AGRO price. Under stress, both fall simultaneously, making full redemption impossible. When USDA redemptions accelerate, AGRO must be minted to cover them, inflating supply, crashing AGRO, and destroying more USDA backing in a reinforcing loop. Identical to the Terra/LUNA failure mode.

**Evidence:**
`additional_notes: "USDA stablecoin backed 60% AGRO / 40% USDC"` — endogenous collateral ratio 60%, far exceeding any safe threshold. Only the 40% USDC component provides genuine backing.

**Fix Proposal:**
Eliminate AGRO as USDA collateral entirely. Replace with exogenous assets only (USDC, ETH, wBTC, or approved commodity tokens). Hard-code minimum CR of 100% exogenous collateral in the smart contract, governance-immutable for at least 12 months post-launch. Add a mint rate limiter (max 0.5% of USDA supply per hour) to prevent bank run acceleration.

---

### [HIGH-01] H-03 — Insider Concentration

**Severity:** High
**Category:** Distribution / Concentration

**Description:**
Team (25%) + investors (20%) = 45% insider allocation, exceeding the 40% High threshold. With 45% of supply controlled by insiders with a short 3-month cliff, post-vesting sell pressure can persistently suppress token price. Additionally, team allocation alone (125M AGRO) approaches governance quorum (5% of 500M = 25M tokens), raising plutocracy risk.

**Evidence:**
`distribution.team_pct = 25`, `distribution.investors_pct = 20`
→ insider total = 45% > 40% High threshold

**Fix Proposal:**
Reduce insider allocation: target team ≤ 15%, investors ≤ 15%, combined ≤ 28%. Reallocate excess to community treasury or ecosystem grants. If cap table is fixed, compensate by extending vesting to 48 months with cliff at 18 months. Separately implement a governance cap: no single address or affiliate group may control > quorum_pct of voting power through any multi-sig or proxy.

---

## Death Spiral Count Format

```
| # | Condition                                       | Status      | Evidence                          |
|---|---|---|---|
| 1 | Collateral is endogenous                        | ✅ TRIGGERED | USDA 60% backed by AGRO           |
| 2 | Backing MC < liability MC                       | ⚠️ Unknown  | USDA supply not stated            |
| 3 | Yield is subsidized, not earned                 | ✅ TRIGGERED | Staking funded by emissions       |
| 4 | APY > 50% with no sustainable source            | ❌           | 25% APY < 50% threshold           |
...

Death Spiral Score: 5 conditions triggered (2 unknown)
```
The near-zero and death spiral count are the two most important single outputs. Report both.

---

## Grade Assignment Format

```
Check F disqualifiers first:
- ≥3 Critical findings?       → [count] — [not yet F / F]
- Ponzi structure (C-03)?     → [triggered / not triggered]
- Death spiral ≥6?            → [count] confirmed, [count] unknown
- Governance flash loan?      → [triggered = F] / [not triggered]
- No lockup at all (C-02)?    → ...

→ Grade: [X] (reason: specific disqualifier OR finding counts)
If hypothetically removing [trigger], grade would be [Y] — [finding count summary].
```

---

## Executive Summary Format

```
## Executive Summary

**Overall Grade: [X]**

| Severity      | Count |
|---|---|
| Critical      | N |
| High          | N |
| Medium        | N |
| Low           | N |
| Informational | N |

[1-2 sentences: the grade and the specific findings that determined it.]
[1 sentence: the most dangerous finding and its mechanism.]
[1 sentence on a genuine strength, if any.]
```

Example: *"Grade F triggered by C-05 (no governance timelock — $8M treasury extractable via flash loan in one transaction). Separately, C-01 (USDA backed 60% by AGRO) replicates the Terra/LUNA death spiral. Five of ten death spiral conditions triggered. The model's one genuine strength is real protocol revenue from commodity loan interest, which provides a foundation once governance and collateral design are corrected."*

---

## Quality Standards

**Do:**
- Cite the exact YAML field and value in every Evidence section
- Calculate the numeric consequence (stress-adjusted runway, insider allocation sum, etc.)
- In Fix Proposals: name the specific contract, parameter, timeline, and threshold
- In death spiral count: show the check-by-check reasoning, mark unknowns separately
- In grade assignment: show the F disqualifier check before grade bands

**Don't:**
- Write "the team allocation is high and could cause sell pressure" — show the math and trigger
- Write "consider adding a timelock" — specify minimum duration, contract type, and when it must be in place
- Skip ambiguous fields — create I-05 findings and state your assumption explicitly
- Inflate severity — a short unbonding period alone is Low, not High
- Report simulations without interpretation — charts are outputs, not findings
