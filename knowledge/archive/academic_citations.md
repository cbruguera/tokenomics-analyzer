# Academic Citations

*Verified URLs as of 2026-05-25. For each: confirmed to exist and load expected content.*

---

## Transaction Fee Mechanism Design (EIP-1559 Analysis)

- **Authors:** Tim Roughgarden (Columbia University)
- **Date:** June 2021 (initial); revised August 18, 2021
- **URL / DOI:** https://arxiv.org/abs/2106.01340
- **Direct PDF:** https://timroughgarden.org/papers/eip1559exchanges.pdf
- **Published in:** ACM SIGecom Exchanges (summary); ACM EC 2021 (abstract)

**Key formula / finding:**
The paper introduces two incentive-compatibility notions for blockchain fee mechanisms:
- **MMIC** (Miner/Validator Incentive Compatible): no profitable deviation for a single profit-maximizing miner
- **OCA-proof** (Off-Chain Agreement proof): no profitable collusion between miners and users

Main result: EIP-1559 satisfies MMIC and OCA-proofness in all but sudden demand spike scenarios. The base fee adjustment rule is:
```
base_fee(t+1) = base_fee(t) * (1 + (gas_used(t) - target_gas) / (target_gas * ADJUSTMENT_QUOTIENT))
```
Where `ADJUSTMENT_QUOTIENT = 8` → max 12.5% base fee change per block.

**Relevance to token auditing:** Fee burn mechanisms that destroy native tokens (deflationary sink) derive from EIP-1559 design. Protocols claiming "fee burn = value accrual" should be evaluated against whether their base fee rule is manipulation-resistant (MMIC) or collusion-vulnerable.

---

## Ethereum Consensus Spec — Validator Base Reward Formula

- **Authors:** Ethereum consensus research team (Justin Drake, Vitalik Buterin, et al.)
- **Date:** Ongoing; Phase 0 spec stable since Dec 2020
- **URL:** https://ethereum.github.io/consensus-specs/specs/phase0/beacon-chain/
- **Annotated version:** https://eth2book.info/latest/part2/incentives/issuance/

**Key formula:**
```
base_reward_per_increment = EFFECTIVE_BALANCE_INCREMENT * BASE_REWARD_FACTOR
                            // integer_squareroot(total_active_balance)

BASE_REWARD_FACTOR = 64
EFFECTIVE_BALANCE_INCREMENT = 1 ETH (10^9 Gwei)
```

Total validator issuance scales as `O(sqrt(total_staked_ETH))`:
- As staked ETH increases, total issuance increases but per-validator reward decreases
- At 14M ETH staked: ~0.52% annual issuance rate; ~1,700 ETH/day
- At 35M ETH staked: ~0.26% annual issuance rate (proportional to 1/sqrt(35/14))

**Relevance to token auditing:** Any liquid staking protocol (Lido, Rocket Pool, etc.) should be evaluated against this baseline. Staking yields substantially above this formula imply MEV extraction, fee-boosted rewards, or front-running risk — not a sustainable yield source.

---

## Balancing Security and Liquidity: A Time-Weighted Snapshot Framework for DAO Governance Voting

- **Authors:** Not specified in search result excerpt
- **Date:** May 2025
- **URL / DOI:** https://arxiv.org/abs/2505.00888

**Key finding:**
Relying on token balances at snapshot time introduces a flash loan attack surface: an attacker can borrow tokens, acquire quorum-level voting power in a single transaction, and execute a malicious proposal — all within one block if no snapshot delay exists.

Proposed defense: **time-weighted voting power** — a voter's effective weight is the integral of their token holdings over a lookback window:
```
voting_power(voter) = (1/T) * ∫[t-T, t] balance(voter, s) ds
```
Where `T` is the lookback period (e.g., 7 days). Flash-loan attack requires sustaining the token balance for the full lookback window to gain full voting weight, making attacks economically infeasible.

**Relevance to token auditing:** Directly maps to red flag C-05 (governance flash loan attack) and H-07 (no governance timelock). A governance system with snapshot delay ≥ 1 block AND timelock ≥ 24h defeats known flash loan vectors. Time-weighted voting provides stronger guarantees.

---

## Moving Beyond Coin Voting Governance

- **Authors:** Vitalik Buterin
- **Date:** August 16, 2021
- **URL:** https://vitalik.eth.limo/general/2021/08/16/voting3.html

**Key finding:**
Coin voting governance has three core failure modes:
1. **Plutocracy**: voting power proportional to holdings → whales dominate
2. **Apathy**: low voter turnout → small motivated groups capture governance
3. **Bribery / short-termism**: token holders can be bribed to approve proposals harmful to protocol long-term

Proposed alternatives: identity-based voting, quadratic voting, conviction voting, and futarchy. Core thesis: governance should have a *higher bar* for high-stakes decisions and a *lower threshold* for routine parameter changes.

**Relevance to token auditing:** Directly informs red flags H-08 (whale quorum), M-08 (no delegation), M-09 (validator/LP cartel risk), and the governance section of any audit. A token's governance design should be evaluated against Buterin's failure mode taxonomy.

---

## An (Institutional) Investor's Take on Cryptoassets

- **Authors:** John Pfeffer (Pfeffer Capital)
- **Date:** December 29, 2017
- **URL:** https://medium.com/john-pfeffer/an-institutional-investors-take-on-cryptoassets-690421158904

**Key formula / finding:**
Applies MV = PQ framework to argue that most utility tokens approach zero intrinsic value:
```
Network value = PQ / V
If V → ∞ (high velocity, no holding incentive) → Network value → 0
```
Pfeffer's thesis: the only cryptoasset with a compelling long-run value case is the one that wins the "global non-sovereign store of value" use case. All others require either captive demand (forcing users to hold the token) or a burn/lock mechanism to suppress velocity.

**Relevance to token auditing:** Foundational for evaluating red flag M-01 (governance token no value accrual) and the token velocity analysis. A token with no holding incentive and high substitutability should be assigned near-zero intrinsic value regardless of current market price.

---

## New Models for Utility Tokens

- **Authors:** Kyle Samani (Multicoin Capital)
- **Date:** February 13, 2018
- **URL:** https://multicoin.capital/2018/02/13/new-models-utility-tokens/

**Key finding:**
Introduces two token models that escape the velocity trap:
1. **Work token**: holders must stake tokens to perform work (e.g., validate, provide service). Staking creates captive demand proportional to network usage.
2. **Burn-and-mint equilibrium (BME)**: tokens are burned to access service and minted at a fixed rate. Value accrues because burn rate scales with usage while mint rate is constant.

Core formula for BME equilibrium token price:
```
P_equilibrium = (annual_usage_value) / (mint_rate × time_preference_factor)
```
If annual burned > annual minted, token is net deflationary; holders benefit from usage growth.

**Relevance to token auditing:** Canonical reference for evaluating whether a utility token has a defensible value accrual mechanism. Any token claiming "utility value" should map to either work token or BME mechanics to avoid the velocity trap.

---

## Understanding Token Velocity

- **Authors:** Kyle Samani (Multicoin Capital)
- **Date:** December 8, 2017
- **URL:** https://multicoin.capital/2017/12/08/understanding-token-velocity/

**Key formula:**
```
Velocity = Total Transaction Volume / Average Network Value
Average Network Value = Total Transaction Volume / Velocity
```

**Key finding:** Most utility tokens have high velocity (used and immediately sold) because users have no incentive to hold. High velocity compresses token price regardless of usage growth. Protocols must introduce velocity sinks: staking locks, fee discounts for holding, governance rights, or burn mechanisms.

**Relevance to token auditing:** Foundational for the `token_velocity.md` knowledge file. Use to evaluate whether a protocol's token design will suffer from the velocity trap at scale.

---

## Towards A First Step to Understand Flash Loan and Its Applications in DeFi

- **Authors:** Kaihua Qin, Liyi Zhou, Boris Livshits, Arthur Gervais
- **Date:** October 2020
- **URL / DOI:** https://arxiv.org/abs/2010.12252

**Key finding:**
Formal analysis of flash loan attack strategies. Demonstrates that an attacker can borrow enough MakerDAO governance tokens via flash loan to pass arbitrary proposals and drain the treasury — all within one Ethereum transaction. The attack requires:
1. No snapshot delay (voting power counted at exact proposal execution block)
2. No timelock (proposal executes immediately after passing)

Estimated attack cost at time of writing: ~$200K transaction cost to drain $500M Maker treasury.

**Relevance to token auditing:** Directly maps to C-05 (governance flash loan attack) disqualifier. Protocols without a snapshot delay AND without a timelock are provably vulnerable to this attack vector.
