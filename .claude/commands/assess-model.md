# /assess-model

Run a completeness assessment on a token model description without proceeding to a full audit. Returns a section-by-section completeness scorecard and a prioritized list of gaps to address. Useful for early-stage teams not yet ready for a full audit.

**Usage:** `/assess-model [description or file path]`

Pass either a verbal description, a path to a partially-filled TokenModel YAML, or a path to any document describing the token model (whitepaper excerpt, pitch deck text, etc.).

---

## Execution

### Step 1 — Extract what's present

Read the input and extract everything that can be mapped to the six universal questions. Do not force-fit — if something is ambiguous, note it as partial rather than filling it in with an inference.

### Step 2 — Score each question

Score each of the six universal questions on a 0–100% scale based on how completely it is answered. Use the criteria below.

**Q1: Who gets the tokens and when?** *(distribution + vesting)*
- 100%: Team, investor, ecosystem, community, treasury allocations all stated as %; vesting cliff and duration known for team and investors
- 50%: Allocations stated but vesting unknown, or vesting stated but allocations vague
- 0%: No distribution information

**Q2: What is the total supply trajectory?** *(emission + burn)*
- 100%: Total supply (or uncapped confirmation), emission schedule type, annual emission rate, and burn mechanism all stated
- 50%: Total supply known but emission rate or schedule type missing
- 0%: No supply information

**Q3: Why would anyone hold this token?** *(utility + demand drivers)*
- 100%: Primary use cases stated, staking mechanics described (if present), demand drivers beyond speculation identified
- 50%: Use cases listed but mechanics vague, or single use case with no staking detail
- 0%: No utility described beyond "governance" or "ecosystem"

**Q4: How does the protocol generate value, and who captures it?** *(revenue + value accrual)*
- 100%: Revenue sources identified, fee rate or revenue estimate provided, mechanism by which revenue reaches token holders described
- 50%: Revenue sources named but no rate or accrual mechanism
- 0%: No revenue model described, or "future revenue" with no mechanism

**Q5: Who governs the system, and with what checks?** *(governance)*
- 100%: Voting mechanism, quorum %, timelock duration, and proposal threshold all stated
- 50%: Governance exists but timelock or quorum unknown
- 0%: No governance described

**Q6: What resources does the protocol have to survive adversity?** *(treasury + runway)*
- 100%: Treasury size, composition (% stablecoins vs. native), and monthly burn rate all known
- 50%: Treasury mentioned but size or composition unknown
- 0%: No treasury information

### Step 3 — Output the scorecard

```
COMPLETENESS ASSESSMENT — [Token Name]
=======================================
Q1  Distribution & Vesting    [bar]  XX%  [gap count and severity]
Q2  Supply Trajectory         [bar]  XX%  [gap count and severity]
Q3  Demand & Utility          [bar]  XX%  [gap count and severity]
Q4  Revenue & Value Accrual   [bar]  XX%  [gap count and severity]
Q5  Governance                [bar]  XX%  [gap count and severity]
Q6  Treasury & Runway         [bar]  XX%  [gap count and severity]

Overall: XX% complete

[READY FOR AUDIT / GAPS SHOULD BE ADDRESSED BEFORE FULL AUDIT]
```

Mark questions below 50% as CRITICAL gaps. Mark questions 50–79% as SIGNIFICANT gaps. Mark 80–99% as MINOR gaps.

Use █ for filled, ░ for missing, e.g. `████████░░  80%`

### Step 4 — List targeted questions

Output a prioritized question list, Critical gaps first. For each gap:
- State the specific question in plain language (no schema jargon)
- Explain in one sentence why it matters for the audit (what finding it could affect)

Example format:
```
QUESTIONS TO ADDRESS (priority order)
======================================
[CRITICAL — Q4]
1. Does fee revenue from the protocol flow to token holders? If yes, how — direct
   distribution, buyback-and-burn, or treasury accumulation?
   Why it matters: determines whether the token has any fundamental value basis
   beyond governance rights.

2. What is the approximate annual protocol revenue, or fee rate charged?
   Why it matters: needed to calculate whether staking yield is real or purely dilutive.

[SIGNIFICANT — Q5]
3. Is there a timelock between governance vote passing and execution? If so, how long?
   Why it matters: no timelock is a Critical finding (flash loan governance attack surface).
```

### Step 5 — Recommendation

End with one of:
- **"Ready for full audit."** — overall ≥ 75% with no CRITICAL gaps
- **"Address critical gaps before full audit."** — any question below 50%
- **"Proceed with noted gaps."** — overall 50–74%; audit can run but findings will include I-05 informational gaps

Do not proceed to parsing or auditing. This command is assessment-only.
