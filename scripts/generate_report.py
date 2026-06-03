"""
Nazar — Report Chart Generator
Generates 3 matplotlib charts for the daily report:
  1. report_1_table.png  — Main comparison table
  2. report_2_creative.png — Creative/ad-level breakdown
  3. report_3_chart.png  — Bar chart comparison

Customize the data dicts (yesterday, day_before, creatives)
before running. Typically called from an agent pipeline.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os, warnings
warnings.filterwarnings('ignore')

# ── DATA ──────────────────────────────────────────────────
# Replace with your own data from the Meta API

yesterday = {
    'spend': 0, 'impressions': 0, 'reach': 0,
    'clicks': 0, 'link_clicks': 0, 'lpv': 0,
    'cpc': 0, 'cpm': 0, 'ctr': 0, 'cost_lpv': 0, 'lpv_rate': 0,
    'purchases': 0, 'purchase_value': 0, 'click_to_pur': 0,
    'roas': 0, 'cpa': 0
}

day_before = {
    'spend': 0, 'impressions': 0, 'reach': 0,
    'clicks': 0, 'link_clicks': 0, 'lpv': 0,
    'cpc': 0, 'cpm': 0, 'ctr': 0, 'cost_lpv': 0, 'lpv_rate': 0,
    'purchases': 0, 'purchase_value': 0, 'click_to_pur': 0,
    'roas': 0, 'cpa': 0
}

creatives_yesterday = []
creatives_db = []

# ── HELPERS ───────────────────────────────────────────────

def fmt_rp(v):
    if v == 0: return 'Rp0'
    if v >= 1_000_000: return f'Rp{v/1_000_000:.1f}M'
    if v >= 1_000: return f'Rp{v/1_000:.0f}K'
    return f'Rp{v:,.0f}'

def delta(new, old, lower_better=False):
    if old == 0:
        if new == 0: return '--', '#888'
        return '\u25b2 NEW', '#2ecc71'
    pct = (new - old) / old * 100
    if lower_better:
        if pct < -3: return f'\u25bc{abs(pct):.0f}%', '#2ecc71'
        elif pct > 3: return f'\u25b2+{pct:.0f}%', '#e74c3c'
        else: return f'{pct:+.0f}%', '#f39c12'
    else:
        if pct > 3: return f'\u25b2+{pct:.0f}%', '#2ecc71'
        elif pct < -3: return f'\u25bc{abs(pct):.0f}%', '#e74c3c'
        else: return f'{pct:+.0f}%', '#f39c12'

# ── STYLING ───────────────────────────────────────────────

DARK = '#0f1923'; BG1 = '#1a2736'; GREEN = '#2ecc71'
RED = '#e74c3c'; AMBER = '#f39c12'; TEXT = '#ecf0f1'
SUB = '#7f8c8d'; BLUE = '#3498db'

def generate_charts(yesterday, day_before, creatives_yesterday, creatives_db,
                    headline="", footnote="", date_range=""):
    """
    Generate all 3 report images.

    Args:
        yesterday, day_before: dicts with metric keys
        creatives_yesterday: list of dicts with keys:
            name, spend, cpc, ctr, lc, lpv, cost_lpv, pur, cpa, ctop
        creatives_db: same structure for comparison
        headline: top-line summary text
        footnote: bottom-of-chart note
        date_range: e.g. "27 Mei vs 28 Mei 2026"
    """

    # ── IMAGE 1: Main Table ───────────────────────────────
    fig1, (ax_h, ax_t) = plt.subplots(2, 1, figsize=(10, 9), facecolor=DARK,
                                       gridspec_kw={'height_ratios': [0.25, 0.75]})
    ax_h.set_facecolor(DARK); ax_h.axis('off')
    ax_h.text(0.5, 0.85, 'Meta Ads  |  Your Account', fontsize=20, fontweight='bold', color=TEXT, ha='center')
    ax_h.text(0.5, 0.45, date_range, fontsize=11, color=SUB, ha='center')
    ax_h.text(0.5, 0.1, headline, fontsize=13, fontweight='bold', color=GREEN, ha='center')

    ax_t.set_facecolor(DARK); ax_t.axis('off')
    metrics = [
        ('Spend', 'spend', False), ('Impressions', 'impressions', False), ('Reach', 'reach', False),
        ('Clicks', 'clicks', False), ('Link Clicks', 'link_clicks', False), ('LP Views', 'lpv', False),
        ('CPC', 'cpc', True), ('CPM', 'cpm', True), ('CTR', 'ctr', False),
        ('Cost / LPV', 'cost_lpv', True), ('LP View Rate', 'lpv_rate', False),
        ('Purchase*', 'purchases', False), ('Purchase Value', 'purchase_value', False),
        ('Click \u2192 Purchase', 'click_to_pur', False), ('ROAS (est.)', 'roas', False), ('CPA (est.)', 'cpa', True),
    ]
    col_w = [0.28, 0.24, 0.24, 0.14]
    n = len(metrics); rh = 0.90 / (n + 1.2)

    for j, (lbl, w) in enumerate(zip(['Metric', 'Day Before', 'Yesterday', '\u0394'], col_w)):
        ax_t.text(sum(col_w[:j]) + w/2, 0.98, lbl, fontsize=11, fontweight='bold', color=SUB, ha='center', va='center')

    for i, (label, key, lb) in enumerate(metrics):
        y_pos = 0.98 - (i + 1) * rh
        bg = BG1 if i % 2 == 0 else DARK
        rect = mpatches.FancyBboxPatch((0.01, y_pos - rh*0.4), 0.88, rh*0.8,
                                        boxstyle="round,pad=0.02", facecolor=bg, edgecolor='none')
        ax_t.add_patch(rect)
        dv, yv = day_before[key], yesterday[key]
        d, dc = delta(yv, dv, lb)
        if key in ('spend', 'cpc', 'cpm', 'cost_lpv', 'cpa', 'purchase_value'):
            ds, ys = fmt_rp(dv), fmt_rp(yv)
        elif key in ('impressions', 'reach', 'clicks', 'link_clicks', 'lpv'):
            ds, ys = f'{dv:,}', f'{yv:,}'
        elif key == 'purchases': ds, ys = f'{dv}', f'{yv}'
        elif key == 'ctr': ds, ys = f'{dv:.2f}%', f'{yv:.2f}%'
        elif key in ('lpv_rate', 'click_to_pur'): ds, ys = f'{dv:.1f}%', f'{yv:.1f}%'
        elif key == 'roas': ds, ys = f'{dv:.2f}x', f'{yv:.2f}x'
        else: ds, ys = str(dv), str(yv)
        is_key = key in ('purchases', 'roas', 'cpa')
        val_color, val_w = (dc, 'bold') if is_key else (TEXT, 'normal')
        ax_t.text(0.03, y_pos, label, fontsize=12, color=TEXT, ha='left', va='center')
        ax_t.text(sum(col_w[:1]) + col_w[1]/2, y_pos, ds, color=TEXT, fontsize=12, ha='center', va='center')
        ax_t.text(sum(col_w[:2]) + col_w[2]/2, y_pos, ys, color=val_color, fontweight=val_w, fontsize=12, ha='center', va='center')
        ax_t.text(sum(col_w[:3]) + col_w[3]/2, y_pos, d, color=dc, fontweight='bold', fontsize=12, ha='center', va='center')

    ax_t.text(0.03, 0.02, footnote, fontsize=9, color=AMBER, ha='left', va='center')
    path1 = 'report_1_table.png'
    fig1.savefig(path1, dpi=150, bbox_inches='tight', facecolor=DARK); plt.close(fig1)

    # ── IMAGE 2: Creative Breakdown ───────────────────────
    if creatives_yesterday:
        fig2 = plt.figure(figsize=(10, 6.5), facecolor=DARK)
        ax_c = fig2.add_axes([0.05, 0.08, 0.9, 0.88])
        ax_c.set_facecolor(DARK); ax_c.axis('off')
        ax_c.text(0.01, 0.96, 'Creative Breakdown', fontsize=14, fontweight='bold', color=TEXT)
        ax_c.text(0.01, 0.90, '  vs previous day (small gray) | Pur* = includes pending', fontsize=9, color=SUB)

        clabels = ['Creative', 'Spend', 'CPC', 'CTR', 'Link\u2192LPV', 'Cost/LPV', 'Pur*', 'CPA', 'C\u2192P']
        cw = [0.22, 0.10, 0.08, 0.07, 0.10, 0.09, 0.05, 0.10, 0.07]

        for j, (lbl, w) in enumerate(zip(clabels, cw)):
            ax_c.text(sum(cw[:j]) + w/2, 0.83, lbl, fontsize=8, fontweight='bold', color=SUB, ha='center', va='center')

        for i, c in enumerate(creatives_yesterday):
            y = 0.83 - (i + 1) * 0.12
            bg = BG1 if i % 2 == 0 else DARK
            rect = mpatches.FancyBboxPatch((0.01, y-0.05), 0.88, 0.10,
                                            boxstyle="round,pad=0.02", facecolor=bg, edgecolor='none')
            ax_c.add_patch(rect)
            lpv_info = f'{c["lc"]}\u2192{c["lpv"]}'
            vals = [c['name'], fmt_rp(c['spend']), fmt_rp(c['cpc']), f"{c['ctr']:.2f}%",
                    lpv_info, fmt_rp(c['cost_lpv']), str(c['pur']), fmt_rp(c['cpa']), f"{c['ctop']:.1f}%"]
            for j, (val, w) in enumerate(zip(vals, cw)):
                x = sum(cw[:j]) + w/2
                if j == 0:
                    clr = GREEN if c['pur'] > 0 else RED
                    ax_c.text(0.03, y, val, fontsize=10, color=clr, ha='left', va='center', fontweight='bold')
                elif j == 6:
                    clr = GREEN if c['pur'] > 0 else RED
                    ax_c.text(x, y, val, fontsize=10, color=clr, ha='center', va='center', fontweight='bold')
                else:
                    ax_c.text(x, y, val, fontsize=10, color=TEXT, ha='center', va='center')

        for i, c in enumerate(creatives_db):
            y = 0.83 - (len(creatives_yesterday) + i + 1.8) * 0.12
            lpv_info = f'{c["lc"]}\u2192{c["lpv"]}'
            vals = [c['name'], fmt_rp(c['spend']), fmt_rp(c['cpc']), f"{c['ctr']:.2f}%",
                    lpv_info, fmt_rp(c['cost_lpv']), str(c['pur']), fmt_rp(c['cpa']), f"{c['ctop']:.1f}%"]
            for j, (val, w) in enumerate(zip(vals, cw)):
                x = sum(cw[:j]) + w/2
                ax_c.text(x if j > 0 else 0.03, y, val, fontsize=8, color=SUB,
                          ha='left' if j == 0 else 'center', va='center')

        path2 = 'report_2_creative.png'
        fig2.savefig(path2, dpi=150, bbox_inches='tight', facecolor=DARK); plt.close(fig2)
    else:
        path2 = None

    # ── IMAGE 3: Bar Chart ────────────────────────────────
    fig3, ax_b = plt.subplots(figsize=(10, 5.5), facecolor=DARK)
    ax_b.set_facecolor(DARK)
    bar_labels = ['Purchase*', 'ROAS', 'CPA\n(est)', 'CPC', 'Cost / LPV', 'CTR']
    yv = [day_before['purchases'], day_before['roas'], day_before['cpa'],
          day_before['cpc'], day_before['cost_lpv'], day_before['ctr']]
    dv = [yesterday['purchases'], yesterday['roas'], yesterday['cpa'],
          yesterday['cpc'], yesterday['cost_lpv'], yesterday['ctr']]

    x = np.arange(len(bar_labels)); w = 0.35
    ax_b.bar(x - w/2, yv, w, color=BLUE, alpha=0.6, label='Day Before', zorder=3)
    b2 = ax_b.bar(x + w/2, dv, w, color=GREEN, alpha=0.85, label='Yesterday', zorder=3)

    ax_b.set_xticks(x); ax_b.set_xticklabels(bar_labels, fontsize=12, color=SUB)
    ax_b.tick_params(colors=SUB, labelsize=11)
    for sp in ['bottom', 'left']: ax_b.spines[sp].set_color('#2c3e50')
    for sp in ['top', 'right']: ax_b.spines[sp].set_visible(False)
    ax_b.grid(axis='y', alpha=0.12, color=TEXT)

    for bar, val in zip(b2, dv):
        if val > 0:
            lbl = f'{val/1000:.0f}K' if val >= 1000 else f'{val:.1f}'
            ax_b.text(bar.get_x() + bar.get_width()/2,
                      bar.get_height() + max(max(yv), max(dv)) * 0.04,
                      lbl, ha='center', fontsize=10, color=GREEN, fontweight='bold')

    ax_b.legend(fontsize=11, loc='upper right', facecolor=BG1, edgecolor='#2c3e50', labelcolor=TEXT)
    ax_b.set_title('Performance Comparison', fontsize=16, color=TEXT, fontweight='bold', pad=15)

    path3 = 'report_3_chart.png'
    fig3.savefig(path3, dpi=150, bbox_inches='tight', facecolor=DARK); plt.close(fig3)

    print(f"Generated: {path1}, {path2 or 'N/A'}, {path3}")


if __name__ == '__main__':
    generate_charts(
        yesterday, day_before, creatives_yesterday, creatives_db,
        headline="⬆ Customize this data before running",
        footnote="",
        date_range=""
    )
