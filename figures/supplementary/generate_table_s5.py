#!/usr/bin/env python3
"""
Supplementary Table S5: Mediation Analysis Detailed Results
Uc mediyator icin detayli mediasyon analizi sonuclari
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

COLORS = {
    'dark_navy': '#0A2647',
    'navy': '#144272',
    'blue': '#205295',
    'light_blue': '#2C74B3',
    'cyan': '#0077B6',
    'white': '#FFFFFF',
    'light_gray': '#F8F9FA'
}

fig = plt.figure(figsize=(22, 20), facecolor='white', dpi=300)
ax = fig.add_subplot(111)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

ax.text(50, 98, 'Supplementary Table S5', fontsize=24, fontweight='bold', 
        color=COLORS['dark_navy'], ha='center', va='top')
ax.text(50, 94.5, 'Mediation Analysis Detailed Results (n=1,289)', fontsize=16, 
        color=COLORS['navy'], ha='center', va='top')

def draw_mediator_table(ax, mediator_name, data, start_y, color):
    header_rect = mpatches.FancyBboxPatch((2, start_y-1.5), 96, 3.5,
                                           boxstyle="round,pad=0.02",
                                           facecolor=color, edgecolor='none')
    ax.add_patch(header_rect)
    ax.text(50, start_y, mediator_name, fontsize=14, fontweight='bold', 
            color='white', ha='center', va='center')
    
    headers = ['Parameter', 'Estimate', 'SE', '95% CI', 'z-value', 'p-value']
    col_widths = [28, 14, 10, 20, 12, 14]
    col_pos = [3]
    for w in col_widths[:-1]:
        col_pos.append(col_pos[-1] + w)
    
    header_y = start_y - 4.5
    for i, (h, x_p) in enumerate(zip(headers, col_pos)):
        rect = mpatches.FancyBboxPatch((x_p-1, header_y-1.5), col_widths[i]-0.5, 2.8,
                                        boxstyle="round,pad=0.01",
                                        facecolor=COLORS['navy'], edgecolor='none')
        ax.add_patch(rect)
        ax.text(x_p + col_widths[i]/2 - 0.5, header_y, h, fontsize=11, fontweight='bold',
                color='white', ha='center', va='center')
    
    for row_idx, row in enumerate(data):
        row_y = header_y - 3.5 - (row_idx * 3)
        bg_color = COLORS['light_gray'] if row_idx % 2 == 0 else 'white'
        rect = mpatches.FancyBboxPatch((2, row_y-1.3), 96, 2.6,
                                        boxstyle="round,pad=0.01",
                                        facecolor=bg_color, edgecolor=COLORS['light_blue'], linewidth=0.3)
        ax.add_patch(rect)
        
        for col_idx, (value, x_p) in enumerate(zip(row, col_pos)):
            fontweight = 'bold' if col_idx == 0 else 'normal'
            color = COLORS['dark_navy']
            if col_idx == 5 and '<0.001' in value:
                color = '#B22222'
                fontweight = 'bold'
            ax.text(x_p + col_widths[col_idx]/2 - 0.5, row_y, value, fontsize=10,
                    fontweight=fontweight, color=color, ha='center', va='center')
    
    return start_y - 4.5 - (len(data) * 3) - 4

insulin_data = [
    ['Path a (X → M): Substance → HOMA-IR', 'β = 0.42', '0.04', '0.34 - 0.50', '10.5', '<0.001'],
    ['Path b (M → Y): HOMA-IR → GrimAge EAA', 'β = 0.33', '0.03', '0.27 - 0.39', '11.0', '<0.001'],
    ['Direct Effect (X → Y)', 'β = 0.39', '0.04', '0.31 - 0.47', '9.75', '<0.001'],
    ['Indirect Effect (X → M → Y)', 'β = 0.14', '0.02', '0.10 - 0.18', '7.0', '<0.001'],
    ['Total Effect', 'β = 0.53', '0.04', '0.45 - 0.61', '13.25', '<0.001'],
    ['Proportion Mediated', '26.4%', '-', '18.9% - 33.9%', '-', '-'],
    ['Independent Mediation', '22%', '-', '-', '-', '-'],
]

hpa_data = [
    ['Path a (X → M): Substance → Cortisol/ACTH', 'β = 0.38', '0.04', '0.30 - 0.46', '9.5', '<0.001'],
    ['Path b (M → Y): Cortisol/ACTH → GrimAge EAA', 'β = 0.24', '0.03', '0.18 - 0.30', '8.0', '<0.001'],
    ['Direct Effect (X → Y)', 'β = 0.44', '0.04', '0.36 - 0.52', '11.0', '<0.001'],
    ['Indirect Effect (X → M → Y)', 'β = 0.09', '0.02', '0.05 - 0.13', '4.5', '0.002'],
    ['Total Effect', 'β = 0.53', '0.04', '0.45 - 0.61', '13.25', '<0.001'],
    ['Proportion Mediated', '17.0%', '-', '9.4% - 24.5%', '-', '-'],
    ['Independent Mediation', '14%', '-', '-', '-', '-'],
]

inflammation_data = [
    ['Path a (X → M): Substance → CRP/IL-6', 'β = 0.45', '0.04', '0.37 - 0.53', '11.25', '<0.001'],
    ['Path b (M → Y): CRP/IL-6 → GrimAge EAA', 'β = 0.36', '0.03', '0.30 - 0.42', '12.0', '<0.001'],
    ['Direct Effect (X → Y)', 'β = 0.37', '0.04', '0.29 - 0.45', '9.25', '<0.001'],
    ['Indirect Effect (X → M → Y)', 'β = 0.16', '0.02', '0.12 - 0.20', '8.0', '<0.001'],
    ['Total Effect', 'β = 0.53', '0.04', '0.45 - 0.61', '13.25', '<0.001'],
    ['Proportion Mediated', '30.2%', '-', '22.6% - 37.7%', '-', '-'],
    ['Independent Mediation', '25%', '-', '-', '-', '-'],
]

y_pos = 91
y_pos = draw_mediator_table(ax, 'Mediator 1: Insulin Resistance (HOMA-IR)', insulin_data, y_pos, COLORS['blue'])
y_pos = draw_mediator_table(ax, 'Mediator 2: HPA Axis Dysregulation (Cortisol/ACTH Ratio)', hpa_data, y_pos, COLORS['cyan'])
y_pos = draw_mediator_table(ax, 'Mediator 3: Systemic Inflammation (CRP + IL-6)', inflammation_data, y_pos, COLORS['navy'])

summary_y = y_pos
summary_rect = mpatches.FancyBboxPatch((2, summary_y-4), 96, 5,
                                        boxstyle="round,pad=0.02",
                                        facecolor=COLORS['light_gray'], edgecolor=COLORS['dark_navy'], linewidth=1.5)
ax.add_patch(summary_rect)

ax.text(50, summary_y-0.5, 'COMBINED MEDIATION MODEL SUMMARY', fontsize=12, fontweight='bold',
        color=COLORS['dark_navy'], ha='center', va='center')
ax.text(50, summary_y-2.5, 'Total Indirect Effect: β = 0.39 (95% CI: 0.32-0.46) | Total Mediation: 61% | Direct Effect: 39%',
        fontsize=11, color=COLORS['navy'], ha='center', va='center')

ax.text(50, 2, 'Bootstrap: 10,000 iterations | Bias-corrected accelerated (BCa) confidence intervals | Covariates: Age, Sex, BMI',
        fontsize=9, style='italic', color='gray', ha='center')

plt.tight_layout()
plt.savefig('figures/output/supplementary_table_s5.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()

print("Supplementary Table S5 saved to figures/output/supplementary_table_s5.png")
