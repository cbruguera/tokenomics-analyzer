# Audit Scoring Rubric

## Grade Definitions

### Grade A — Sound Design
No critical flaws. Model demonstrates sustainable economics with strong incentive alignment.

**All must be true:**
- 0 Critical findings
- ≤1 High findings
- ≤3 Medium findings
- Death spiral checklist: ≤1 condition triggered
- Treasury runway ≥24 months
- Staking yield source: ≥50% from protocol revenue (not pure inflation)
- Insider allocation (team + investors combined) ≤25%
- Team vesting: cliff ≥12 months, total duration ≥36 months

---

### Grade B — Adequate, Improvements Needed
No critical flaws. Minor weaknesses present that should be addressed before launch.

**All must be true:**
- 0 Critical findings
- 2–3 High findings
- ≤5 Medium findings
- Death spiral checklist: ≤2 conditions triggered
- Treasury runway ≥12 months
- Insider allocation ≤35%
- All team/investor tokens have some form of vesting

---

### Grade C — Significant Weaknesses
One critical flaw or several compounding high-severity issues. Requires remediation before launch.

**Criteria:**
- ≤1 Critical finding (with no death spiral conditions triggered)
- OR 4–5 High findings
- Death spiral checklist: 3–4 conditions triggered
- Treasury runway 6–12 months
- Insider allocation ≤45%

---

### Grade D — Severe Design Flaws
Multiple critical flaws or systemic economic risks. Substantial redesign required.

**Criteria:**
- 2 Critical findings, OR
- 6–7 High findings, OR
- Death spiral checklist: 5 conditions triggered
- Treasury runway 3–6 months

---

### Grade F — Not Viable
Fundamental economic failure mode present. Do not launch in current form.

**Any single condition below = automatic F:**

| Disqualifier | Threshold |
|---|---|
| Critical finding count | ≥3 |
| Ponzi structure | Any evidence: early rewards funded by late entrants, zero external revenue |
| Death spiral checklist | ≥6 conditions triggered simultaneously |
| Team/investor lockup | None whatsoever |
| Inflationary staking trap | Yield 100% inflationary + no burn mechanism + no demand drivers + no revenue |
| Governance flash loan risk | Executable via flash loan with no snapshot delay AND no timelock |
| Insider allocation | >60% (team + investors) |
| APY claim | >1000% annualized with no verifiable revenue source |
| Algorithmic stablecoin | 0% exogenous collateral |

---

## Scoring Process

1. Parse the TokenModel → load relevant knowledge files per `INDEX.md`
2. Run `red_flags_master.md` checklist top to bottom → record each finding
3. Run death spiral checklist from `failure_postmortems.md` → count triggered conditions
4. Check all Grade F automatic disqualifiers first — if any triggered, grade is F
5. If no F disqualifier: assign highest applicable tier based on finding counts
6. **Downgrade by one tier** if: simulation shows death spiral triggers under standard bear market scenario (−80% price over 6 months)
7. **Upgrade by one tier** if: model has ≥2 of the following — real yield, strong burn mechanism, exogenous collateral, long vesting, competitive governance security

---

## Grade → Report Language

| Grade | Executive summary opening | Recommended action |
|---|---|---|
| A | "The token economic model demonstrates sound design with strong incentive alignment." | Optional improvements only |
| B | "The model is functional with notable weaknesses that should be addressed before launch." | Address High findings before launch |
| C | "The model contains significant design flaws that pose material economic risk." | Remediation required before launch |
| D | "The model has severe economic design flaws that are likely to cause value destruction." | Substantial redesign required |
| F | "The model is not economically viable in its current form and should not launch." | Do not launch |

---

## Finding Count Reference

| Grade | Critical | High | Medium | Death Spiral Conditions |
|---|---|---|---|---|
| A | 0 | ≤1 | ≤3 | ≤1 |
| B | 0 | 2–3 | ≤5 | ≤2 |
| C | ≤1 | 4–5 | Any | 3–4 |
| D | 2 | 6–7 | Any | 5 |
| F | ≥3 | Any | Any | ≥6 (or any disqualifier) |
