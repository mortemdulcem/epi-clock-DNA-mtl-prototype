"""
EpiClock v4.0 - Clinical Decision Flowchart
Epigenetic Age Acceleration Intervention Decision Tree
UNODC Corporate Standards Compliant
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, ConnectionPatch
import numpy as np

# UNODC Color Palette
UNODC_PRIMARY = '#0050A0'
UNODC_SECONDARY = '#003366'
UNODC_ACCENT = '#00A7D8'

# Severity colors
COLOR_MILD = '#E8F5E9'
COLOR_MILD_BORDER = '#2E7D32'
COLOR_MODERATE = '#FFF8E1'
COLOR_MODERATE_BORDER = '#FF8F00'
COLOR_SEVERE = '#FFEBEE'
COLOR_SEVERE_BORDER = '#C62828'
COLOR_NEUTRAL = '#F5F5F5'
COLOR_DECISION = '#E1F5FE'

def draw_box(ax, x, y, width, height, text, facecolor, edgecolor, 
             fontsize=10, fontweight='normal', linestyle='-', linewidth=2):
    """Draw a rounded rectangle box with text"""
    box = FancyBboxPatch((x - width/2, y - height/2), width, height,
                          boxstyle="round,pad=0.02,rounding_size=0.02",
                          facecolor=facecolor, edgecolor=edgecolor,
                          linewidth=linewidth, linestyle=linestyle,
                          transform=ax.transData, zorder=2)
    ax.add_patch(box)
    ax.text(x, y, text, ha='center', va='center', fontsize=fontsize,
            fontweight=fontweight, wrap=True, zorder=3,
            color=UNODC_SECONDARY if fontweight == 'bold' else '#333333')
    return box

def draw_diamond(ax, x, y, size, text, facecolor, edgecolor):
    """Draw a decision diamond"""
    diamond = plt.Polygon([(x, y+size), (x+size, y), (x, y-size), (x-size, y)],
                          facecolor=facecolor, edgecolor=edgecolor,
                          linewidth=2, zorder=2)
    ax.add_patch(diamond)
    ax.text(x, y, text, ha='center', va='center', fontsize=11,
            fontweight='bold', color=UNODC_SECONDARY, zorder=3)

def draw_arrow(ax, start, end, color='#666666'):
    """Draw an arrow between two points"""
    ax.annotate('', xy=end, xytext=start,
                arrowprops=dict(arrowstyle='->', color=color, lw=1.5),
                zorder=1)

# Figure setup
fig, ax = plt.subplots(figsize=(18, 14), facecolor='white')
ax.set_xlim(0, 18)
ax.set_ylim(0, 14)
ax.set_aspect('equal')
ax.axis('off')

# Title
ax.text(9, 13.5, 'Clinical Decision Tree for Epigenetic Age Acceleration Management',
        ha='center', va='center', fontsize=18, fontweight='bold', color=UNODC_PRIMARY)
ax.text(9, 13.0, 'Evidence-Based Intervention Selection Algorithm',
        ha='center', va='center', fontsize=12, style='italic', color='#666666')

# === LEVEL 1: Starting node ===
draw_box(ax, 9, 11.5, 3.5, 0.8, 'Epigenetic Age\nAcceleration (EAA)', 
         COLOR_NEUTRAL, '#333333', fontsize=12, fontweight='bold')

# Arrow to decision
draw_arrow(ax, (9, 11.1), (9, 10.3))

# === LEVEL 2: Decision diamond ===
draw_diamond(ax, 9, 9.5, 0.7, 'EAA\nSeverity?', COLOR_DECISION, UNODC_PRIMARY)

# === LEVEL 3: Severity branches ===
# Mild (left)
draw_arrow(ax, (8.3, 9.5), (4.5, 8.2))
ax.text(5.8, 9.1, 'Mild\n(+1-3 yr)', ha='center', va='center', fontsize=10, 
        color=COLOR_MILD_BORDER, fontweight='bold')
draw_box(ax, 4.5, 7.5, 3.2, 0.9, 'Lifestyle\nInterventions',
         COLOR_MILD, COLOR_MILD_BORDER, fontsize=11, fontweight='bold')

# Moderate (center)
draw_arrow(ax, (9, 8.8), (9, 8.2))
ax.text(9.8, 8.5, 'Moderate\n(+3-5 yr)', ha='left', va='center', fontsize=10,
        color=COLOR_MODERATE_BORDER, fontweight='bold')
draw_box(ax, 9, 7.5, 3.2, 0.9, 'Combined\nIntervention',
         COLOR_MODERATE, COLOR_MODERATE_BORDER, fontsize=11, fontweight='bold')

# Severe (right)
draw_arrow(ax, (9.7, 9.5), (13.5, 8.2))
ax.text(12.2, 9.1, 'Severe\n(>5 yr)', ha='center', va='center', fontsize=10,
        color=COLOR_SEVERE_BORDER, fontweight='bold')
draw_box(ax, 13.5, 7.5, 3.2, 0.9, 'Combined +\nSubstance Cessation',
         COLOR_SEVERE, COLOR_SEVERE_BORDER, fontsize=11, fontweight='bold')

# === LEVEL 4: Specific interventions ===
# Mild interventions
draw_arrow(ax, (3.5, 7.0), (3, 6.0))
draw_arrow(ax, (5.5, 7.0), (6, 6.0))

draw_box(ax, 3, 5.3, 2.4, 1.0, 'Exercise\n-2.87 years',
         COLOR_MILD, COLOR_MILD_BORDER, fontsize=10)
draw_box(ax, 6, 5.3, 2.4, 1.0, 'Dietary\nModification\n-3.23 years',
         COLOR_MILD, COLOR_MILD_BORDER, fontsize=10)

# Moderate intervention
draw_arrow(ax, (9, 7.0), (9, 6.0))
draw_box(ax, 9, 5.3, 3.5, 1.2, 'Diet + Exercise +\nStress Management\n-4.60 years',
         COLOR_MODERATE, COLOR_MODERATE_BORDER, fontsize=10)

# Severe interventions
draw_arrow(ax, (12.5, 7.0), (12, 6.0))
draw_arrow(ax, (14.5, 7.0), (15, 6.0))

draw_box(ax, 12, 5.3, 2.6, 1.0, 'Combined\nIntervention\n-4.60 years',
         COLOR_SEVERE, COLOR_SEVERE_BORDER, fontsize=10)
draw_box(ax, 15, 5.3, 2.6, 1.0, 'Substance\nCessation\n-3.18 years',
         COLOR_SEVERE, COLOR_SEVERE_BORDER, fontsize=10)

# === LEVEL 5: Expected outcomes ===
# Mild outcome
draw_arrow(ax, (3, 4.8), (4.5, 3.5))
draw_arrow(ax, (6, 4.8), (4.5, 3.5))
draw_box(ax, 4.5, 2.8, 3.5, 1.0, 'Expected Improvement:\n-2.5 to -3.0 years',
         COLOR_MILD, COLOR_MILD_BORDER, fontsize=10, linestyle='--', linewidth=1.5)

# Moderate outcome
draw_arrow(ax, (9, 4.7), (9, 3.5))
draw_box(ax, 9, 2.8, 3.5, 1.0, 'Expected Improvement:\n-3.5 to -4.5 years',
         COLOR_MODERATE, COLOR_MODERATE_BORDER, fontsize=10, linestyle='--', linewidth=1.5)

# Severe outcome
draw_arrow(ax, (12, 4.8), (13.5, 3.5))
draw_arrow(ax, (15, 4.8), (13.5, 3.5))
draw_box(ax, 13.5, 2.8, 3.5, 1.0, 'Expected Improvement:\n-4.0 to -5.0 years',
         COLOR_SEVERE, COLOR_SEVERE_BORDER, fontsize=10, linestyle='--', linewidth=1.5)

# === Legend ===
legend_y = 1.3
legend_x = 1.5

ax.text(legend_x, legend_y + 0.6, 'Severity Classification', fontsize=11, 
        fontweight='bold', color=UNODC_SECONDARY)

# Mild legend
mild_patch = FancyBboxPatch((legend_x, legend_y), 0.4, 0.3,
                             boxstyle="round,pad=0.02", facecolor=COLOR_MILD, 
                             edgecolor=COLOR_MILD_BORDER, linewidth=1.5)
ax.add_patch(mild_patch)
ax.text(legend_x + 0.6, legend_y + 0.15, 'Mild (+1-3 years)', fontsize=9, va='center')

# Moderate legend
mod_patch = FancyBboxPatch((legend_x + 3, legend_y), 0.4, 0.3,
                            boxstyle="round,pad=0.02", facecolor=COLOR_MODERATE, 
                            edgecolor=COLOR_MODERATE_BORDER, linewidth=1.5)
ax.add_patch(mod_patch)
ax.text(legend_x + 3.6, legend_y + 0.15, 'Moderate (+3-5 years)', fontsize=9, va='center')

# Severe legend
sev_patch = FancyBboxPatch((legend_x + 6.5, legend_y), 0.4, 0.3,
                            boxstyle="round,pad=0.02", facecolor=COLOR_SEVERE, 
                            edgecolor=COLOR_SEVERE_BORDER, linewidth=1.5)
ax.add_patch(sev_patch)
ax.text(legend_x + 7.1, legend_y + 0.15, 'Severe (>5 years)', fontsize=9, va='center')

# Evidence note
ax.text(legend_x + 10, legend_y + 0.15, 'Dashed boxes = Expected outcomes', 
        fontsize=9, style='italic', color='#666666')

# Footer
ax.text(9, 0.4, 'Note: Effect sizes based on meta-analysis of 6 studies (n=473). '
        'Individual responses may vary. Clinical judgment should guide final decisions.',
        ha='center', fontsize=9, style='italic', color='#666666')

# Source
ax.text(0.5, 0.1, 'Source: EpiClock v4.0 Meta-Analysis Database',
        ha='left', fontsize=8, color='#9CA3AF', fontfamily='monospace')

plt.tight_layout()

# Save
plt.savefig('figures/clinical_decision_flowchart.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.savefig('figures/clinical_decision_flowchart.pdf', bbox_inches='tight',
            facecolor='white', edgecolor='none')

print("Clinical decision flowchart saved successfully!")
