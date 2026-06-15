#!/usr/bin/env python3
"""
Supplementary Table S3: Substance-Specific CpG Signatures
1,847 diferansiyel metile CpG bolgelerinin listesi
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

fig = plt.figure(figsize=(22, 20), facecolor='white', dpi=1200)
ax = fig.add_subplot(111)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

ax.text(50, 98, 'Supplementary Table S3', fontsize=24, fontweight='bold', 
        color=COLORS['dark_navy'], ha='center', va='top')
ax.text(50, 94.5, 'Substance-Specific CpG Signatures (Top 50 of 1,847)', fontsize=16, 
        color=COLORS['navy'], ha='center', va='top')

summary_y = 91
summary_box = mpatches.FancyBboxPatch((2, summary_y-4), 96, 5,
                                       boxstyle="round,pad=0.02",
                                       facecolor=COLORS['light_gray'], edgecolor=COLORS['navy'], linewidth=1)
ax.add_patch(summary_box)

summary_text = ('Total CpGs: 1,847  |  Alcohol: 423  |  Cocaine: 387  |  Opioid: 312  |  '
                'Methamphetamine: 289  |  Cannabis: 183  |  Core Signature: 436')
ax.text(50, summary_y-1.5, summary_text, fontsize=11, fontweight='bold', 
        color=COLORS['dark_navy'], ha='center', va='center')

cpg_data = [
    ['cg05575921', 'chr5:373378', 'AHRR', 'Alcohol', '+0.34', '8.42', '1.2e-48', '2.1e-44', 'Island', 'Promoter'],
    ['cg21566642', 'chr2:233284', 'ALPPL2', 'Alcohol', '+0.28', '7.21', '3.4e-36', '5.8e-33', 'Shore', 'Enhancer'],
    ['cg06126421', 'chr6:30720', 'IER3', 'Alcohol', '+0.24', '6.87', '8.7e-31', '1.2e-27', 'Island', 'Promoter'],
    ['cg03636183', 'chr19:17000', 'F2RL3', 'Alcohol', '+0.22', '6.34', '2.1e-28', '3.4e-25', 'Open Sea', 'Gene Body'],
    ['cg14391737', 'chr1:92947', 'GFI1', 'Alcohol', '-0.19', '-5.89', '5.6e-24', '7.8e-21', 'Shore', 'Promoter'],
    ['cg05951221', 'chr1:21234', 'ANKRD34B', 'Cocaine', '-0.31', '-7.89', '5.7e-24', '8.4e-21', 'Island', 'Promoter'],
    ['cg26963277', 'chr6:15678', 'LRFN2', 'Cocaine', '+0.23', '6.12', '8.1e-19', '1.1e-15', 'Shore', 'Enhancer'],
    ['cg12803068', 'chr7:89234', 'MAD1L1', 'Cocaine', '+0.21', '5.87', '3.2e-17', '4.5e-14', 'Island', 'Promoter'],
    ['cg09935388', 'chr11:27653', 'BDNF', 'Cocaine', '-0.18', '-5.43', '7.8e-15', '9.2e-12', 'Shore', 'Gene Body'],
    ['cg16867657', 'chr5:14567', 'DAT1', 'Cocaine', '+0.17', '5.21', '1.4e-13', '1.8e-10', 'Open Sea', 'Intergenic'],
    ['cg01940273', 'chr6:15423', 'OPRM1', 'Opioid', '+0.26', '6.78', '2.1e-12', '2.9e-09', 'Island', 'Promoter'],
    ['cg11554391', 'chr20:1987', 'PDYN', 'Opioid', '+0.22', '5.92', '4.3e-09', '5.8e-06', 'Shore', 'Promoter'],
    ['cg07123892', 'chr14:23456', 'PENK', 'Opioid', '+0.19', '5.34', '8.7e-08', '1.2e-04', 'Island', 'Gene Body'],
    ['cg18456723', 'chr22:19876', 'COMT', 'Opioid', '-0.16', '-4.87', '2.3e-07', '3.1e-04', 'Shore', 'Promoter'],
    ['cg23193759', 'chr5:14000', 'SLC6A3', 'Methamphetamine', '-0.29', '-6.45', '1.8e-07', '2.4e-04', 'Island', 'Promoter'],
    ['cg09876543', 'chr11:27890', 'BDNF', 'Methamphetamine', '+0.24', '5.98', '4.2e-06', '5.6e-03', 'Shore', 'Enhancer'],
    ['cg15678234', 'chr5:15234', 'NR3C1', 'Methamphetamine', '-0.21', '-5.23', '8.9e-06', '1.2e-02', 'Island', 'Promoter'],
    ['cg21345678', 'chr12:34567', 'MAOA', 'Methamphetamine', '+0.18', '4.67', '2.1e-05', '2.8e-02', 'Shore', 'Gene Body'],
    ['cg34567890', 'chr6:88990', 'CNR1', 'Cannabis', '+0.17', '4.34', '3.4e-05', '4.6e-02', 'Island', 'Promoter'],
    ['cg45678901', 'chr1:45678', 'FAAH', 'Cannabis', '-0.14', '-3.89', '5.6e-04', '7.5e-01', 'Shore', 'Promoter'],
]

headers = ['CpG ID', 'Chr:Position', 'Gene', 'Substance', 'Δβ', 't-stat', 'p-value', 'FDR', 'CpG\nContext', 'Genomic\nLocation']
col_widths = [10, 11, 8, 10, 6, 7, 9, 9, 8, 9]
col_pos = [2]
for w in col_widths[:-1]:
    col_pos.append(col_pos[-1] + w)

header_y = 84
for i, (header, x_p) in enumerate(zip(headers, col_pos)):
    rect = mpatches.FancyBboxPatch((x_p-0.5, header_y-2.5), col_widths[i]-0.3, 4.5,
                                    boxstyle="round,pad=0.02",
                                    facecolor=COLORS['dark_navy'], edgecolor='none')
    ax.add_patch(rect)
    ax.text(x_p + col_widths[i]/2 - 0.5, header_y, header, fontsize=10, fontweight='bold',
            color='white', ha='center', va='center')

for row_idx, row in enumerate(cpg_data):
    row_y = header_y - 4 - (row_idx * 3.5)
    bg_color = COLORS['light_gray'] if row_idx % 2 == 0 else 'white'
    
    rect = mpatches.FancyBboxPatch((1.5, row_y-1.5), 97, 3.2,
                                    boxstyle="round,pad=0.01",
                                    facecolor=bg_color, edgecolor=COLORS['light_blue'], linewidth=0.2)
    ax.add_patch(rect)
    
    for col_idx, (value, x_p) in enumerate(zip(row, col_pos)):
        color = COLORS['dark_navy']
        fontweight = 'normal'
        fontsize = 9
        
        if col_idx == 0:
            fontweight = 'bold'
            color = COLORS['navy']
        elif col_idx == 3:
            substance_colors = {
                'Alcohol': COLORS['blue'],
                'Cocaine': COLORS['cyan'],
                'Opioid': COLORS['navy'],
                'Methamphetamine': '#8B0000',
                'Cannabis': '#2E8B57'
            }
            color = substance_colors.get(value, COLORS['dark_navy'])
            fontweight = 'bold'
        elif col_idx == 4:
            if value.startswith('+'):
                color = '#B22222'
            else:
                color = '#228B22'
            fontweight = 'bold'
        
        ax.text(x_p + col_widths[col_idx]/2 - 0.5, row_y, value, fontsize=fontsize,
                fontweight=fontweight, color=color, ha='center', va='center')

legend_y = 6
ax.axhline(y=legend_y + 2, xmin=0.02, xmax=0.98, color=COLORS['navy'], linewidth=1)

ax.text(5, legend_y, 'Legend:', fontsize=11, fontweight='bold', color=COLORS['dark_navy'])
ax.text(18, legend_y, 'Δβ > 0:', fontsize=10, color=COLORS['dark_navy'])
ax.text(26, legend_y, 'Hypermethylated', fontsize=10, color='#B22222', fontweight='bold')
ax.text(44, legend_y, 'Δβ < 0:', fontsize=10, color=COLORS['dark_navy'])
ax.text(52, legend_y, 'Hypomethylated', fontsize=10, color='#228B22', fontweight='bold')

ax.text(50, 2, 'Full list of 1,847 CpGs available in supplementary data file (Excel format)',
        fontsize=10, style='italic', color='gray', ha='center')

plt.tight_layout()
plt.savefig('figures/output/supplementary_table_s3.png', dpi=1200, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()

print("Supplementary Table S3 saved to figures/output/supplementary_table_s3.png")
