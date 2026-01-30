#!/usr/bin/env python3
"""
Supplementary Figure S1: Data Processing Pipeline Flowchart
Publication-ready, Q1 journal quality
UNODC color palette: #0A2647, #144272, #205295, #2C74B3, #0077B6
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Polygon
from matplotlib.lines import Line2D
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

fig = plt.figure(figsize=(16, 20), facecolor='white', dpi=300)
ax = fig.add_axes([0.02, 0.02, 0.96, 0.96])
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')
ax.set_facecolor('white')

def draw_stage_box(ax, x, y, width, height, title, subtitle=None, color='#144272', 
                   icon_text=None, stage_num=None):
    shadow = FancyBboxPatch((x - width/2 + 0.3, y - height/2 - 0.3), width, height,
                            boxstyle="round,pad=0.01,rounding_size=0.8",
                            facecolor='#C0C0C0', alpha=0.3, edgecolor='none')
    ax.add_patch(shadow)
    
    rect = FancyBboxPatch((x - width/2, y - height/2), width, height,
                          boxstyle="round,pad=0.01,rounding_size=0.8",
                          facecolor=color, edgecolor=COLORS['border'], linewidth=1.2)
    ax.add_patch(rect)
    
    if stage_num:
        circle = Circle((x - width/2 + 2.5, y + height/2 - 1.5), 1.8, 
                        facecolor='white', edgecolor=color, linewidth=1.5)
        ax.add_patch(circle)
        ax.text(x - width/2 + 2.5, y + height/2 - 1.5, str(stage_num), 
                fontsize=20, fontweight='bold', color=color, ha='center', va='center',
                fontfamily='serif')
    
    if subtitle:
        ax.text(x, y + 0.8, title, fontsize=22, fontweight='bold',
                color='white', ha='center', va='center', fontfamily='serif')
        ax.text(x, y - 1.2, subtitle, fontsize=36,
                color='white', ha='center', va='center', fontfamily='serif', style='italic')
    else:
        ax.text(x, y, title, fontsize=22, fontweight='bold',
                color='white', ha='center', va='center', fontfamily='serif')

def draw_sub_box(ax, x, y, width, height, text, highlight=False):
    color = COLORS['light_bg'] if not highlight else '#E8F4FD'
    border = COLORS['navy'] if not highlight else COLORS['cyan']
    
    rect = FancyBboxPatch((x - width/2, y - height/2), width, height,
                          boxstyle="round,pad=0.01,rounding_size=0.3",
                          facecolor=color, edgecolor=border, linewidth=0.8)
    ax.add_patch(rect)
    
    lines = text.split('\n')
    if len(lines) == 1:
        ax.text(x, y, text, fontsize=16, fontweight='normal',
                color=COLORS['dark_navy'], ha='center', va='center', fontfamily='serif')
    else:
        ax.text(x, y + 0.8, lines[0], fontsize=16, fontweight='bold',
                color=COLORS['dark_navy'], ha='center', va='center', fontfamily='serif')
        ax.text(x, y - 0.8, lines[1], fontsize=14,
                color=COLORS['navy'], ha='center', va='center', fontfamily='serif')

def draw_arrow(ax, x1, y1, x2, y2, style='normal'):
    if style == 'normal':
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='-|>', color=COLORS['navy'], 
                                   lw=1.5, mutation_scale=12))
    elif style == 'branch':
        mid_y = (y1 + y2) / 2
        ax.plot([x1, x1], [y1, mid_y], color=COLORS['navy'], lw=1.2, solid_capstyle='round')
        ax.plot([x1, x2], [mid_y, mid_y], color=COLORS['navy'], lw=1.2, solid_capstyle='round')
        ax.annotate('', xy=(x2, y2), xytext=(x2, mid_y),
                    arrowprops=dict(arrowstyle='-|>', color=COLORS['navy'], 
                                   lw=1.2, mutation_scale=10))

def draw_connector_line(ax, x1, y1, x2, y2):
    ax.plot([x1, x2], [y1, y2], color=COLORS['light_blue'], lw=0.8, 
            linestyle='--', alpha=0.7)

ax.text(50, 98, 'Supplementary Figure S1', fontsize=36, fontweight='bold', 
        color=COLORS['dark_navy'], ha='center', va='top', fontfamily='serif')
ax.text(50, 95.5, 'DNA Methylation Data Processing and Analysis Pipeline', fontsize=26, 
        color=COLORS['navy'], ha='center', va='top', fontfamily='serif')

header_rect = FancyBboxPatch((5, 93), 90, 0.15, boxstyle="square",
                              facecolor=COLORS['cyan'], edgecolor='none')
ax.add_patch(header_rect)

y_pos = 89
draw_stage_box(ax, 50, y_pos, 38, 5.5, 'RAW DATA INPUT', 
               subtitle='15 GEO/ArrayExpress Datasets (n=10,542)', 
               color=COLORS['dark_navy'], stage_num=1)

draw_arrow(ax, 50, y_pos - 2.75, 50, y_pos - 5)

y_pos = 81
draw_stage_box(ax, 50, y_pos, 38, 5.5, 'IDAT FILE PROCESSING', 
               subtitle='Illumina 450K/EPIC BeadChip Arrays', 
               color=COLORS['navy'], stage_num=2)

draw_arrow(ax, 50, y_pos - 2.75, 50, y_pos - 5)

y_pos = 72.5
qc_rect = FancyBboxPatch((8, y_pos - 7), 84, 13, boxstyle="round,pad=0.01,rounding_size=0.5",
                          facecolor='white', edgecolor=COLORS['blue'], linewidth=1.5, linestyle='-')
ax.add_patch(qc_rect)

ax.text(12, y_pos + 4.5, '3', fontsize=20, fontweight='bold', 
        color='white', ha='center', va='center', fontfamily='serif',
        bbox=dict(boxstyle='circle,pad=0.3', facecolor=COLORS['blue'], edgecolor='none'))
ax.text(50, y_pos + 4.5, 'QUALITY CONTROL MODULE', fontsize=24, fontweight='bold',
        color=COLORS['blue'], ha='center', va='center', fontfamily='serif')

qc_items = [
    ('Detection p-value', '<0.01 threshold'),
    ('Bisulfite Conversion', '>95% efficiency'),
    ('Sex Prediction', 'getSex() validation'),
    ('Missing Data', '<5% per sample')
]
for i, (title, desc) in enumerate(qc_items):
    x_pos = 17 + i * 22
    draw_sub_box(ax, x_pos, y_pos - 1.5, 18, 5, f'{title}\n{desc}')

draw_arrow(ax, 50, y_pos - 7, 50, y_pos - 10)

y_pos = 57
filter_rect = FancyBboxPatch((8, y_pos - 7), 84, 13, boxstyle="round,pad=0.01,rounding_size=0.5",
                              facecolor='white', edgecolor=COLORS['light_blue'], linewidth=1.5)
ax.add_patch(filter_rect)

ax.text(12, y_pos + 4.5, '4', fontsize=20, fontweight='bold', 
        color='white', ha='center', va='center', fontfamily='serif',
        bbox=dict(boxstyle='circle,pad=0.3', facecolor=COLORS['light_blue'], edgecolor='none'))
ax.text(50, y_pos + 4.5, 'PROBE FILTERING', fontsize=24, fontweight='bold',
        color=COLORS['light_blue'], ha='center', va='center', fontfamily='serif')

filter_items = [
    ('Cross-reactive', '29,233 probes removed'),
    ('SNP-affected', 'MAF>0.01 excluded'),
    ('Sex Chromosomes', 'X/Y probes removed'),
    ('Low Detection', 'p>0.01 filtered')
]
for i, (title, desc) in enumerate(filter_items):
    x_pos = 17 + i * 22
    draw_sub_box(ax, x_pos, y_pos - 1.5, 18, 5, f'{title}\n{desc}')

draw_arrow(ax, 50, y_pos - 7, 50, y_pos - 10)

y_pos = 44
draw_stage_box(ax, 30, y_pos, 30, 5.5, 'NORMALIZATION', 
               subtitle='Functional Normalization (funnorm)', 
               color=COLORS['cyan'], stage_num=5)

draw_stage_box(ax, 70, y_pos, 30, 5.5, 'BATCH CORRECTION', 
               subtitle='ComBat Empirical Bayes', 
               color=COLORS['cyan'], stage_num=6)

ax.annotate('', xy=(53, y_pos), xytext=(47, y_pos),
            arrowprops=dict(arrowstyle='<->', color=COLORS['navy'], lw=1.5))

draw_arrow(ax, 50, y_pos - 2.75, 50, y_pos - 5.5)

y_pos = 35
draw_stage_box(ax, 50, y_pos, 42, 5.5, 'CELL COMPOSITION ESTIMATION', 
               subtitle='Houseman Reference-based Deconvolution (6 cell types)', 
               color=COLORS['blue'], stage_num=7)

draw_arrow(ax, 50, y_pos - 2.75, 50, y_pos - 5.5)

y_pos = 24
clock_rect = FancyBboxPatch((5, y_pos - 9), 90, 16, boxstyle="round,pad=0.01,rounding_size=0.5",
                             facecolor=COLORS['light_bg'], edgecolor=COLORS['dark_navy'], linewidth=2)
ax.add_patch(clock_rect)

ax.text(9, y_pos + 5.5, '8', fontsize=20, fontweight='bold', 
        color='white', ha='center', va='center', fontfamily='serif',
        bbox=dict(boxstyle='circle,pad=0.3', facecolor=COLORS['dark_navy'], edgecolor='none'))
ax.text(50, y_pos + 5.5, 'EPIGENETIC CLOCK CALCULATION', fontsize=26, fontweight='bold',
        color=COLORS['dark_navy'], ha='center', va='center', fontfamily='serif')

clocks = [
    ('Horvath', '353 CpGs', '2013'),
    ('Hannum', '71 CpGs', '2013'),
    ('PhenoAge', '513 CpGs', '2018'),
    ('GrimAge', '1,030 CpGs', '2019'),
    ('DunedinPACE', '173 CpGs', '2022')
]
for i, (name, cpgs, year) in enumerate(clocks):
    x_pos = 14 + i * 18
    
    clock_box = FancyBboxPatch((x_pos - 7.5, y_pos - 6.5), 15, 9,
                                boxstyle="round,pad=0.01,rounding_size=0.4",
                                facecolor='white', edgecolor=COLORS['navy'], linewidth=1)
    ax.add_patch(clock_box)
    
    ax.text(x_pos, y_pos + 0.5, name, fontsize=20, fontweight='bold',
            color=COLORS['dark_navy'], ha='center', va='center', fontfamily='serif')
    ax.text(x_pos, y_pos - 1.8, cpgs, fontsize=16,
            color=COLORS['navy'], ha='center', va='center', fontfamily='serif')
    ax.text(x_pos, y_pos - 3.8, f'({year})', fontsize=14,
            color=COLORS['light_blue'], ha='center', va='center', fontfamily='serif')

draw_arrow(ax, 50, y_pos - 9, 50, y_pos - 12)

y_pos = 7
output_rect = FancyBboxPatch((5, y_pos - 5), 90, 10, boxstyle="round,pad=0.01,rounding_size=0.5",
                              facecolor=COLORS['dark_navy'], edgecolor=COLORS['border'], linewidth=2)
ax.add_patch(output_rect)

ax.text(9, y_pos + 3.5, '9', fontsize=20, fontweight='bold', 
        color=COLORS['dark_navy'], ha='center', va='center', fontfamily='serif',
        bbox=dict(boxstyle='circle,pad=0.3', facecolor='white', edgecolor='none'))
ax.text(50, y_pos + 3.5, 'STATISTICAL ANALYSIS & OUTPUT', fontsize=26, fontweight='bold',
        color='white', ha='center', va='center', fontfamily='serif')

outputs = [
    'EAA Calculation',
    'ML Classification',
    'Differential Analysis',
    'Clinical Reports'
]
for i, output in enumerate(outputs):
    x_pos = 17 + i * 22
    ax.text(x_pos, y_pos - 0.5, output, fontsize=36, fontweight='bold',
            color='white', ha='center', va='center', fontfamily='serif')

final_rect = FancyBboxPatch((15, y_pos - 4.2), 70, 2.5,
                             boxstyle="round,pad=0.01,rounding_size=0.3",
                             facecolor=COLORS['cyan'], edgecolor='white', linewidth=1)
ax.add_patch(final_rect)
ax.text(50, y_pos - 3, 'Final Dataset: n = 10,542 samples  |  773,765 CpGs  |  5 Clocks  |  6 Substance Categories',
        fontsize=36, fontweight='bold', color='white', ha='center', va='center', fontfamily='serif')

legend_items = [
    (COLORS['dark_navy'], 'Input/Output'),
    (COLORS['navy'], 'Core Processing'),
    (COLORS['blue'], 'Quality & Analysis'),
    (COLORS['light_blue'], 'Filtering'),
    (COLORS['cyan'], 'Normalization/Results')
]

legend_y = 1.5
ax.text(5, legend_y, 'Pipeline Stages:', fontsize=16, fontweight='bold',
        color=COLORS['dark_navy'], ha='left', va='center', fontfamily='serif')

for i, (color, label) in enumerate(legend_items):
    x_pos = 22 + i * 16
    rect = Rectangle((x_pos - 1.5, legend_y - 0.6), 2.5, 1.2, 
                     facecolor=color, edgecolor='none')
    ax.add_patch(rect)
    ax.text(x_pos + 2, legend_y, label, fontsize=14,
            color=COLORS['dark_navy'], ha='left', va='center', fontfamily='serif')

plt.savefig('figures/output/supplementary_figure_s1.png', dpi=1200, bbox_inches='tight',
            facecolor='white', edgecolor='none', pad_inches=0.1)
plt.savefig('figures/output/supplementary_figure_s1.pdf', format='pdf', bbox_inches='tight',
            facecolor='white', edgecolor='none', pad_inches=0.1)
plt.close()

print("Supplementary Figure S1 saved - Publication quality!")
print("  - PNG: figures/output/supplementary_figure_s1.png (1200 DPI)")
print("  - PDF: figures/output/supplementary_figure_s1.pdf")
