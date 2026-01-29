#!/usr/bin/env python3
"""
Table 14: Tissue pH Performance Evaluation - Postmortem Forensic Theme
Publication-ready visualization for medRxiv submission
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, FancyArrowPatch, Polygon, Wedge
import numpy as np

# UNODC Blue-Black Color Palette - Forensic/Postmortem Theme
COLORS = {
    'primary': '#0A2647',
    'secondary': '#144272', 
    'tertiary': '#205295',
    'accent': '#2C74B3',
    'highlight': '#0077B6',
    'text': '#1a1a2e',
    'white': '#FFFFFF',
    'light_bg': '#f0f4f8',
    'dark_bg': '#0d1b2a',
}

# pH Category Data
ph_data = [
    {'category': 'Excellent Quality', 'range': '>6.5', 'n': 28, 
     'mae': 2.8, 'ci': '2.1-3.6', 'r2': 0.93, 'status': 'OPTIMAL', 'color': COLORS['highlight']},
    {'category': 'Good Quality', 'range': '6.0-6.5', 'n': 42,
     'mae': 3.6, 'ci': '3.0-4.3', 'r2': 0.89, 'status': 'GOOD', 'color': COLORS['accent']},
    {'category': 'Moderate Quality', 'range': '5.5-6.0', 'n': 26,
     'mae': 5.1, 'ci': '4.2-6.1', 'r2': 0.78, 'status': 'CAUTION', 'color': COLORS['tertiary']},
    {'category': 'Poor Quality', 'range': '<5.5', 'n': 12,
     'mae': 8.4, 'ci': '6.7-10.3', 'r2': 0.52, 'status': 'NOT REC.', 'color': COLORS['secondary']},
]

# Create figure
fig = plt.figure(figsize=(18, 14), facecolor='white')

# Main axes
ax = fig.add_axes([0.02, 0.02, 0.96, 0.96])
ax.set_facecolor('white')
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# ============ HEADER SECTION ============
# Dark header bar
header = FancyBboxPatch((2, 88), 96, 10, boxstyle="round,pad=0.01,rounding_size=0.5",
                         facecolor=COLORS['primary'], edgecolor=COLORS['accent'], linewidth=2)
ax.add_patch(header)

# Title
ax.text(50, 94, 'POSTMORTEM TISSUE pH ANALYSIS', ha='center', va='center',
        fontsize=22, fontweight='bold', color='white', fontfamily='serif')
ax.text(50, 90, 'DNA Methylation Clock Performance by Tissue Acidification Level',
        ha='center', va='center', fontsize=12, color=COLORS['highlight'], fontfamily='serif')

# ============ LEFT PANEL - TISSUE DEGRADATION DIAGRAM ============
# Panel border
left_panel = FancyBboxPatch((3, 25), 30, 60, boxstyle="round,pad=0.01,rounding_size=0.3",
                             facecolor=COLORS['light_bg'], edgecolor=COLORS['primary'], linewidth=2)
ax.add_patch(left_panel)

ax.text(18, 83, 'Postmortem Tissue', ha='center', va='center',
        fontsize=13, fontweight='bold', color=COLORS['primary'], fontfamily='serif')
ax.text(18, 80, 'pH Degradation Timeline', ha='center', va='center',
        fontsize=10, color=COLORS['text'], fontfamily='serif')

# Draw tissue sample containers (test tubes/vials)
tube_x = [10, 18, 26]
tube_colors = [COLORS['highlight'], COLORS['tertiary'], COLORS['secondary']]
tube_labels = ['Fresh\n0-6h', 'Moderate\n12-24h', 'Degraded\n>48h']
tube_ph = ['pH 6.8', 'pH 5.8', 'pH 5.2']

for i, (x, col, label, ph) in enumerate(zip(tube_x, tube_colors, tube_labels, tube_ph)):
    # Tube body
    tube = FancyBboxPatch((x-3, 50), 6, 20, boxstyle="round,pad=0.01,rounding_size=0.3",
                          facecolor='white', edgecolor=COLORS['primary'], linewidth=2)
    ax.add_patch(tube)
    
    # Liquid level (decreasing pH = more degraded)
    liquid_height = 18 - i * 4
    liquid = Rectangle((x-2.5, 50.5), 5, liquid_height, facecolor=col, alpha=0.7)
    ax.add_patch(liquid)
    
    # Tube cap
    cap = Rectangle((x-3.5, 70), 7, 3, facecolor=COLORS['primary'], edgecolor=COLORS['accent'], linewidth=1)
    ax.add_patch(cap)
    
    # Labels
    ax.text(x, 46, label, ha='center', va='top', fontsize=8, color=COLORS['text'], fontfamily='serif')
    ax.text(x, 55 + liquid_height/2, ph, ha='center', va='center', fontsize=9, 
            fontweight='bold', color='white', fontfamily='serif')

# PMI Arrow
ax.annotate('', xy=(28, 40), xytext=(8, 40),
            arrowprops=dict(arrowstyle='->', color=COLORS['primary'], lw=2))
ax.text(18, 37, 'PMI (Postmortem Interval)', ha='center', va='center',
        fontsize=9, color=COLORS['primary'], fontfamily='serif', style='italic')

# pH decrease indicator
ax.text(18, 32, 'Tissue Acidification', ha='center', va='center',
        fontsize=10, fontweight='bold', color=COLORS['secondary'], fontfamily='serif')
ax.text(18, 29, 'pH 7.0 → 5.0', ha='center', va='center',
        fontsize=11, color=COLORS['text'], fontfamily='serif')

# ============ RIGHT PANEL - pH CATEGORIES TABLE ============
right_x = 36
panel_width = 62

# Panel header
table_header = FancyBboxPatch((right_x, 78), panel_width, 7, 
                               boxstyle="round,pad=0.01,rounding_size=0.3",
                               facecolor=COLORS['primary'], edgecolor=COLORS['accent'], linewidth=2)
ax.add_patch(table_header)

# Header text
headers = ['pH Category', 'Range', 'n', 'MAE', '95% CI', 'R²', 'Status']
header_x = [right_x+8, right_x+22, right_x+30, right_x+38, right_x+48, right_x+56, right_x+62]
for hx, htxt in zip(header_x, headers):
    ax.text(hx, 81.5, htxt, ha='center', va='center', fontsize=10, 
            fontweight='bold', color='white', fontfamily='serif')

# Data rows
row_height = 12
for i, data in enumerate(ph_data):
    y = 75 - i * row_height
    
    # Row background (alternating)
    row_bg = FancyBboxPatch((right_x, y - row_height + 2), panel_width, row_height - 1,
                             boxstyle="round,pad=0.01,rounding_size=0.2",
                             facecolor='white' if i % 2 == 0 else COLORS['light_bg'],
                             edgecolor=data['color'], linewidth=2)
    ax.add_patch(row_bg)
    
    # Color indicator bar
    indicator = Rectangle((right_x, y - row_height + 2), 2, row_height - 1,
                          facecolor=data['color'], edgecolor='none')
    ax.add_patch(indicator)
    
    # Data values
    row_y = y - row_height/2 + 1
    ax.text(right_x + 8, row_y, data['category'], ha='center', va='center',
            fontsize=10, fontweight='bold', color=COLORS['primary'], fontfamily='serif')
    ax.text(right_x + 22, row_y, f"pH {data['range']}", ha='center', va='center',
            fontsize=10, color=COLORS['text'], fontfamily='serif')
    ax.text(right_x + 30, row_y, str(data['n']), ha='center', va='center',
            fontsize=10, color=COLORS['text'], fontfamily='serif')
    ax.text(right_x + 38, row_y, f"{data['mae']} yr", ha='center', va='center',
            fontsize=10, fontweight='bold', color=COLORS['primary'], fontfamily='serif')
    ax.text(right_x + 48, row_y, data['ci'], ha='center', va='center',
            fontsize=10, color=COLORS['text'], fontfamily='serif')
    ax.text(right_x + 56, row_y, f"{data['r2']:.2f}", ha='center', va='center',
            fontsize=10, fontweight='bold', color=COLORS['primary'], fontfamily='serif')
    
    # Status badge
    badge = FancyBboxPatch((right_x + 57, row_y - 2.5), 10, 5,
                            boxstyle="round,pad=0.01,rounding_size=0.3",
                            facecolor=data['color'], edgecolor='white', linewidth=1)
    ax.add_patch(badge)
    ax.text(right_x + 62, row_y, data['status'], ha='center', va='center',
            fontsize=7, fontweight='bold', color='white', fontfamily='serif')

# ============ BOTTOM SECTION - STATISTICS & LEGEND ============
# Statistics box
stats_box = FancyBboxPatch((36, 8), 62, 14, boxstyle="round,pad=0.01,rounding_size=0.3",
                            facecolor=COLORS['primary'], edgecolor=COLORS['accent'], linewidth=2)
ax.add_patch(stats_box)

ax.text(67, 18, 'STATISTICAL ANALYSIS', ha='center', va='center',
        fontsize=12, fontweight='bold', color='white', fontfamily='serif')
ax.text(67, 14, 'ANOVA: F(3,104) = 18.4, p < 0.001 ***', ha='center', va='center',
        fontsize=11, color=COLORS['highlight'], fontfamily='serif')
ax.text(67, 10.5, 'Significant difference in MAE across tissue pH categories', ha='center', va='center',
        fontsize=10, color='white', fontfamily='serif')

# Forensic note
note_box = FancyBboxPatch((3, 8), 30, 14, boxstyle="round,pad=0.01,rounding_size=0.3",
                           facecolor=COLORS['light_bg'], edgecolor=COLORS['tertiary'], linewidth=2)
ax.add_patch(note_box)

ax.text(18, 18, 'FORENSIC NOTE', ha='center', va='center',
        fontsize=11, fontweight='bold', color=COLORS['primary'], fontfamily='serif')
ax.text(18, 14, 'PMI-corrected Horvath clock', ha='center', va='center',
        fontsize=9, color=COLORS['text'], fontfamily='serif')
ax.text(18, 11, 'Total n = 108 postmortem samples', ha='center', va='center',
        fontsize=9, color=COLORS['text'], fontfamily='serif')

# Footer legend
ax.text(50, 4, 'MAE = Mean Absolute Error | CI = Confidence Interval | R² = Coefficient of Determination | PMI = Postmortem Interval',
        ha='center', va='center', fontsize=8, color=COLORS['tertiary'], fontfamily='serif')

plt.savefig('figures/output/table_14_ph_performance.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.savefig('figures/output/table_14_ph_performance.pdf', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("Table 14 - Postmortem pH Performance saved!")
plt.close()
