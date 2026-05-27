# Token Archetypes

## Formulas per Archetype

| Archetype | Key Formulas |
|---|---|
| **Currency** | MV=PQ → P = MV/Q; Stock-to-Flow SF = stock/annual_issuance; inflation = block_reward × blocks/year / circulating |
| **Utility/Work** | Velocity V = (GDP_on_chain × price) / M; net_supply = issuance − fee_burn; deflationary when burn > issuance |
| **Governance** | vp_i = tokens_i / total (linear); quorum passes if (yes / total_supply) ≥ threshold AND yes > no |
| **veToken** | ve_i = tokens_locked × (t_remaining / t_max); boost = min(2.5, 1 + 1.5 × (ve_i/ve_total) / (lp_i/lp_total)) |
| **Rebasing** | AMPL: supply_new = supply_old × (price / target); OHM backing = treasury_assets / circulating; RAI: p_r(t+1) = p_r(t) × (1 + rate × Δt) |
| **Real-Yield** | APR = (fees_distributed_annual / staked_value) × 100; GMX MPs: 0.01 × staked_GMX per second (100% APR) |
| **Dual-Token** | MKR/DAI: surplus = stability_fees; MKR burns when surplus > buffer; GLP_price = AUM / GLP_supply |
| **LST** | rETH_price = ETH_in_pool / rETH_supply (accumulating); apr_lst = consensus + tips + MEV − operator_fee |

---

## Failure Patterns

| Archetype | Failure Mode | Mechanism | Real Example |
|---|---|---|---|
| **Currency** | Miner capitulation spiral | Price drop → hash rate falls → security degrades → price drop | BCH/BSV post-fork |
| **Currency** | Velocity inflation | Adoption as medium of exchange without SoV demand → V rises → price suppressed | Payment coins 2017–2018 |
| **Utility/Work** | Token not required | Protocol accepts ETH/stablecoins; native token loses utility | Most 2017 ICO tokens |
| **Utility/Work** | Velocity trap | Users hold minimum; P → 0 as adoption grows | Nearly all "gas" tokens without burn |
| **Utility/Work** | Demand-supply mismatch | Large unlock vs. slow demand growth | FIL 2021–2022 |
| **Governance** | Voter apathy | Low participation → proposals pass with tiny minority | Compound governance proposals |
| **Governance** | Plutocratic capture | Whales drain treasury or set favorable parameters | Mango Markets (MNGO) |
| **Governance** | Worthless option | No fee capture, no burns; pure speculation | Most early DeFi governance tokens |
| **veToken** | Bribe-driven vote capture | External protocols aggregate votes → control gauge weights | Curve wars 2021–2022 |
| **veToken** | Late-entrant dilution | Early lockers hold max boost; new LPs need proportionally more vePower | veCRV boost gap |
| **Dual-Token** | Stability token bank run | Confidence crisis → redemption surge → governance token death spiral | LUNA/UST May 2022 |
| **Dual-Token** | P2E sink/source imbalance | More SLP minted than burned → hyperinflation → scholar exit loop | AXS/SLP 2022 |
| **Rebasing** | Reflexive ponzi collapse | High APY only sustainable with new entrants; treasury backing < market cap | OHM Nov 2021–2022 |
| **Real-Yield** | Circular yield | Fees paid in native token; price drops → real APR drops → stakers exit → price drops | SNX pre-Perps v2 |
| **LST** | Depeg cascade | LST < ETH peg → protocols collateralized on LST face mass liquidation | stETH May 2022 |

---

## Classification Decision Tree

```
Unit of account / store of value with no protocol utility?
  YES → CURRENCY (BTC, LTC)
  NO ↓

Holding/staking grants rights to protocol revenue or fee distribution?
  YES → Fees in ETH/stablecoins?  YES → REAL-YIELD (GMX, SNX)
                                   NO  → governance token w/ self-referential yield
  NO ↓

Token required to consume a specific protocol service (gas, storage)?
  YES → UTILITY / WORK TOKEN (ETH-gas, FIL, HNT)
  NO ↓

Supply automatically expands/contracts based on price signals?
  YES → REBASING TOKEN
        Hard collateral? YES → RAI/AMPL-style
        Backing is governance token? YES → HIGH RISK (OHM-fork)
  NO ↓

Claim on staked ETH/L1 with yield pass-through?
  YES → LIQUID STAKING TOKEN (stETH, rETH)
  NO ↓

Locked for time-weighted voting power or emissions boost?
  YES → veToken / VOTE-ESCROW (veCRV, veBAL, vePENDLE)
  NO ↓

Governs protocol parameters, treasury, or upgrade proposals?
  YES → Separate stable/utility token in same system?
        YES → DUAL-TOKEN (MKR/DAI, AXS/SLP, GMX/GLP)
        NO  → GOVERNANCE TOKEN (UNI, COMP, ARB)
  NO ↓

UNCLASSIFIED — review whitepaper for explicit value accrual mechanism
```

---

## Simulation Approach per Archetype

| Archetype | Primary Simulation | Key State Variables |
|---|---|---|
| Currency | Stock-to-flow Monte Carlo; miner/holder ABM | hash_rate, block_reward, circulating_supply, price |
| Utility/Work | Velocity model (system dynamics) | active_users, tx_volume, fee_burn_rate, staking_rate |
| Governance | Voting game theory; whale concentration | holder_distribution, quorum_rate, proposal_frequency |
| veToken | Lock decay diff. equations; gauge weight sweep | total_locked, avg_lock_time, gauge_weights, bribe_APR |
| Dual-Token (algo) | Bank run scenario; Monte Carlo on collateral stress | collateral_ratio, mint_rate, redemption_queue, peg_price |
| Dual-Token (P2E) | Agent-based with player segments; sink/source accounting | daily_mint, daily_burn, active_players, token_price |
| Rebasing | PID controller simulation; oracle manipulation scenario | supply, target_price, oracle_price, rebase_dampener |
| Real-Yield | Revenue projection; debt pool correlation stress | fees_usd, staked_value, debt_pool_composition |
| LST | Slashing scenario; depeg cascade Monte Carlo | operator_count, slash_history, peg_deviation, DeFi_collateral |
