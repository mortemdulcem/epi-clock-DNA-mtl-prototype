#!/usr/bin/env python3
"""
Supplementary Table S6: Moderation Analysis Detailed Results
Duygu duzenleme ve oz-kontrol moderasyon analizi
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

fig = plt.figure(figsize=(22, 22), facecolor='white', dpi=1200)
ax = fig.add_subplot(111)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

ax.text(50, 98, 'Supplementary Table S6', fontsize=24, fontweight='bold', 
        color=COLORS['dark_navy'], ha='center', va='top')
ax.text(50, 94.5, 'Moderation Analysis Detailed Results', fontsize=16, 
        color=COLORS['navy'], ha='center', va='top')

ders_y = 91
ders_rect = mpatches.FancyBboxPatch((2, ders_y-1.5), 96, 3.5,
                                     boxstyle="round,pad=0.02",
                                     facecolor=COLORS['blue'], edgecolor='none')
ax.add_patch(ders_rect)
ax.text(50, ders_y, 'Moderator 1: Emotion Regulation (DERS Score)', fontsize=14, fontweight='bold',
        color='white', ha='center', va='center')

ders_model = [
    ['Substance Use Duration', 'β = 0.42', '0.06', '0.30 - 0.54', '<0.001'],
    ['DERS Score', 'β = 0.28', '0.05', '0.18 - 0.38', '<0.001'],
    ['Substance × DERS Interaction', 'β = 0.38', '0.07', '0.24 - 0.52', '<0.001'],
    ['Model R²', '0.67', '-', '-', '-'],
    ['Interaction ΔR²', '0.09', '-', '-', '-'],
    ['F-statistic (Interaction)', '42.3', '-', '-', '<0.001'],
]

headers = ['Model Term', 'Estimate', 'SE', '95% CI', 'p-value']
col_widths_m = [32, 16, 10, 20, 16]
col_pos_m = [3]
for w in col_widths_m[:-1]:
    col_pos_m.append(col_pos_m[-1] + w)

header_y = ders_y - 5
for i, (h, x_p) in enumerate(zip(headers, col_pos_m)):
    ax.text(x_p + col_widths_m[i]/2, header_y, h, fontsize=11, fontweight='bold',
            color=COLORS['dark_navy'], ha='center', va='center')

for row_idx, row in enumerate(ders_model):
    row_y = header_y - 3 - (row_idx * 2.8)
    bg_color = COLORS['light_gray'] if row_idx % 2 == 0 else 'white'
    rect = mpatches.FancyBboxPatch((2, row_y-1.2), 96, 2.4,
                                    boxstyle="round,pad=0.01",
                                    facecolor=bg_color, edgecolor=COLORS['light_blue'], linewidth=0.3)
    ax.add_patch(rect)
    for col_idx, (value, x_p) in enumerate(zip(row, col_pos_m)):
        fontweight = 'bold' if col_idx == 0 else 'normal'
        ax.text(x_p + col_widths_m[col_idx]/2, row_y, value, fontsize=10,
                fontweight=fontweight, color=COLORS['dark_navy'], ha='center', va='center')

slopes_y = header_y - 3 - (len(ders_model) * 2.8) - 3
slopes_rect = mpatches.FancyBboxPatch((5, slopes_y-1), 90, 2.5,
                                       boxstyle="round,pad=0.02",
                                       facecolor=COLORS['navy'], edgecolor='none')
ax.add_patch(slopes_rect)
ax.text(50, slopes_y, 'Simple Slopes Analysis (DERS Levels)', fontsize=12, fontweight='bold',
        color='white', ha='center', va='center')

ders_slopes = [
    ['Low DERS (-1 SD)', 'β = 0.18', '0.05', '0.08 - 0.28', '0.001', 'Good regulation'],
    ['Mean DERS', 'β = 0.42', '0.06', '0.30 - 0.54', '<0.001', 'Moderate'],
    ['High DERS (+1 SD)', 'β = 0.66', '0.07', '0.52 - 0.80', '<0.001', 'Poor regulation'],
]

slopes_headers = ['DERS Level', 'β', 'SE', '95% CI', 'p-value', 'Interpretation']
col_widths_s = [18, 12, 8, 18, 12, 20]
col_pos_s = [5]
for w in col_widths_s[:-1]:
    col_pos_s.append(col_pos_s[-1] + w)

sh_y = slopes_y - 3
for i, (h, x_p) in enumerate(zip(slopes_headers, col_pos_s)):
    ax.text(x_p + col_widths_s[i]/2, sh_y, h, fontsize=10, fontweight='bold',
            color=COLORS['dark_navy'], ha='center', va='center')

for row_idx, row in enumerate(ders_slopes):
    row_y = sh_y - 2.5 - (row_idx * 2.5)
    bg_color = COLORS['light_gray'] if row_idx % 2 == 0 else 'white'
    rect = mpatches.FancyBboxPatch((4, row_y-1), 92, 2.2,
                                    boxstyle="round,pad=0.01",
                                    facecolor=bg_color, edgecolor=COLORS['light_blue'], linewidth=0.2)
    ax.add_patch(rect)
    for col_idx, (value, x_p) in enumerate(zip(row, col_pos_s)):
        fontweight = 'bold' if col_idx == 0 else 'normal'
        ax.text(x_p + col_widths_s[col_idx]/2, row_y, value, fontsize=9,
                fontweight=fontweight, color=COLORS['dark_navy'], ha='center', va='center')

jn_y = sh_y - 2.5 - (len(ders_slopes) * 2.5) - 2
jn_rect = mpatches.FancyBboxPatch((5, jn_y-2), 90, 3,
                                   boxstyle="round,pad=0.02",
                                   facecolor=COLORS['light_gray'], edgecolor=COLORS['blue'], linewidth=1)
ax.add_patch(jn_rect)
ax.text(50, jn_y, 'Johnson-Neyman: Effect becomes significant at DERS > 68 (42% of sample above threshold)',
        fontsize=10, fontweight='bold', color=COLORS['dark_navy'], ha='center', va='center')

scs_y = jn_y - 6
scs_rect = mpatches.FancyBboxPatch((2, scs_y-1.5), 96, 3.5,
                                    boxstyle="round,pad=0.02",
                                    facecolor=COLORS['cyan'], edgecolor='none')
ax.add_patch(scs_rect)
ax.text(50, scs_y, 'Moderator 2: Self-Control (SCS-B Score)', fontsize=14, fontweight='bold',
        color='white', ha='center', va='center')

scs_model = [
    ['Substance Use Duration', 'β = 0.48', '0.07', '0.34 - 0.62', '<0.001'],
    ['SCS-B Score', 'β = -0.22', '0.06', '-0.34 - -0.10', '<0.001'],
    ['Substance × SCS-B Interaction', 'β = -0.26', '0.08', '-0.42 - -0.10', '0.002'],
    ['Model R²', '0.61', '-', '-', '-'],
    ['Interaction ΔR²', '0.05', '-', '-', '-'],
    ['F-statistic (Interaction)', '18.7', '-', '-', '0.002'],
]

sh_y2 = scs_y - 5
for i, (h, x_p) in enumerate(zip(headers, col_pos_m)):
    ax.text(x_p + col_widths_m[i]/2, sh_y2, h, fontsize=11, fontweight='bold',
            color=COLORS['dark_navy'], ha='center', va='center')

for row_idx, row in enumerate(scs_model):
    row_y = sh_y2 - 2.8 - (row_idx * 2.6)
    bg_color = COLORS['light_gray'] if row_idx % 2 == 0 else 'white'
    rect = mpatches.FancyBboxPatch((2, row_y-1.1), 96, 2.2,
                                    boxstyle="round,pad=0.01",
                                    facecolor=bg_color, edgecolor=COLORS['light_blue'], linewidth=0.3)
    ax.add_patch(rect)
    for col_idx, (value, x_p) in enumerate(zip(row, col_pos_m)):
        fontweight = 'bold' if col_idx == 0 else 'normal'
        color = COLORS['dark_navy']
        if col_idx == 1 and '-' in value and 'β' in value:
            color = '#228B22'
        ax.text(x_p + col_widths_m[col_idx]/2, row_y, value, fontsize=10,
                fontweight=fontweight, color=color, ha='center', va='center')

summary_y = 6
summary_rect = mpatches.FancyBboxPatch((2, summary_y-3), 96, 5,
                                        boxstyle="round,pad=0.02",
                                        facecolor=COLORS['dark_navy'], edgecolor='none')
ax.add_patch(summary_rect)
ax.text(50, summary_y, 'KEY FINDING: High psychological resilience attenuates substance-EAA effects by 50-70%',
        fontsize=12, fontweight='bold', color='white', ha='center', va='center')

ax.text(50, 1, 'DERS: Difficulties in Emotion Regulation Scale | SCS-B: Brief Self-Control Scale',
        fontsize=9, style='italic', color='gray', ha='center')

plt.tight_layout()
plt.savefig('figures/output/supplementary_table_s6.png', dpi=1200, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()

print("Supplementary Table S6 saved to figures/output/supplementary_table_s6.png")
