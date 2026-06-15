#!/usr/bin/env python3
"""
Supplementary Table S2: Quality Control Metrics
Kalite kontrol metrikleri detaylari
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

fig = plt.figure(figsize=(20, 18), facecolor='white', dpi=1200)
ax = fig.add_subplot(111)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

ax.text(50, 98, 'Supplementary Table S2', fontsize=24, fontweight='bold', 
        color=COLORS['dark_navy'], ha='center', va='top')
ax.text(50, 94.5, 'Quality Control Metrics', fontsize=16, 
        color=COLORS['navy'], ha='center', va='top')

section1_y = 90
rect1 = mpatches.FancyBboxPatch((2, section1_y-2), 96, 4,
                                 boxstyle="round,pad=0.02",
                                 facecolor=COLORS['dark_navy'], edgecolor='none')
ax.add_patch(rect1)
ax.text(50, section1_y, 'A. Sample-Level Quality Control', fontsize=14, fontweight='bold',
        color='white', ha='center', va='center')

sample_qc_data = [
    ['Metric', 'Threshold', 'Samples Tested', 'Pass Rate', 'Failed', 'Action'],
    ['Detection p-value', '<0.01 mean', '10,542', '97.8%', '232', 'Excluded'],
    ['Bisulfite Conversion', '>95%', '10,542', '99.2%', '84', 'Excluded'],
    ['Sex Prediction', 'Match reported', '10,542', '99.6%', '42', 'Corrected'],
    ['PC Outlier Score', '<3 SD', '10,310', '98.4%', '165', 'Flagged'],
    ['Missing Data', '<5%', '10,145', '99.1%', '91', 'Imputed'],
]

headers_y = section1_y - 5
col_widths_s = [20, 16, 14, 12, 10, 14]
col_pos_s = [3]
for w in col_widths_s[:-1]:
    col_pos_s.append(col_pos_s[-1] + w)

for row_idx, row in enumerate(sample_qc_data):
    row_y = headers_y - (row_idx * 4)
    bg_color = COLORS['dark_navy'] if row_idx == 0 else (COLORS['light_gray'] if row_idx % 2 == 1 else 'white')
    text_color = 'white' if row_idx == 0 else COLORS['dark_navy']
    
    rect = mpatches.FancyBboxPatch((2, row_y - 1.8), 96, 3.5,
                                    boxstyle="round,pad=0.01",
                                    facecolor=bg_color, edgecolor=COLORS['light_blue'], linewidth=0.3)
    ax.add_patch(rect)
    
    for col_idx, (value, x_pos) in enumerate(zip(row, col_pos_s)):
        fontweight = 'bold' if row_idx == 0 or col_idx == 0 else 'normal'
        ax.text(x_pos + col_widths_s[col_idx]/2 - 1, row_y, value, fontsize=10,
                fontweight=fontweight, color=text_color, ha='center', va='center')

section2_y = section1_y - 30
rect2 = mpatches.FancyBboxPatch((2, section2_y-2), 96, 4,
                                 boxstyle="round,pad=0.02",
                                 facecolor=COLORS['dark_navy'], edgecolor='none')
ax.add_patch(rect2)
ax.text(50, section2_y, 'B. Probe-Level Quality Control', fontsize=14, fontweight='bold',
        color='white', ha='center', va='center')

probe_qc_data = [
    ['Filter Category', 'EPIC Probes', '450K Probes', 'Total Removed', 'Justification'],
    ['Low Detection (>5% samples)', '8,234', '4,127', '12,361', 'Unreliable signal'],
    ['Cross-Reactive Probes', '44,210', '29,233', '73,443', 'Chen et al., 2013'],
    ['SNP-Affected (MAF>0.01)', '18,765', '11,234', '29,999', 'Genetic confounding'],
    ['Sex Chromosome Probes', '19,681', '11,648', '31,329', 'Sex bias removal'],
    ['Non-CpG Probes', '2,876', '2,876', '2,876', 'Non-CpG methylation'],
    ['Probes After Filtering', '773,765', '406,459', '-', 'Final analysis set'],
]

headers_y2 = section2_y - 5
col_widths_p = [24, 14, 14, 16, 24]
col_pos_p = [3]
for w in col_widths_p[:-1]:
    col_pos_p.append(col_pos_p[-1] + w)

for row_idx, row in enumerate(probe_qc_data):
    row_y = headers_y2 - (row_idx * 4)
    bg_color = COLORS['dark_navy'] if row_idx == 0 else (COLORS['light_gray'] if row_idx % 2 == 1 else 'white')
    text_color = 'white' if row_idx == 0 else COLORS['dark_navy']
    
    rect = mpatches.FancyBboxPatch((2, row_y - 1.8), 96, 3.5,
                                    boxstyle="round,pad=0.01",
                                    facecolor=bg_color, edgecolor=COLORS['light_blue'], linewidth=0.3)
    ax.add_patch(rect)
    
    for col_idx, (value, x_pos) in enumerate(zip(row, col_pos_p)):
        fontweight = 'bold' if row_idx == 0 or col_idx == 0 else 'normal'
        ax.text(x_pos + col_widths_p[col_idx]/2 - 1, row_y, value, fontsize=10,
                fontweight=fontweight, color=text_color, ha='center', va='center')

section3_y = section2_y - 35
rect3 = mpatches.FancyBboxPatch((2, section3_y-2), 96, 4,
                                 boxstyle="round,pad=0.02",
                                 facecolor=COLORS['dark_navy'], edgecolor='none')
ax.add_patch(rect3)
ax.text(50, section3_y, 'C. Batch Effect Correction (ComBat)', fontsize=14, fontweight='bold',
        color='white', ha='center', va='center')

batch_data = [
    ['Principal Component', 'Pre-Correction\nVariance (%)', 'Post-Correction\nVariance (%)', 'Reduction', 'Batch Association\n(p-value pre)', 'Batch Association\n(p-value post)'],
    ['PC1', '32.4%', '8.7%', '-73.1%', '<1e-50', '0.42'],
    ['PC2', '18.6%', '6.2%', '-66.7%', '<1e-42', '0.31'],
    ['PC3', '11.3%', '4.8%', '-57.5%', '<1e-28', '0.18'],
    ['PC4', '7.8%', '3.9%', '-50.0%', '<1e-15', '0.24'],
    ['PC5', '5.2%', '3.1%', '-40.4%', '<1e-8', '0.56'],
]

headers_y3 = section3_y - 5
col_widths_b = [18, 16, 16, 12, 18, 18]
col_pos_b = [2]
for w in col_widths_b[:-1]:
    col_pos_b.append(col_pos_b[-1] + w)

for row_idx, row in enumerate(batch_data):
    row_y = headers_y3 - (row_idx * 4.5)
    bg_color = COLORS['dark_navy'] if row_idx == 0 else (COLORS['light_gray'] if row_idx % 2 == 1 else 'white')
    text_color = 'white' if row_idx == 0 else COLORS['dark_navy']
    
    rect = mpatches.FancyBboxPatch((1, row_y - 2), 98, 4,
                                    boxstyle="round,pad=0.01",
                                    facecolor=bg_color, edgecolor=COLORS['light_blue'], linewidth=0.3)
    ax.add_patch(rect)
    
    for col_idx, (value, x_pos) in enumerate(zip(row, col_pos_b)):
        fontweight = 'bold' if row_idx == 0 or col_idx == 0 else 'normal'
        color = text_color
        if row_idx > 0 and col_idx == 3:
            color = '#228B22'
        ax.text(x_pos + col_widths_b[col_idx]/2, row_y, value, fontsize=9,
                fontweight=fontweight, color=color, ha='center', va='center')

ax.text(50, 2, 'Note: ComBat empirical Bayes batch correction successfully removed batch effects while preserving biological variation.',
        fontsize=9, style='italic', color='gray', ha='center')

plt.tight_layout()
plt.savefig('figures/output/supplementary_table_s2.png', dpi=1200, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()

print("Supplementary Table S2 saved to figures/output/supplementary_table_s2.png")
