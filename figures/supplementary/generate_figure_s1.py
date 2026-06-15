#!/usr/bin/env python3
"""
Supplementary Figure S1: Data Processing Pipeline Flowchart
Publication-ready, Q1 journal quality
UNODC color palette: #0A2647, #144272, #205295, #2C74B3, #0077B6
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
import numpy as np

COLORS = {
    'dark_navy': '#0A2647',
    'navy': '#144272',
    'blue': '#205295',
    'light_blue': '#2C74B3',
    'cyan': '#0077B6',
    'white': '#FFFFFF',
    'light_bg': '#F0F4F8',
    'border': '#0A2647'
}

fig = plt.figure(figsize=(20, 28), facecolor='white', dpi=150)
ax = fig.add_axes([0.02, 0.02, 0.96, 0.96])
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')
ax.set_facecolor('white')

def draw_stage_box(ax, x, y, width, height, title, subtitle=None, color='#144272', stage_num=None):
    shadow = FancyBboxPatch((x - width/2 + 0.3, y - height/2 - 0.3), width, height,
                            boxstyle="round,pad=0.01,rounding_size=0.5",
                            facecolor='#C0C0C0', alpha=0.3, edgecolor='none')
    ax.add_patch(shadow)
    
    rect = FancyBboxPatch((x - width/2, y - height/2), width, height,
                          boxstyle="round,pad=0.01,rounding_size=0.5",
                          facecolor=color, edgecolor=COLORS['border'], linewidth=2)
    ax.add_patch(rect)
    
    if stage_num:
        circle = Circle((x - width/2 + 3, y), 2, 
                        facecolor='white', edgecolor=color, linewidth=2)
        ax.add_patch(circle)
        ax.text(x - width/2 + 3, y, str(stage_num), 
                fontsize=18, fontweight='bold', color=color, ha='center', va='center',
                fontfamily='serif')
    
    if subtitle:
        ax.text(x + 2, y + 1.8, title, fontsize=20, fontweight='bold',
                color='white', ha='center', va='center', fontfamily='serif')
        ax.text(x + 2, y - 1.8, subtitle, fontsize=16,
                color='white', ha='center', va='center', fontfamily='serif', style='italic')
    else:
        ax.text(x, y, title, fontsize=20, fontweight='bold',
                color='white', ha='center', va='center', fontfamily='serif')

def draw_sub_box(ax, x, y, width, height, line1, line2):
    rect = FancyBboxPatch((x - width/2, y - height/2), width, height,
                          boxstyle="round,pad=0.01,rounding_size=0.3",
                          facecolor=COLORS['light_bg'], edgecolor=COLORS['navy'], linewidth=1.2)
    ax.add_patch(rect)
    
    ax.text(x, y + 1.5, line1, fontsize=14, fontweight='bold',
            color=COLORS['dark_navy'], ha='center', va='center', fontfamily='serif')
    ax.text(x, y - 1.5, line2, fontsize=12,
            color=COLORS['navy'], ha='center', va='center', fontfamily='serif')

def draw_arrow(ax, x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='-|>', color=COLORS['navy'], 
                               lw=2.5, mutation_scale=18))

ax.text(50, 98, 'Supplementary Figure S1', fontsize=32, fontweight='bold', 
        color=COLORS['dark_navy'], ha='center', va='top', fontfamily='serif')
ax.text(50, 94.5, 'DNA Methylation Data Processing and Analysis Pipeline', fontsize=22, 
        color=COLORS['navy'], ha='center', va='top', fontfamily='serif')

header_rect = FancyBboxPatch((10, 92), 80, 0.3, boxstyle="square",
                              facecolor=COLORS['cyan'], edgecolor='none')
ax.add_patch(header_rect)

y_pos = 87
draw_stage_box(ax, 50, y_pos, 55, 7, 'RAW DATA INPUT', 
               subtitle='15 GEO/ArrayExpress Datasets (n=10,542)', 
               color=COLORS['dark_navy'], stage_num=1)

draw_arrow(ax, 50, y_pos - 3.5, 50, y_pos - 6)

y_pos = 77
draw_stage_box(ax, 50, y_pos, 55, 7, 'IDAT FILE PROCESSING', 
               subtitle='Illumina 450K/EPIC BeadChip Arrays', 
               color=COLORS['navy'], stage_num=2)

draw_arrow(ax, 50, y_pos - 3.5, 50, y_pos - 6)

y_pos = 65
qc_rect = FancyBboxPatch((5, y_pos - 9), 90, 17, boxstyle="round,pad=0.01,rounding_size=0.4",
                          facecolor='white', edgecolor=COLORS['blue'], linewidth=2)
ax.add_patch(qc_rect)

ax.text(10, y_pos + 5.5, '3', fontsize=18, fontweight='bold', 
        color='white', ha='center', va='center', fontfamily='serif',
        bbox=dict(boxstyle='circle,pad=0.4', facecolor=COLORS['blue'], edgecolor='none'))
ax.text(50, y_pos + 5.5, 'QUALITY CONTROL MODULE', fontsize=22, fontweight='bold',
        color=COLORS['blue'], ha='center', va='center', fontfamily='serif')

qc_items = [
    ('Detection p-value', '<0.01 threshold'),
    ('Bisulfite Conversion', '>95% efficiency'),
    ('Sex Prediction', 'getSex() validation'),
    ('Missing Data', '<5% per sample')
]
for i, (title, desc) in enumerate(qc_items):
    x_pos = 16 + i * 23
    draw_sub_box(ax, x_pos, y_pos - 2, 20, 8, title, desc)

draw_arrow(ax, 50, y_pos - 9, 50, y_pos - 12)

y_pos = 47
filter_rect = FancyBboxPatch((5, y_pos - 9), 90, 17, boxstyle="round,pad=0.01,rounding_size=0.4",
                              facecolor='white', edgecolor=COLORS['light_blue'], linewidth=2)
ax.add_patch(filter_rect)

ax.text(10, y_pos + 5.5, '4', fontsize=18, fontweight='bold', 
        color='white', ha='center', va='center', fontfamily='serif',
        bbox=dict(boxstyle='circle,pad=0.4', facecolor=COLORS['light_blue'], edgecolor='none'))
ax.text(50, y_pos + 5.5, 'PROBE FILTERING', fontsize=22, fontweight='bold',
        color=COLORS['light_blue'], ha='center', va='center', fontfamily='serif')

filter_items = [
    ('Cross-reactive', '29,233 removed'),
    ('SNP-affected', 'MAF>0.01'),
    ('Sex Chromosomes', 'X/Y removed'),
    ('Low Detection', 'p>0.01 filtered')
]
for i, (title, desc) in enumerate(filter_items):
    x_pos = 16 + i * 23
    draw_sub_box(ax, x_pos, y_pos - 2, 20, 8, title, desc)

draw_arrow(ax, 50, y_pos - 9, 50, y_pos - 12)

y_pos = 31
draw_stage_box(ax, 27, y_pos, 38, 7, 'NORMALIZATION', 
               subtitle='Functional Normalization', 
               color=COLORS['cyan'], stage_num=5)

draw_stage_box(ax, 73, y_pos, 38, 7, 'BATCH CORRECTION', 
               subtitle='ComBat Empirical Bayes', 
               color=COLORS['cyan'], stage_num=6)

ax.annotate('', xy=(55, y_pos), xytext=(45, y_pos),
            arrowprops=dict(arrowstyle='<->', color=COLORS['navy'], lw=2.5))

draw_arrow(ax, 50, y_pos - 3.5, 50, y_pos - 6)

y_pos = 21
draw_stage_box(ax, 50, y_pos, 60, 7, 'CELL COMPOSITION ESTIMATION', 
               subtitle='Houseman Deconvolution (6 cell types)', 
               color=COLORS['blue'], stage_num=7)

draw_arrow(ax, 50, y_pos - 3.5, 50, y_pos - 6)

y_pos = 9
clock_rect = FancyBboxPatch((3, y_pos - 7), 94, 17, boxstyle="round,pad=0.01,rounding_size=0.4",
                             facecolor=COLORS['light_bg'], edgecolor=COLORS['dark_navy'], linewidth=2.5)
ax.add_patch(clock_rect)

ax.text(8, y_pos + 7.5, '8', fontsize=18, fontweight='bold', 
        color='white', ha='center', va='center', fontfamily='serif',
        bbox=dict(boxstyle='circle,pad=0.4', facecolor=COLORS['dark_navy'], edgecolor='none'))
ax.text(50, y_pos + 7.5, 'EPIGENETIC CLOCK CALCULATION', fontsize=24, fontweight='bold',
        color=COLORS['dark_navy'], ha='center', va='center', fontfamily='serif')

clocks = [
    ('Horvath', '353 CpGs', '2013'),
    ('Hannum', '71 CpGs', '2013'),
    ('PhenoAge', '513 CpGs', '2018'),
    ('GrimAge', '1,030 CpGs', '2019'),
    ('DunedinPACE', '173 CpGs', '2022')
]
for i, (name, cpgs, year) in enumerate(clocks):
    x_pos = 12 + i * 19
    
    clock_box = FancyBboxPatch((x_pos - 8, y_pos - 5), 16, 10,
                                boxstyle="round,pad=0.01,rounding_size=0.3",
                                facecolor='white', edgecolor=COLORS['navy'], linewidth=1.5)
    ax.add_patch(clock_box)
    
    ax.text(x_pos, y_pos + 2, name, fontsize=16, fontweight='bold',
            color=COLORS['dark_navy'], ha='center', va='center', fontfamily='serif')
    ax.text(x_pos, y_pos - 0.5, cpgs, fontsize=14,
            color=COLORS['navy'], ha='center', va='center', fontfamily='serif')
    ax.text(x_pos, y_pos - 3, f'({year})', fontsize=12,
            color=COLORS['light_blue'], ha='center', va='center', fontfamily='serif')

plt.savefig('figures/output/supplementary_figure_s1.png', dpi=600, bbox_inches='tight',
            facecolor='white', edgecolor='none', pad_inches=0.1)
plt.savefig('figures/output/supplementary_figure_s1.pdf', format='pdf', bbox_inches='tight',
            facecolor='white', edgecolor='none', pad_inches=0.1)
plt.close()

print("Supplementary Figure S1 saved!")
