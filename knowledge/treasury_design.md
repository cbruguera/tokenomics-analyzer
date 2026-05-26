# Treasury Design

## Key Formulas

### Runway
```
Runway (months) = Stablecoin_Reserves / Monthly_Burn_Rate

Adjusted_Runway (months) = (Stablecoin_Reserves + Liquid_Non-Native_Assets × Haircut)
                           / Monthly_Burn_Rate

Haircut: BTC/ETH = 0.85; blue-chip DeFi tokens = 0.60; illiquid positions = 0.20
```
- `Monthly_Burn_Rate` = contributor salaries + infra + audits + grants disbursed (cash-equivalent)
- Native token held in treasury is excluded from runway numerator — it is not sovereign over its own price
- **Minimum viable runway by stage:**
  - Pre-revenue: ≥ 24 months stablecoin runway
  - Early revenue (protocol fees < burn): ≥ 18 months
  - Sustainable (fees ≥ burn): ≥ 12 months buffer

### Diversification Ratio
```
Native_Concentration = Native_Token_Value / Total_Treasury_Value

Stablecoin_Coverage_Ratio = Stablecoin_Reserves / (12 × Monthly_Burn_Rate)
```
- **Benchmark bands** (from Llama/Tally treasury health frameworks and observed practice):
  | Stage         | Max Native | Min Stablecoin | Min Non-Native Non-Stable |
  |---------------|-----------|----------------|---------------------------|
  | Pre-revenue   | 50%       | 40%            | 10%                       |
  | Early revenue | 60%       | 30%            | 10%                       |
  | Sustainable   | 70%       | 20%            | 10%                       |
- Native > 80% of treasury = critical red flag regardless of stage

### Protocol-Owned Liquidity (POL)
```
Bond_Discount = (Market_Price − Bond_Price) / Market_Price
POL_Ratio     = Protocol_Owned_LP_Value / Total_Liquidity_in_Pool

Revenue_from_POL = TVL_in_owned_LP × Pool_Fee_Rate × Volume_Utilization
```
- Olympus bond vesting period: typically 5 days; creates sell pressure at vest
- OHM backing per token: `Backing = Treasury_Value_excl_OHM / OHM_Circulating_Supply`
- Bond profitable for protocol only when `Bond_Discount > 0` and market price > backing value

### Grant Streaming (Sablier/Superfluid model)
```
Released(t) = Grant_Total × (t − t_start) / (t_end − t_start)   [linear]
Cliff_Release = Grant_Total × Cliff_Pct  at  t = t_cliff
```

---

## Core Principles

1. **Stablecoins are the unit of treasury solvency.** Native token holdings inflate paper value but are not usable to pay salaries or auditors without market impact. Size runway only in stablecoins or highly liquid non-native assets.

2. **Diversify before you need to.** Token price is highest during bull markets; that is the window to swap a portion of native holdings into stablecoins via on-chain OTC (e.g., via Gnosis auction, Uniswap TWAP) without causing panic. Waiting until runway < 12 months forces distressed selling.

3. **Protocol-owned liquidity reduces rent to mercenary LPs.** POL (Olympus bonds, Tokemak reactors) lets the protocol own its own liquidity permanently, capturing fee revenue and eliminating the APY arms race. Trade-off: locked capital, impermanent loss accrues to protocol.

4. **Streaming > lump-sum for grants.** Lump-sum disbursements remove accountability leverage. Stream grants with a cliff (e.g., 10% at 30 days, remainder linearly over 12 months) so the DAO can revoke the stream if milestones are missed.

5. **On-chain transparency is non-negotiable.** All treasury flows — grants, contributor payments, swap proceeds — must be traceable on-chain. Off-chain multisigs controlled by founding team members with no on-chain reporting are governance risk.

6. **The surplus buffer is a shock absorber, not idle capital.** MakerDAO's Surplus Buffer (target: 250M DAI as of 2023) absorbs bad debt before MKR is minted and diluted. Protocols should target a surplus equal to 6–12 months of worst-case bad-debt exposure.

7. **Tokemak-style reactors decouple liquidity direction from token rewards.** Liquidity Directors stake TOKE to vote on where protocol-owned liquidity is deployed; this lets the protocol earn yield on its treasury while subsidizing liquidity for partner protocols.

8. **Avoid circular treasury investment.** Treasury should not hold significant positions in tokens of protocols that hold significant positions in the protocol's own token — this creates correlated collapse risk.

9. **Separate operating budget from reserve treasury.** Maintain a 3–6 month operating multisig funded from the reserve; governance votes are only needed for large reserve drawdowns, not routine payroll.

10. **Uniswap Grants Program lesson: pipeline > treasury size.** Uniswap's $74M treasury (as of 2023) was underdeployed because no systematic grant pipeline existed. Treasury idle in native tokens earns nothing and depreciates in real terms if token price falls.

---

## Failure Patterns

### 1. Native Token Concentration — SushiSwap (2020–2021)
- At peak, >90% of Sushi treasury was held in SUSHI tokens
- 0xMaki incident: core dev attempted to liquidate ~$14M SUSHI without governance approval
- When SUSHI price fell 70% in a bear market, effective runway collapsed from "years" to months
- **Mechanism:** Circular dependency — treasury value depends on token price, which depends on protocol health, which depends on treasury spending capacity

### 2. No On-Chain Visibility — Build Finance DAO (2022)
- Treasury controlled by a small multisig with no on-chain reporting
- Hostile takeover: attacker accumulated governance tokens cheaply (low liquidity, low participation), passed proposal to transfer treasury to attacker-controlled wallet
- ~$470K drained; DAO had no time-lock, no guardian, no on-chain audit trail
- **Mechanism:** Opacity + weak governance = single point of failure

### 3. Unsustainable POL via High-APY Bonding — Olympus Forks (2021–2022)
- Fork protocols offered 10,000–100,000%+ staking APY to attract TVL
- Bond discounts were deeply negative (bonds priced above market) — protocol paying more than it received
- Treasury backing per token eroded; when price broke below backing, mass exits triggered death spiral
- **Mechanism:** `Bond_Discount < 0` + reflexive staking = treasury drain accelerates as price falls

### 4. Lump-Sum Grant Mismanagement — Uniswap Grants v1 (2020)
- First grants program disbursed lump sums with minimal milestone accountability
- Several grants delivered no output; no clawback mechanism existed
- **Mechanism:** Lump-sum + no on-chain streaming = no enforcement leverage post-disbursement

### 5. Surplus Buffer Breach — MakerDAO Black Thursday (March 2020)
- ETH price crashed 50% in hours; liquidation bots failed (gas spike), auctions settled at $0
- 5.4M DAI in bad debt exceeded the then-~500K DAI surplus buffer
- Emergency MKR dilution (flop auction) required, diluting all holders
- **Mechanism:** Surplus buffer undersized relative to liquidation cascade exposure; buffer must scale with total collateral at risk

### 6. Nouns DAO Fork Pressure (2023)
- Nouns DAO treasury grew to >27,000 ETH (~$40M+) with no mandatory spending mechanism
- A "ragequit" fork faction (Nouns DAO fork, Sept 2023) exercised new fork mechanism to claim pro-rata treasury share
- ~20% of token holders forked out, extracting ~$27M ETH equivalent
- **Mechanism:** Idle, growing treasury with no clear purpose creates exit incentives; treasury must have a spend thesis or face redemption pressure

---

## Mitigations / Best Practices

### Diversification Checklist
- [ ] Stablecoin reserves cover ≥ 18 months of burn (pre-revenue) or ≥ 12 months (revenue-generating)
- [ ] Native token concentration < 60% of total treasury
- [ ] At least one non-correlated asset class held (BTC, ETH, or RWA-backed stablecoin)
- [ ] Regular (quarterly) rebalancing governance proposal to top up stablecoin buffer
- [ ] TWAP or Gnosis auction used for large native → stablecoin swaps (no market sells)

### Runway Red Flags
- [ ] Runway < 12 months in stablecoin terms → critical; trigger diversification governance vote immediately
- [ ] Runway calculated including native tokens at current market price → misleading; restate stablecoin-only
- [ ] No separation between reserve treasury and operating budget → governance bottleneck + security risk
- [ ] Monthly burn rate not publicly reported or on-chain → opacity red flag

### POL Design Rules
- Use bonds with `Bond_Discount ≥ 0` — never sell discounted bonds that benefit buyers at protocol expense
- Vest bonds over ≥ 5 days to dampen sell pressure; longer vest (14–30 days) preferred for large issuances
- Set a maximum POL target (e.g., own ≤ 50% of pool) to avoid price manipulation risk
- Tokemak model: segregate reactor capital from operational treasury; earned fees re-enter reserve

### Grant Disbursement Rules
- Minimum cliff: 10–20% released after 30–90 day proof-of-work milestone
- Remainder streamed linearly (Sablier, Superfluid, or LlamaPay) over 6–12 months
- Include on-chain cancellation rights for DAO multisig if milestones missed
- Maximum single grant size: cap at 1–2% of stablecoin reserves without supermajority vote

### Minimum Viable Treasury Thresholds
| Stage          | Stablecoin Floor | Total Treasury Floor | Rationale                              |
|----------------|-----------------|---------------------|----------------------------------------|
| Pre-product    | $500K           | $1M                 | 24-month minimal team runway           |
| Pre-revenue    | $2M             | $5M                 | 18-month ops + audit + security budget |
| Early revenue  | $5M             | $15M                | 12-month ops + growth grants           |
| Sustainable    | $10M            | $30M+               | Surplus buffer + POL + grants pipeline |

### On-Chain Transparency Minimum Bar
- All treasury wallets labeled and enumerated in governance docs
- Monthly treasury report published on-chain or in governance forum with: opening balance, inflows, outflows by category, closing balance, runway restatement
- Any single transfer > 1% of treasury requires a time-locked governance vote (≥ 48-hour delay)
- Multisig signers publicly doxxed or at minimum pseudonymous with on-chain track record

---

## Key Sources

- MakerDAO Surplus Buffer MIP (MIP84, MIP65 — 2022–2023 era): https://forum.makerdao.com/t/mip84-activate-protocol-owned-vault-emulation/17713 ; https://makerburn.com/#/ — Note: MakerDAO rebranded as Sky Protocol in August 2024 under the "Endgame" plan; MIP84/MIP65 were superseded by the Endgame governance framework (MIP104+). Historical mechanics remain relevant; verify current operational status against Sky Protocol docs.
- Olympus DAO documentation and bonding mechanics: https://docs.olympusdao.finance/main/overview/intro ; https://olympusdao.medium.com/introducing-olympus-pro-d8db3052fca5
- Tokemak documentation (reactors, liquidity direction): https://docs.tokemak.xyz/
- SushiSwap 0xMaki treasury incident: https://www.coindesk.com/markets/2020/09/11/sushiswap-drama-everything-you-need-to-know/ ; https://forum.sushi.com/t/re-addressing-the-treasury/1936
- Nouns DAO fork event (Sept 2023): https://nouns.wtf/vote/301 ; https://dune.com/queries/2933190
- Uniswap Grants Program v1/v2 retrospective: https://gov.uniswap.org/t/uniswap-grants-program-v2-launch/13685
- Llama treasury management platform: https://llama.xyz/ ; https://twitter.com/llamacommunity_
- Tally treasury health research: https://www.tally.xyz/
- LlamaPay streaming protocol: https://llamapay.io/
- MakerDAO Black Thursday post-mortem: https://forum.makerdao.com/t/black-thursday-response-thread/1433
- Hasu & Uncommon Core — "How to think about DAO treasury": https://uncommoncore.co/a-new-mental-model-for-defis-treasury-problem/
- Delphi Digital DAO treasury diversification report (2022): https://members.delphidigital.io/
- Build Finance DAO hostile takeover: https://forum.buildfinance.io/t/urgent-hostile-governance-takeover/427
