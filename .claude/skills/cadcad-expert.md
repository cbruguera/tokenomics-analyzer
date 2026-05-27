# Skill: cadcad-expert

**Layer:** 0 (Foundation — active during Step 5: Simulate)

**Purpose:** Governs simulation script generation and interpretation. Ensures simulations are correctly parameterized, produce the required chart outputs, and that their results are interpreted through the correct analytical lenses — not just reported as chart descriptions.

---

## Generation Protocol

Simulations are generated ad-hoc at runtime for each token. For every simulation step:

1. **Read the reference template** from `simulations/templates/<script>.py`
2. **Read the parsed TokenModel** YAML for this token
3. **Generate a token-specific script**: copy the template, substitute the token's parameters into `PARAMS`, adjust state update functions for any novel mechanisms
4. **Save** to `simulations/<token-slug>/<script>.py`
5. **Run** with `.venv/bin/python simulations/<token-slug>/<script>.py <token-slug> --model models/<token-slug>.yaml`
6. **Interpret** the outputs (see Interpretation section below)

The shared parameter loader (`simulations/utils.py`) handles YAML parsing and baseline defaults. Do not re-implement parameter loading in generated scripts.

---

## Parameter Override Priority

1. TokenModel YAML fields (highest — always use if available)
2. `knowledge/simulation_baselines.md` defaults (use when YAML field is `unknown`)
3. Script defaults (lowest — only if not in baselines)

Log the source of every parameter:
```python
print(f"initial_circulating: {PARAMS['initial_circulating']} (source: TokenModel)")
print(f"price_volatility: {PARAMS['price_volatility']} (source: simulation_baselines.md default)")
```

Required parameters — if unknown, raise before running:
```python
required = ['initial_circulating', 'total_supply', 'emission_rate_annual_pct']
for param in required:
    if param not in PARAMS or PARAMS[param] == 'unknown':
        raise ValueError(f"Required parameter '{param}' is unknown. Cannot run simulation.")
```

---

## Required Outputs

All charts: 1200×800px, saved as PNG, labeled axes with units, legend.

| Script | Output file | Must show |
|---|---|---|
| `emission.py` | `supply.png` | Total supply, circulating, staked, locked over 120 months |
| `emission.py` | `dilution.png` | Monthly new supply as % of circulating; flag months >5% |
| `monte_carlo.py` | `price_bands.png` | P10/P25/P50/P75/P90 price over 120 months |
| `staking.py` | `staking.png` | Staking rate %, APY, and unstaking events over time |
| `staking.py` | `runway.png` | Treasury runway in months over time |
| `death_spiral.py` | `stress_triggers.png` | Which death spiral conditions activate and at what month |

---

## Scenarios

Always run Base. Add Bear and Stress.

```python
SCENARIOS = {
    "base":   {"demand_growth_y1": 0.20, "demand_growth_y4plus": 0.10, "vol": 1.20},
    "bear":   {"demand_growth_y1": 0.00, "demand_growth_y2": -0.30, "demand_growth_y3": -0.50, "vol": 1.20},
    "stress": {"shock_month": 12, "shock_magnitude": -0.80, "vol": 1.20},
}
```

---

## Dilution Event Detection

Flag months where new supply > 5% of circulating:
```python
df['dilution_event'] = (df['new_supply_pct'] > 0.05)
dilution_months = df[df['dilution_event']].index.tolist()
if dilution_months:
    print(f"WARNING: Dilution events detected at months: {dilution_months}")
```
Mark these months with red vertical lines on the supply chart.

---

## Simulation Interpretation

Running simulations and producing charts is not the goal. Interpret outputs through these lenses before writing the report.

### emission.py

**supply.png — what to look for:**
- Circulating at launch < 10% with large locked categories = high future sell pressure risk
- When do major vesting cliffs hit? Team + investor cliffs coinciding in the same quarter = compounded sell pressure
- Circulating supply growing in sudden jumps vs. smoothly? Jumps = supply shocks at vesting events

**dilution.png — what to look for:**
- Count months above 5% threshold. A cluster in first 18 months = critical: market must absorb massive supply before organic demand has developed
- Max monthly dilution > 10% = structural design flaw regardless of timing

**Mechanism design interpretation:**
- High early dilution creates adverse selection: only speculators expecting to exit before the dilution will buy at launch. Long-term holders face guaranteed supply inflation. The incentive structure selects against the participants the protocol needs.
- Coincident team + investor cliffs create a predictable exit window that rational insiders will exploit.

### monte_carlo.py

**price_bands.png — what to look for:**
- P10–P90 gap = model uncertainty. Very wide band = highly sensitive to demand assumptions; projections unreliable in either direction
- P50 in Base declining toward zero within 36 months = model fundamentally unsound
- **The near-zero percentage is the single most important number**: what fraction of paths collapse by month 36? Above 20% in Base = critical risk. Above 50% in Bear = structural fragility.
- Compare Base vs. Bear vs. Stress P50 paths: a robust model shows a meaningful but survivable gap. A fragile model shows Bear P50 near zero while Base is healthy — this discontinuity means no resilience margin.

**Monetary theory interpretation:**
- If circulating supply grows 5× over 3 years but demand (TVL, users, revenue) doesn't grow proportionally, implied token price must fall ~5×. The Monte Carlo encodes the protocol's monetary policy.
- Combined reading: high dilution + high price uncertainty = near-certain value destruction in all but the most optimistic paths.

### sensitivity.py

**sensitivity_heatmap.png — what to look for:**
- Where is the current token's position relative to the viable zone (green contour)? Inside = has margin. Edge = small adverse changes trigger instability. Outside = already in danger zone.
- Which axis drives outcomes more? Steeper gradient = more sensitive to that parameter.

**equilibrium_map.png — what to look for:**
- What fraction of parameter space is viable? < 10% viable = protocol only works under a narrow set of conditions — high structural fragility.
- Is the viable zone centered near current parameters, or far away? Far = needs redesign, not tuning.

**Complex systems interpretation:**
- The boundary of the viable zone IS the phase transition boundary. Operating near it means small shocks can trigger qualitative state changes — the defining feature of systems vulnerable to rapid collapse.
