# Treasury Design

## Key Formulas

### Runway
```
Runway (months) = Stablecoin_Reserves / Monthly_Burn_Rate

Adjusted_Runway = (Stablecoins + Liquid_Non-Native × Haircut) / Monthly_Burn_Rate
```
Haircut: BTC/ETH = 0.85; blue-chip DeFi tokens = 0.60; illiquid positions = 0.20

**Native token is excluded from runway numerator.** A protocol that needs funds during a crisis is precisely the time when native token price has collapsed.

**Minimum viable runway by stage:**
| Stage         | Stablecoin Runway |
|---|---|
| Pre-revenue   | ≥ 24 months |
| Early revenue (fees < burn) | ≥ 18 months |
| Sustainable (fees ≥ burn)   | ≥ 12 months |

### Diversification
```
Native_Concentration = Native_Token_Value / Total_Treasury_Value
Stablecoin_Coverage  = Stablecoin_Reserves / (12 × Monthly_Burn_Rate)
```
| Stage         | Max Native | Min Stablecoin |
|---|---|---|
| Pre-revenue   | 50%        | 40%            |
| Early revenue | 60%        | 30%            |
| Sustainable   | 70%        | 20%            |

**Native > 80% = critical red flag regardless of stage.**

### Protocol-Owned Liquidity (POL)
```
Bond_Discount = (Market_Price − Bond_Price) / Market_Price
POL_Ratio     = Protocol_Owned_LP_Value / Total_Liquidity_in_Pool
Revenue_POL   = TVL_owned × Pool_Fee_Rate × Volume_Utilization
```
Bonds only profitable for protocol when `Bond_Discount ≥ 0`. Never sell bonds at discount to market.

---

## Minimum Viable Treasury Thresholds

| Stage         | Stablecoin Floor | Total Treasury Floor |
|---|---|---|
| Pre-product   | $500K   | $1M   |
| Pre-revenue   | $2M     | $5M   |
| Early revenue | $5M     | $15M  |
| Sustainable   | $10M    | $30M+ |

---

## Checklist

**Runway Red Flags**
- [ ] Runway < 12 months in stablecoin terms → critical; trigger diversification governance vote
- [ ] Runway calculated including native tokens at market price → misleading; restate stablecoin-only
- [ ] Monthly burn rate not publicly reported or on-chain → opacity red flag
- [ ] No separation between reserve treasury and operating budget → governance bottleneck + security risk

**Diversification**
- [ ] Stablecoin reserves cover ≥ 18 months of burn (pre-revenue) or ≥ 12 months (revenue-generating)
- [ ] Native concentration < 60% of total treasury
- [ ] At least one non-correlated asset held (BTC, ETH, or RWA-backed stablecoin)
- [ ] TWAP or Gnosis auction used for large native → stablecoin swaps (no market sells)

**Governance / Transparency**
- [ ] All treasury wallets labeled and enumerated in governance docs
- [ ] Any transfer > 1% of treasury requires time-locked governance vote (≥ 48h delay)
- [ ] Monthly treasury report published on-chain: opening balance, inflows, outflows, runway restatement
