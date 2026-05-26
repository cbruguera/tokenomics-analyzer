Parse a verbal description of a token economic model into a structured TokenModel YAML file.

Arguments: $ARGUMENTS
(A verbal description of the token model — can be a few sentences or several paragraphs, or a path to a document)

---

## Steps

### Step 1 — Read schema
Read `models/schema.yaml` to understand the full schema structure.

### Step 2 — Extract what's present
Extract all information from the input in $ARGUMENTS and map it to schema fields. Do not force-fit ambiguous claims — mark as partial rather than inferring. Note any red flags spotted during extraction (per `token-model-parser` skill) for use in Step 6.

### Step 3 — Score completeness
Score each of the six universal questions on a 0–100% scale using the criteria in `token-model-parser` skill. Identify specific gaps within each question.

### Step 4 — Display completeness scorecard
Print the scorecard in this format before doing anything else:

```
COMPLETENESS SCORECARD
======================
Q1 Distribution & Vesting    ████████░░  80%  [2 gaps]
Q2 Supply Trajectory         ██████████  100%
Q3 Demand & Utility          ████░░░░░░  40%  [3 gaps — CRITICAL]
Q4 Revenue & Value Accrual   ██░░░░░░░░  20%  [4 gaps — CRITICAL]
Q5 Governance                ██████░░░░  60%  [2 gaps]
Q6 Treasury & Runway         ████████░░  80%  [1 gap]

Overall: 63% complete. Proceeding to targeted questions.
```

Mark any question < 50% as `CRITICAL`. Mark 50–74% as `SIGNIFICANT`. Leave 75–100% unmarked.

Bar rendering: each `█` = 10%. Use `░` for unfilled segments. Always 10 characters wide.

### Step 5 — Ask targeted gap questions
Generate up to 5 questions ordered by audit-criticality (see priority order in `token-model-parser` skill). Present as a numbered list. Wait for answers before proceeding.

If the user says "proceed with what you have" or provides no response to a specific question: mark that field `unknown` and create an I-05 finding — do not block the parse.

### Step 6 — Parse to YAML and save
Incorporate all answers, apply all field extraction rules from the `token-model-parser` skill, and save the complete TokenModel to `models/<token-name>.yaml`.

### Step 7 — Print parse summary
Print a concise summary:
- Token name and archetypes identified
- Overall completeness % (from scorecard)
- Fields set to `unknown` and the I-05 findings they generated
- Any Critical red flags spotted during extraction
- What happens next (Step 2 of the full audit workflow: classify archetypes)
