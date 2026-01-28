"""
EpiClock v4.0 - Figure 3: Mediation Analysis - Physiological Pathways
Professional Publication-Ready Visualization for Q1 Academic Journals
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np

# UNODC Color Palette
UNODC_PRIMARY = '#0050A0'
UNODC_SECONDARY = '#003366'
UNODC_ACCENT = '#00A7D8'

# Pathway colors
PATHWAY_COLORS = {
    'Insulin': '#E53935',
    'HPA': '#7B1FA2',
    'Inflammation': '#FF6F00'
}

# Data from Table 11
substances = ['Alcohol', 'Cocaine', 'Opioids', 'Methamphetamine', 'Polysubstance']
n_samples = [2183, 1030, 1360, 48, 720]

# Insulin Resistance Mediation (%)
insulin_mediation = [38, 29, 36, 42, 34]
insulin_ci_lower = [31, 22, 28, 18, 27]
insulin_ci_upper = [46, 37, 44, 68, 41]

# Cortisol/ACTH Increase (%)
hpa_increase = [34, 42, 51, 38, 45]

# CRP levels (mg/L)
crp_levels = [3.8, 4.2, 3.4, 5.1, 6.3]
crp_control = 1.2

# IL-6 levels (pg/mL)
il6_levels = [5.7, 6.3, 4.9, 7.8, 9.2]
il6_control = 2.1

# Overall mediation percentages
overall_mediation = {
    'Insulin Resistance': 34,
    'HPA Axis': 29,
    'Inflammation': 37
}

# Create figure
fig = plt.figure(figsize=(18, 14), facecolor='white')
gs = fig.add_gridspec(2, 3, height_ratios=[1.2, 1], hspace=0.35, wspace=0.25)

# === PANEL A: Mediation Model Diagram ===
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_facecolor('white')
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)
ax1.axis('off')

def draw_box(ax, x, y, w, h, text, color, fontsize=10):
    box = FancyBboxPatch((x-w/2, y-h/2), w, h,
                          boxstyle="round,pad=0.03,rounding_size=0.05",
                          facecolor=color, edgecolor='white',
                          linewidth=2, alpha=0.9)
    ax.add_patch(box)
    ax.text(x, y, text, ha='center', va='center', fontsize=fontsize,
            fontweight='bold', color='white', wrap=True)

def draw_arrow(ax, start, end, text='', color='#333333', curved=False):
    style = "Simple,tail_width=0.5,head_width=4,head_length=4"
    if curved:
        arrow = FancyArrowPatch(start, end, connectionstyle="arc3,rad=0.3",
                                arrowstyle=style, color=color, linewidth=2)
    else:
        arrow = FancyArrowPatch(start, end, arrowstyle=style, color=color, linewidth=2)
    ax.add_patch(arrow)
    if text:
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2 + 0.3
        ax.text(mid_x, mid_y, text, ha='center', va='center', fontsize=9,
                fontweight='bold', color=color)

# Draw boxes
draw_box(ax1, 2, 5, 2.5, 1.2, 'Substance\nUse', UNODC_SECONDARY, 11)
draw_box(ax1, 8, 5, 2.5, 1.2, 'Epigenetic\nAge (EAA)', UNODC_PRIMARY, 11)

# Mediators
draw_box(ax1, 5, 8, 2.2, 0.9, 'Insulin\nResistance', PATHWAY_COLORS['Insulin'], 9)
draw_box(ax1, 5, 5, 2.2, 0.9, 'HPA Axis\nDysregulation', PATHWAY_COLORS['HPA'], 9)
draw_box(ax1, 5, 2, 2.2, 0.9, 'Systemic\nInflammation', PATHWAY_COLORS['Inflammation'], 9)

# Arrows - Direct path (c')
draw_arrow(ax1, (3.3, 5), (6.7, 5), "c'=0.42***", '#666666')

# Arrows - Indirect paths
draw_arrow(ax1, (3.3, 5.6), (3.9, 7.5), 'a₁', PATHWAY_COLORS['Insulin'])
draw_arrow(ax1, (6.1, 7.5), (6.7, 5.6), 'b₁', PATHWAY_COLORS['Insulin'])

draw_arrow(ax1, (3.3, 5.3), (3.9, 5.3), 'a₂', PATHWAY_COLORS['HPA'])
draw_arrow(ax1, (6.1, 5.3), (6.7, 5.3), 'b₂', PATHWAY_COLORS['HPA'])

draw_arrow(ax1, (3.3, 4.4), (3.9, 2.5), 'a₃', PATHWAY_COLORS['Inflammation'])
draw_arrow(ax1, (6.1, 2.5), (6.7, 4.4), 'b₃', PATHWAY_COLORS['Inflammation'])

# Mediation percentages
ax1.text(5, 9.3, '34% mediation', fontsize=10, ha='center', color=PATHWAY_COLORS['Insulin'], fontweight='bold')
ax1.text(7.5, 5.8, '29%', fontsize=9, ha='left', color=PATHWAY_COLORS['HPA'], fontweight='bold')
ax1.text(5, 0.7, '37% mediation', fontsize=10, ha='center', color=PATHWAY_COLORS['Inflammation'], fontweight='bold')

ax1.set_title('A. Multiple Mediation Model', fontsize=14, fontweight='bold',
              color=UNODC_PRIMARY, pad=10)

# === PANEL B: Mediation Percentages by Substance ===
ax2 = fig.add_subplot(gs[0, 1:])
ax2.set_facecolor('#FAFAFA')

x = np.arange(len(substances))
width = 0.25

# Calculate errors for insulin
insulin_errors = np.array([[insulin_mediation[i] - insulin_ci_lower[i] for i in range(len(insulin_mediation))],
                           [insulin_ci_upper[i] - insulin_mediation[i] for i in range(len(insulin_mediation))]])

# Bars
bars1 = ax2.bar(x - width, insulin_mediation, width, label='Insulin Resistance',
                color=PATHWAY_COLORS['Insulin'], edgecolor='white', linewidth=1.5)
ax2.errorbar(x - width, insulin_mediation, yerr=insulin_errors, fmt='none',
             ecolor='#333333', elinewidth=1.5, capsize=3)

bars2 = ax2.bar(x, hpa_increase, width, label='HPA Axis (+Cortizol/ACTH)',
                color=PATHWAY_COLORS['HPA'], edgecolor='white', linewidth=1.5)

bars3 = ax2.bar(x + width, [30, 35, 28, 40, 38], width, label='Inflammation (CRP-mediated)',
                color=PATHWAY_COLORS['Inflammation'], edgecolor='white', linewidth=1.5)

ax2.set_ylabel('Mediation Effect (%)', fontsize=13, fontweight='bold', color=UNODC_SECONDARY)
ax2.set_xticks(x)
ax2.set_xticklabels(substances, fontsize=11)
ax2.set_ylim(0, 75)
ax2.legend(loc='upper right', fontsize=10, framealpha=0.95)

ax2.yaxis.grid(True, linestyle='--', alpha=0.3)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

ax2.set_title('B. Mediation Effects by Substance and Pathway', fontsize=14,
              fontweight='bold', color=UNODC_PRIMARY, loc='left', pad=15)

# === PANEL C: Inflammatory Markers (CRP) ===
ax3 = fig.add_subplot(gs[1, 0])
ax3.set_facecolor('#FAFAFA')

colors_crp = [PATHWAY_COLORS['Inflammation']] * len(substances) + ['#4CAF50']
all_crp = crp_levels + [crp_control]
all_labels = substances + ['Control']

y_pos = np.arange(len(all_labels))
bars = ax3.barh(y_pos, all_crp, height=0.6, color=colors_crp, edgecolor='white', linewidth=2)

# Control reference line
ax3.axvline(x=crp_control, color='#4CAF50', linestyle='--', linewidth=2, alpha=0.7)

for i, (bar, val) in enumerate(zip(bars, all_crp)):
    ax3.text(val + 0.15, bar.get_y() + bar.get_height()/2,
             f'{val:.1f}', ha='left', va='center', fontsize=10, fontweight='bold')

ax3.set_yticks(y_pos)
ax3.set_yticklabels(all_labels, fontsize=10)
ax3.set_xlabel('CRP Level (mg/L)', fontsize=12, fontweight='bold', color=UNODC_SECONDARY)
ax3.set_xlim(0, 8)

ax3.xaxis.grid(True, linestyle='--', alpha=0.3)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)

ax3.set_title('C. C-Reactive Protein Levels', fontsize=14, fontweight='bold',
              color=UNODC_PRIMARY, loc='left', pad=15)

# === PANEL D: IL-6 Comparison ===
ax4 = fig.add_subplot(gs[1, 1])
ax4.set_facecolor('#FAFAFA')

all_il6 = il6_levels + [il6_control]

bars = ax4.barh(y_pos, all_il6, height=0.6, color=colors_crp, edgecolor='white', linewidth=2)
ax4.axvline(x=il6_control, color='#4CAF50', linestyle='--', linewidth=2, alpha=0.7)

for i, (bar, val) in enumerate(zip(bars, all_il6)):
    ax4.text(val + 0.2, bar.get_y() + bar.get_height()/2,
             f'{val:.1f}', ha='left', va='center', fontsize=10, fontweight='bold')

ax4.set_yticks(y_pos)
ax4.set_yticklabels(all_labels, fontsize=10)
ax4.set_xlabel('IL-6 Level (pg/mL)', fontsize=12, fontweight='bold', color=UNODC_SECONDARY)
ax4.set_xlim(0, 12)

ax4.xaxis.grid(True, linestyle='--', alpha=0.3)
ax4.spines['top'].set_visible(False)
ax4.spines['right'].set_visible(False)

ax4.set_title('D. Interleukin-6 Levels', fontsize=14, fontweight='bold',
              color=UNODC_PRIMARY, loc='left', pad=15)

# === PANEL E: Overall Mediation Pie ===
ax5 = fig.add_subplot(gs[1, 2])
ax5.set_facecolor('white')

# Pie chart of overall mediation
labels = list(overall_mediation.keys())
sizes = list(overall_mediation.values())
colors_pie = [PATHWAY_COLORS['Insulin'], PATHWAY_COLORS['HPA'], PATHWAY_COLORS['Inflammation']]

wedges, texts, autotexts = ax5.pie(sizes, labels=labels, colors=colors_pie, autopct='%1.0f%%',
                                     startangle=90, explode=(0.02, 0.02, 0.02),
                                     wedgeprops=dict(edgecolor='white', linewidth=2))

for text in texts:
    text.set_fontsize(10)
    text.set_fontweight('bold')
for autotext in autotexts:
    autotext.set_fontsize(11)
    autotext.set_fontweight('bold')
    autotext.set_color('white')

ax5.set_title('E. Overall Mediation Contribution', fontsize=14, fontweight='bold',
              color=UNODC_PRIMARY, pad=15)

# Add center circle for donut effect
centre_circle = Circle((0, 0), 0.5, fc='white', linewidth=2, edgecolor='#E5E7EB')
ax5.add_patch(centre_circle)
ax5.text(0, 0, 'Total\nMediation', ha='center', va='center', fontsize=10, fontweight='bold', color=UNODC_SECONDARY)

# Main title
fig.suptitle('Figure 3. Physiological Mediation Pathways in Substance-Induced EAA',
             fontsize=20, fontweight='bold', color=UNODC_PRIMARY, y=0.99)
fig.text(0.5, 0.95, 'Multiple Mediation Analysis | Sub-cohort n=2,847 (Insulin), n=1,523 (HPA), n=2,134 (Inflammation)',
         ha='center', fontsize=11, style='italic', color='#666666')

# Footer
fig.text(0.5, 0.01, 
         'EAA: Epigenetic Age Acceleration; CRP: C-Reactive Protein; IL-6: Interleukin-6; HPA: Hypothalamic-Pituitary-Adrenal. '
         '*p<0.05, **p<0.01, ***p<0.001',
         ha='center', fontsize=9, style='italic', color='#666666')

plt.tight_layout(rect=[0, 0.03, 1, 0.93])

# Save
plt.savefig('figures/figure_3_mediation_analysis.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('figures/figure_3_mediation_analysis.pdf', bbox_inches='tight', facecolor='white')
print("Figure 3 saved successfully!")
