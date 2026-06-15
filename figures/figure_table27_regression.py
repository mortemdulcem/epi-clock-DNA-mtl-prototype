#!/usr/bin/env python3
"""
Table 27: Hierarchical Multivariate Regression Analysis - Professional Visualization
Publication-ready for medRxiv submission
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, FancyArrowPatch, Wedge
import numpy as np

# UNODC Blue-Black Color Palette
COLORS = {
    'primary': '#0A2647',
    'secondary': '#144272', 
    'tertiary': '#205295',
    'accent': '#2C74B3',
    'highlight': '#0077B6',
    'text': '#1a1a2e',
    'white': '#FFFFFF',
    'light_bg': '#f0f4f8',
}

# Regression Model Data
models = [
    {'name': 'Model 1', 'vars': 'Age + Sex', 'r2': 0.12, 'delta_r2': None, 'f': None, 'p': None},
    {'name': 'Model 2', 'vars': '+ Substance use duration', 'r2': 0.30, 'delta_r2': 0.18, 'f': 287.4, 'p': '<0.001'},
    {'name': 'Model 3', 'vars': '+ Physiological mediators\n(HOMA-IR, Cortisol/ACTH, Inflammation)', 'r2': 0.37, 'delta_r2': 0.07, 'f': 94.3, 'p': '<0.001'},
    {'name': 'Model 4', 'vars': '+ Psychological moderators\n(DERS, SCS-B)', 'r2': 0.42, 'delta_r2': 0.05, 'f': 67.8, 'p': '<0.001'},
]

# Create figure with two panels
fig = plt.figure(figsize=(20, 14), facecolor='white')

# ============ HEADER ============
ax_header = fig.add_axes([0.02, 0.88, 0.96, 0.10])
ax_header.set_xlim(0, 100)
ax_header.set_ylim(0, 100)
ax_header.axis('off')

header = FancyBboxPatch((0, 10), 100, 80, boxstyle="round,pad=0.01,rounding_size=0.5",
                         facecolor=COLORS['primary'], edgecolor=COLORS['accent'], linewidth=2)
ax_header.add_patch(header)

ax_header.text(50, 65, 'HIERARCHICAL MULTIVARIATE REGRESSION ANALYSIS', ha='center', va='center',
               fontsize=28, fontweight='bold', color='white', fontfamily='serif')
ax_header.text(50, 35, 'Epigenetic Age Acceleration Predictors (n = 3,847)', ha='center', va='center',
               fontsize=18, color=COLORS['highlight'], fontfamily='serif')

# ============ LEFT PANEL - STACKED BAR / R² BUILD-UP ============
ax_left = fig.add_axes([0.05, 0.25, 0.42, 0.58])
ax_left.set_facecolor('white')

# Build cumulative R² visualization
bar_width = 0.6
y_pos = np.arange(4)

# Base R² values for stacking
r2_base = 0.12
r2_substance = 0.18
r2_physio = 0.07
r2_psycho = 0.05

# Horizontal stacked bars showing R² components
colors_stack = [COLORS['secondary'], COLORS['tertiary'], COLORS['accent'], COLORS['highlight']]
labels_stack = ['Demographics\n(Age, Sex)', 'Substance Use\nDuration', 'Physiological\nMediators', 'Psychological\nModerators']
values = [0.12, 0.18, 0.07, 0.05]
cumulative = [0.12, 0.30, 0.37, 0.42]

# Draw stacked horizontal bar
left_pos = 0
for i, (val, col, lab) in enumerate(zip(values, colors_stack, labels_stack)):
    bar = ax_left.barh(0, val, left=left_pos, height=0.5, color=col, edgecolor='white', linewidth=2)
    
    # Label inside bar
    if val >= 0.05:
        ax_left.text(left_pos + val/2, 0, f'{val*100:.0f}%', ha='center', va='center',
                    fontsize=20, fontweight='bold', color='white', fontfamily='serif')
    left_pos += val

# Y-axis label
ax_left.set_yticks([0])
ax_left.set_yticklabels(['Explained\nVariance (R²)'], fontsize=16, fontweight='bold', color=COLORS['primary'])

# X-axis
ax_left.set_xlim(0, 0.5)
ax_left.set_xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])
ax_left.set_xticklabels(['0%', '10%', '20%', '30%', '40%', '50%'], fontsize=14)
ax_left.set_xlabel('Cumulative Explained Variance (R²)', fontsize=16, fontweight='bold', color=COLORS['primary'])

# Title
ax_left.set_title('A. Variance Decomposition', fontsize=18, fontweight='bold', 
                  color=COLORS['primary'], pad=15, loc='left')

# Legend below
legend_y = -0.35
for i, (col, lab, val) in enumerate(zip(colors_stack, labels_stack, values)):
    x_pos = 0.02 + i * 0.12
    rect = Rectangle((x_pos, legend_y), 0.02, 0.08, transform=ax_left.transAxes,
                      facecolor=col, edgecolor='white', linewidth=1)
    ax_left.add_patch(rect)
    ax_left.text(x_pos + 0.025, legend_y + 0.04, f'{lab.replace(chr(10), " ")}: {val*100:.0f}%', 
                transform=ax_left.transAxes, fontsize=12, va='center', color=COLORS['text'])

ax_left.spines['top'].set_visible(False)
ax_left.spines['right'].set_visible(False)
ax_left.spines['left'].set_color(COLORS['primary'])
ax_left.spines['bottom'].set_color(COLORS['primary'])

# ============ RIGHT PANEL - MODEL PROGRESSION ============
ax_right = fig.add_axes([0.55, 0.25, 0.42, 0.58])
ax_right.set_facecolor('white')
ax_right.set_xlim(0, 100)
ax_right.set_ylim(0, 100)
ax_right.axis('off')

ax_right.text(50, 98, 'B. Model Progression', ha='center', va='top',
              fontsize=18, fontweight='bold', color=COLORS['primary'], fontfamily='serif')

# Draw model boxes with arrows
box_height = 18
box_width = 90
start_y = 88

for i, model in enumerate(models):
    y = start_y - i * (box_height + 5)
    
    # Model box
    box_color = colors_stack[i]
    model_box = FancyBboxPatch((5, y - box_height), box_width, box_height,
                                boxstyle="round,pad=0.02,rounding_size=0.5",
                                facecolor=COLORS['white'], edgecolor=box_color, linewidth=3)
    ax_right.add_patch(model_box)
    
    # Color indicator
    indicator = Rectangle((5, y - box_height), 4, box_height, facecolor=box_color, edgecolor='none')
    ax_right.add_patch(indicator)
    
    # Model name
    ax_right.text(12, y - 4, model['name'], fontsize=18, fontweight='bold',
                  color=COLORS['primary'], fontfamily='serif')
    
    # Variables
    ax_right.text(12, y - 10, model['vars'], fontsize=12, color=COLORS['text'],
                  fontfamily='serif', va='top')
    
    # R² value - large
    ax_right.text(70, y - 6, f"R² = {model['r2']:.2f}", fontsize=20, fontweight='bold',
                  color=COLORS['primary'], ha='center', fontfamily='serif')
    
    # Delta R² and stats
    if model['delta_r2']:
        ax_right.text(70, y - 12, f"ΔR² = {model['delta_r2']:.2f}", fontsize=14,
                      color=box_color, ha='center', fontweight='bold', fontfamily='serif')
        ax_right.text(88, y - 6, f"F = {model['f']}", fontsize=12, color=COLORS['text'],
                      ha='center', fontfamily='serif')
        ax_right.text(88, y - 11, f"p {model['p']}", fontsize=12, color=COLORS['tertiary'],
                      ha='center', fontfamily='serif')
    
    # Arrow to next model
    if i < len(models) - 1:
        arrow = FancyArrowPatch((50, y - box_height - 1), (50, y - box_height - 4),
                                arrowstyle='->', mutation_scale=15,
                                color=COLORS['primary'], linewidth=2)
        ax_right.add_patch(arrow)

# ============ BOTTOM SUMMARY ============
ax_bottom = fig.add_axes([0.05, 0.05, 0.90, 0.15])
ax_bottom.set_xlim(0, 100)
ax_bottom.set_ylim(0, 100)
ax_bottom.axis('off')

# Summary box
summary_box = FancyBboxPatch((0, 20), 100, 75, boxstyle="round,pad=0.01,rounding_size=0.5",
                              facecolor=COLORS['primary'], edgecolor=COLORS['accent'], linewidth=2)
ax_bottom.add_patch(summary_box)

ax_bottom.text(50, 80, 'KEY FINDINGS', ha='center', va='center',
               fontsize=18, fontweight='bold', color='white', fontfamily='serif')

ax_bottom.text(50, 58, 'Substance use (18%) + Physiological mediators (7%) + Psychological moderators (5%)',
               ha='center', va='center', fontsize=16, color=COLORS['highlight'], fontfamily='serif')

ax_bottom.text(50, 38, 'Together explain 30% of epigenetic aging variance beyond demographics',
               ha='center', va='center', fontsize=17, fontweight='bold', color='white', fontfamily='serif')

# Footer
ax_bottom.text(50, 8, 'HOMA-IR = Homeostatic Model Assessment for Insulin Resistance | DERS = Difficulties in Emotion Regulation Scale | SCS-B = Self-Compassion Scale',
               ha='center', va='center', fontsize=11, color=COLORS['tertiary'], fontfamily='serif')

plt.savefig('figures/output/table_27_regression.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.savefig('figures/output/table_27_regression.pdf', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("Table 27 - Hierarchical Regression saved!")
plt.close()
