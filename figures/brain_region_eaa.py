"""
EpiClock v4.0 - Brain Region Epigenetic Age Acceleration
Professional Publication-Ready Visualization for Q1 Academic Journals
UNODC Corporate Standards Compliant
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

# UNODC Color Palette
UNODC_PRIMARY = '#0050A0'
UNODC_SECONDARY = '#003366'
UNODC_ACCENT = '#00A7D8'

# Brain region colors (neuroanatomy-inspired)
COLOR_PFC = '#1565C0'      # Prefrontal Cortex - deep blue (executive function)
COLOR_NAC = '#7B1FA2'      # Nucleus Accumbens - purple (reward)
COLOR_HIPP = '#00897B'     # Hippocampus - teal (memory)

# Data
regions = ['Prefrontal\nCortex', 'Nucleus\nAccumbens', 'Hippocampus']
regions_short = ['PFC', 'NAc', 'HIPP']
n_samples = [48, 36, 24]
eaa_values = [5.3, 4.1, 3.2]
ci_lower = [4.2, 3.2, 2.3]
ci_upper = [6.5, 5.1, 4.2]
functions = ['Decision-making,\nimpulse control', 'Reward system,\naddiction center', 'Memory,\nlearning']

# Calculate error bars
errors_lower = [eaa_values[i] - ci_lower[i] for i in range(len(eaa_values))]
errors_upper = [ci_upper[i] - eaa_values[i] for i in range(len(eaa_values))]
errors = np.array([errors_lower, errors_upper])

colors = [COLOR_PFC, COLOR_NAC, COLOR_HIPP]

# Figure with two panels
fig = plt.figure(figsize=(16, 10), facecolor='white')

# Create grid spec for layout
gs = fig.add_gridspec(2, 2, height_ratios=[2.5, 1], width_ratios=[1.2, 1],
                      hspace=0.35, wspace=0.25)

# === PANEL A: Bar Chart ===
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_facecolor('#FAFAFA')

x_pos = np.arange(len(regions))
bar_width = 0.6

# Create bars with error bars
bars = ax1.bar(x_pos, eaa_values, bar_width, color=colors, 
               edgecolor='white', linewidth=2, alpha=0.9, zorder=3)

# Add error bars
ax1.errorbar(x_pos, eaa_values, yerr=errors, fmt='none', 
             ecolor='#333333', elinewidth=2.5, capsize=8, capthick=2.5, zorder=4)

# Add value labels on bars
for i, (bar, val, n) in enumerate(zip(bars, eaa_values, n_samples)):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.4,
             f'+{val} yr', ha='center', va='bottom', fontsize=14, 
             fontweight='bold', color=colors[i])
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height()/2,
             f'n={n}', ha='center', va='center', fontsize=11, 
             fontweight='bold', color='white')

# Add functional annotations below bars
for i, (pos, func) in enumerate(zip(x_pos, functions)):
    ax1.text(pos, -0.8, func, ha='center', va='top', fontsize=9,
             color='#666666', style='italic')

# Axis formatting
ax1.set_ylabel('Horvath Epigenetic Age Acceleration (years)', fontsize=13, 
               fontweight='bold', color=UNODC_SECONDARY, labelpad=10)
ax1.set_xticks(x_pos)
ax1.set_xticklabels(regions, fontsize=12, fontweight='500')
ax1.set_ylim(0, 8)
ax1.set_xlim(-0.7, 2.7)

# Add significance brackets
def add_significance_bracket(ax, x1, x2, y, text, h=0.15):
    ax.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5, c='#333333')
    ax.text((x1+x2)/2, y+h+0.1, text, ha='center', va='bottom', fontsize=10, fontweight='bold')

add_significance_bracket(ax1, 0, 1, 6.8, '*', h=0.15)
add_significance_bracket(ax1, 0, 2, 7.3, '***', h=0.15)

# Grid
ax1.yaxis.grid(True, linestyle='--', alpha=0.4, color='#D1D5DB', zorder=0)
ax1.set_axisbelow(True)

# Spines
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_linewidth(1.5)
ax1.spines['bottom'].set_linewidth(1.5)

# Panel label
ax1.text(-0.12, 1.05, 'A', transform=ax1.transAxes, fontsize=20, 
         fontweight='bold', color=UNODC_PRIMARY)

# Statistics annotation
stats_box = ('ANOVA Results\n'
             '─────────────\n'
             'F(2, 105) = 8.7\n'
             'p < 0.001 ***')
props = dict(boxstyle='round,pad=0.5', facecolor='white', 
             edgecolor=UNODC_PRIMARY, alpha=0.95, linewidth=1.5)
ax1.text(0.97, 0.97, stats_box, transform=ax1.transAxes, fontsize=10,
         verticalalignment='top', horizontalalignment='right',
         bbox=props, fontfamily='monospace', color=UNODC_SECONDARY)

# === PANEL B: Brain Schematic ===
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_facecolor('white')
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.set_aspect('equal')
ax2.axis('off')

# Simple brain outline (sagittal view)
from matplotlib.patches import Ellipse, Circle, Polygon, Arc

# Brain outline
brain_outline = Ellipse((5, 5), 8, 6.5, facecolor='#F5F5F5', 
                         edgecolor='#9E9E9E', linewidth=2, zorder=1)
ax2.add_patch(brain_outline)

# Prefrontal Cortex (front)
pfc = Ellipse((2.2, 5.5), 2, 2.5, facecolor=COLOR_PFC, alpha=0.7,
              edgecolor=COLOR_PFC, linewidth=2, zorder=2)
ax2.add_patch(pfc)
ax2.text(2.2, 5.5, 'PFC\n+5.3 yr', ha='center', va='center', 
         fontsize=10, fontweight='bold', color='white')

# Nucleus Accumbens (subcortical)
nac = Circle((4, 4), 0.8, facecolor=COLOR_NAC, alpha=0.8,
             edgecolor=COLOR_NAC, linewidth=2, zorder=2)
ax2.add_patch(nac)
ax2.text(4, 4, 'NAc\n+4.1', ha='center', va='center', 
         fontsize=9, fontweight='bold', color='white')

# Hippocampus (medial temporal)
hipp = Ellipse((6.5, 3.5), 2.2, 1.2, angle=-20, facecolor=COLOR_HIPP, alpha=0.8,
               edgecolor=COLOR_HIPP, linewidth=2, zorder=2)
ax2.add_patch(hipp)
ax2.text(6.5, 3.5, 'HIPP\n+3.2', ha='center', va='center', 
         fontsize=9, fontweight='bold', color='white')

# Cerebellum outline
cerebellum = Ellipse((7.5, 2), 2, 1.5, facecolor='#E0E0E0', 
                     edgecolor='#9E9E9E', linewidth=1.5, zorder=1)
ax2.add_patch(cerebellum)

# Labels
ax2.text(5, 9.2, 'Sagittal View - Brain Regions', ha='center', fontsize=12, 
         fontweight='bold', color=UNODC_SECONDARY)

# Legend
ax2.text(0.5, 1.5, 'Region', fontsize=9, fontweight='bold', color='#666666')
ax2.add_patch(FancyBboxPatch((0.3, 0.8), 0.4, 0.4, boxstyle="round,pad=0.02",
                              facecolor=COLOR_PFC, edgecolor='none'))
ax2.text(0.9, 1.0, 'Prefrontal Cortex', fontsize=8, va='center')
ax2.add_patch(FancyBboxPatch((3.3, 0.8), 0.4, 0.4, boxstyle="round,pad=0.02",
                              facecolor=COLOR_NAC, edgecolor='none'))
ax2.text(3.9, 1.0, 'Nucleus Accumbens', fontsize=8, va='center')
ax2.add_patch(FancyBboxPatch((6.3, 0.8), 0.4, 0.4, boxstyle="round,pad=0.02",
                              facecolor=COLOR_HIPP, edgecolor='none'))
ax2.text(6.9, 1.0, 'Hippocampus', fontsize=8, va='center')

# Panel label
ax2.text(-0.05, 1.05, 'B', transform=ax2.transAxes, fontsize=20, 
         fontweight='bold', color=UNODC_PRIMARY)

# === PANEL C: Post-hoc Table ===
ax3 = fig.add_subplot(gs[1, :])
ax3.axis('off')

# Table data
table_data = [
    ['Prefrontal Cortex vs Nucleus Accumbens', '+1.2', '0.024', '*'],
    ['Prefrontal Cortex vs Hippocampus', '+2.1', '<0.001', '***'],
    ['Nucleus Accumbens vs Hippocampus', '+0.9', '0.18', 'NS']
]
col_labels = ['Comparison', 'Mean Difference (years)', 'p-value', 'Significance']

# Create table
table = ax3.table(cellText=table_data, colLabels=col_labels,
                  cellLoc='center', loc='center',
                  colWidths=[0.4, 0.2, 0.15, 0.12])

# Style table
table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1.1, 2.0)

# Header styling
for j in range(4):
    cell = table[(0, j)]
    cell.set_facecolor(UNODC_PRIMARY)
    cell.set_text_props(color='white', fontweight='bold', fontsize=10)
    cell.set_height(0.12)

# Row styling
for i in range(1, 4):
    for j in range(4):
        cell = table[(i, j)]
        if i % 2 == 0:
            cell.set_facecolor('#F8FAFC')
        else:
            cell.set_facecolor('white')
        cell.set_edgecolor('#E5E7EB')
        
        # Highlight significance column
        if j == 3:
            if table_data[i-1][3] == '***':
                cell.set_text_props(fontweight='bold', color=COLOR_PFC)
            elif table_data[i-1][3] == '*':
                cell.set_text_props(fontweight='bold', color=COLOR_NAC)
            else:
                cell.set_text_props(color='#9CA3AF')

# Panel label and title
ax3.text(0.02, 0.95, 'C', transform=ax3.transAxes, fontsize=20, 
         fontweight='bold', color=UNODC_PRIMARY)
ax3.text(0.5, 0.95, 'Post-hoc Pairwise Comparisons (Tukey HSD)', 
         transform=ax3.transAxes, ha='center', fontsize=13, 
         fontweight='bold', color=UNODC_SECONDARY)

# Significance legend
ax3.text(0.5, 0.08, '*p<0.05, ***p<0.001, NS: Non-significant',
         transform=ax3.transAxes, ha='center', fontsize=10, 
         style='italic', color='#666666')

# Main title
fig.suptitle('Epigenetic Age Acceleration by Brain Region in Substance Use Disorders',
             fontsize=18, fontweight='bold', color=UNODC_PRIMARY, y=0.98)
fig.text(0.5, 0.94, 'Postmortem Analysis with PMI Correction | Total n=108',
         ha='center', fontsize=12, style='italic', color='#666666')

# Footer
fig.text(0.5, 0.02, 
         'Figure X. Regional differences in epigenetic age acceleration among postmortem brain samples '
         'from individuals with substance use disorders. Error bars represent 95% confidence intervals.',
         ha='center', fontsize=9, style='italic', color='#666666', wrap=True)

plt.tight_layout(rect=[0, 0.04, 1, 0.92])

# Save
plt.savefig('figures/brain_region_eaa.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.savefig('figures/brain_region_eaa.pdf', bbox_inches='tight',
            facecolor='white', edgecolor='none')

print("Brain region EAA figure saved successfully!")
