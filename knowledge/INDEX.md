# Knowledge Base Index

> **Authoritative source:** `AGENT_MANIFEST.md` (project root) contains the complete component inventory, dependency graph, and consistency invariants. This file is a human-readable quick reference for audit use. Keep it in sync with the manifest.

---

## File Descriptions

| File | Content |
|---|---|
| `token_archetypes.md` | Taxonomy of token types (currency, utility, governance, ve-token, dual-token, rebasing, real-yield, liquid-staking), value accrual formulas per archetype, failure modes, and classification decision tree |
| `failure_postmortems.md` | Key formulas, core principles, per-case warning signs, on-chain distress signals, and prevention changes for Terra/LUNA, Iron Finance, OHM, Anchor Protocol, and Basis Cash. 10-condition death spiral checklist. Mandatory design requirements. |
| `token_velocity.md` | MV=PQ framework, velocity trap patterns, sink mechanism effectiveness table, quantitative velocity benchmarks |
| `staking_dynamics.md` | Ethereum issuance formula, staking equilibrium model, reflexivity loop equations, inflationary Ponzi conditions, design levers |
| `governance_attacks.md` | Flash loan attack anatomy (Beanstalk), Tornado Cash trojan proposal, Build Finance DAO takeover, 22-item red flag checklist |
| `vetokens_and_emissions.md` | veCRV boost formula, Solidly/ve(3,3) failure analysis, Velodrome fixes, emission decay curve formulas, bribe market health thresholds |
| `treasury_design.md` | Runway formula, diversification benchmarks by protocol stage, POL mechanics, grant streaming math, minimum viable treasury thresholds |
| `scoring_rubric.md` | Grade A–F definitions with quantitative thresholds (finding counts, treasury runway, insider allocation, death spiral conditions). Grade F automatic disqualifiers. Scoring process. |
| `red_flags_master.md` | **Single source of truth for the weakness scanner.** 51 flags (8C/14H/14M/10L/5I) — each entry includes the trigger condition AND the YAML fields to inspect AND evaluation notes for borderline cases. Run top-to-bottom for every audit. |
| `simulation_baselines.md` | Default parameters for cadCAD and Mesa simulations: initial conditions, scenario definitions, Monte Carlo parameters, actor distributions, staking reflexivity loop, stress test thresholds, required chart outputs. |
| `reference_benchmarks.md` | Live benchmark data (retrieved 2026-05-25) for BTC, ETH, UNI, CRV, GMX, stETH/LDO. Refresh every 6 months via `/update-knowledge benchmarks`. |
| `failure_postmortems_2024.md` | Post-2024 incidents: Stream Finance/xUSD (Nov 2025), Compound governance capture (Jul 2024), token-treasury dependency collapse (2024–2026). New formulas, warning signs, prevention. Refresh every 6 months via `/update-knowledge incidents`. |
| `url_corrections.md` | Verified status of all URLs cited in knowledge files as of 2026-05-25. Re-verify via `/update-knowledge urls`. |
| `academic_citations.md` | Verified citations: Roughgarden EIP-1559, Ethereum consensus spec, Buterin governance posts, Samani token models, Pfeffer cryptoassets, flash loan governance paper. |
| `fee_economics.md` | Revenue taxonomy, Fee Coverage Ratio (FCR) formula, unit economics benchmarks (revenue/TVL, P/F ratio), value accrual mechanism patterns, fee distribution design patterns (GMX/Curve/MakerDAO), sustainability thresholds, and red flag patterns for fee-based tokens. |
| `worked_example.md` | **Quality calibration anchor.** Complete fictional audit (AgroFi/AGRO) with parsed YAML, all findings with evidence, death spiral count, grade assignment, executive summary. Load before writing any report. |

---

## Selective Loading Map

| Condition | Load |
|---|---|
| **Always (audit mode)** | `token_archetypes.md`, `failure_postmortems.md`, `red_flags_master.md`, `scoring_rubric.md` |
| Staking mechanism present | `staking_dynamics.md` |
| Governance / voting rights | `governance_attacks.md` |
| Emission schedule or inflationary supply | `vetokens_and_emissions.md` |
| Treasury described or mentioned | `treasury_design.md` |
| Utility / payment / fee token | `token_velocity.md` |
| ve-token / vote-escrow mechanics | `vetokens_and_emissions.md` + `governance_attacks.md` |
| Algorithmic stablecoin or rebasing token | `staking_dynamics.md` (postmortems already loaded) |
| Real-yield / fee-sharing token | `token_velocity.md` + `treasury_design.md` + `fee_economics.md` |
| Liquid staking token | `staking_dynamics.md` + `token_velocity.md` |
| 2024–2026 design patterns (yield products, leverage stablecoins) | `failure_postmortems_2024.md` |
| Running simulations (Step 5) | `simulation_baselines.md` |
| Benchmarking step | `reference_benchmarks.md` |
| Before writing any report | `worked_example.md` |
| Citing sources | `academic_citations.md`, `url_corrections.md` |
| **Maintenance mode only** | `AGENT_MANIFEST.md` (repo root — one level above `agent/`) |
