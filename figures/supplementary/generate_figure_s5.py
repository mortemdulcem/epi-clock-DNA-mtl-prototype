#!/usr/bin/env python3
"""
Supplementary Figure S5: Mediation Path Diagrams
Uc mediyator icin path diyagramlari
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
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

fig, axes = plt.subplots(1, 3, figsize=(20, 8), facecolor='white', dpi=1200)

fig.suptitle('Supplementary Figure S5: Mediation Path Diagrams', 
             fontsize=18, fontweight='bold', color=COLORS['dark_navy'], y=0.98)

mediators = [
    ('Insulin Resistance\n(HOMA-IR)', 'β=0.42***', 'β=0.33***', 'β=0.39***', '26.4%', COLORS['blue']),
    ('HPA Axis\n(Cortisol/ACTH)', 'β=0.38***', 'β=0.24***', 'β=0.44***', '17.0%', COLORS['cyan']),
    ('Systemic Inflammation\n(CRP + IL-6)', 'β=0.45***', 'β=0.36***', 'β=0.37***', '30.2%', COLORS['navy']),
]

def draw_path_diagram(ax, mediator_name, path_a, path_b, direct, mediation_pct, color):
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    iv_rect = FancyBboxPatch((5, 40), 25, 20,
                              boxstyle="round,pad=0.02",
                              facecolor=COLORS['dark_navy'], edgecolor='none')
    ax.add_patch(iv_rect)
    ax.text(17.5, 50, 'Substance\nUse Duration', fontsize=11, fontweight='bold',
            color='white', ha='center', va='center')
    
    med_rect = FancyBboxPatch((37.5, 75), 25, 18,
                               boxstyle="round,pad=0.02",
                               facecolor=color, edgecolor='none')
    ax.add_patch(med_rect)
    ax.text(50, 84, mediator_name, fontsize=10, fontweight='bold',
            color='white', ha='center', va='center')
    
    dv_rect = FancyBboxPatch((70, 40), 25, 20,
                              boxstyle="round,pad=0.02",
                              facecolor=COLORS['dark_navy'], edgecolor='none')
    ax.add_patch(dv_rect)
    ax.text(82.5, 50, 'GrimAge\nEAA', fontsize=11, fontweight='bold',
            color='white', ha='center', va='center')
    
    ax.annotate('', xy=(38, 78), xytext=(28, 58),
                arrowprops=dict(arrowstyle='->', color=color, lw=2.5,
                               connectionstyle='arc3,rad=0.2'))
    ax.text(28, 72, f'Path a\n{path_a}', fontsize=10, fontweight='bold',
            color=color, ha='center', va='center')
    
    ax.annotate('', xy=(72, 58), xytext=(62, 78),
                arrowprops=dict(arrowstyle='->', color=color, lw=2.5,
                               connectionstyle='arc3,rad=0.2'))
    ax.text(72, 72, f'Path b\n{path_b}', fontsize=10, fontweight='bold',
            color=color, ha='center', va='center')
    
    ax.annotate('', xy=(70, 50), xytext=(30, 50),
                arrowprops=dict(arrowstyle='->', color='gray', lw=2, linestyle='--'))
    ax.text(50, 44, f"Direct Effect (c')\n{direct}", fontsize=10, fontweight='bold',
            color='gray', ha='center', va='center')
    
    med_box = FancyBboxPatch((35, 15), 30, 15,
                              boxstyle="round,pad=0.02",
                              facecolor=COLORS['light_gray'], edgecolor=color, linewidth=2)
    ax.add_patch(med_box)
    ax.text(50, 22.5, f'Mediation: {mediation_pct}', fontsize=12, fontweight='bold',
            color=COLORS['dark_navy'], ha='center', va='center')
    
    ax.text(50, 5, '***p<0.001', fontsize=9, style='italic', color='gray', ha='center')

for idx, (med_name, pa, pb, direct, pct, color) in enumerate(mediators):
    draw_path_diagram(axes[idx], med_name, pa, pb, direct, pct, color)

fig.text(0.5, 0.02, 
         'Total Indirect Effect: β = 0.39 | Combined Mediation: 61% | Covariates: Age, Sex, BMI',
         ha='center', fontsize=11, fontweight='bold', color=COLORS['dark_navy'])

plt.tight_layout(rect=[0, 0.05, 1, 0.95])
plt.savefig('figures/output/supplementary_figure_s5.png', dpi=1200, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()

print("Supplementary Figure S5 saved to figures/output/supplementary_figure_s5.png")
