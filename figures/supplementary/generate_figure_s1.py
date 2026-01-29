#!/usr/bin/env python3
"""
Supplementary Figure S1: Data Processing Pipeline Flowchart
Veri isleme pipeline akis diyagrami
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
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

fig, ax = plt.subplots(figsize=(18, 22), facecolor='white', dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

ax.text(50, 98, 'Supplementary Figure S1', fontsize=20, fontweight='bold', 
        color=COLORS['dark_navy'], ha='center', va='top')
ax.text(50, 95, 'Data Processing Pipeline Flowchart', fontsize=16, 
        color=COLORS['navy'], ha='center', va='top')

def draw_box(ax, x, y, width, height, text, color, text_color='white', fontsize=11, subtext=None):
    rect = FancyBboxPatch((x - width/2, y - height/2), width, height,
                          boxstyle="round,pad=0.02,rounding_size=0.5",
                          facecolor=color, edgecolor=COLORS['dark_navy'], linewidth=1.5)
    ax.add_patch(rect)
    if subtext:
        ax.text(x, y + 1, text, fontsize=fontsize, fontweight='bold',
                color=text_color, ha='center', va='center')
        ax.text(x, y - 1.5, subtext, fontsize=fontsize-2,
                color=text_color, ha='center', va='center', style='italic')
    else:
        ax.text(x, y, text, fontsize=fontsize, fontweight='bold',
                color=text_color, ha='center', va='center')

def draw_arrow(ax, x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=COLORS['navy'], lw=2))

draw_box(ax, 50, 90, 35, 5, 'RAW DATA INPUT', COLORS['dark_navy'], subtext='15 GEO/ArrayExpress Datasets')
draw_arrow(ax, 50, 87.5, 50, 85)

draw_box(ax, 50, 82, 35, 5, 'IDAT FILE PROCESSING', COLORS['navy'], subtext='minfi R package')
draw_arrow(ax, 50, 79.5, 50, 77)

qc_y = 73
draw_box(ax, 50, qc_y, 40, 6, 'QUALITY CONTROL', COLORS['blue'], fontsize=12)

qc_items = ['Detection p-value\n(<0.01)', 'Bisulfite\nConversion (>95%)', 'Sex\nPrediction', 'Missing Data\n(<5%)']
for i, item in enumerate(qc_items):
    x_pos = 20 + i * 20
    draw_box(ax, x_pos, qc_y - 8, 16, 5, item, COLORS['light_gray'], 
             text_color=COLORS['dark_navy'], fontsize=9)
    draw_arrow(ax, 50, qc_y - 3, x_pos, qc_y - 5.5)

draw_arrow(ax, 50, 61, 50, 58)

draw_box(ax, 50, 55, 40, 6, 'PROBE FILTERING', COLORS['blue'], fontsize=12)

filter_items = ['Cross-reactive\nProbes', 'SNP-affected\n(MAF>0.01)', 'Sex Chromosome\nProbes', 'Low Detection\nProbes']
for i, item in enumerate(filter_items):
    x_pos = 20 + i * 20
    draw_box(ax, x_pos, 55 - 8, 16, 5, item, COLORS['light_gray'], 
             text_color=COLORS['dark_navy'], fontsize=9)

draw_arrow(ax, 50, 43.5, 50, 41)

draw_box(ax, 50, 38, 35, 5, 'NORMALIZATION', COLORS['cyan'], subtext='Functional Normalization (funnorm)')
draw_arrow(ax, 50, 35.5, 50, 33)

draw_box(ax, 50, 30, 35, 5, 'BATCH CORRECTION', COLORS['cyan'], subtext='ComBat Empirical Bayes')
draw_arrow(ax, 50, 27.5, 50, 25)

draw_box(ax, 50, 22, 40, 5, 'CELL COMPOSITION', COLORS['light_blue'], 
         subtext='Houseman Reference-based Deconvolution')
draw_arrow(ax, 50, 19.5, 50, 17)

clock_y = 13
draw_box(ax, 50, clock_y, 45, 6, 'EPIGENETIC CLOCK CALCULATION', COLORS['navy'], fontsize=12)

clocks = ['Horvath\n(353 CpG)', 'Hannum\n(71 CpG)', 'PhenoAge\n(513 CpG)', 'GrimAge\n(1030 CpG)', 'DunedinPACE\n(173 CpG)']
for i, clock in enumerate(clocks):
    x_pos = 15 + i * 17.5
    draw_box(ax, x_pos, clock_y - 7, 15, 4.5, clock, COLORS['light_gray'], 
             text_color=COLORS['dark_navy'], fontsize=8)

draw_arrow(ax, 50, 2.5, 50, 0.5)

draw_box(ax, 50, -2, 40, 5, 'STATISTICAL ANALYSIS', COLORS['dark_navy'], 
         subtext='EAA Calculation, ML Classification')

result_rect = FancyBboxPatch((2, -0.5), 96, 4,
                              boxstyle="round,pad=0.02",
                              facecolor='white', edgecolor=COLORS['dark_navy'], linewidth=1, linestyle='--')
ax.add_patch(result_rect)
ax.text(50, 1.5, 'Final Dataset: n=10,542 samples | 773,765 CpGs | 5 Clocks | 6 Substance Categories',
        fontsize=10, fontweight='bold', color=COLORS['dark_navy'], ha='center', va='center')

plt.tight_layout()
plt.savefig('figures/output/supplementary_figure_s1.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()

print("Supplementary Figure S1 saved to figures/output/supplementary_figure_s1.png")
