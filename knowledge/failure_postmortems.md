# Token Failure Postmortems

## Key Formulas

**Algorithmic stablecoin mint/burn parity:**
```
1 UST minted  ⟺  $1 USD worth of LUNA burned
1 UST redeemed ⟺  $1 USD worth of LUNA minted
```
Death spiral trigger: if LUNA market cap < UST market cap, full redemption is impossible without hyperinflating LUNA supply.

**Reflexivity condition (generic):**
```
Token price P drives yield Y (via rebase/emissions)
Y drives demand D → D drives P
If dP/dt < 0 → dY/dt < 0 → dD/dt < 0 → reinforcing collapse
```

**OHM rebase APY:**
```
APY = (1 + rebase_rate)^(rebase_periods_per_year) - 1
At 0.5% per 8-hour epoch: APY ≈ 100,000%
Sustainable only if POL treasury yield > rebase dilution rate
```

**Iron Finance partial-collateral:**
```
IRON = x% USDC + (1-x)% TITAN (by market value at mint time)
Bank run loop: TITAN price ↓ → collateral shortfall → more TITAN minted → TITAN price ↓
```

**Anchor yield sustainability:**
```
Real yield = staking rewards on bLUNA/bETH collateral ≈ 6–8%
Promised yield = 20% APY
Deficit = ~12–14% covered by finite LFG reserve
Reserve runway ≈ weeks at peak TVL ($17B)
```

---

## Core Principles

1. **Endogenous collateral is not collateral.** Using the protocol's own token as backing creates circular dependency; collateral value falls simultaneously with liabilities.
2. **Artificial yield inflates demand for the pegged asset, not organic usage.** When yield disappears, demand evaporates faster than supply can contract.
3. **Reflexive designs amplify both upswings and downswings symmetrically.** Any self-reinforcing rise is an equally self-reinforcing fall.
4. **Backing asset MC must exceed outstanding liabilities at all times.** A protocol is insolvent the moment backing MC < liability MC, even if the peg temporarily holds.
5. **APY >50% annualized attracts mercenary capital that exits on any negative signal.**
6. **Thin liquidity at the peg allows small sells to trigger automated death spirals.** Protocol-owned liquidity must scale with supply.
7. **(3,3) staking cooperation collapses the moment any large holder defects.** "Last one out loses everything" dominates.
8. **Treasury drawn down to pay yield has a calculable end date.** Runway <30 days is a critical risk signal.
9. **On-chain metrics diverge from narrative weeks before collapse.** Supply growth, peg deviation, TVL outflows all signal distress early.
10. **Governance cannot act fast enough to stop a bank run.** Circuit breakers must be in smart contracts, not dependent on human response.

---

## Failure Patterns

### Terra / LUNA (May 2022)
*Algorithmic stablecoin backed by endogenous LUNA; Anchor Protocol offered 20% APY on UST deposits, funded by finite LFG reserve. UST/LUNA mint-burn parity meant LUNA hyperinflated as UST was redeemed under stress.*

**Design warning signs:**
- Backing asset (LUNA) was endogenous — not an independent store of value
- UST demand was entirely yield-driven (Anchor), not organic commerce
- LFG BTC reserve was ~10% of UST market cap at peak — insufficient for a full bank run
- Mint/burn rate was uncapped — no circuit breaker on LUNA issuance velocity
- Curve liquidity pool thin relative to outstanding UST supply

**On-chain distress signals:**
- Anchor Reserve depletion rate accelerating (weeks before collapse)
- Curve UST/3pool imbalance >55% UST composition days before depeg
- Large wallet UST withdrawals from Anchor in the week prior
- LUNA/UST mint volume spike visible on-chain before public awareness
- LFG BTC wallet outflows 48h before public announcement

**Prevention design changes:**
- Cap total UST supply as fraction of LUNA market cap (e.g., max 50%)
- Implement mint/burn rate limiter (e.g., max 0.1% of supply per hour)
- Require exogenous collateral (BTC, ETH) ≥100% — not as reserve add-on
- Decouple demand driver from the token itself (do not subsidize yield with emissions)
- Protocol-owned liquidity sized to handle a 30% bank run scenario

---

### Iron Finance / TITAN (June 2021)
*Partial-collateral stablecoin (75% USDC + 25% TITAN). Algorithmic CR reduction meant the system was least protected at peak popularity. Instant uncapped redemption enabled bank run in a single block.*

**Design warning signs:**
- TITAN had no fundamental value beyond subsidizing the peg
- Algorithmic CR reduction → least protected at peak popularity
- No minimum CR floor enforced in smart contracts
- Redemption mechanism uncapped and instant
- TITAN liquidity thin relative to IRON supply it backed

**On-chain distress signals:**
- TITAN price deviation from 7-day MA >20% (day before collapse)
- Large TITAN wallet sell orders in DEX order flow hours before collapse
- IRON peg deviation >0.3% on Curve — first sign of confidence loss
- TITAN/USDC LP withdrawal acceleration (LPs exiting before bank run)

**Prevention design changes:**
- Hard-code minimum CR floor (≥90%) — governance-immutable for ≥12 months
- Add time-delay on large redemptions (24h for redemptions >$100K)
- Require TITAN market cap ≥ 3× the TITAN-backed portion of outstanding IRON
- Use TWAP pricing (≥1h) for collateral valuation to prevent manipulation
- Cap total IRON supply relative to exogenous collateral on hand

---

### Olympus DAO / OHM (Late 2021 – 2022)
*Rebase mechanism paid stakers >100,000% APY in OHM. (3,3) social game theory assumed coordinated staking but had no enforcement. Protocol-owned liquidity via bonding was innovative; the yield promise was not sustainable.*

**Design warning signs:**
- APY paid in native token — real yield was zero; 100% dilutive
- Price/RFV ratio 40–50× at peak (4,000–5,000% premium to backing)
- No mechanism to reduce rebase rate as supply grew
- (3,3) was social consensus with no contractual enforcement
- Forks launched with smaller treasuries but identical APY promises

**On-chain distress signals:**
- OHM price/RFV ratio declining (compression from 50× toward 10×)
- Bonding discount shrinking — treasury no longer attracting capital
- Staking ratio declining — holders beginning to exit
- Large OHM unstaking events on-chain before price collapse
- Fork protocol treasuries draining faster than inflows

**Prevention design changes:**
- Tie rebase rate to treasury sustainability metric (e.g., treasury yield / staked supply)
- Cap price/backing ratio; auto-reduce emissions when ratio exceeds threshold
- Implement rage-quit buyback: if price < RFV, treasury buys at RFV floor
- Require minimum 30-day lockup for staked positions
- Publish daily treasury inflow vs. rebase obligation ratio as first-class metric

---

### Anchor Protocol (2021 – 2022)
*Fixed 20% APY on UST funded ~6–8% by real staking yield and the rest by finite LFG grants. Reserve runway was publicly calculable months before collapse. UST demand was 80%+ Anchor-dependent.*

**Design warning signs:**
- Yield was a fixed-rate promise creating a liability, not a market incentive
- Real yield from collateral (~6–8%) never close to promised rate (20%)
- Reserve runway calculable publicly; analysts published "X days to empty" months before
- No automatic yield adjustment tied to reserve level
- bLUNA as primary collateral created circular risk: Anchor depended on LUNA health

**On-chain distress signals:**
- Anchor Reserve wallet balance declining (public Dune dashboards)
- Borrow/deposit ratio trending down (fewer borrowers → more reserve drain)
- bLUNA/LUNA peg deviation widening (liquidation risk increasing)
- Large UST deposit wallet exit positions accumulating
- UST Curve pool imbalance growing 2 weeks before collapse

**Prevention design changes:**
- Implement dynamic yield rate tied to reserve balance: yield = min(real_yield, reserve_ratio × target)
- Cap maximum deposit TVL relative to sustainable yield capacity
- Require yield funded entirely by real revenue within 6 months of launch
- Diversify collateral away from endogenous assets
- Publish reserve runway as mandatory on-chain metric; governance alerts at <90 days

---

### Basis Cash (December 2020 – 2021)
*Three-token seigniorage system (BAC stablecoin, BAB bonds, BAS shares). Bond overhang accumulated when peg was not restored; new seigniorage would go entirely to bond redemption with no upside for new buyers. No exogenous collateral at any ratio.*

**Design warning signs:**
- Bond mechanism required confidence that peg would return — self-fulfilling with no guarantee
- Seigniorage share value was entirely speculative future expansion
- No exogenous collateral backstop at any ratio
- Bond issuance unlimited — overhang could grow to exceed any realistic recovery seigniorage
- All protocol value was circular (BAC→BAB→BAC→BAS→BAC)

**On-chain distress signals:**
- BAC/DAI price persistently below $0.99 for >7 consecutive days
- BAB outstanding supply growing faster than BAC total supply (overhang accumulating)
- BAS staking withdrawals increasing
- Liquidity mining rewards decreasing without organic replacement

**Prevention design changes:**
- Require minimum exogenous collateral ratio (even 20% USDC) for liquidation floor
- Cap total bond issuance at a multiple of protocol treasury value
- Implement bond expiry: bonds not redeemed within N months become worthless
- Tie seigniorage to real fee revenue, not purely expansion-phase minting
- Use price oracle with >1h TWAP before triggering contraction/expansion

---

## Mitigations / Best Practices

### Death Spiral Checklist

A protocol presents HIGH collapse risk if **3 or more** conditions are simultaneously true:

| # | Condition | Signal Threshold |
|---|---|---|
| 1 | Collateral is endogenous (protocol's own token) | Any endogenous collateral >0% |
| 2 | Backing asset MC < outstanding liability MC | Ratio <1.0 |
| 3 | Yield is subsidized, not earned from real revenue | Subsidy >30% of total yield |
| 4 | APY >50% annualized with no sustainable source | APY >50% + treasury runway <1yr |
| 5 | Peg deviates >1% for >24 hours | Depeg >1% for 24h |
| 6 | Treasury reserve runway <60 days at current burn | Runway <60 days |
| 7 | No mint/burn rate limiter in smart contract | Unlimited issuance velocity |
| 8 | Protocol liquidity <10% of outstanding supply | Liquidity/supply <0.10 |
| 9 | Top-10 holders control >40% of collateral token | Concentration >40% |
| 10 | Demand driver is a single internal yield product | >60% TVL from one source |

### Mandatory Design Requirements

**Collateral:**
- Minimum 100% exogenous collateral for any stablecoin claiming store-of-value status
- Hard-code minimum CR floor (≥80%) — governance-immutable for ≥12 months post-launch
- Use TWAP (minimum 1 hour) for all collateral valuations

**Supply mechanics:**
- Mint/burn rate cap: no more than 1% of total supply per hour without a 48h timelock
- Bond/debt instruments: hard expiry + total issuance cap relative to treasury size
- Rebase/emission rates must auto-reduce when price/backing ratio falls below threshold

**Yield sustainability:**
- Any protocol promising >10% APY must publish a real-time yield coverage ratio = real_revenue / promised_yield_obligations
- Coverage ratio <1.0 triggers automatic yield reduction (no governance vote required)
- Reserve funds for yield subsidies must be escrowed on-chain with transparent runway tracking

**Liquidity:**
- Protocol-owned liquidity ≥15% of total stablecoin/debt supply at all times
- Automatic liquidity injection from treasury when on-chain depth falls below threshold

**Circuit breakers:**
- Peg deviation circuit breaker: if peg deviates >5% for >1 hour, pause minting
- Progressive redemption fees during stress: 0% normal → 1% if depeg >2% → 5% if depeg >5%
- Large redemption time-delay: redemptions >0.1% of total supply face a 24h delay

**Monitoring obligations (on-chain readable):**
- Backing ratio
- Reserve runway in days
- Yield coverage ratio
- Protocol-owned liquidity depth

---

## Key Sources

- Nansen Research, "The Terra/LUNA Crash" (May 2022)
- Rekt News, "Iron Finance — REKT" (June 2021), rekt.news/iron-finance-rekt
- Rekt News, Olympus DAO analysis, rekt.news
- Anchor Protocol whitepaper (2021), anchorprotocol.com (archived)
- Basis Cash docs (2020), basis.cash (archived)
- Frax Finance documentation — contrast case for partial-collateral that survived
- Terra on-chain data: Dune Analytics terra-collapse queries (public)
- OlympusDAO documentation and forum posts, forum.olympusdao.finance (2021)
- Delphi Digital, "The Rise and Fall of Algorithmic Stablecoins" (2022)
