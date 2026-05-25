# Governance Attacks

## Key Formulas

**Flash Loan Viability Condition**
```
attack_viable = (flash_loan_available_tokens > quorum_threshold)
                AND (snapshot_block == execution_block OR no_time_delay)
                AND (flash_loan_fee < expected_drain_value)
```

**Beanstalk Specific (April 17, 2022)**
- Attacker borrowed ~$1B in assets via Aave flash loan
- Converted to ~79M BEAN + ~36M BEAN3CRV LP tokens in a single transaction
- Held >67% of governance weight; quorum was ~32% of total BEAN supply
- Proposal BIP-18 was malicious; BIP-18 execution drained $182M from the Silo
- Total cost to attacker: ~$250K in flash loan fees; net profit: ~$80M

**Quorum Threshold Safety Bands**
```
if quorum < 10% of circulating supply       → high manipulation risk
if quorum 10–20%                            → moderate risk (whale-capturable)
if quorum > 20% + time-weighted            → lower risk
if proposal passes with <5% of supply      → red flag regardless of quorum rule
```

**Plutocracy Capture Threshold**
```
single_actor_capture_risk = top_holder_voting_power / total_voting_power
if top_5_holders > 51% of votes            → de facto oligarchy
if voter_turnout < 5% of token supply      → top holder likely controls outcome
```

**Time-Lock Break-Even**
```
minimum_timelock = max(flash_loan_duration, 1 block) + delta
safe_timelock    ≥ 48 hours for parameter changes
safe_timelock    ≥ 7 days  for treasury withdrawals / contract upgrades
```

---

## Core Principles

1. Voting power must be snapshotted at a block prior to proposal creation, never at execution block.
2. A mandatory time-lock (minimum 48 h for low-risk, 7 days for high-risk) must separate vote finalization from execution.
3. Quorum must be defined as a percentage of circulating (not total) supply and must be >= 10%.
4. No single address or colluding group should be able to unilaterally reach quorum; cap individual delegation at 5–10%.
5. Emergency powers (guardian / multisig) must be limited to pause/veto only, not execution of arbitrary calls.
6. Governance over treasury withdrawals must be separate from governance over protocol parameters.
7. Proposal submission should require a non-trivial deposit or minimum token lock to deter spam and drive-by attacks.
8. All governance-executable calls must be whitelisted; arbitrary calldata execution is a critical attack surface.
9. Vote delegation creates power concentration; delegated voting weight must be capped or time-weighted.
10. Off-chain signaling (Snapshot) must never substitute for on-chain execution without an additional security layer.

---

## Failure Patterns

### Flash Loan Governance Attack (Beanstalk, April 2022)

**Preconditions**
- Governance token (BEAN) had no snapshot delay; voting weight computed at execution block.
- BIP proposals executable in the same transaction as vote if quorum was met.
- Silo deposits counted as voting weight; attacker could deposit via flash loan, vote, then withdraw.

**Step-by-Step Mechanics**
1. Attacker deployed a malicious proposal (BIP-18) one block earlier with a hidden `emergencyCommit` path.
2. In a single Ethereum transaction:
   a. Flash loan ~$1B USDC/USDT/DAI from Aave.
   b. Swapped into BEAN and BEAN3CRV LP tokens via Curve.
   c. Deposited tokens into Beanstalk Silo, acquiring ~79% voting weight.
   d. Called `emergencyCommit` on BIP-18 (required only 2/3 majority, met instantly).
   e. BIP-18 execution transferred all Silo assets to attacker-controlled address.
   f. Repaid flash loan.
3. Total execution: one transaction, one block.

**Enabling Contract Conditions**
- `emergencyCommit`: allowed immediate execution if 2/3 supermajority met, no time-lock.
- Snapshot at execution block, not at proposal-creation block.
- No withdrawal delay on Silo deposits used as collateral.
- No cap on voting power from a single address.

**Root Cause Summary**
- Atomic vote + execute in the same transaction.
- Flash-loan-accessible governance weight.
- No delay between quorum achievement and execution.

---

### Tornado Cash Governance Attack (May 2023)

**Preconditions**
- TORN token governance; proposal execution required only a majority of participating votes (no minimum supply quorum).
- Attacker exploited a contract that allowed arbitrary contract deployment via `create2` inside a proposal.

**Step-by-Step Mechanics**
1. Attacker submitted a proposal with apparently benign calldata.
2. Proposal passed after attacker accumulated enough TORN (bought cheaply; low liquidity).
3. Execution deployed a malicious contract via `create2` at a deterministic address.
4. Malicious contract granted the attacker 1.2M votes (TORN from the governance contract itself).
5. With self-granted votes, attacker passed further proposals to drain the community treasury and upgrade the router.
6. Community regained partial control weeks later via counter-proposal.

**Enabling Conditions**
- Proposals could deploy arbitrary contracts.
- No whitelist of allowed calls in governance execution.
- Token liquidity low enough that attacker could acquire majority without flash loan.
- No guardian veto or multisig override mechanism.

---

### Build Finance DAO Hostile Takeover (February 2022)

**Preconditions**
- Very low voter participation (typical turnout < 2% of supply).
- No quorum requirement; majority of votes cast, not majority of supply.
- BUILD token distributed thinly; whale could accumulate on open market.

**Step-by-Step Mechanics**
1. Hostile actor accumulated BUILD tokens over weeks on open market (cheap, illiquid).
2. Submitted a proposal to transfer minting rights and treasury control to attacker wallet.
3. Proposal passed because attacker held >50% of votes cast; legitimate community did not mobilize.
4. Attacker minted large quantities of BUILD tokens and drained treasury.
5. No time-lock, no multisig override, no guardian.

**Enabling Conditions**
- No quorum as fraction of total supply — only plurality of participating votes required.
- No time-lock between proposal passage and execution.
- No minimum proposal submission stake.
- Community apathy and no active monitoring.

---

### Low Turnout / Plutocracy Capture (General Pattern)

**Mechanics**
- In bear markets or mature protocols, voter participation drops to 1–5% of supply.
- A single whale holding 2–3% of supply can constitute 30–60% of effective votes.
- Accumulation is gradual (weeks/months), below radar of governance monitoring.
- Captured governance redirects fee flows, upgrades contracts, or changes tokenomics in whale's favor.

**Amplifying Factors**
- Vote delegation: delegated tokens pile power onto a small set of delegates.
- Token concentration from ICO/seed tranches with no vesting on governance rights.
- No cool-down period between token acquisition and voting eligibility.

---

### Malicious Proposal / Trojan Proposal Pattern

**Mechanics**
- Proposal contains multiple encoded calls; benign-looking description hides malicious calldata.
- Proposal is bundled with an urgent legitimate change to pressure voters to approve quickly.
- Proposal exploits a deterministic address (CREATE2) to deploy a contract that doesn't exist yet at review time.
- Time pressure is manufactured: "critical bug fix" framing.

**Enabling Conditions**
- No mandatory human review period before on-chain vote begins.
- Proposal description not verified against calldata by tooling.
- No simulation of proposal effects in a forked environment before vote.

---

## Mitigations / Best Practices

### Time-Lock Requirements and Limitations

| Change Type              | Minimum Time-lock | Notes                                  |
|--------------------------|-------------------|----------------------------------------|
| Protocol parameter tweak | 48 hours          | Covers most MEV / manipulation windows |
| Treasury withdrawal      | 7 days            | Allows community to organize veto      |
| Contract upgrade         | 7–14 days         | Requires upgrade path audit            |
| Emergency pause          | 0 hours           | Guardian only; pause ≠ execution       |

**Limitations of Time-locks Alone**
- Time-lock does not prevent a majority-holder from still executing a malicious proposal after the delay.
- Time-lock is ineffective if the guardian/multisig is compromised.
- Very long time-locks reduce protocol agility and may delay legitimate security patches.

---

### Time-Weighted Voting

- Voting power = f(tokens, lock_duration): longer locks → proportionally higher weight.
- Prevents flash loan attacks because borrowed tokens have zero lock duration.
- Prevents rapid accumulation attacks because weight accrues over time.
- Implementation: veToken model (veCRV, veBAL); token locked for 1 week–4 years.
- Risk: veToken model concentrates power in early adopters and long-term whales.

---

### Conviction Voting

- Vote weight accumulates continuously the longer tokens are staked on a proposal.
- Proposals reach execution threshold only after sustained community commitment.
- Flash loan attacks impossible: a flash loan held for milliseconds accumulates near-zero conviction.
- Used by: Gardens (1Hive), Commons Stack.
- Limitation: slow to respond in genuine emergencies; not suited for time-sensitive parameter changes.

---

### Optimistic Governance

- Proposals execute automatically after a time-lock unless vetoed.
- Shifts burden: requires active veto rather than active vote for routine changes.
- Guardian / security council holds veto power for the time-lock window.
- Risk: guardian capture; guardian must itself be decentralized (multisig with diverse signers).
- Example: Optimism's Security Council + Governor model.

---

### Guardian Multisig Design

- Multisig threshold should be M-of-N where N ≥ 7 and M ≥ 5.
- Signers must be geographically and organizationally diverse.
- Guardian powers must be strictly limited: pause, veto, not arbitrary execution.
- Multisig should have a defined sunset or transition to on-chain governance.
- Key rotation and signer replacement must themselves require governance vote.

---

### Vote Delegation Risks and Mitigations

- Delegation creates "super-delegates" with disproportionate power.
- Mitigation: cap delegated voting weight per address (e.g., max 5% of total supply).
- Mitigation: enforce delegation transparency with on-chain registry.
- Mitigation: allow token holders to revoke delegation at any time, effective next epoch.
- Risk: inactive delegates who hold large delegations become governance deadweight or attack vectors.

---

### Governance Red Flag Checklist

**Critical (immediate risk)**
- [ ] Voting snapshot taken at execution block, not proposal-creation block
- [ ] Vote + execute possible in a single transaction or without time-lock
- [ ] No minimum quorum as a percentage of circulating supply
- [ ] Governance executor can make arbitrary external calls (no whitelist)
- [ ] Silo/staking deposits eligible for voting without lock-up delay
- [ ] Flash-loan-accessible assets count toward governance weight
- [ ] Single address holds >20% of total voting power

**High Risk**
- [ ] Quorum threshold < 10% of circulating supply
- [ ] Time-lock < 48 hours for any governance-executable action
- [ ] No guardian or emergency multisig with veto capability
- [ ] Proposal submission requires zero stake or deposit
- [ ] Voter turnout consistently < 5% of circulating supply
- [ ] Top 5 addresses control > 40% of voting power

**Moderate Risk**
- [ ] No mandatory proposal simulation / effect preview tooling
- [ ] Off-chain Snapshot votes bridged to on-chain execution without secondary safeguard
- [ ] Delegation uncapped; delegates can accumulate unbounded voting power
- [ ] No cooling-off period between token acquisition and voting eligibility
- [ ] No on-chain calldata verification against human-readable proposal description
- [ ] Time-lock can be bypassed via "emergency" path accessible to non-guardian actors

**Process / Operational**
- [ ] No formal governance monitoring or alerting for large proposal submissions
- [ ] No independent security council or governance watchdog
- [ ] No post-mortem or revision process for failed/attacked governance cycles
- [ ] Governance documentation does not specify what actions are permissible

---

## Key Sources

- Beanstalk BIP-18 flash loan governance attack, April 17 2022 — on-chain transaction analysis; PeckShield and Halborn post-mortems. From training knowledge.
- Tornado Cash governance attack, May 2023 — attacker proposal #20, community post-mortems by Tornadocash community and independent researchers. From training knowledge.
- Build Finance DAO hostile takeover, February 2022 — community forum post-mortems and on-chain data. From training knowledge.
- Vitalik Buterin, "Moving beyond coin voting governance" (2021) — arguments against plutocracy, quadratic voting, and time-weighted alternatives. From training knowledge.
- Vitalik Buterin, "DAOs are not corporations" (2022) — decentralization-security tradeoffs in governance design. From training knowledge.
- 1Hive / Gardens conviction voting documentation — conviction voting mechanics and thresholds. From training knowledge.
- Optimism governance documentation, Security Council design — optimistic governance + guardian veto model. From training knowledge.
- OpenZeppelin Governor contracts documentation — standard time-lock and quorum implementations. From training knowledge.
