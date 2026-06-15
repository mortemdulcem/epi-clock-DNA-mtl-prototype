"""
EpiClock v4.0 - Figure 2: Substance-Specific Epigenetic Age Acceleration
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

# Substance colors
SUBSTANCE_COLORS = {
    'Alcohol': '#1565C0',
    'Cocaine': '#C62828',
    'Opioids': '#6A1B9A',
    'Methamphetamine': '#EF6C00',
    'Cannabis': '#2E7D32',
    'Polysubstance': '#37474F'
}

# Data from Table 7
substances = ['Alcohol', 'Cocaine', 'Opioids', 'Methamphetamine', 'Cannabis', 'Polysubstance']
n_samples = [2183, 1030, 1360, 48, 194, 720]

# Horvath EAA
horvath_eaa = [2.8, 3.2, 2.4, 4.7, 1.2, 5.8]
horvath_ci_lower = [2.3, 2.7, 1.9, 3.2, 0.7, 5.1]
horvath_ci_upper = [3.4, 3.8, 2.9, 6.3, 1.8, 6.6]

# GrimAge EAA
grimace_eaa = [3.6, 4.1, 2.9, 6.2, 1.6, 7.3]
grimace_ci_lower = [3.1, 3.5, 2.5, 4.5, 1.0, 6.4]
grimace_ci_upper = [4.2, 4.7, 3.4, 8.1, 2.3, 8.3]

# Cohen's d
cohens_d = [0.62, 0.71, 0.53, 1.04, 0.27, 0.89]

colors = [SUBSTANCE_COLORS[s] for s in substances]

# Create figure
fig = plt.figure(figsize=(18, 14), facecolor='white')
gs = fig.add_gridspec(2, 3, height_ratios=[1.2, 1], hspace=0.35, wspace=0.25)

# === PANEL A: Grouped Bar Chart (Horvath vs GrimAge) ===
ax1 = fig.add_subplot(gs[0, :2])
ax1.set_facecolor('#FAFAFA')

x = np.arange(len(substances))
width = 0.35

# Horvath bars
horvath_errors = np.array([[horvath_eaa[i] - horvath_ci_lower[i] for i in range(len(horvath_eaa))],
                           [horvath_ci_upper[i] - horvath_eaa[i] for i in range(len(horvath_eaa))]])
bars1 = ax1.bar(x - width/2, horvath_eaa, width, label='Horvath Clock',
                color=[plt.matplotlib.colors.to_rgba(c, 0.7) for c in colors],
                edgecolor=colors, linewidth=2)
ax1.errorbar(x - width/2, horvath_eaa, yerr=horvath_errors, fmt='none',
             ecolor='#333333', elinewidth=1.5, capsize=4, capthick=1.5)

# GrimAge bars
grimace_errors = np.array([[grimace_eaa[i] - grimace_ci_lower[i] for i in range(len(grimace_eaa))],
                           [grimace_ci_upper[i] - grimace_eaa[i] for i in range(len(grimace_eaa))]])
bars2 = ax1.bar(x + width/2, grimace_eaa, width, label='GrimAge Clock',
                color=colors, edgecolor='white', linewidth=2)
ax1.errorbar(x + width/2, grimace_eaa, yerr=grimace_errors, fmt='none',
             ecolor='#333333', elinewidth=1.5, capsize=4, capthick=1.5)

# Value labels
for i, (h, g) in enumerate(zip(horvath_eaa, grimace_eaa)):
    ax1.text(x[i] - width/2, h + 0.3, f'+{h}', ha='center', fontsize=9, fontweight='bold', color=colors[i])
    ax1.text(x[i] + width/2, g + 0.3, f'+{g}', ha='center', fontsize=9, fontweight='bold', color=colors[i])

# Sample size annotations
for i, (pos, n) in enumerate(zip(x, n_samples)):
    ax1.text(pos, -1.0, f'n={n:,}', ha='center', fontsize=10, color='#666666')

ax1.set_ylabel('Epigenetic Age Acceleration (years)', fontsize=13, fontweight='bold', color=UNODC_SECONDARY)
ax1.set_xticks(x)
ax1.set_xticklabels(substances, fontsize=12, fontweight='500')
ax1.set_ylim(-1.5, 10)
ax1.axhline(y=0, color='#DC2626', linestyle='-', linewidth=1.5, alpha=0.7)
ax1.text(5.5, 0.3, 'No Acceleration', fontsize=9, color='#DC2626', ha='right')

ax1.legend(loc='upper left', fontsize=11, framealpha=0.95)
ax1.yaxis.grid(True, linestyle='--', alpha=0.3)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

ax1.set_title('A. Epigenetic Age Acceleration by Substance Type', fontsize=14, 
              fontweight='bold', color=UNODC_PRIMARY, loc='left', pad=15)

# Stats box
stats_text = 'ANOVA: F=342.7, df=6, p<0.001***'
ax1.text(0.98, 0.98, stats_text, transform=ax1.transAxes, fontsize=10,
         va='top', ha='right', fontfamily='monospace',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor=UNODC_PRIMARY))

# === PANEL B: Effect Size (Cohen's d) ===
ax2 = fig.add_subplot(gs[0, 2])
ax2.set_facecolor('#FAFAFA')

# Horizontal bar chart for effect sizes
y_pos = np.arange(len(substances))
bars3 = ax2.barh(y_pos, cohens_d, height=0.6, color=colors, edgecolor='white', linewidth=2)

# Effect size thresholds
ax2.axvline(x=0.2, color='#FFC107', linestyle='--', linewidth=1.5, alpha=0.7)
ax2.axvline(x=0.5, color='#FF9800', linestyle='--', linewidth=1.5, alpha=0.7)
ax2.axvline(x=0.8, color='#F44336', linestyle='--', linewidth=1.5, alpha=0.7)

# Labels
for i, (bar, val) in enumerate(zip(bars3, cohens_d)):
    ax2.text(val + 0.03, bar.get_y() + bar.get_height()/2,
             f'd={val:.2f}', ha='left', va='center', fontsize=10, fontweight='bold', color=colors[i])

ax2.set_yticks(y_pos)
ax2.set_yticklabels(substances, fontsize=11)
ax2.set_xlabel("Cohen's d Effect Size", fontsize=12, fontweight='bold', color=UNODC_SECONDARY)
ax2.set_xlim(0, 1.3)

# Effect size legend
ax2.text(0.2, 5.7, 'Small', fontsize=8, color='#FFC107', ha='center')
ax2.text(0.5, 5.7, 'Medium', fontsize=8, color='#FF9800', ha='center')
ax2.text(0.8, 5.7, 'Large', fontsize=8, color='#F44336', ha='center')

ax2.xaxis.grid(True, linestyle='--', alpha=0.3)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

ax2.set_title('B. Effect Size Magnitude', fontsize=14, fontweight='bold',
              color=UNODC_PRIMARY, loc='left', pad=15)

# === PANEL C: Dot Plot with CI (GrimAge Focus) ===
ax3 = fig.add_subplot(gs[1, 0])
ax3.set_facecolor('#FAFAFA')

# Sort by effect size
sorted_idx = np.argsort(grimace_eaa)[::-1]
sorted_substances = [substances[i] for i in sorted_idx]
sorted_eaa = [grimace_eaa[i] for i in sorted_idx]
sorted_lower = [grimace_ci_lower[i] for i in sorted_idx]
sorted_upper = [grimace_ci_upper[i] for i in sorted_idx]
sorted_colors = [colors[i] for i in sorted_idx]

y_positions = np.arange(len(sorted_substances))

# CI lines and points
for i, (y, eaa, lower, upper, color) in enumerate(zip(y_positions, sorted_eaa, sorted_lower, sorted_upper, sorted_colors)):
    ax3.hlines(y=y, xmin=lower, xmax=upper, colors=color, linewidth=3, alpha=0.6)
    ax3.scatter(eaa, y, s=200, color=color, edgecolor='white', linewidth=2, zorder=10)
    ax3.text(upper + 0.2, y, f'+{eaa:.1f}', va='center', fontsize=10, fontweight='bold', color=color)

ax3.axvline(x=0, color='#DC2626', linestyle='-', linewidth=2, alpha=0.8)

ax3.set_yticks(y_positions)
ax3.set_yticklabels(sorted_substances, fontsize=11)
ax3.set_xlabel('GrimAge EAA (years)', fontsize=12, fontweight='bold', color=UNODC_SECONDARY)
ax3.set_xlim(-1, 10)

ax3.xaxis.grid(True, linestyle='--', alpha=0.3)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)

ax3.set_title('C. GrimAge EAA (Ranked)', fontsize=14, fontweight='bold',
              color=UNODC_PRIMARY, loc='left', pad=15)

# === PANEL D: Bubble Chart (n vs EAA) ===
ax4 = fig.add_subplot(gs[1, 1])
ax4.set_facecolor('#FAFAFA')

# Bubble sizes proportional to sample size
bubble_sizes = [n/10 for n in n_samples]  # Scale for visibility

for i, (n, eaa, color, substance) in enumerate(zip(n_samples, grimace_eaa, colors, substances)):
    ax4.scatter(n, eaa, s=bubble_sizes[i], color=color, alpha=0.7, 
                edgecolor='white', linewidth=2, label=substance)
    
# Annotations for each point
for i, (n, eaa, substance) in enumerate(zip(n_samples, grimace_eaa, substances)):
    offset_x = 100 if n > 500 else 30
    ax4.annotate(substance, xy=(n, eaa), xytext=(n + offset_x, eaa + 0.3),
                 fontsize=9, color='#333333')

ax4.set_xlabel('Sample Size (n)', fontsize=12, fontweight='bold', color=UNODC_SECONDARY)
ax4.set_ylabel('GrimAge EAA (years)', fontsize=12, fontweight='bold', color=UNODC_SECONDARY)
ax4.set_xscale('log')

ax4.xaxis.grid(True, linestyle='--', alpha=0.3)
ax4.yaxis.grid(True, linestyle='--', alpha=0.3)
ax4.spines['top'].set_visible(False)
ax4.spines['right'].set_visible(False)

ax4.set_title('D. Sample Size vs Effect', fontsize=14, fontweight='bold',
              color=UNODC_PRIMARY, loc='left', pad=15)

# === PANEL E: Summary Heatmap ===
ax5 = fig.add_subplot(gs[1, 2])
ax5.axis('off')

# Create summary table
table_data = [
    ['Alcohol', '+3.6', '3.1-4.2', '0.62', '<0.001'],
    ['Cocaine', '+4.1', '3.5-4.7', '0.71', '<0.001'],
    ['Opioids', '+2.9', '2.5-3.4', '0.53', '<0.001'],
    ['Meth', '+6.2', '4.5-8.1', '1.04', '<0.001'],
    ['Cannabis', '+1.6', '1.0-2.3', '0.27', '<0.001'],
    ['Poly', '+7.3', '6.4-8.3', '0.89', '<0.001']
]
col_labels = ['Substance', 'EAA (yr)', '95% CI', "Cohen's d", 'p-value']

table = ax5.table(cellText=table_data, colLabels=col_labels,
                  cellLoc='center', loc='center', colWidths=[0.22, 0.18, 0.22, 0.18, 0.18])

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.0, 1.8)

# Header styling
for j in range(5):
    cell = table[(0, j)]
    cell.set_facecolor(UNODC_PRIMARY)
    cell.set_text_props(color='white', fontweight='bold')

# Row styling with color coding
for i in range(1, 7):
    table[(i, 0)].set_facecolor(plt.matplotlib.colors.to_rgba(list(SUBSTANCE_COLORS.values())[i-1], 0.2))
    for j in range(1, 5):
        table[(i, j)].set_facecolor('white' if i % 2 == 0 else '#F8FAFC')
        table[(i, j)].set_edgecolor('#E5E7EB')

ax5.set_title('E. Summary Statistics (GrimAge)', fontsize=14, fontweight='bold',
              color=UNODC_PRIMARY, pad=15)

# Main title
fig.suptitle('Figure 2. Substance-Specific Epigenetic Age Acceleration',
             fontsize=20, fontweight='bold', color=UNODC_PRIMARY, y=0.99)
fig.text(0.5, 0.95, 'Comparison Across 6 Substance Categories | Total n=5,535 cases vs n=5,007 controls',
         ha='center', fontsize=12, style='italic', color='#666666')

# Footer
fig.text(0.5, 0.01, 
         'EAA: Epigenetic Age Acceleration. All comparisons vs healthy controls. '
         'Error bars represent 95% confidence intervals. ***p<0.001',
         ha='center', fontsize=9, style='italic', color='#666666')

plt.tight_layout(rect=[0, 0.03, 1, 0.93])

# Save
plt.savefig('figures/figure_2_substance_eaa.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('figures/figure_2_substance_eaa.pdf', bbox_inches='tight', facecolor='white')
print("Figure 2 saved successfully!")
