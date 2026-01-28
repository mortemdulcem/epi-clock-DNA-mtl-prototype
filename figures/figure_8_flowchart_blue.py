"""
EpiClock v4.0 - Figure 8: Clinical Decision Flowchart
Blue-Black Color Scheme - Publication Ready
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

# Blue-Black Color Palette
COLORS = {
    'primary': '#0A2647',
    'secondary': '#144272',
    'accent': '#205295',
    'light': '#2C74B3',
    'highlight': '#0077B6',
    'text': '#1E293B',
    'bg': '#F8FAFC',
}

fig, ax = plt.subplots(figsize=(16, 14), facecolor='white')
ax.set_facecolor('white')
ax.set_xlim(0, 16)
ax.set_ylim(0, 14)
ax.axis('off')

def draw_box(ax, x, y, w, h, text, color, text_color='white'):
    box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                          boxstyle='round,pad=0.05', facecolor=color,
                          edgecolor='white', linewidth=3)
    ax.add_patch(box)
    ax.text(x, y, text, ha='center', va='center', fontsize=10, 
            fontweight='bold', color=text_color, wrap=True)

def draw_diamond(ax, x, y, size, text, color):
    diamond = plt.Polygon([(x, y+size), (x+size, y), (x, y-size), (x-size, y)],
                          facecolor=color, edgecolor='white', linewidth=3)
    ax.add_patch(diamond)
    ax.text(x, y, text, ha='center', va='center', fontsize=9, 
            fontweight='bold', color='white', wrap=True)

def draw_arrow(ax, start, end, color=COLORS['secondary']):
    ax.annotate('', xy=end, xytext=start,
                arrowprops=dict(arrowstyle='->', color=color, lw=2.5,
                               connectionstyle='arc3,rad=0'))

# Title
ax.text(8, 13.5, 'Clinical Decision Algorithm for EAA Assessment',
        ha='center', fontsize=18, fontweight='bold', color=COLORS['primary'])

# Level 1: Patient Entry
draw_box(ax, 8, 12, 4, 1, 'Patient Presents\nfor EAA Assessment', COLORS['primary'])

draw_arrow(ax, (8, 11.5), (8, 10.8))

# Level 2: Sample Collection
draw_box(ax, 8, 10.3, 4.5, 1, 'Collect DNA Sample\n(Blood/Saliva)', COLORS['secondary'])

draw_arrow(ax, (8, 9.8), (8, 9.1))

# Level 3: Analysis
draw_box(ax, 8, 8.6, 4, 1, 'DNA Methylation\nAnalysis', COLORS['accent'])

draw_arrow(ax, (8, 8.1), (8, 7.2))

# Level 4: Decision Diamond
draw_diamond(ax, 8, 6.5, 0.8, 'EAA > 5\nyears?', COLORS['light'])

# Branches
draw_arrow(ax, (7.2, 6.5), (5, 6.5))  # No
draw_arrow(ax, (8.8, 6.5), (11, 6.5))  # Yes

ax.text(6, 6.8, 'No', fontsize=11, fontweight='bold', color=COLORS['text'])
ax.text(10, 6.8, 'Yes', fontsize=11, fontweight='bold', color=COLORS['text'])

# Level 5a: Low Risk
draw_box(ax, 3.5, 5.5, 3.5, 1.2, 'Low-Moderate Risk\nRoutine Monitoring\n(Annual)', COLORS['accent'])

# Level 5b: High Risk
draw_box(ax, 12.5, 5.5, 3.5, 1.2, 'High Risk\nIntensive Intervention\nRequired', COLORS['primary'])

draw_arrow(ax, (3.5, 4.9), (3.5, 4.2))
draw_arrow(ax, (12.5, 4.9), (12.5, 4.2))

# Level 6a: Lifestyle
draw_box(ax, 3.5, 3.5, 3.5, 1.2, 'Lifestyle\nRecommendations\n(Diet, Exercise)', COLORS['light'])

# Level 6b: Clinical Intervention
draw_box(ax, 12.5, 3.5, 3.5, 1.2, 'Clinical Intervention\nSubstance Cessation\nMultidisciplinary Care', COLORS['secondary'])

draw_arrow(ax, (3.5, 2.9), (3.5, 2.2))
draw_arrow(ax, (12.5, 2.9), (12.5, 2.2))

# Level 7: Follow-up
draw_box(ax, 3.5, 1.5, 3, 1, 'Follow-up\n12 months', COLORS['highlight'])
draw_box(ax, 12.5, 1.5, 3, 1, 'Follow-up\n3-6 months', COLORS['primary'])

# Connect to re-assessment
draw_arrow(ax, (5, 1.5), (7, 1.5))
draw_arrow(ax, (11, 1.5), (9, 1.5))

draw_box(ax, 8, 1.5, 2.5, 0.8, 'Re-assess\nEAA', COLORS['accent'])

# Arrows back up
ax.annotate('', xy=(8, 6), xytext=(8, 1.9),
            arrowprops=dict(arrowstyle='->', color=COLORS['secondary'], lw=2,
                           connectionstyle='arc3,rad=0.3', linestyle='--'))

# Legend
legend_y = 13.2
ax.text(1, legend_y, 'Risk Categories:', fontsize=11, fontweight='bold', color=COLORS['text'])
for i, (label, color) in enumerate([('Routine', COLORS['light']), ('Elevated', COLORS['accent']), 
                                     ('High', COLORS['secondary']), ('Critical', COLORS['primary'])]):
    rect = Rectangle((1 + i*2.5, legend_y - 0.6), 0.4, 0.3, facecolor=color, edgecolor='white', linewidth=1)
    ax.add_patch(rect)
    ax.text(1.5 + i*2.5, legend_y - 0.45, label, fontsize=9, va='center')

# Footer
fig.text(0.5, 0.02, 'Based on multi-clock EAA assessment | Thresholds validated in n=10,542 samples',
         ha='center', fontsize=10, style='italic', color='gray')

plt.savefig('figures/output/figure_8_flowchart.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('figures/output/figure_8_flowchart.pdf', bbox_inches='tight', facecolor='white')
print("Figure 8 saved!")
