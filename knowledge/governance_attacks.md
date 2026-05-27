# Governance Attacks

## Key Formulas

**Flash Loan Viability**
```
attack_viable = (flash_loan_available_tokens > quorum_threshold)
                AND (snapshot_block == execution_block OR no_time_delay)
                AND (flash_loan_fee < expected_drain_value)
```

**Beanstalk (Apr 2022) — reference numbers:**
- Borrowed ~$1B via Aave flash loan → acquired >67% voting weight
- Quorum was ~32% of total supply (easily met with borrowed tokens)
- Cost to attacker: ~$250K; net profit: ~$80M from draining the Silo

**Quorum Safety Thresholds**
```
quorum < 10% of circulating supply    → high manipulation risk
quorum 10–20%                         → moderate (whale-capturable)
quorum > 20% + time-weighted          → lower risk
proposal passes with < 5% of supply  → red flag regardless of rule
```

**Plutocracy Capture**
```
top_5_holders > 51% of votes   → de facto oligarchy
voter_turnout < 5% of supply   → top holder likely controls outcome
single_actor > 20% voting power → critical concentration risk
```

**Time-Lock Minimums**
```
parameter changes:         ≥ 48 hours
treasury withdrawals:      ≥ 7 days
contract upgrades:         ≥ 7–14 days
emergency pause:           0 hours (guardian-only; pause ≠ execution)
```

---

## Core Design Rules

1. Voting snapshot at proposal-creation block, never at execution block.
2. Mandatory time-lock between vote finalization and execution.
3. Quorum defined as % of circulating (not total) supply; minimum 10%.
4. No single address can unilaterally reach quorum; individual delegation capped at 5–10%.
5. Emergency powers (guardian/multisig): pause/veto only — no arbitrary execution.
6. Treasury governance separate from protocol parameter governance.
7. Proposal submission requires non-trivial deposit or minimum token lock.
8. All governance-executable calls must be whitelisted; no arbitrary calldata.
9. Off-chain Snapshot must never substitute for on-chain execution without secondary security layer.
10. Delegation must be revocable at any time, capped per address, and visible on-chain.

---

## Red Flag Checklist

**Critical (immediate risk)**
- [ ] Voting snapshot at execution block, not proposal-creation block
- [ ] Vote + execute possible atomically or without any time-lock
- [ ] No minimum quorum as % of circulating supply
- [ ] Governance executor accepts arbitrary external calls (no whitelist)
- [ ] Staking/silo deposits eligible for voting with no lock-up delay
- [ ] Flash-loan-accessible assets count toward governance weight
- [ ] Single address holds > 20% of total voting power

**High Risk**
- [ ] Quorum threshold < 10% of circulating supply
- [ ] Time-lock < 48 hours for any governance-executable action
- [ ] No guardian / emergency multisig with veto capability
- [ ] Proposal submission requires zero stake or deposit
- [ ] Voter turnout consistently < 5% of circulating supply
- [ ] Top 5 addresses control > 40% of voting power

**Moderate Risk**
- [ ] No mandatory proposal simulation / effect preview tooling
- [ ] Snapshot votes bridged to on-chain execution without secondary safeguard
- [ ] Delegation uncapped; delegates can accumulate unbounded voting power
- [ ] No cooling-off period between token acquisition and voting eligibility
- [ ] Time-lock bypassable via "emergency" path accessible to non-guardian actors

**Process / Operational**
- [ ] No governance monitoring or alerting for large proposal submissions
- [ ] No post-mortem process for failed/attacked governance cycles
- [ ] Governance docs do not specify which actions are permissible
