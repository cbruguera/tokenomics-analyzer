# /assess-model

Run a completeness assessment on a token model description without proceeding to a full audit. Returns a section-by-section completeness scorecard and a prioritized list of gaps to address. Useful for early-stage teams not yet ready for a full audit.

**Usage:** `/assess-model [description or file path]`

Pass either a verbal description, a path to a partially-filled TokenModel YAML, or a path to any document describing the token model (whitepaper excerpt, pitch deck text, etc.).

---

## Execution

### Step 1 — Extract what's present

Read the input and extract everything that can be mapped to the six universal questions. Do not force-fit — if something is ambiguous, note it as partial rather than filling it in with an inference.

### Step 2 — Score each question

Score each question in **25% increments** (0%, 25%, 50%, 75%, 100%) based on how completely the input answers it. Apply judgment — the goal is to accurately reflect whether the auditor has enough information to assess that dimension of the model. For each question, briefly note what is present and what is missing.

The sub-criteria below are a reference for what to check, not a mechanical formula. A novel token that answers a question clearly in prose may score higher than one that fills specific fields but leaves the underlying question vague.

**Q1: Who gets the tokens and when?** *(distribution + vesting)*
- Are all major allocation categories identified with approximate %? (team, investors, community, ecosystem, treasury)
- Is the total insider % calculable?
- Are team vesting terms stated (cliff + duration)?
- Are investor vesting terms stated?

**Q2: What is the total supply trajectory?** *(emission + burn)*
- Is total supply stated, or explicitly confirmed as uncapped?
- Is the emission schedule type and rate described?
- Is a burn mechanism described, or explicitly absent?
- Is the resulting circulating supply curve inferable over time?

**Q3: Why would anyone hold this token?** *(utility + demand drivers)*
- Is at least one concrete use case described beyond governance or speculation?
- Is the token required (not optional) for a protocol function, or is the optional nature intentional and explained?
- If staking exists, is the reward source identified (emissions / protocol revenue / mixed)?
- Is there a demand driver tied to protocol growth or usage?

**Q4: How does the protocol generate value, and who captures it?** *(revenue + value accrual)*
- Are revenue sources identified?
- Is a fee rate or revenue estimate provided?
- Is the mechanism by which value reaches token holders described?
- Is it clear whether staking yield is real (exogenous revenue) or inflationary (token emissions)?

**Q5: Who governs the system, and with what checks?** *(governance)*
- Is the voting mechanism described?
- Are quorum and proposal threshold stated?
- Is the timelock duration stated, including explicitly "no timelock"?
- Are there any safeguards against governance attacks described?

**Q6: What resources does the protocol have to survive adversity?** *(treasury + runway)*
- Is treasury size stated or estimable?
- Is treasury composition known (stablecoin vs. native token %)?
- Is monthly burn rate stated?
- Is there a plan for treasury sustainability under bear conditions?

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

Mark questions at 0–25% as CRITICAL gaps. Mark 50% as SIGNIFICANT. Mark 75% as MINOR. 100% = complete.

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
