# Token Model Submission Guide

This guide helps you prepare your token model for a rigorous economic analysis. The more clearly you describe your system, the more concrete and actionable the results will be.

You can submit in any format: prose, bullet points, a whitepaper section, a spreadsheet, or a combination. The analyzer will parse what you provide. You don't need to fill out a form.

---

## Start with the system, not the token

Before describing any tokenomics, describe what your protocol actually does.

- What problem does it solve, and for whom?
- What does a typical user do on the protocol? What do they get out of it?
- Who are the key participants (e.g. liquidity providers, validators, borrowers, traders) and what role does each play?
- How does the protocol generate activity? What drives usage?
- Is the protocol live? If so, what does current usage look like?

This context is not optional background — it is the foundation of the analysis. Token mechanics that look broken in isolation often make sense within a specific system, and vice versa. The analysis cannot properly assess incentive alignment, demand drivers, or sustainability without understanding what the protocol is actually trying to do.

---

## Then describe the token's role in the system

Once the system is clear, explain how the token fits into it:

- What does holding or using the token enable? What can you do with it that you couldn't do without it?
- Is the token required for any core protocol function, or is it optional?
- What behaviors is the token designed to incentivize? Among which participants?
- What is the relationship between protocol activity and token demand? Is there a direct mechanical link, or is the connection indirect?

---

## Key specifics the analysis needs

The following details are required for quantitative analysis. Provide them alongside your system description — in whatever order makes sense for your model.

**Supply and distribution**
- Total supply (or state if uncapped)
- Allocation by category (team, investors, ecosystem/grants, community, treasury, public sale) as percentages
- For team and investors: cliff in months, then vesting duration in months
- Tokens available at launch (TGE) as a percentage of total supply
- Emission schedule: how much new supply enters circulation each year, and how that changes over time
- Burn mechanism, if any

**Economics**
- How does the protocol earn revenue? (trading fees, borrowing fees, liquidation fees, subscriptions, etc.)
- What are the fee rates?
- Where do fees go — burned, distributed to token holders, accumulated in treasury, or some split?
- Are staking rewards funded by protocol revenue, by new token issuance, or both? This distinction is critical.
- Current or projected annual revenue in USD (even a rough estimate helps; state your assumptions)

**Treasury**
- Total treasury value in USD
- Composition: how much is in stablecoins vs. native token vs. other assets
- Monthly operational costs (team, infrastructure, audits)

**Governance**
- Voting mechanism (token-weighted on-chain, Snapshot off-chain, multisig, etc.)
- Timelock: delay between a vote passing and execution on-chain (in days)
- Quorum threshold and proposal requirements
- Who controls emergency functions (contract pause, upgrades), and under what conditions

---

## A few things to be explicit about

**What's live vs. planned.** Clearly distinguish mechanics that exist today from ones on the roadmap. Planned mechanics cannot be analyzed as if they are in effect.

**Where you have unknowns.** If a number isn't finalized yet, say so rather than omitting it. The analysis handles unknowns gracefully — it will flag them and make conservative assumptions. Omissions are harder to work with than stated gaps.

**Don't soften weaknesses.** The analysis will surface design risks regardless. Flagging a known weakness upfront gets you a more useful fix proposal than having it discovered and reported without context.
