"""
EpiClock v4.0 - Intervention Effects Forest Plot
Professional Publication-Ready Visualization
UNODC Corporate Standards Compliant
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# UNODC Color Palette
UNODC_PRIMARY = '#0050A0'
UNODC_SECONDARY = '#003366'
UNODC_ACCENT = '#00A7D8'
UNODC_SUCCESS = '#2E7D32'

# Data
interventions = [
    'Combined Intervention',
    'Dietary Modification',
    'Physical Exercise',
    'Substance Cessation (5 yr)',
    'Mindfulness + Yoga',
    'Substance Cessation (1 yr)',
    'Pooled Effect (All)'
]

effects = [-4.60, -3.23, -2.87, -3.18, -1.96, -1.52, -2.73]
ci_lower = [-5.8, -4.1, -3.6, -4.2, -2.7, -2.3, -3.4]
ci_upper = [-3.4, -2.4, -2.1, -2.1, -1.2, -0.7, -2.1]
sample_sizes = [89, 124, 156, 52, 78, 94, 473]

# Figure setup - wider to accommodate table
fig, (ax_forest, ax_table) = plt.subplots(1, 2, figsize=(16, 8), 
                                           gridspec_kw={'width_ratios': [2.5, 1]},
                                           facecolor='white')
ax_forest.set_facecolor('#FAFAFA')
ax_table.set_facecolor('white')

y_pos = np.arange(len(interventions))

# Color based on effect magnitude
colors = []
for effect in effects:
    if abs(effect) >= 4:
        colors.append(UNODC_PRIMARY)
    elif abs(effect) >= 3:
        colors.append(UNODC_SECONDARY)
    elif abs(effect) >= 2:
        colors.append(UNODC_ACCENT)
    else:
        colors.append('#6B7280')

# Draw confidence intervals and effect points
for i in range(len(interventions)):
    ax_forest.hlines(y=y_pos[i], xmin=ci_lower[i], xmax=ci_upper[i], 
                     colors=colors[i], linewidth=4, alpha=0.8)
    
    ax_forest.plot([ci_lower[i], ci_lower[i]], [y_pos[i]-0.12, y_pos[i]+0.12], 
                   color=colors[i], linewidth=2.5)
    ax_forest.plot([ci_upper[i], ci_upper[i]], [y_pos[i]-0.12, y_pos[i]+0.12], 
                   color=colors[i], linewidth=2.5)
    
    if i == len(interventions) - 1:
        ax_forest.scatter(effects[i], y_pos[i], s=400, color=UNODC_PRIMARY, 
                          marker='D', zorder=10, edgecolor='white', linewidth=2.5)
    else:
        ax_forest.scatter(effects[i], y_pos[i], s=250, color=colors[i], 
                          zorder=10, edgecolor='white', linewidth=2)

# Vertical reference line (null effect)
ax_forest.axvline(x=0, color='#DC2626', linestyle='-', linewidth=2.5, alpha=0.9)

# Shaded beneficial region
ax_forest.axvspan(-7, 0, alpha=0.06, color=UNODC_SUCCESS)

# Y-axis
ax_forest.set_yticks(y_pos)
ax_forest.set_yticklabels(interventions, fontsize=13, fontweight='500')

# X-axis
ax_forest.set_xlabel('Epigenetic Age Change (years)', fontsize=14, fontweight='bold', 
                     labelpad=15, color=UNODC_SECONDARY)
ax_forest.set_xlim(-7, 1.5)
ax_forest.set_ylim(-0.7, len(interventions) - 0.3)

# Title
ax_forest.set_title('Effect of Interventions on\nEpigenetic Age Acceleration', 
                    fontsize=18, fontweight='bold', color=UNODC_PRIMARY, pad=20, loc='left')

# Grid
ax_forest.grid(axis='x', linestyle='--', alpha=0.4, color='#D1D5DB')
ax_forest.set_axisbelow(True)

# Spines
ax_forest.spines['top'].set_visible(False)
ax_forest.spines['right'].set_visible(False)
ax_forest.spines['left'].set_linewidth(1.5)
ax_forest.spines['bottom'].set_linewidth(1.5)

# Annotations
ax_forest.annotate('Beneficial\n(Age Reduction)', xy=(-6, 6.3), fontsize=11, 
                   color=UNODC_SUCCESS, fontweight='bold', ha='left')
ax_forest.annotate('No Effect', xy=(0.15, 6.3), fontsize=11, 
                   color='#DC2626', fontweight='bold', ha='left')

# Horizontal separator for pooled effect
ax_forest.axhline(y=len(interventions)-1.5, color='#9CA3AF', linewidth=1.5, linestyle='--', alpha=0.6)

# === TABLE PANEL ===
ax_table.axis('off')

# Table data
table_data = []
for i in range(len(interventions)):
    effect_str = f'{effects[i]:.2f}'
    ci_str = f'[{ci_lower[i]:.1f}, {ci_upper[i]:.1f}]'
    n_str = f'{sample_sizes[i]}'
    table_data.append([effect_str, ci_str, n_str])

# Column headers
col_labels = ['Effect\n(years)', '95% CI', 'n']

# Create table
table = ax_table.table(
    cellText=table_data,
    colLabels=col_labels,
    cellLoc='center',
    loc='center',
    colWidths=[0.3, 0.4, 0.2]
)

# Style table
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1.2, 2.2)

# Header styling
for j in range(3):
    cell = table[(0, j)]
    cell.set_facecolor(UNODC_PRIMARY)
    cell.set_text_props(color='white', fontweight='bold', fontsize=11)
    cell.set_height(0.08)

# Row styling
for i in range(1, len(interventions) + 1):
    for j in range(3):
        cell = table[(i, j)]
        if i == len(interventions):  # Pooled effect row
            cell.set_facecolor('#E3F2FD')
            cell.set_text_props(fontweight='bold')
        elif i % 2 == 0:
            cell.set_facecolor('#F8FAFC')
        else:
            cell.set_facecolor('white')
        cell.set_edgecolor('#E5E7EB')

ax_table.set_title('Summary Statistics', fontsize=14, fontweight='bold', 
                   color=UNODC_SECONDARY, pad=10)

# Legend
legend_elements = [
    mpatches.Patch(facecolor=UNODC_PRIMARY, edgecolor='white', label='Strong (>4 yr)'),
    mpatches.Patch(facecolor=UNODC_SECONDARY, edgecolor='white', label='Moderate (3-4 yr)'),
    mpatches.Patch(facecolor=UNODC_ACCENT, edgecolor='white', label='Mild (2-3 yr)'),
    mpatches.Patch(facecolor='#6B7280', edgecolor='white', label='Minimal (<2 yr)')
]
ax_forest.legend(handles=legend_elements, loc='lower left', framealpha=0.95, 
                 fontsize=10, title='Effect Magnitude', title_fontsize=11,
                 bbox_to_anchor=(0.02, 0.02))

# Footer
fig.text(0.5, 0.02, 
         'Note: Error bars represent 95% confidence intervals. Total n=473 across 6 studies. '
         'Negative values indicate epigenetic age reduction.',
         ha='center', fontsize=10, color='#6B7280', style='italic')

# Heterogeneity
fig.text(0.02, 0.02, 
         'Heterogeneity: I²=42.3%, Q=8.67, p=0.19',
         ha='left', fontsize=9, color='#9CA3AF', fontfamily='monospace')

plt.tight_layout(rect=[0, 0.05, 1, 0.98])

# Save
plt.savefig('figures/intervention_forest_plot.png', dpi=300, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
plt.savefig('figures/intervention_forest_plot.pdf', bbox_inches='tight', 
            facecolor='white', edgecolor='none')

print("Forest plot saved successfully!")
