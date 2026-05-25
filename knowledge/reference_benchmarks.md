# Reference Benchmarks

*Last updated: 2026-05-25. Data retrieved from CoinGecko, DeFiLlama, protocol docs, and Ethereum Foundation sources.*

---

## Bitcoin (BTC)

| Parameter | Value | Source |
|---|---|---|
| Max supply | 21,000,000 BTC (hard cap) | Bitcoin protocol / Bitcoin Wiki |
| Circulating supply | ~19.86M BTC (94.6% of max) | blockchain.com/charts, May 2026 |
| Annual inflation | ~0.82% (post-April 2024 halving) | coinbird.com/learn/crypto-inflation |
| Team allocation | 0% — no premine, no team allocation | Bitcoin genesis design |
| Vesting | N/A | — |
| Staking yield | N/A (PoW; no staking) | — |
| Governance | No formal on-chain governance | — |
| Timelock | N/A | — |
| Treasury | No protocol treasury | — |
| Protocol revenue | N/A (miner fees go to miners) | — |
| P/Revenue | N/A | — |

---

## Ethereum (ETH)

| Parameter | Value | Source |
|---|---|---|
| Max supply | None (no hard cap; post-Merge burn can exceed issuance) | ethereum.org |
| Circulating supply | ~120M ETH | ethereum.org/en/supply/ |
| Annual inflation (net) | ~+0.18–0.23% (2025–2026; inflationary due to low L1 activity/burn) | blockworks.co, everstake.one 2025 annual report |
| Consensus layer issuance | ~0.52% annualized (with ~14M ETH staked) | ethereum.org/roadmap/merge/issuance/ |
| Annual validator issuance | ~1,700 ETH/day (~620K ETH/year) | ethereum.org |
| Team allocation (at genesis) | ~16.7% (Ethereum Foundation pre-sale and early contributors) | Ethereum genesis allocation, training knowledge |
| Vesting | No formal vesting; EF sells periodically | Ethereum Foundation transparency reports |
| Staking yield | 3.5–4% APY (Lido stETH); 2.84% consensus-only | defillama.com, lido.fi |
| Governance | Off-chain (EIP process + rough consensus); no on-chain voting | ethereum.org |
| Timelock | N/A (no on-chain protocol governance) | — |
| Treasury | Ethereum Foundation: ~$1.6B+ (ETH + stablecoins) | EF transparency report 2024 |
| Protocol revenue | EIP-1559 burn: ~3–70 ETH/day in 2025 (historically low); not "revenue" per se | dune.com ETH burn dashboards |
| P/Revenue | N/A — burn-as-revenue model; not directly comparable | — |

**Base reward formula (consensus spec):**
```
base_reward_per_increment = EFFECTIVE_BALANCE_INCREMENT * BASE_REWARD_FACTOR
                            // integer_squareroot(total_active_balance)
```
`BASE_REWARD_FACTOR = 64`; total issuance scales as `O(sqrt(total_stake))`.

Source: ethereum.github.io/consensus-specs/specs/phase0/beacon-chain/, eth2book.info/latest/part2/incentives/issuance/

---

## Uniswap (UNI)

| Parameter | Value | Source |
|---|---|---|
| Max supply | 1,000,000,000 UNI (minted at genesis; 100M burned Dec 2025) | blog.uniswap.org/uni, coindesk.com Dec 2025 |
| Circulating supply | ~900M UNI post-burn | — |
| Annual inflation | ~0% (no new emissions; supply now deflationary via fee-switch burns) | UNIfication proposal, Dec 2025 |
| Team allocation | 21.27% team + 18.04% investors + 0.69% advisors = **~40% insider** | blog.uniswap.org/uni |
| Vesting | 4-year linear; cliff details unspecified; fully vested by 2024 | Uniswap tokenomics docs |
| Staking yield | None historically; fee switch activated Dec 28, 2025 (fees → UNI burn, not staker yield) | coindesk.com Dec 2025 |
| Yield source | Real revenue (post-fee switch: protocol fees → burn) | UNIfication proposal |
| Governance | On-chain Compound Governor Bravo; **2-day timelock** | vote.uniswapfoundation.org |
| Treasury | ~330M UNI remaining in community treasury (43% original allocation minus 100M burned) | Uniswap Foundation |
| Protocol revenue | $1.05B in trading fees in 2025 (all to LPs pre-switch; fees to burns post-switch) | blockworks.co |
| P/Revenue | ~$5–6B market cap (estimate) / $1.05B = ~5–6x | — |

---

## Curve DAO (CRV / veCRV)

| Parameter | Value | Source |
|---|---|---|
| Max supply | 3,030,303,031 CRV | resources.curve.finance/crv-token/supply-distribution/ |
| Circulating supply | ~1.47B CRV (~48.5% of max, as of March 2026) | coindcx.com, mexc.co |
| Annual inflation | ~5.02% (reduced Aug 14, 2025; cut 15.9% from prior rate) | resources.curve.finance, BTCC |
| Team allocation | ~17% (team + investors at launch); Egorov held ~47% at launch — diluted by emissions | Curve DAO docs, training knowledge |
| Vesting | 4-year for early liquidity providers / team | curve.readthedocs.io |
| veCRV locked | ~40–50% of circulating supply locked | resources.curve.finance/crv-token/faq/ |
| Staking yield (veCRV) | 5–10% APY (trading fees + bribes from gauge votes) | Votium, Hidden Hand data |
| Yield source | Real yield: 50% of trading fees go to veCRV holders (3CRV); rest is bribe income | Curve DAO docs |
| Governance | veCRV weighted voting; gauge weights reset weekly; no formal timelock disclosed | curve.finance |
| Treasury | 10% of all protocol revenue allocated to DAO treasury (June 2025 governance vote — first-ever) | coinmarketcap.com CRV updates |
| Protocol revenue | Not publicly aggregated; DeFiLlama tracks per-pool; estimated $50–100M+ annualized in peak years | defillama.com/protocol/curve |
| P/Revenue | Difficult to calculate (revenue distributed directly to veCRV holders, not protocol treasury) | — |

---

## GMX (GMX)

| Parameter | Value | Source |
|---|---|---|
| Max supply | 13,250,000 GMX (hard cap; increase requires governance vote) | docs.gmx.io/docs/tokenomics/gmx-token/ |
| Circulating supply | ~10,395,551 GMX (78.5% of max) | defillama.com/protocol/gmx, May 2026 |
| Annual inflation | Near-zero (esGMX rewards vest linearly into GMX over 1 year; capped) | GMX docs |
| Team allocation | 1.9% (250,000 tokens for core contributors) | tokenomist.ai/gmx |
| Vesting | 2-year linear for team; most supply from XVIX/Gambit migration (45.3%) | tokenomist.ai/gmx |
| Staking yield | 5–12% real yield (ETH/AVAX); **staking currently suspended** — fees buying back GMX until price reaches $90 | defillama.com, tokenomics.com |
| Yield source | Real yield: 27% of protocol fees (leverage trading, liquidations, borrowing, swaps) to stakers | docs.gmx.io/docs/tokenomics/rewards/ |
| Governance | Multi-sig; governance forum-based; no published formal timelock | docs.gmx.io |
| TVL | $201M (primarily Arbitrum) as of Q2 2026 | defillama.com/protocol/gmx |
| Treasury | 10% of fees → protocol treasury; floor price fund: 2M tokens (15.1% supply) | GMX docs |
| Protocol revenue (annualized) | $8.83M to token holders; $23.86M total fees | defillama.com/protocol/gmx, Q2 2026 |
| P/Revenue | $68.21M market cap / $8.83M = **~7.7x** (to token holders); ~3x on total fees | defillama.com |

*Note: GMX experienced a $42M re-entrancy exploit in July 2025; $40M subsequently returned.*

---

## Lido Staked ETH (stETH / LDO)

| Parameter | Value | Source |
|---|---|---|
| stETH supply | ~9.2M ETH staked via Lido | lido.fi, datawallet.com |
| Lido market share | ~24–28% of all staked ETH | datawallet.com, everstake.one |
| stETH staking yield | 3.5–4% APY (real yield from ETH consensus rewards) | lido.fi, defillama.com |
| Lido protocol fee | 10% of staking rewards (split: 5% node operators, 5% DAO treasury) | lido.fi docs |
| LDO total supply | 1,000,000,000 LDO | lido.fi |
| LDO circulating | ~896M LDO (89.6%) | lido.fi, May 2026 |
| LDO inflation | ~0% (majority distributed; no ongoing emission) | — |
| Team / insider allocation | ~64% at launch (Lido DAO treasury + team + investors); most fully vested by now | Lido genesis allocation, training knowledge |
| Vesting | 1-year cliff, 1-year linear for founding team | Lido docs |
| LDO staking yield | None directly (LDO is governance token; fees go to treasury and node operators) | — |
| Governance | LDO token voting; **72-hour timelock** | lido.fi governance docs |
| Protocol revenue (annualized) | 10% of ~4% yield on ~9.2M ETH; at ETH ~$3,000 ≈ **~$110M/year** | lido.fi |
| P/Revenue | $1.88B LDO market cap / ~$110M = **~17x** | lido.fi, May 2026 |

---

## Comparison Table

| Parameter | BTC | ETH | UNI | CRV | GMX | stETH (LDO) |
|---|---|---|---|---|---|---|
| Annual inflation % | 0.82% | 0.18–0.23% (net) | ~0% (deflationary) | ~5.02% | ~0% | ~0% (LDO) |
| Team / insider % | 0% | ~17% (EF) | ~40% | ~17% | 1.9% | ~64% (launch) |
| Vesting duration | N/A | Informal | 4 years (complete) | 4 years | 2 years | 1yr cliff + 1yr |
| Staking yield | N/A | 3.5–4% | 0% (burns, no yield) | 5–10% (veCRV) | 5–12% (suspended) | 3.5–4% |
| Yield source | N/A | Real (consensus) | Real (fee burns) | Real (fees + bribes) | Real (protocol fees) | Real (ETH staking) |
| Governance timelock | N/A | N/A | 2 days | Not specified | Not specified | 72 hours |
| Treasury composition | None | Mixed (EF) | ~330M UNI | 10% of fees (new) | 10% of fees + reserve | 5% of yield |
| P/Revenue ratio | N/A | N/A | ~5–6x | N/A (distributed) | ~7.7x | ~17x |

---

## Notes and Caveats

- All figures are point-in-time; crypto protocol parameters change frequently.
- GMX staking is temporarily suspended pending $90 price trigger; yield history is real-yield precedent.
- UNI fee switch and burn mechanism activated December 28, 2025 — pre-switch comparisons may be in older sources.
- CRV DAO treasury allocation voted June 2025; prior to this, no treasury accumulation existed.
- ETH net inflation is highly sensitive to L1 transaction volume; can flip deflationary during high-activity periods.
- Lido team/insider allocation figure is from genesis and has been diluted by community distributions.
