"""
EpiClock v4.0 - Figure 1: Epigenetic Clock Performance Comparison
Professional Publication-Ready Visualization for Q1 Academic Journals
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

# UNODC Color Palette
UNODC_PRIMARY = '#0050A0'
UNODC_SECONDARY = '#003366'
UNODC_ACCENT = '#00A7D8'

# Clock-specific colors
COLORS = {
    'Horvath': '#E53935',
    'Hannum': '#FB8C00', 
    'PhenoAge': '#7CB342',
    'GrimAge': '#00ACC1',
    'DunedinPACE': '#5E35B1',
    'Ensemble': UNODC_PRIMARY
}

# Data from Table 6
clocks = ['Horvath', 'Hannum', 'PhenoAge', 'GrimAge', 'DunedinPACE', 'Ensemble']
mae = [3.6, 3.8, 3.1, 2.4, 2.7, 2.1]
mae_ci_lower = [3.3, 3.5, 2.8, 2.2, 2.4, 1.9]
mae_ci_upper = [3.9, 4.1, 3.4, 2.6, 3.0, 2.3]
r2 = [0.91, 0.89, 0.92, 0.94, 0.93, 0.96]
rmse = [4.8, 5.1, 4.2, 3.2, 3.6, 2.8]

# Calculate errors
mae_errors = np.array([[mae[i] - mae_ci_lower[i] for i in range(len(mae))],
                       [mae_ci_upper[i] - mae[i] for i in range(len(mae))]])

colors = [COLORS[c] for c in clocks]

# Create figure with 2x2 layout
fig = plt.figure(figsize=(16, 12), facecolor='white')
gs = fig.add_gridspec(2, 2, hspace=0.35, wspace=0.3)

# === PANEL A: MAE Bar Chart ===
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_facecolor('#FAFAFA')

x_pos = np.arange(len(clocks))
bars = ax1.bar(x_pos, mae, width=0.7, color=colors, edgecolor='white', linewidth=2, alpha=0.9)
ax1.errorbar(x_pos, mae, yerr=mae_errors, fmt='none', ecolor='#333333', 
             elinewidth=2, capsize=6, capthick=2)

# Value labels
for i, (bar, val) in enumerate(zip(bars, mae)):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.25,
             f'{val}', ha='center', va='bottom', fontsize=12, fontweight='bold', color=colors[i])

ax1.set_ylabel('Mean Absolute Error (years)', fontsize=12, fontweight='bold', color=UNODC_SECONDARY)
ax1.set_xticks(x_pos)
ax1.set_xticklabels(clocks, fontsize=11, rotation=15, ha='right')
ax1.set_ylim(0, 5)
ax1.set_title('A. Prediction Accuracy (MAE)', fontsize=14, fontweight='bold', 
              color=UNODC_PRIMARY, loc='left', pad=10)

# Best performer highlight
ax1.axhline(y=2.1, color=UNODC_PRIMARY, linestyle='--', linewidth=1.5, alpha=0.5)
ax1.text(5.5, 2.3, 'Best: 2.1 yr', fontsize=9, color=UNODC_PRIMARY, ha='right')

ax1.yaxis.grid(True, linestyle='--', alpha=0.3)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# === PANEL B: R² Comparison ===
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_facecolor('#FAFAFA')

bars2 = ax2.barh(x_pos, r2, height=0.6, color=colors, edgecolor='white', linewidth=2, alpha=0.9)

for i, (bar, val) in enumerate(zip(bars2, r2)):
    ax2.text(val + 0.01, bar.get_y() + bar.get_height()/2,
             f'{val:.2f}', ha='left', va='center', fontsize=11, fontweight='bold', color=colors[i])

ax2.set_xlabel('Coefficient of Determination (R²)', fontsize=12, fontweight='bold', color=UNODC_SECONDARY)
ax2.set_yticks(x_pos)
ax2.set_yticklabels(clocks, fontsize=11)
ax2.set_xlim(0.85, 1.0)
ax2.set_title('B. Variance Explained (R²)', fontsize=14, fontweight='bold',
              color=UNODC_PRIMARY, loc='left', pad=10)

# Reference line
ax2.axvline(x=0.95, color='#2E7D32', linestyle='--', linewidth=1.5, alpha=0.5)
ax2.text(0.951, 5.5, 'Excellent (>0.95)', fontsize=9, color='#2E7D32', rotation=90, va='top')

ax2.xaxis.grid(True, linestyle='--', alpha=0.3)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

# === PANEL C: RMSE Lollipop Chart ===
ax3 = fig.add_subplot(gs[1, 0])
ax3.set_facecolor('#FAFAFA')

# Lollipop chart
for i, (clock, r, color) in enumerate(zip(clocks, rmse, colors)):
    ax3.hlines(y=i, xmin=0, xmax=r, color=color, linewidth=3, alpha=0.7)
    ax3.scatter(r, i, s=200, color=color, edgecolor='white', linewidth=2, zorder=10)
    ax3.text(r + 0.15, i, f'{r}', va='center', fontsize=11, fontweight='bold', color=color)

ax3.set_yticks(range(len(clocks)))
ax3.set_yticklabels(clocks, fontsize=11)
ax3.set_xlabel('Root Mean Square Error (years)', fontsize=12, fontweight='bold', color=UNODC_SECONDARY)
ax3.set_xlim(0, 6)
ax3.set_title('C. Prediction Error (RMSE)', fontsize=14, fontweight='bold',
              color=UNODC_PRIMARY, loc='left', pad=10)

ax3.xaxis.grid(True, linestyle='--', alpha=0.3)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)

# === PANEL D: Radar Chart ===
ax4 = fig.add_subplot(gs[1, 1], projection='polar')

# Normalize metrics for radar (invert MAE and RMSE so higher is better)
mae_norm = [1 - (m - 2) / 2 for m in mae]  # Normalize: lower MAE = higher score
r2_norm = [(r - 0.88) / 0.08 for r in r2]  # Normalize to 0-1
rmse_norm = [1 - (r - 2.5) / 3 for r in rmse]  # Normalize: lower RMSE = higher score

# Radar setup
categories = ['Accuracy\n(1/MAE)', 'Variance\nExplained', 'Precision\n(1/RMSE)']
N = len(categories)
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]

# Plot each clock
for i, clock in enumerate(clocks):
    values = [mae_norm[i], r2_norm[i], rmse_norm[i]]
    values += values[:1]
    ax4.plot(angles, values, 'o-', linewidth=2, color=colors[i], label=clock, alpha=0.8)
    ax4.fill(angles, values, alpha=0.1, color=colors[i])

ax4.set_xticks(angles[:-1])
ax4.set_xticklabels(categories, fontsize=10, fontweight='bold')
ax4.set_ylim(0, 1)
ax4.set_title('D. Multi-Metric Performance Profile', fontsize=14, fontweight='bold',
              color=UNODC_PRIMARY, pad=20)
ax4.legend(loc='lower left', bbox_to_anchor=(-0.3, -0.15), ncol=3, fontsize=9)

# Main title
fig.suptitle('Figure 1. Epigenetic Clock Performance Comparison',
             fontsize=18, fontweight='bold', color=UNODC_PRIMARY, y=0.98)
fig.text(0.5, 0.94, '10-fold Cross-Validation Results | n=10,542 methylation profiles',
         ha='center', fontsize=12, style='italic', color='#666666')

# Footer
fig.text(0.5, 0.02, 
         'MAE: Mean Absolute Error; RMSE: Root Mean Square Error; R²: Coefficient of Determination. '
         'Error bars represent 95% confidence intervals.',
         ha='center', fontsize=9, style='italic', color='#666666')

plt.tight_layout(rect=[0, 0.04, 1, 0.92])

# Save
plt.savefig('figures/figure_1_clock_performance.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('figures/figure_1_clock_performance.pdf', bbox_inches='tight', facecolor='white')
print("Figure 1 saved successfully!")
