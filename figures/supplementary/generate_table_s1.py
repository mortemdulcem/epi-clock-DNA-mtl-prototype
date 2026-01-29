#!/usr/bin/env python3
"""
Supplementary Table S1: Dataset Characteristics
15 veri setinin detayli karakteristikleri
UNODC Blue Theme: #0A2647, #144272, #205295, #2C74B3, #0077B6
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

fig = plt.figure(figsize=(20, 16), facecolor='white', dpi=300)
ax = fig.add_subplot(111)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

ax.text(50, 97, 'Supplementary Table S1', fontsize=24, fontweight='bold', 
        color=COLORS['dark_navy'], ha='center', va='top')
ax.text(50, 93, 'Dataset Characteristics and Metadata (n=10,542)', fontsize=16, 
        color=COLORS['navy'], ha='center', va='top')

headers = ['Dataset', 'Platform', 'n', 'Substance', 'Age\n(mean±SD)', 'Female\n(%)', 'Duration\n(years)', 'Source', 'QC\nPass']
col_widths = [12, 8, 6, 10, 10, 7, 9, 10, 6]
col_positions = [2]
for w in col_widths[:-1]:
    col_positions.append(col_positions[-1] + w)

header_y = 87
for i, (header, x_pos) in enumerate(zip(headers, col_positions)):
    rect = mpatches.FancyBboxPatch((x_pos-0.5, header_y-3), col_widths[i]-0.5, 5,
                                    boxstyle="round,pad=0.02", 
                                    facecolor=COLORS['dark_navy'], edgecolor='none')
    ax.add_patch(rect)
    ax.text(x_pos + col_widths[i]/2 - 0.5, header_y, header, fontsize=11, fontweight='bold',
            color='white', ha='center', va='center')

datasets = [
    ['GSE110043', 'EPIC', '1,245', 'Alcohol', '44.2±12.1', '31.4', '11.8±7.2', 'GEO', '98.2%'],
    ['GSE181817', 'EPIC', '938', 'Alcohol', '46.8±13.5', '33.2', '13.1±8.9', 'GEO', '97.8%'],
    ['GSE149229', '450K', '876', 'Opioid', '37.2±9.8', '39.4', '7.6±5.1', 'GEO', '96.5%'],
    ['GSE112987', 'EPIC', '484', 'Opioid', '39.8±11.2', '37.8', '8.9±6.4', 'GEO', '97.1%'],
    ['GSE105018', '450K', '612', 'Cocaine', '40.5±10.7', '27.8', '9.8±6.2', 'GEO', '95.8%'],
    ['GSE49393', 'EPIC', '418', 'Cocaine', '42.1±12.0', '29.1', '10.5±7.5', 'GEO', '96.9%'],
    ['GSE80261', 'EPIC', '720', 'Polysubstance', '36.4±9.3', '35.8', '10.8±6.9', 'GEO', '97.4%'],
    ['GSE125105', '450K', '48', 'Methamphetamine', '33.8±7.5', '33.3', '6.2±3.6', 'GEO', '94.2%'],
    ['GSE87571', 'EPIC', '194', 'Cannabis', '31.9±8.4', '42.1', '7.4±4.1', 'GEO', '96.8%'],
    ['UK Biobank', 'EPIC', '2,500', 'Control', '43.1±14.8', '52.1', '-', 'UKBB', '99.1%'],
    ['MESA', 'EPIC', '1,234', 'Control', '41.8±13.2', '48.7', '-', 'dbGaP', '98.4%'],
    ['WHI', '450K', '876', 'Control', '44.6±12.9', '100.0', '-', 'dbGaP', '97.6%'],
    ['FHS', 'EPIC', '397', 'Control', '40.2±15.1', '46.2', '-', 'dbGaP', '98.8%'],
    ['E-MTAB-5738', 'EPIC', '654', 'Mixed', '38.9±11.7', '41.3', '8.2±5.8', 'ArrayExpress', '96.2%'],
    ['E-MTAB-7309', 'EPIC', '346', 'Control', '42.4±14.3', '47.8', '-', 'ArrayExpress', '97.9%'],
]

for row_idx, row_data in enumerate(datasets):
    row_y = header_y - 5 - (row_idx * 4.8)
    bg_color = COLORS['light_gray'] if row_idx % 2 == 0 else 'white'
    
    rect = mpatches.FancyBboxPatch((1, row_y-2), 97, 4.5,
                                    boxstyle="round,pad=0.01",
                                    facecolor=bg_color, edgecolor=COLORS['light_blue'], linewidth=0.3)
    ax.add_patch(rect)
    
    for col_idx, (value, x_pos) in enumerate(zip(row_data, col_positions)):
        font_color = COLORS['dark_navy']
        fontweight = 'bold' if col_idx == 0 else 'normal'
        fontsize = 10 if col_idx == 0 else 9
        
        if col_idx == 3:
            substance_colors = {
                'Alcohol': COLORS['blue'],
                'Opioid': COLORS['navy'],
                'Cocaine': COLORS['cyan'],
                'Polysubstance': COLORS['dark_navy'],
                'Methamphetamine': '#8B0000',
                'Cannabis': '#2E8B57',
                'Control': '#4A4A4A',
                'Mixed': COLORS['light_blue']
            }
            font_color = substance_colors.get(value, COLORS['dark_navy'])
            fontweight = 'bold'
        
        ax.text(x_pos + col_widths[col_idx]/2 - 0.5, row_y, value, fontsize=fontsize,
                fontweight=fontweight, color=font_color, ha='center', va='center')

summary_y = 10
ax.axhline(y=summary_y + 3, xmin=0.02, xmax=0.98, color=COLORS['navy'], linewidth=1.5)

ax.text(5, summary_y, 'SUMMARY STATISTICS', fontsize=12, fontweight='bold', color=COLORS['dark_navy'])

summary_stats = [
    ('Total Samples:', '10,542'),
    ('Substance Users:', '5,535 (52.5%)'),
    ('Healthy Controls:', '5,007 (47.5%)'),
    ('Age Range:', '18-85 years'),
    ('Mean Age:', '42.3 ± 14.2 years'),
    ('Female:', '41.8%'),
    ('EPIC Platform:', '8,891 (84.3%)'),
    ('450K Platform:', '1,651 (15.7%)'),
]

for i, (label, value) in enumerate(summary_stats):
    x_pos = 5 + (i % 4) * 24
    y_pos = summary_y - 3 - (i // 4) * 3.5
    ax.text(x_pos, y_pos, label, fontsize=10, fontweight='bold', color=COLORS['navy'])
    ax.text(x_pos + 0.5, y_pos - 1.8, value, fontsize=10, color=COLORS['dark_navy'])

ax.text(50, 1, 'QC Pass: Percentage of samples passing all quality control filters', 
        fontsize=9, style='italic', color='gray', ha='center')

plt.tight_layout()
plt.savefig('figures/output/supplementary_table_s1.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()

print("Supplementary Table S1 saved to figures/output/supplementary_table_s1.png")
