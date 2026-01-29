#!/usr/bin/env python3
"""
Table 14: Tissue pH Performance Evaluation - Professional Schematic
Publication-ready visualization for medRxiv submission
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, FancyArrowPatch
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
    'light_bg': '#f8f9fa',
    'success': '#0A2647',
    'warning': '#205295',
    'danger': '#144272',
}

# pH Category Data
ph_data = [
    {'category': 'Excellent Quality', 'category_tr': 'Mukemmel Kalite', 'range': '>6.5', 'n': 28, 
     'mae': 2.8, 'ci': '2.1-3.6', 'r2': 0.93, 'status': 'Optimal', 'color': COLORS['highlight']},
    {'category': 'Good Quality', 'category_tr': 'Iyi Kalite', 'range': '6.0-6.5', 'n': 42,
     'mae': 3.6, 'ci': '3.0-4.3', 'r2': 0.89, 'status': 'Good', 'color': COLORS['accent']},
    {'category': 'Moderate Quality', 'category_tr': 'Orta Kalite', 'range': '5.5-6.0', 'n': 26,
     'mae': 5.1, 'ci': '4.2-6.1', 'r2': 0.78, 'status': 'Caution', 'color': COLORS['tertiary']},
    {'category': 'Poor Quality', 'category_tr': 'Zayif Kalite', 'range': '<5.5', 'n': 12,
     'mae': 8.4, 'ci': '6.7-10.3', 'r2': 0.52, 'status': 'Not Recommended', 'color': COLORS['secondary']},
]

# Create figure
fig, ax = plt.subplots(figsize=(16, 12), facecolor='white')
ax.set_facecolor('white')
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Title
ax.text(50, 96, 'Table 14. Tissue pH Performance Evaluation', 
        ha='center', va='top', fontsize=24, fontweight='bold', color=COLORS['primary'],
        fontfamily='serif')
ax.text(50, 91, 'Postmortem DNA Methylation Analysis Quality Assessment',
        ha='center', va='top', fontsize=14, color=COLORS['text'], fontfamily='serif')

# pH Scale visualization at top
scale_y = 83
ax.text(10, scale_y + 4, 'pH Scale:', fontsize=12, fontweight='bold', color=COLORS['text'], fontfamily='serif')

# Draw pH gradient bar
for i, ph_val in enumerate(np.linspace(5.0, 7.0, 100)):
    if ph_val > 6.5:
        c = COLORS['highlight']
    elif ph_val > 6.0:
        c = COLORS['accent']
    elif ph_val > 5.5:
        c = COLORS['tertiary']
    else:
        c = COLORS['secondary']
    ax.add_patch(Rectangle((20 + i*0.6, scale_y), 0.6, 3, facecolor=c, edgecolor='none'))

# pH labels
ax.text(20, scale_y - 1.5, '5.0', ha='center', fontsize=10, color=COLORS['text'])
ax.text(50, scale_y - 1.5, '6.0', ha='center', fontsize=10, color=COLORS['text'])
ax.text(80, scale_y - 1.5, '7.0', ha='center', fontsize=10, color=COLORS['text'])

# Category boxes
box_height = 14
start_y = 70
box_width = 88

for i, data in enumerate(ph_data):
    y = start_y - i * (box_height + 2)
    
    # Main category box
    main_box = FancyBboxPatch((6, y - box_height + 2), box_width, box_height - 1,
                               boxstyle="round,pad=0.02,rounding_size=0.8",
                               facecolor=COLORS['white'], edgecolor=data['color'],
                               linewidth=3, alpha=0.95)
    ax.add_patch(main_box)
    
    # Left color indicator
    indicator = Rectangle((6, y - box_height + 2), 4, box_height - 1,
                          facecolor=data['color'], edgecolor='none')
    ax.add_patch(indicator)
    
    # Category name and pH range
    ax.text(12, y - 2, data['category'], fontsize=14, fontweight='bold', 
            color=COLORS['primary'], va='center', fontfamily='serif')
    ax.text(12, y - 6, f"pH {data['range']}", fontsize=11, 
            color=COLORS['text'], va='center', fontfamily='serif')
    ax.text(12, y - 10, f"n = {data['n']}", fontsize=10, 
            color=COLORS['tertiary'], va='center', fontfamily='serif')
    
    # Metrics section
    metrics_x = 42
    
    # MAE
    ax.text(metrics_x, y - 2, 'MAE:', fontsize=10, color=COLORS['text'], 
            va='center', fontfamily='serif')
    ax.text(metrics_x + 8, y - 2, f"{data['mae']} yr", fontsize=12, fontweight='bold',
            color=COLORS['primary'], va='center', fontfamily='serif')
    
    # 95% CI
    ax.text(metrics_x, y - 6, '95% CI:', fontsize=10, color=COLORS['text'],
            va='center', fontfamily='serif')
    ax.text(metrics_x + 10, y - 6, data['ci'], fontsize=11,
            color=COLORS['text'], va='center', fontfamily='serif')
    
    # R²
    ax.text(metrics_x, y - 10, 'R²:', fontsize=10, color=COLORS['text'],
            va='center', fontfamily='serif')
    ax.text(metrics_x + 5, y - 10, f"{data['r2']:.2f}", fontsize=12, fontweight='bold',
            color=COLORS['primary'], va='center', fontfamily='serif')
    
    # Visual R² bar
    bar_x = 65
    bar_width = 20
    # Background bar
    ax.add_patch(Rectangle((bar_x, y - 7), bar_width, 4, 
                           facecolor=COLORS['light_bg'], edgecolor=COLORS['tertiary'], linewidth=1))
    # Filled bar
    ax.add_patch(Rectangle((bar_x, y - 7), bar_width * data['r2'], 4,
                           facecolor=data['color'], edgecolor='none'))
    ax.text(bar_x + bar_width + 1, y - 5, f"{data['r2']*100:.0f}%", fontsize=9,
            color=COLORS['text'], va='center', fontfamily='serif')
    
    # Status indicator
    status_x = 88
    if data['status'] == 'Optimal':
        symbol = 'check_circle'
        status_color = COLORS['highlight']
        symbol_text = 'OPTIMAL'
    elif data['status'] == 'Good':
        symbol = 'check'
        status_color = COLORS['accent']
        symbol_text = 'GOOD'
    elif data['status'] == 'Caution':
        symbol = 'warning'
        status_color = COLORS['tertiary']
        symbol_text = 'CAUTION'
    else:
        symbol = 'x'
        status_color = COLORS['secondary']
        symbol_text = 'NOT REC.'
    
    # Status circle
    circle = Circle((status_x, y - 6), 2.5, facecolor=status_color, edgecolor='white', linewidth=2)
    ax.add_patch(circle)
    ax.text(status_x, y - 6, symbol_text[0], ha='center', va='center', 
            fontsize=8, fontweight='bold', color='white', fontfamily='serif')

# Statistics box at bottom
stats_y = 8
stats_box = FancyBboxPatch((15, stats_y - 5), 70, 10,
                            boxstyle="round,pad=0.02,rounding_size=0.5",
                            facecolor=COLORS['primary'], edgecolor=COLORS['accent'],
                            linewidth=2, alpha=0.95)
ax.add_patch(stats_box)

ax.text(50, stats_y + 2, 'Statistical Analysis', ha='center', va='center',
        fontsize=12, fontweight='bold', color='white', fontfamily='serif')
ax.text(50, stats_y - 2, 'ANOVA: F = 18.4, p < 0.001 (Significant difference in MAE across pH categories)',
        ha='center', va='center', fontsize=11, color='white', fontfamily='serif')

# Legend
legend_y = 2
ax.text(10, legend_y, 'MAE = Mean Absolute Error | CI = Confidence Interval | R² = Coefficient of Determination',
        fontsize=9, color=COLORS['tertiary'], fontfamily='serif')

plt.tight_layout()
plt.savefig('figures/output/table_14_ph_performance.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.savefig('figures/output/table_14_ph_performance.pdf', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("Table 14 pH Performance schematic saved!")
plt.close()
