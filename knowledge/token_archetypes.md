# Token Archetypes

## Key Formulas

### Currency Token
- **Quantity Theory:** MV = PQ → P = MV/Q (token price rises if Q grows faster than M or V falls)
- **Stock-to-Flow:** SF = stock / annual_issuance; price ~ SF^n (BTC: n≈3 empirically)
- **Inflation rate:** i = block_reward × blocks_per_year / circulating_supply

### Utility / Work Token
- **Velocity model:** V = (GDP_on_chain × token_price) / M; high V suppresses price
- **Burn rate:** net_supply_change = issuance − fee_burn; deflationary when fee_burn > issuance
- **ETH gas price:** base_fee doubles if blocks >50% full (EIP-1559); fee = (base_fee + priority_fee) × gas_used

### Governance Token
- **Voting power:** vp_i = tokens_i / total_tokens (linear); or sqrt(tokens_i) (quadratic voting)
- **Quorum:** proposal passes if (yes_votes / total_supply) ≥ quorum_threshold AND yes_votes > no_votes

### veToken (Vote-Escrow)
- **vePower:** ve_i = tokens_locked × (t_remaining / t_max); decays linearly to 0
- **Boost multiplier (Curve):** boost = min(2.5, 1 + 1.5 × (ve_i / ve_total) / (lp_i / lp_total))
- **Gauge weight → emission share:** emission_to_pool = total_emission × gauge_weight_i / sum(gauge_weights)

### Rebasing Token
- **AMPL target rebase:** supply_new = supply_old × (price / target_price); partial adjustment via dampener
- **OHM RFV backing:** backing_per_token = treasury_assets / circulating_supply; protocol buys below backing
- **RAI redemption price:** p_r(t+1) = p_r(t) × (1 + redemption_rate × Δt); rate is PI controller output

### Real-Yield / Fee-Sharing Token
- **APR:** apr = (fees_distributed_annualized / staked_token_value) × 100
- **GMX multiplier points:** mp_accrual = 0.01 × staked_GMX_or_esGMX per second (100% APR on MPs)
- **SNX C-ratio:** c_ratio = staked_SNX_value / outstanding_sUSD_debt; min 400% (legacy)

### Dual-Token System
- **MKR/DAI stability fee accrual:** surplus = stability_fees_accrued; MKR burns when surplus > buffer
- **GMX/GLP:** GLP_price = AUM / GLP_supply; GMX stakers receive 30% of fees, GLP 70%
- **AXS/SLP:** SLP mint rate = f(match_outcome, energy); sink = breeding_cost in SLP

### Liquid Staking Token
- **Exchange rate (rebasing, e.g. stETH):** stETH ≈ ETH 1:1, rewards added to balance daily
- **Exchange rate (accumulating, e.g. rETH):** rETH_price = ETH_in_pool / rETH_supply; rises monotonically
- **LST yield:** apr_lst = consensus_rewards + execution_tips + MEV − operator_fee

---

## Core Principles

1. **Value accrual must be endogenous.** Tokens with no on-chain claim on revenue or utility depend entirely on greater-fool demand.
2. **Velocity is the enemy of price.** High-turnover tokens (payments, gaming) require sinks or locking to suppress V in MV=PQ.
3. **Inflation must be earned.** Issuance is sustainable only if new supply funds proportional network growth or is offset by burns.
4. **Governance tokens need credible economic stake.** Pure governance tokens without fee capture are vulnerable to apathy and plutocratic capture.
5. **Lock-up alignment creates short-termism risk.** veTokens concentrate power in long-term holders; late entrants face diluted governance and boosted competitors.
6. **Dual-token systems split value but concentrate risk.** Stability token absorbs volatility; governance token absorbs tail risk; correlation breaks in stress.
7. **Rebasing does not create value.** Supply adjustments move purchasing power, not fundamental value; reflexivity can accelerate both rise and collapse.
8. **Real yield is durable only with real revenue.** Fee-sharing APRs collapse if protocol revenue is denominated in native token or depends on token price.
9. **Liquid staking tokens introduce systemic collateral risk.** If LST depegs, protocols treating LST = ETH face cascading liquidations.
10. **Treasury concentration is a governance attack vector.** Protocols where treasury >> market cap allow hostile governance takeover with modest capital.

---

## Failure Patterns

| Archetype | Failure Mode | Mechanism | Real Example |
|-----------|-------------|-----------|--------------|
| **Currency** | Miner capitulation spiral | Price drop → miners unprofitable → hash rate falls → security budget drops → price drop | BCH, BSV post-fork |
| **Currency** | Velocity inflation | Adoption as medium of exchange without SoV demand → V rises → price depressed | Literal "payment coins" 2017–2018 |
| **Currency** | Supply shock (halving cliff) | Subsidy halving without fee market → miner exodus → 51% attack risk | ETC (51% attacked 3×) |
| **Utility/Work** | Token not required (fat protocol bypass) | Protocol accepts ETH/stablecoins; native token loses utility | Many 2017 ICO tokens |
| **Utility/Work** | Velocity trap | Rational users hold token only long enough to use service; P → 0 as adoption grows | Nearly all "gas" tokens without burn |
| **Utility/Work** | Demand-supply mismatch | FIL: large miner supply unlock vs. slow storage demand growth | FIL 2021–2022 unlock pressure |
| **Governance** | Voter apathy / quorum failure | Low participation → proposals pass with tiny minority; governance paralysis | Numerous Compound governance proposals |
| **Governance** | Plutocratic capture | Whales coordinate to drain treasury or set favorable parameters | Mango Markets exploit (MNGO) |
| **Governance** | Governance token = worthless option | No fee capture, no burns; token price tracks speculation only | Most early DeFi governance tokens |
| **veToken** | Bribe-driven vote capture | External protocols (Convex, Votium) aggregate CRV → control gauge weights → extract value | Curve wars 2021–2022 |
| **veToken** | Liquidity fragmentation | Long lock-ups exit via secondary liquid wrappers (cvxCRV, yCRV) at persistent discount | cvxCRV 2022–2023 depeg |
| **veToken** | Late-entrant dilution | Early lockers hold max boost indefinitely; new LPs need proportionally more vePower | veCRV boost gap |
| **Dual-Token** | Stability token bank run | Confidence crisis in collateral → redemption surge → governance token death spiral | LUNA/UST May 2022 |
| **Dual-Token** | P2E sink/source imbalance | More SLP minted than burned → hyperinflation → scholar exit loop | AXS/SLP 2022 collapse |
| **Dual-Token** | GLP pool imbalance | Traders net profitable → GLP stakers net losers → GLP exits → AUM falls → liquidity crisis | GMX (stress scenario) |
| **Rebasing** | Reflexive ponzi collapse | OHM: high APY only sustainable with new entrants; treasury backing < market cap → panic sell | OHM Nov 2021 – 2022 |
| **Rebasing** | Oracle dependency | AMPL/RAI react to price oracle; manipulated oracle → unintended supply expansion | AMPL during low liquidity |
| **Rebasing** | Non-rebasing UX confusion | Negative rebase surprises holders who don't understand dilution | AMPL 2020 correction |
| **Real-Yield** | Circular yield (self-referential fees) | Fees paid in native token; token price drops → real APR drops → stakers exit → price drops | SNX pre-Perps v2 |
| **Real-Yield** | Debt pool socialization | SNX: all stakers share protocol debt; one asset spike → debt underwater for all stakers | sUSD depeg events |
| **Real-Yield** | Concentration of escrowed supply | dYdX: large DYDX vest → sell pressure vs. fee APR | dYdX 2022 unlock cliff |
| **LST** | Depeg cascade | LST < ETH peg → protocols collateralized on LST face mass liquidation | stETH May 2022 (Celsius/3AC) |
| **LST** | Slashing risk propagation | Operator slashing reduces LST backing → LST price drops → downstream DeFi exposure | (Systemic risk, not yet realized at scale) |
| **LST** | Withdrawal queue risk | Pre-Shapella stETH: no redemption → peg entirely market-driven | stETH 2021–2022 discount |

---

## Mitigations / Best Practices

### Per-Archetype Recommendations

| Archetype | Key Mitigations |
|-----------|----------------|
| **Currency** | Fee market (EIP-1559 style); difficulty adjustment; merge-mining for security budget; stockpile SoV narrative |
| **Utility/Work** | Mandatory on-chain burn for service consumption; lockdrop/staking to reduce velocity; token-denominated SLAs; deflationary cap |
| **Governance** | Fee capture → buyback-and-burn or dividend; delegation UX; time-locked execution; multi-sig veto for catastrophic proposals; quadratic voting |
| **veToken** | Liquid wrapper with canonical status to reduce fragmentation; decaying bribe weighting; minimum lock duration for governance; gauge weight caps per pool |
| **Dual-Token (algo-stable)** | Hard collateral backing ≥ 100% at all times; circuit breakers on redemption volume; separate stability and growth token risk; regular audits of peg defense capacity |
| **Dual-Token (P2E)** | Calibrate sink/source ratio before launch; dynamic burn mechanisms tied to token price; separate competitive from casual economies |
| **Rebasing** | External collateral (not governance token); PID controller with tested parameters; transparent backing dashboard; circuit breakers |
| **Real-Yield** | Fees in ETH/USDC not native token; debt caps per staker; hedging tools for debt pool exposure; vesting for escrowed rewards |
| **LST** | Operator diversification; slashing insurance fund; correlated collateral haircuts in lending protocols; withdrawal queue liquidity buffers |

### Classification Decision Tree

```
Is the token primarily a unit of account / store of value with no protocol utility?
  YES → CURRENCY TOKEN (BTC, LTC)
  NO ↓

Does holding/staking the token grant rights to protocol revenue or fee distribution?
  YES → Is revenue in ETH/stablecoins?
    YES → REAL-YIELD / FEE-SHARING TOKEN (GMX, dYdX, SNX)
    NO  → Governance token with self-referential yield (see governance branch)
  NO ↓

Is the token required to consume a specific protocol service (gas, storage, bandwidth)?
  YES → UTILITY / WORK TOKEN (ETH-gas, FIL, HNT)
  NO ↓

Does the token supply automatically expand or contract based on price signals?
  YES → REBASING TOKEN
    Is there hard collateral backing? YES → RAI (PID rebase) / AMPL-style
    Is backing primarily governance token? YES → HIGH RISK (OHM-fork)
  NO ↓

Does the token represent a claim on staked ETH (or other L1) with yield pass-through?
  YES → LIQUID STAKING TOKEN (stETH, rETH)
  NO ↓

Is the token locked in exchange for time-weighted voting power and/or emissions boost?
  YES → veToken / VOTE-ESCROW TOKEN (veCRV, veBAL, vePENDLE)
  NO ↓

Does the token govern protocol parameters, treasury, or upgrade proposals?
  YES → Is there a separate stable/utility token in the same system?
    YES → DUAL-TOKEN SYSTEM (MKR/DAI, AXS/SLP, GMX/GLP)
    NO  → GOVERNANCE TOKEN (UNI, COMP, ARB)
  NO ↓

UNCLASSIFIED — review whitepaper for explicit value accrual mechanism
```

### Simulation Approach per Archetype

| Archetype | Primary Simulation Method | Key State Variables |
|-----------|--------------------------|---------------------|
| Currency | Agent-based (miner/holder/speculator); stock-to-flow Monte Carlo | hash_rate, block_reward, circulating_supply, price |
| Utility/Work | System dynamics (velocity model); demand/supply ABM | active_users, tx_volume, fee_burn_rate, staking_rate |
| Governance | Voting game theory; Shapley value for whale concentration | holder_distribution, quorum_rate, proposal_frequency |
| veToken | Differential equations for lock decay; gauge weight optimization | total_locked, avg_lock_time, gauge_weights, bribe_APR |
| Dual-Token (algo) | Scenario analysis for bank run; Monte Carlo on collateral stress | collateral_ratio, mint_rate, redemption_queue, peg_price |
| Dual-Token (P2E) | Agent-based with scholar/whale/casual segments; sink/source accounting | daily_mint, daily_burn, active_players, token_price |
| Rebasing | PID controller simulation; scenario analysis on oracle manipulation | supply, target_price, oracle_price, rebase_dampener |
| Real-Yield | Revenue projection model; debt pool correlation stress test | fees_usd, staked_value, debt_pool_composition |
| LST | Slashing scenario analysis; depeg cascade Monte Carlo | operator_count, slash_history, peg_deviation, DeFi_collateral_exposure |

---

## Key Sources

- Messari "Token Classification Framework" (TCF) — https://messari.io/report/token-classification-framework
- Token Engineering Commons — https://tokenengineeringcommunity.github.io/website/
- Voshmgir, S. (2019). *Token Economy*. BlockchainHub Berlin. https://token.kitchen/book
- Curve Finance veCRV docs — https://curve.readthedocs.io/dao-vecrv.html
- Cronje, A. (2022). ve(3,3) design post — https://andrecronje.medium.com/ve-3-3-44466eaa088b
- Delphi Digital "The Ownership Economy" — https://members.delphidigital.io/reports/the-ownership-economy
- Gauntlet Network: MakerDAO, Compound, and Aave parameter analysis — https://gauntlet.network/research
- OHM post-mortem analysis — https://olympusdao.medium.com/
- Reiff, N. (2023). "What Are Tokenomics?" Investopedia. https://www.investopedia.com/terms/t/tokenomics.asp
- Frax Finance RAI/FEI analysis — https://docs.frax.finance
- Lido Finance stETH docs — https://docs.lido.fi
- RocketPool rETH docs — https://docs.rocketpool.net
- GMX v2 Docs — https://docs.gmx.io
- Pendle Finance veToken docs — https://docs.pendle.finance
- Zargham, M. et al. (2019). "Economic Games as Estimators." cadCAD whitepaper. https://epub.wu.ac.at/7433/
- Buterin, V. (2017). "On Medium of Exchange Token Valuations." https://vitalik.ca/general/2017/10/17/moe.html
- Li, X. & Mann, W. (2021). "Initial Coin Offering and Platform Building." *Journal of Finance*. (governance token empirics)
