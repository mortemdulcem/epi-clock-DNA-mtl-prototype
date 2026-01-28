"""
EpiClock v4.0 - Figure 4: Sample Characteristics and Study Overview
Professional Publication-Ready Visualization for Q1 Academic Journals
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Wedge
import numpy as np

# UNODC Color Palette
UNODC_PRIMARY = '#0050A0'
UNODC_SECONDARY = '#003366'
UNODC_ACCENT = '#00A7D8'

# Substance colors
COLORS = {
    'Control': '#4CAF50',
    'Alcohol': '#1565C0',
    'Opioids': '#6A1B9A',
    'Cocaine': '#C62828',
    'Polysubstance': '#37474F',
    'Cannabis': '#2E7D32',
    'Methamphetamine': '#EF6C00'
}

# Data from Table 2
groups = ['Control', 'Alcohol', 'Opioids', 'Cocaine', 'Polysubstance', 'Cannabis', 'Methamphetamine']
n_samples = [5007, 2183, 1360, 1030, 720, 194, 48]
ages = [42.3, 45.7, 38.4, 41.2, 36.8, 32.5, 34.1]
age_sd = [14.2, 12.8, 10.5, 11.3, 9.7, 8.9, 7.8]
female_pct = [48.2, 32.1, 38.7, 28.4, 35.2, 41.2, 33.3]
usage_years = [0, 12.4, 8.2, 10.1, 11.3, 7.8, 6.5]
usage_sd = [0, 8.3, 5.7, 6.8, 7.2, 4.5, 3.9]

colors = [COLORS[g] for g in groups]

# Create figure
fig = plt.figure(figsize=(18, 14), facecolor='white')
gs = fig.add_gridspec(2, 3, height_ratios=[1, 1], hspace=0.3, wspace=0.25)

# === PANEL A: Sample Size Distribution (Treemap-style) ===
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_facecolor('white')
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)
ax1.axis('off')

# Simple proportional representation
total = sum(n_samples)
cumulative = 0
bar_height = 8
y_start = 1

for i, (group, n, color) in enumerate(zip(groups, n_samples, colors)):
    width = (n / total) * 10
    rect = FancyBboxPatch((cumulative, y_start), width - 0.05, bar_height,
                          boxstyle="round,pad=0.01", facecolor=color,
                          edgecolor='white', linewidth=2, alpha=0.85)
    ax1.add_patch(rect)
    
    # Labels for larger segments
    if width > 1:
        ax1.text(cumulative + width/2, y_start + bar_height/2,
                f'{group}\nn={n:,}\n({n/total*100:.1f}%)',
                ha='center', va='center', fontsize=9, fontweight='bold',
                color='white')
    cumulative += width

ax1.set_title('A. Sample Distribution (n=10,542)', fontsize=14, fontweight='bold',
              color=UNODC_PRIMARY, pad=10)

# === PANEL B: Pie Chart of Groups ===
ax2 = fig.add_subplot(gs[0, 1])

# Separate control and substance users
substance_n = sum(n_samples[1:])
control_n = n_samples[0]

# Outer ring - all groups
sizes_outer = n_samples
colors_outer = colors

wedges, texts, autotexts = ax2.pie(sizes_outer, colors=colors_outer,
                                    autopct=lambda pct: f'{pct:.1f}%' if pct > 5 else '',
                                    startangle=90, pctdistance=0.75,
                                    wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2))

for autotext in autotexts:
    autotext.set_fontsize(9)
    autotext.set_fontweight('bold')
    autotext.set_color('white')

# Center text
ax2.text(0, 0, f'Total\nn={total:,}', ha='center', va='center',
         fontsize=14, fontweight='bold', color=UNODC_SECONDARY)

ax2.set_title('B. Cohort Composition', fontsize=14, fontweight='bold',
              color=UNODC_PRIMARY, pad=10)

# Legend
legend_labels = [f'{g} (n={n:,})' for g, n in zip(groups, n_samples)]
ax2.legend(wedges, legend_labels, loc='center left', bbox_to_anchor=(1, 0.5),
           fontsize=9, framealpha=0.95)

# === PANEL C: Age Distribution by Group ===
ax3 = fig.add_subplot(gs[0, 2])
ax3.set_facecolor('#FAFAFA')

y_pos = np.arange(len(groups))

# Horizontal bars with error bars
bars = ax3.barh(y_pos, ages, height=0.6, color=colors, edgecolor='white', linewidth=2, alpha=0.85)
ax3.errorbar(ages, y_pos, xerr=age_sd, fmt='none', ecolor='#333333',
             elinewidth=1.5, capsize=4, capthick=1.5)

for i, (bar, age, sd) in enumerate(zip(bars, ages, age_sd)):
    ax3.text(age + sd + 1, bar.get_y() + bar.get_height()/2,
             f'{age:.1f}±{sd:.1f}', ha='left', va='center', fontsize=9, fontweight='bold')

ax3.set_yticks(y_pos)
ax3.set_yticklabels(groups, fontsize=10)
ax3.set_xlabel('Age (years)', fontsize=12, fontweight='bold', color=UNODC_SECONDARY)
ax3.set_xlim(0, 70)

ax3.xaxis.grid(True, linestyle='--', alpha=0.3)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)

ax3.set_title('C. Age Distribution by Group', fontsize=14, fontweight='bold',
              color=UNODC_PRIMARY, loc='left', pad=10)

# === PANEL D: Sex Distribution ===
ax4 = fig.add_subplot(gs[1, 0])
ax4.set_facecolor('#FAFAFA')

x_pos = np.arange(len(groups))
width = 0.35

bars_f = ax4.bar(x_pos - width/2, female_pct, width, label='Female',
                 color='#E91E63', edgecolor='white', linewidth=1.5, alpha=0.8)
bars_m = ax4.bar(x_pos + width/2, [100 - f for f in female_pct], width, label='Male',
                 color='#2196F3', edgecolor='white', linewidth=1.5, alpha=0.8)

# Add percentage labels
for bar, pct in zip(bars_f, female_pct):
    if pct > 10:
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{pct:.0f}%', ha='center', fontsize=8, fontweight='bold')

ax4.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold', color=UNODC_SECONDARY)
ax4.set_xticks(x_pos)
ax4.set_xticklabels(groups, fontsize=9, rotation=30, ha='right')
ax4.set_ylim(0, 80)
ax4.axhline(y=50, color='#999999', linestyle='--', linewidth=1, alpha=0.5)
ax4.legend(loc='upper right', fontsize=10)

ax4.yaxis.grid(True, linestyle='--', alpha=0.3)
ax4.spines['top'].set_visible(False)
ax4.spines['right'].set_visible(False)

ax4.set_title('D. Sex Distribution by Group', fontsize=14, fontweight='bold',
              color=UNODC_PRIMARY, loc='left', pad=10)

# === PANEL E: Substance Use Duration ===
ax5 = fig.add_subplot(gs[1, 1])
ax5.set_facecolor('#FAFAFA')

# Only substance users (exclude control)
substance_groups = groups[1:]
substance_usage = usage_years[1:]
substance_sd = usage_sd[1:]
substance_colors = colors[1:]

y_pos = np.arange(len(substance_groups))

bars = ax5.barh(y_pos, substance_usage, height=0.6, color=substance_colors,
                edgecolor='white', linewidth=2, alpha=0.85)
ax5.errorbar(substance_usage, y_pos, xerr=substance_sd, fmt='none',
             ecolor='#333333', elinewidth=1.5, capsize=4, capthick=1.5)

for bar, val, sd in zip(bars, substance_usage, substance_sd):
    ax5.text(val + sd + 0.5, bar.get_y() + bar.get_height()/2,
             f'{val:.1f}±{sd:.1f} yr', ha='left', va='center', fontsize=10, fontweight='bold')

ax5.set_yticks(y_pos)
ax5.set_yticklabels(substance_groups, fontsize=10)
ax5.set_xlabel('Duration of Use (years)', fontsize=12, fontweight='bold', color=UNODC_SECONDARY)
ax5.set_xlim(0, 25)

ax5.xaxis.grid(True, linestyle='--', alpha=0.3)
ax5.spines['top'].set_visible(False)
ax5.spines['right'].set_visible(False)

ax5.set_title('E. Duration of Substance Use', fontsize=14, fontweight='bold',
              color=UNODC_PRIMARY, loc='left', pad=10)

# === PANEL F: Summary Statistics Table ===
ax6 = fig.add_subplot(gs[1, 2])
ax6.axis('off')

# Table data
table_data = [
    ['Control', '5,007', '42.3±14.2', '48.2%', '-'],
    ['Alcohol', '2,183', '45.7±12.8', '32.1%', '12.4±8.3'],
    ['Opioids', '1,360', '38.4±10.5', '38.7%', '8.2±5.7'],
    ['Cocaine', '1,030', '41.2±11.3', '28.4%', '10.1±6.8'],
    ['Polysubstance', '720', '36.8±9.7', '35.2%', '11.3±7.2'],
    ['Cannabis', '194', '32.5±8.9', '41.2%', '7.8±4.5'],
    ['Methamphetamine', '48', '34.1±7.8', '33.3%', '6.5±3.9'],
    ['TOTAL', '10,542', '-', '-', '-']
]
col_labels = ['Group', 'n', 'Age (yr)', 'Female', 'Use (yr)']

table = ax6.table(cellText=table_data, colLabels=col_labels,
                  cellLoc='center', loc='center',
                  colWidths=[0.28, 0.15, 0.22, 0.15, 0.2])

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.0, 1.7)

# Header styling
for j in range(5):
    cell = table[(0, j)]
    cell.set_facecolor(UNODC_PRIMARY)
    cell.set_text_props(color='white', fontweight='bold')

# Row styling
for i in range(1, 9):
    color = colors[i-1] if i <= 7 else UNODC_SECONDARY
    alpha = 0.15 if i <= 7 else 0.3
    table[(i, 0)].set_facecolor(plt.matplotlib.colors.to_rgba(color, alpha))
    if i == 8:  # Total row
        for j in range(5):
            table[(i, j)].set_facecolor('#E3F2FD')
            table[(i, j)].set_text_props(fontweight='bold')
    for j in range(1, 5):
        table[(i, j)].set_facecolor('white' if i % 2 == 0 else '#F8FAFC')
        table[(i, j)].set_edgecolor('#E5E7EB')

ax6.set_title('F. Cohort Characteristics Summary', fontsize=14, fontweight='bold',
              color=UNODC_PRIMARY, pad=10)

# Main title
fig.suptitle('Figure 4. Study Cohort Characteristics',
             fontsize=20, fontweight='bold', color=UNODC_PRIMARY, y=0.99)
fig.text(0.5, 0.95, 'DNA Methylation Profiles from 15 Independent Datasets | 7 Substance Categories',
         ha='center', fontsize=12, style='italic', color='#666666')

# Footer
fig.text(0.5, 0.01,
         'Data sources: GEO (Gene Expression Omnibus), UK Biobank, MESA, WHI, FHS, KORA, Rotterdam Study. '
         'Error bars represent standard deviation.',
         ha='center', fontsize=9, style='italic', color='#666666')

plt.tight_layout(rect=[0, 0.03, 1, 0.93])

# Save
plt.savefig('figures/figure_4_sample_characteristics.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('figures/figure_4_sample_characteristics.pdf', bbox_inches='tight', facecolor='white')
print("Figure 4 saved successfully!")
