"""
death_spiral.py — Collapse stress test
tokenomics-analyzer | Phase 3.2 core script

Runs three stress scenarios and tracks all 10 death spiral conditions
(from failure_postmortems.md) at each month. Records the month each
condition first activates per scenario.

Scenarios:
  1. Standard Bear  — price declines -80% over 6 months, then flat
  2. Flash Crash    — -90% price shock at month 1, slow recovery
  3. Revenue Collapse — revenue drops to $0 at month 6, stays there

Collapse detection: sell_pressure > buy_pressure for 3 consecutive months
→ triggers a one-tier grade downgrade per scoring_rubric.md (Standard Bear only).

Run:
  python death_spiral.py <token_slug> [--model models/<token_slug>.yaml]

Outputs (to analysis/<token_slug>/):
  stress_triggers.png    — timeline of condition activation per scenario
  runway.png             — treasury balance + months remaining
  death_spiral_data.csv  — full monthly state per scenario
"""

import sys
import argparse
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from utils import load_params, log_params, fmt_tokens


# ── Scenario price trajectories ───────────────────────────────────────────────

def price_path(scenario, initial_price, n_steps):
    """Return array of token prices over n_steps months."""
    prices = np.zeros(n_steps)
    prices[0] = initial_price

    if scenario == 'standard_bear':
        # -80% over 6 months (linear monthly drop), then flat
        monthly_drop = 0.80 / 6
        for t in range(1, n_steps):
            if t <= 6:
                prices[t] = prices[t - 1] * (1 - monthly_drop)
            else:
                prices[t] = prices[6]

    elif scenario == 'flash_crash':
        # -90% in month 1, then 2% monthly recovery (slow)
        prices[1] = initial_price * 0.10
        for t in range(2, n_steps):
            prices[t] = min(prices[t - 1] * 1.02, initial_price)

    elif scenario == 'revenue_collapse':
        # No price shock — price follows mild bear (-20% total over 12m, then flat)
        for t in range(1, n_steps):
            if t <= 12:
                prices[t] = prices[t - 1] * (1 - 20 / 100 / 12)
            else:
                prices[t] = prices[12]

    return prices


def revenue_path(scenario, monthly_revenue_base, n_steps):
    """Return array of monthly protocol revenue in USD."""
    revenue = np.zeros(n_steps)
    for t in range(n_steps):
        if scenario == 'revenue_collapse' and t >= 6:
            revenue[t] = 0.0
        else:
            revenue[t] = monthly_revenue_base
    return revenue


# ── Death spiral condition checks ─────────────────────────────────────────────
# Each check returns True if the condition is triggered at this month.

def check_conditions(t, state, params):
    """
    Evaluate all 10 death spiral conditions for a given month's state.
    Returns dict of {condition_num: bool}.

    Conditions from failure_postmortems.md:
    1  Collateral is endogenous
    2  Backing MC < outstanding liability MC
    3  Yield is subsidized, not earned
    4  APY > 50% + treasury runway < 1yr
    5  Peg deviation > 1% for > 24h  (non-stablecoin: always False)
    6  Treasury runway < 60 days
    7  No mint/burn rate limiter
    8  Protocol liquidity < 10% of supply
    9  Top-10 holders > 40% of collateral
    10 Demand driver is single internal yield product
    """
    p = params
    price = state['price']
    treasury = state['treasury_usd']
    monthly_burn = state['monthly_burn_usd']
    staking_rate = state['staking_rate']
    total_supply = p['total_supply']
    circulating = total_supply * (1 - staking_rate)
    revenue = state['monthly_revenue_usd']

    # Annualized staking APY: emission / (staked supply * price)
    annual_emission_usd = (
        (p.get('emission_rate_annual_pct') or 0) / 100 * total_supply * price
    )
    staked_value_usd = total_supply * staking_rate * price
    apy = (annual_emission_usd / staked_value_usd) if staked_value_usd > 0 else 0

    # Real yield fraction: how much of staking reward is covered by revenue
    annual_revenue_usd = revenue * 12
    subsidy_fraction = max(0, 1 - annual_revenue_usd / max(annual_emission_usd, 1))

    # Treasury runway in months
    net_burn = max(0.01, monthly_burn - revenue)
    runway_months = treasury / net_burn if net_burn > 0 else 999

    # Protocol liquidity estimate: treasury holds some as liquid tokens
    # Proxy: liquid_pct * treasury_token_value / circulating_supply_value
    liquid_pct = p.get('treasury_liquid_pct', 0.30)
    treasury_token_value = (p.get('treasury_usd') or 0) * liquid_pct
    circulating_value = circulating * price
    liquidity_ratio = (treasury_token_value / circulating_value) if circulating_value > 0 else 0

    return {
        1: (p.get('endogenous_collateral_pct', 0) or 0) > 0,
        2: False,  # requires outstanding liability data; set False if unknown
        3: subsidy_fraction > 0.30,
        4: apy > 0.50 and runway_months < 12,
        5: False,  # peg deviation — only relevant for stablecoins
        6: runway_months < 2,   # < 60 days ≈ < 2 months
        7: not p.get('has_mint_burn_rate_limiter', False),
        8: liquidity_ratio < 0.10,
        9: (p.get('top10_holder_pct', 0) or 0) > 0.40,
        10: (p.get('single_yield_source_pct', 0) or 0) > 0.60,
    }


# ── Simulation loop ────────────────────────────────────────────────────────────

def run_simulation(params, n_steps=120):
    """
    Run the three stress scenarios.
    Returns dict scenario → {state arrays, condition_first_trigger, collapse_month}.
    """
    p = params
    total = p['total_supply']
    initial_price = p['initial_price_usd']
    initial_treasury = p.get('treasury_usd') or 0
    monthly_burn = p.get('monthly_burn_usd') or 0
    monthly_revenue_base = (p.get('annual_revenue_usd') or 0) / 12

    results = {}
    scenarios = ['standard_bear', 'flash_crash', 'revenue_collapse']

    for scen in scenarios:
        prices = price_path(scen, initial_price, n_steps)
        revenues = revenue_path(scen, monthly_revenue_base, n_steps)

        # State arrays
        treasury = np.zeros(n_steps)
        staking_rate_arr = np.zeros(n_steps)
        sell_pressure_arr = np.zeros(n_steps)
        buy_pressure_arr = np.zeros(n_steps)
        runway_arr = np.zeros(n_steps)

        treasury[0] = initial_treasury
        staking_rate_arr[0] = p['initial_staking_rate']

        # Condition trigger months: -1 = never triggered
        condition_first = {i: -1 for i in range(1, 11)}

        # Collapse detection state
        consecutive_net_sell = 0
        collapse_month = -1

        for t in range(1, n_steps):
            price = prices[t]
            price_prev = prices[t - 1]
            price_30d_return = (price - price_prev) / max(price_prev, 1e-9)
            revenue = revenues[t]

            # Staking rate: equilibrate toward scenario target
            if scen == 'standard_bear':
                target_staking = max(0.05, p['initial_staking_rate'] - 0.40)
                speed = 0.05
            elif scen == 'flash_crash':
                target_staking = max(0.02, p['initial_staking_rate'] - 0.60)
                speed = 0.10
            else:
                target_staking = p['initial_staking_rate'] * 0.80
                speed = 0.02

            staking_rate = np.clip(
                staking_rate_arr[t - 1] + speed * (target_staking - staking_rate_arr[t - 1]),
                0.0, 0.95
            )
            # Mass unstaking trigger
            if price_30d_return < -0.40:
                staking_rate = max(0.0, staking_rate - 0.15)

            staking_rate_arr[t] = staking_rate

            # Treasury update
            net_flow = revenue - monthly_burn
            treasury[t] = max(0.0, treasury[t - 1] + net_flow)

            net_burn = max(0.01, monthly_burn - revenue)
            runway_arr[t] = treasury[t] / net_burn if net_burn > 0 else 999

            # Sell / buy pressure (normalized 0–1 proxies)
            # Sell: token inflation + unstaking pressure + price decline momentum
            emission_monthly = (p.get('emission_rate_annual_pct') or 0) / 100 / 12
            unstaking_pressure = max(0, staking_rate_arr[t - 1] - staking_rate) * total * price
            inflation_pressure = emission_monthly * total * price
            momentum_sell = max(0, -price_30d_return) * 0.5
            sell = (unstaking_pressure + inflation_pressure) / max(total * price, 1) + momentum_sell

            # Buy: protocol revenue demand + staking incentive pull
            apy_est = (
                (p.get('emission_rate_annual_pct') or 0) / 100 * total * price
                / max(total * staking_rate * price, 1)
            )
            buy = (revenue / max(total * price, 1)) + max(0, apy_est - p['opportunity_cost']) * 0.1

            sell_pressure_arr[t] = min(sell, 1.0)
            buy_pressure_arr[t] = min(buy, 1.0)

            # Collapse detection
            if sell > buy:
                consecutive_net_sell += 1
                if consecutive_net_sell >= 3 and collapse_month == -1:
                    collapse_month = t
            else:
                consecutive_net_sell = 0

            # Check conditions
            state = {
                'price': price,
                'treasury_usd': treasury[t],
                'monthly_burn_usd': monthly_burn,
                'staking_rate': staking_rate,
                'monthly_revenue_usd': revenue,
            }
            triggered = check_conditions(t, state, p)
            for cond_num, is_triggered in triggered.items():
                if is_triggered and condition_first[cond_num] == -1:
                    condition_first[cond_num] = t

        results[scen] = {
            'prices': prices,
            'revenues': revenues,
            'treasury': treasury,
            'staking_rate': staking_rate_arr,
            'sell_pressure': sell_pressure_arr,
            'buy_pressure': buy_pressure_arr,
            'runway': runway_arr,
            'condition_first': condition_first,
            'collapse_month': collapse_month,
        }

    return results


# ── Output ─────────────────────────────────────────────────────────────────────

CONDITION_LABELS = {
    1: 'Endogenous collateral',
    2: 'Backing MC < liability MC',
    3: 'Yield subsidized (>30%)',
    4: 'APY>50% + runway<12m',
    5: 'Peg deviation (stablecoin)',
    6: 'Treasury runway <60d',
    7: 'No mint/burn rate limiter',
    8: 'Protocol liquidity <10%',
    9: 'Top-10 holders >40%',
    10: 'Demand: single yield source',
}

SCENARIO_CONFIG = {
    'standard_bear':    {'label': 'Standard Bear (−80% / 6m)', 'color': '#dc2626'},
    'flash_crash':      {'label': 'Flash Crash (−90% m1)',      'color': '#7c3aed'},
    'revenue_collapse': {'label': 'Revenue Collapse (m6)',       'color': '#ea580c'},
}


def save_outputs(results, params, output_dir, token_slug):
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    name = params.get('token_name', token_slug)
    symbol = params.get('token_symbol', token_slug.upper())
    n_steps = len(results['standard_bear']['prices'])
    months = np.arange(n_steps)

    # ── stress_triggers.png ────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(14, 7))
    fig.suptitle(f'{name} ({symbol}) — Death Spiral Trigger Timeline',
                 fontsize=13, fontweight='bold')

    n_conditions = 10
    scen_names = list(SCENARIO_CONFIG.keys())
    row_height = 0.25
    y_positions = {cond: (n_conditions - cond) for cond in range(1, n_conditions + 1)}

    for scen_idx, scen in enumerate(scen_names):
        cfg = SCENARIO_CONFIG[scen]
        r = results[scen]
        offset = (scen_idx - 1) * row_height

        for cond_num in range(1, n_conditions + 1):
            first_month = r['condition_first'][cond_num]
            y = y_positions[cond_num] + offset

            if first_month == -1:
                # Never triggered — draw light gray dash
                ax.plot([0, n_steps - 1], [y, y], color='#e5e7eb', linewidth=0.8, zorder=1)
            else:
                # Draw line up to trigger, then mark trigger
                ax.plot([0, first_month], [y, y], color=cfg['color'],
                        linewidth=2.0, alpha=0.5, zorder=2)
                ax.plot(first_month, y, 's', color=cfg['color'],
                        markersize=8, zorder=3, label=None)
                ax.annotate(f'm{first_month}', xy=(first_month, y),
                            xytext=(4, 0), textcoords='offset points',
                            fontsize=7, color=cfg['color'], va='center')

        # Collapse month marker
        cm = r['collapse_month']
        if cm != -1:
            ax.axvline(cm, color=cfg['color'], linestyle='--', linewidth=1.2,
                       alpha=0.7, label=f'{cfg["label"]} collapse m{cm}')

    # Y-axis labels
    ax.set_yticks([y_positions[c] for c in range(1, n_conditions + 1)])
    ax.set_yticklabels([f'C{c}: {CONDITION_LABELS[c]}' for c in range(1, n_conditions + 1)],
                       fontsize=9)
    ax.set_xlabel('Month', fontsize=10)
    ax.set_xlim(0, n_steps - 1)
    ax.set_ylim(-1, n_conditions + 0.5)
    ax.grid(axis='x', alpha=0.3)

    # Legend patches for scenarios
    patches = [mpatches.Patch(color=SCENARIO_CONFIG[s]['color'],
                               label=SCENARIO_CONFIG[s]['label']) for s in scen_names]
    ax.legend(handles=patches, loc='lower right', fontsize=8)

    plt.tight_layout()
    plt.savefig(out / 'stress_triggers.png', dpi=100, bbox_inches='tight')
    plt.close()
    print('  stress_triggers.png')

    # ── runway.png ─────────────────────────────────────────────────────────────
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    fig.suptitle(f'{name} ({symbol}) — Treasury Runway Under Stress', fontsize=13, fontweight='bold')

    for scen, cfg in SCENARIO_CONFIG.items():
        r = results[scen]
        ax1.plot(months, r['treasury'] / 1e6, color=cfg['color'],
                 linewidth=2, label=cfg['label'])
        # Cap runway display at 60 months for readability
        runway_capped = np.minimum(r['runway'], 60)
        ax2.plot(months, runway_capped, color=cfg['color'], linewidth=2)

    ax1.set_ylabel('Treasury Balance (USD M)', fontsize=10)
    ax1.legend(fontsize=9)
    ax1.grid(alpha=0.3)
    ax1.set_ylim(bottom=0)

    ax2.axhline(12, color='#f59e0b', linestyle='--', linewidth=1.2, label='12m warning')
    ax2.axhline(2, color='#dc2626', linestyle='--', linewidth=1.2, label='60d critical')
    ax2.set_ylabel('Runway (months, capped at 60)', fontsize=10)
    ax2.set_xlabel('Month', fontsize=10)
    ax2.legend(fontsize=9)
    ax2.grid(alpha=0.3)
    ax2.set_ylim(bottom=0)
    ax2.set_xlim(0, n_steps - 1)

    plt.tight_layout()
    plt.savefig(out / 'runway.png', dpi=100, bbox_inches='tight')
    plt.close()
    print('  runway.png')

    # ── death_spiral_data.csv ──────────────────────────────────────────────────
    rows = []
    for scen in scen_names:
        r = results[scen]
        for t in range(n_steps):
            row = {
                'scenario': scen,
                'month': t,
                'price': round(float(r['prices'][t]), 6),
                'treasury_usd': round(float(r['treasury'][t]), 2),
                'runway_months': round(float(min(r['runway'][t], 999)), 2),
                'staking_rate': round(float(r['staking_rate'][t]), 4),
                'sell_pressure': round(float(r['sell_pressure'][t]), 4),
                'buy_pressure': round(float(r['buy_pressure'][t]), 4),
            }
            # Condition state at this month (re-derive from first-trigger data)
            for cond_num in range(1, 11):
                ft = r['condition_first'][cond_num]
                row[f'cond_{cond_num}'] = (ft != -1 and t >= ft)
            rows.append(row)
    pd.DataFrame(rows).to_csv(out / f'{token_slug}_death_spiral_data.csv', index=False)
    print(f'  {token_slug}_death_spiral_data.csv')

    # ── Summary ────────────────────────────────────────────────────────────────
    print(f'\n── Death Spiral Summary ─────────────────────────────────────────────')
    for scen, cfg in SCENARIO_CONFIG.items():
        r = results[scen]
        cm = r['collapse_month']
        triggered = [c for c, m in r['condition_first'].items() if m != -1]
        first_trigger = min((m for m in r['condition_first'].values() if m != -1), default=-1)
        print(f'  {cfg["label"]}')
        print(f'    Conditions triggered: {len(triggered)}/10  '
              f'(first: {"m" + str(first_trigger) if first_trigger != -1 else "none"})')
        print(f'    Collapse detected: {"month " + str(cm) if cm != -1 else "no collapse"}')
        if scen == 'standard_bear' and cm != -1:
            print(f'    ⚠  GRADE DOWNGRADE TRIGGER: death spiral under standard bear scenario')


# ── Entry point ────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Death spiral stress test — tokenomics-analyzer')
    parser.add_argument('token_slug', help='Token slug, e.g. nova-protocol')
    parser.add_argument('--model', help='Path to TokenModel YAML')
    args = parser.parse_args()

    slug = args.token_slug
    model_path = args.model or f'models/{slug}.yaml'

    print(f'\n── Loading parameters: {slug} ───────────────────────────────────────')
    params, sources = load_params(slug, model_path)
    log_params(params, sources)

    if not params.get('total_supply'):
        print('WARNING: total_supply unknown — using 1,000,000,000 as placeholder')
        params['total_supply'] = 1_000_000_000

    # Derive endogenous_collateral_pct from model if not already set
    # (set this field in the YAML for stablecoin tokens that use own token as collateral)
    if 'endogenous_collateral_pct' not in params:
        params['endogenous_collateral_pct'] = 0

    n_steps = int(params['n_steps'])
    print(f'\n── Running death spiral stress test ({n_steps} months × 3 scenarios) ──')
    results = run_simulation(params, n_steps=n_steps)

    output_dir = f'analysis/{slug}'
    print(f'── Saving outputs → {output_dir}/ ──────────────────────────────────')
    save_outputs(results, params, output_dir, slug)
    print(f'\nDone.\n')

    return results, params


if __name__ == '__main__':
    main()
