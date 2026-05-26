# Token Audit Report: {{token.name}} ({{token.symbol}})

**Date:** {{date}}
**Audit Grade:** {{grade}}  <!-- A / B / C / D / F -->
**Archetypes:** {{token.archetypes}}
**Chain:** {{token.chain}}
**Stage:** {{token.launch_stage}}

---

## Executive Summary

<!-- 3-5 sentences. Overall assessment, most critical finding, and one key strength.
     State the grade and justify it briefly. -->

**Overall Grade: {{grade}}**

| Severity | Count |
|---|---|
| Critical | {{count_critical}} |
| High | {{count_high}} |
| Medium | {{count_medium}} |
| Low | {{count_low}} |
| Informational | {{count_info}} |

---

## 1. Model Overview

<!-- Summarize the parsed TokenModel. Cover: what the protocol does, token utility,
     supply mechanics, distribution, and treasury. Keep to ~200 words. -->

### Supply Mechanics
<!-- Emission schedule, burn mechanism, total supply, initial circulating -->

### Distribution & Vesting
<!-- Allocation table with cliff/duration per category. Flag any unusual concentrations. -->

### Value Accrual
<!-- How does protocol revenue reach token holders? If it doesn't, say so explicitly. -->

---

## 2. Findings

<!-- List all findings in descending severity order.
     Format each as shown below. -->

---

### [CRITICAL-01] {{finding_title}}

**Severity:** Critical
**Category:** Supply / Demand / Incentives / Concentration / Game Theory

**Description:**
<!-- What the problem is and why it matters. -->

**Evidence:**
<!-- Which specific model parameters trigger this finding. -->

**Fix Proposal:**
<!-- Concrete, specific remediation. Not "consider improving X" — say exactly what to change. -->

---

### [HIGH-01] {{finding_title}}

**Severity:** High
**Category:** <!-- same categories -->

**Description:**

**Evidence:**

**Fix Proposal:**

---

<!-- Repeat pattern for all Medium, Low, and Informational findings.
     Medium and below do not require Fix Proposals but should include them when straightforward. -->

---

## 3. Simulation Results

<!-- One subsection per simulation run. Include the chart image path and key takeaways.
     Do not just describe what the chart shows — interpret it. -->

### 3.1 Emission Model
![Emission Chart](../analysis/{{token_slug}}/emission.png)

**Key findings:**
<!-- What does the supply curve reveal? When does inflation peak? When does sell pressure peak? -->

### 3.2 Staking Dynamics
<!-- Include if staking simulation was run -->
![Staking Chart](../analysis/{{token_slug}}/staking.png)

**Key findings:**

### 3.3 Token Velocity
<!-- Include if velocity simulation was run -->

### 3.4 Agent-Based Model
<!-- Include if agents simulation was run -->

### 3.5 Death Spiral Stress Test
<!-- Include if death_spiral simulation was run -->
**Conditions that trigger collapse:**
<!-- List the parameter thresholds at which the model breaks -->

### 3.6 Monte Carlo Scenarios
![Monte Carlo Chart](../analysis/{{token_slug}}/monte_carlo.png)

**P10 / P50 / P90 price at 3 years:** {{p10}} / {{p50}} / {{p90}}

---

## 4. System Dynamics Analysis

<!-- This section answers: how does the system behave, and under what conditions does it work?
     Draw from simulation outputs. Be specific — cite parameter values and chart data. -->

### 4.1 Equilibrium Conditions

<!-- What combination of parameters keeps the token system in a stable state?
     Identify the equilibrium ranges for key variables (staking rate, emission rate,
     token price, treasury balance). State explicitly:
     "The system is stable when [X]; it breaks when [Y]."
     If the model has no stable equilibrium under realistic conditions, say so. -->

### 4.2 Viable Operating Conditions

<!-- Under what macro and protocol-level conditions does this model perform well?
     - Bull case: what growth trajectory validates the model's assumptions?
     - Base case: what "good enough" steady state keeps the protocol solvent?
     - Bear case: what conditions can the model survive, and for how long?
     What external factors (market price, adoption rate, competitor actions, macro) 
     have the most influence on outcomes? -->

### 4.3 Parameter Sensitivity

<!-- Which design parameters have the highest leverage on outcomes?
     E.g.: "A 2% increase in emission rate reduces treasury runway from 18 to 11 months."
     Identify the levers the team controls and their relative effect sizes.
     Flag parameters where small changes produce disproportionate outcomes. -->

### 4.4 Sustainability Requirements

<!-- What does the protocol need to achieve to stay within the viable operating range?
     State concrete, measurable milestones:
     - Revenue targets (monthly protocol revenue floor)
     - Staking rate floor (below which APY reflexivity destabilizes)
     - Treasury minimums (runway floor under bear conditions)
     - Governance participation thresholds
     - Adoption / TVL / volume milestones that change the model's viability
     These are not recommendations — they are conditions derived from the simulations. -->

---

## 5. Benchmarks

<!-- Compare key metrics against 2-3 comparable protocols. Use a table where possible. -->

| Metric | {{token.symbol}} | {{comparable_1}} | {{comparable_2}} |
|---|---|---|---|
| Team allocation % | | | |
| Team vesting (cliff / total) | | | |
| Inflation rate Y1 | | | |
| Staking yield source | | | |
| Governance timelock | | | |
| Treasury runway (months) | | | |

**Key differences:**
<!-- What does this model do better or worse than its comparables? -->

---

## 6. Recommendations

<!-- Synthesis of findings and system dynamics analysis into a prioritized action plan.
     Three tiers: fix what's broken, optimize for viability, monitor what matters. -->

### 6.1 Critical Fixes
<!-- Address Critical and High findings first. Be specific: name the parameter, the mechanism, the exact change. -->

1. **[Critical]** {{recommendation}}
2. **[High]** {{recommendation}}

### 6.2 Optimization Roadmap
<!-- Beyond fixing findings: design changes that most improve long-term viability,
     derived from the system dynamics analysis. These may not be "findings" per se
     but are meaningful improvements to sustainability and equilibrium stability.
     Rank by impact on the viability conditions identified in Section 4.4. -->

1. {{optimization}}
2. {{optimization}}

### 6.3 Monitoring Indicators
<!-- What should the team track on an ongoing basis to know if the model is staying on track?
     For each indicator: state the metric, the healthy range, and what action to take if it drifts.
     E.g.: "Staking rate — healthy: 30–60%. Below 30%: APY reflexivity risk, consider emission reduction." -->

| Indicator | Healthy Range | Warning Signal | Action |
|---|---|---|---|
| {{metric}} | {{range}} | {{threshold}} | {{action}} |

---

## 7. Appendix

### A. Parsed TokenModel
<!-- Embed or link the full models/<token-slug>.yaml -->

### B. Simulation Parameters
<!-- Key parameters used across simulations: time horizon, initial price, initial supply, scenarios -->

### C. Assumptions & Limitations
<!-- What could not be determined from the description, what was assumed, what this audit does not cover -->
