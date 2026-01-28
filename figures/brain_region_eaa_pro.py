"""
EpiClock v4.0 - Brain Region Epigenetic Age Acceleration (PROFESSIONAL VERSION)
High-Tech Scientific Visualization for Q1 Academic Journals
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, Ellipse, Polygon, Arc, Rectangle
from matplotlib.collections import LineCollection
import numpy as np

# UNODC Color Palette
UNODC_PRIMARY = '#0050A0'
UNODC_SECONDARY = '#003366'
UNODC_ACCENT = '#00A7D8'

# High-tech colors
TECH_BG = '#0A1628'
TECH_GRID = '#1E3A5F'
TECH_ACCENT = '#00D4FF'
TECH_GLOW = '#00A7D8'

# Brain region colors (neon-style)
COLOR_PFC = '#FF4081'      # Prefrontal Cortex - magenta
COLOR_NAC = '#7C4DFF'      # Nucleus Accumbens - purple
COLOR_HIPP = '#00E676'     # Hippocampus - green

# Data
regions = ['Prefrontal Cortex', 'Nucleus Accumbens', 'Hippocampus']
n_samples = [48, 36, 24]
eaa_values = [5.3, 4.1, 3.2]
ci_lower = [4.2, 3.2, 2.3]
ci_upper = [6.5, 5.1, 4.2]
functions = ['Executive function\nImpulse control', 'Reward processing\nAddiction center', 'Memory formation\nLearning']

colors = [COLOR_PFC, COLOR_NAC, COLOR_HIPP]

# Create figure with dark theme
fig = plt.figure(figsize=(20, 12), facecolor=TECH_BG)
gs = fig.add_gridspec(1, 2, width_ratios=[1.3, 1], wspace=0.15)

# === PANEL A: High-Tech Brain Schematic ===
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_facecolor(TECH_BG)
ax1.set_xlim(0, 16)
ax1.set_ylim(0, 12)
ax1.set_aspect('equal')
ax1.axis('off')

# Grid lines (tech aesthetic)
for i in range(0, 17, 1):
    ax1.axvline(x=i, color=TECH_GRID, linewidth=0.3, alpha=0.3)
for i in range(0, 13, 1):
    ax1.axhline(y=i, color=TECH_GRID, linewidth=0.3, alpha=0.3)

# Brain outline (sagittal view) - more detailed
theta = np.linspace(0, 2*np.pi, 100)

# Main brain shape
brain_x = 8 + 5.5 * np.cos(theta) * (1 + 0.15*np.cos(2*theta))
brain_y = 6 + 4 * np.sin(theta) * (1 + 0.1*np.sin(3*theta))
ax1.fill(brain_x, brain_y, facecolor='#0D2137', edgecolor=TECH_ACCENT, 
         linewidth=2, alpha=0.8, zorder=1)

# Inner glow effect
for i, alpha in enumerate([0.1, 0.05, 0.02]):
    brain_x_inner = 8 + (5.5 - i*0.3) * np.cos(theta) * (1 + 0.15*np.cos(2*theta))
    brain_y_inner = 6 + (4 - i*0.2) * np.sin(theta) * (1 + 0.1*np.sin(3*theta))
    ax1.fill(brain_x_inner, brain_y_inner, facecolor=TECH_ACCENT, alpha=alpha, zorder=1)

# Cerebellum
cerebellum_x = 12 + 1.5 * np.cos(theta)
cerebellum_y = 2.5 + 1 * np.sin(theta)
ax1.fill(cerebellum_x, cerebellum_y, facecolor='#0D2137', edgecolor=TECH_GRID, 
         linewidth=1.5, alpha=0.6, zorder=1)

# Brain stem
brain_stem = Polygon([(11, 2), (12, 1), (13, 1.5), (12.5, 3)], 
                     facecolor='#0D2137', edgecolor=TECH_GRID, linewidth=1.5, alpha=0.6)
ax1.add_patch(brain_stem)

# === PREFRONTAL CORTEX ===
pfc_x = 4 + 1.8 * np.cos(theta)
pfc_y = 7 + 2.2 * np.sin(theta)
ax1.fill(pfc_x, pfc_y, facecolor=COLOR_PFC, edgecolor='white', linewidth=3, alpha=0.85, zorder=5)
# Glow effect
for i, alpha in enumerate([0.3, 0.15, 0.05]):
    pfc_glow_x = 4 + (1.8 + i*0.4) * np.cos(theta)
    pfc_glow_y = 7 + (2.2 + i*0.4) * np.sin(theta)
    ax1.plot(pfc_glow_x, pfc_glow_y, color=COLOR_PFC, linewidth=2-i*0.5, alpha=alpha, zorder=4)

# PFC Label with data
ax1.text(4, 7, 'PFC', ha='center', va='center', fontsize=16, fontweight='bold', color='white', zorder=6)
ax1.text(4, 6.2, '+5.3 yr', ha='center', va='center', fontsize=11, fontweight='bold', color='white', zorder=6)

# === NUCLEUS ACCUMBENS ===
nac = Circle((7.5, 5), 1.2, facecolor=COLOR_NAC, edgecolor='white', linewidth=3, alpha=0.85, zorder=5)
ax1.add_patch(nac)
# Glow
for i, alpha in enumerate([0.3, 0.15, 0.05]):
    nac_glow = Circle((7.5, 5), 1.2 + i*0.3, facecolor='none', 
                      edgecolor=COLOR_NAC, linewidth=2-i*0.5, alpha=alpha, zorder=4)
    ax1.add_patch(nac_glow)

ax1.text(7.5, 5.2, 'NAc', ha='center', va='center', fontsize=14, fontweight='bold', color='white', zorder=6)
ax1.text(7.5, 4.4, '+4.1 yr', ha='center', va='center', fontsize=10, fontweight='bold', color='white', zorder=6)

# === HIPPOCAMPUS ===
hipp_x = 10 + 1.8 * np.cos(theta)
hipp_y = 4 + 0.9 * np.sin(theta)
# Rotate
angle = -25 * np.pi / 180
hipp_x_rot = 10 + (hipp_x - 10) * np.cos(angle) - (hipp_y - 4) * np.sin(angle)
hipp_y_rot = 4 + (hipp_x - 10) * np.sin(angle) + (hipp_y - 4) * np.cos(angle)
ax1.fill(hipp_x_rot, hipp_y_rot, facecolor=COLOR_HIPP, edgecolor='white', linewidth=3, alpha=0.85, zorder=5)
# Glow
for i, alpha in enumerate([0.3, 0.15, 0.05]):
    hipp_glow_x = 10 + (1.8 + i*0.3) * np.cos(theta)
    hipp_glow_y = 4 + (0.9 + i*0.2) * np.sin(theta)
    hipp_glow_x_rot = 10 + (hipp_glow_x - 10) * np.cos(angle) - (hipp_glow_y - 4) * np.sin(angle)
    hipp_glow_y_rot = 4 + (hipp_glow_x - 10) * np.sin(angle) + (hipp_glow_y - 4) * np.cos(angle)
    ax1.plot(hipp_glow_x_rot, hipp_glow_y_rot, color=COLOR_HIPP, linewidth=2-i*0.5, alpha=alpha, zorder=4)

ax1.text(10, 4.2, 'HIPP', ha='center', va='center', fontsize=12, fontweight='bold', color='white', zorder=6)
ax1.text(10, 3.5, '+3.2 yr', ha='center', va='center', fontsize=10, fontweight='bold', color='white', zorder=6)

# Connection lines (neural pathways)
def draw_connection(ax, start, end, color, style='solid'):
    mid_x = (start[0] + end[0]) / 2
    mid_y = (start[1] + end[1]) / 2 + 0.5
    t = np.linspace(0, 1, 50)
    x = (1-t)**2 * start[0] + 2*(1-t)*t * mid_x + t**2 * end[0]
    y = (1-t)**2 * start[1] + 2*(1-t)*t * mid_y + t**2 * end[1]
    for i, alpha in enumerate([0.6, 0.3, 0.1]):
        ax.plot(x, y, color=color, linewidth=3-i, alpha=alpha, linestyle=style, zorder=3)

draw_connection(ax1, (5.5, 6), (6.5, 5.3), '#FFFFFF')
draw_connection(ax1, (8.5, 4.8), (9, 4.2), '#FFFFFF')

# Data callouts with lines
def draw_callout(ax, region_pos, label_pos, text_lines, color):
    # Connection line
    ax.plot([region_pos[0], label_pos[0]], [region_pos[1], label_pos[1]], 
            color=color, linewidth=1.5, alpha=0.8, linestyle='--', zorder=7)
    ax.scatter([label_pos[0]], [label_pos[1]], s=30, color=color, zorder=8)
    
    # Text box
    box = FancyBboxPatch((label_pos[0] - 1.2, label_pos[1] - 0.8), 2.4, 1.6,
                          boxstyle="round,pad=0.05", facecolor=TECH_BG,
                          edgecolor=color, linewidth=2, alpha=0.95, zorder=8)
    ax1.add_patch(box)
    
    for i, line in enumerate(text_lines):
        ax1.text(label_pos[0], label_pos[1] + 0.3 - i*0.5, line, 
                ha='center', va='center', fontsize=9, color='white', zorder=9)

draw_callout(ax1, (4, 9.2), (2, 11), ['n=48', '95% CI: 4.2-6.5'], COLOR_PFC)
draw_callout(ax1, (7.5, 6.2), (6, 8.5), ['n=36', '95% CI: 3.2-5.1'], COLOR_NAC)
draw_callout(ax1, (11, 4.8), (13, 7), ['n=24', '95% CI: 2.3-4.2'], COLOR_HIPP)

# Title
ax1.text(8, 11.5, 'BRAIN REGION ANALYSIS', ha='center', va='center',
         fontsize=18, fontweight='bold', color=TECH_ACCENT, zorder=10)
ax1.text(8, 10.8, 'Postmortem Epigenetic Age Acceleration', ha='center', va='center',
         fontsize=12, color='#8899AA', style='italic', zorder=10)

# Scale bar
ax1.plot([1, 3], [1, 1], color='white', linewidth=2)
ax1.text(2, 0.5, '~2 cm', ha='center', color='white', fontsize=9)

# === PANEL B: Statistics Dashboard ===
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_facecolor(TECH_BG)
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 12)
ax2.axis('off')

# Grid
for i in range(0, 11, 1):
    ax2.axvline(x=i, color=TECH_GRID, linewidth=0.3, alpha=0.3)
for i in range(0, 13, 1):
    ax2.axhline(y=i, color=TECH_GRID, linewidth=0.3, alpha=0.3)

# Title
ax2.text(5, 11.5, 'STATISTICAL ANALYSIS', ha='center', fontsize=16, 
         fontweight='bold', color=TECH_ACCENT)

# Region cards
def draw_stat_card(ax, x, y, region, eaa, ci_l, ci_u, n, func, color):
    # Card background
    card = FancyBboxPatch((x-2.3, y-1.3), 4.6, 2.6,
                          boxstyle="round,pad=0.05", facecolor='#0D1F30',
                          edgecolor=color, linewidth=2, alpha=0.95)
    ax.add_patch(card)
    
    # Header
    ax.text(x, y + 0.9, region, ha='center', fontsize=12, fontweight='bold', color=color)
    
    # EAA value (large)
    ax.text(x - 1.5, y, f'+{eaa}', ha='center', fontsize=24, fontweight='bold', color='white')
    ax.text(x - 1.5, y - 0.6, 'years', ha='center', fontsize=9, color='#8899AA')
    
    # Stats
    ax.text(x + 1, y + 0.2, f'n = {n}', ha='left', fontsize=10, color='white')
    ax.text(x + 1, y - 0.3, f'95% CI: {ci_l}-{ci_u}', ha='left', fontsize=9, color='#8899AA')
    ax.text(x + 1, y - 0.8, func.replace('\n', ' | '), ha='left', fontsize=8, color='#667788')

draw_stat_card(ax2, 5, 9, 'PREFRONTAL CORTEX', 5.3, 4.2, 6.5, 48, 
               'Executive function | Impulse control', COLOR_PFC)
draw_stat_card(ax2, 5, 6, 'NUCLEUS ACCUMBENS', 4.1, 3.2, 5.1, 36,
               'Reward system | Addiction center', COLOR_NAC)
draw_stat_card(ax2, 5, 3, 'HIPPOCAMPUS', 3.2, 2.3, 4.2, 24,
               'Memory | Learning', COLOR_HIPP)

# ANOVA Box
anova_box = FancyBboxPatch((0.5, 0.3), 4, 1.4, boxstyle="round,pad=0.05",
                            facecolor='#0D1F30', edgecolor=TECH_ACCENT, linewidth=2)
ax2.add_patch(anova_box)
ax2.text(2.5, 1.2, 'ANOVA', ha='center', fontsize=11, fontweight='bold', color=TECH_ACCENT)
ax2.text(2.5, 0.7, 'F = 8.7 | p < 0.001 ***', ha='center', fontsize=10, color='white', fontfamily='monospace')

# Post-hoc Box
posthoc_box = FancyBboxPatch((5.5, 0.3), 4, 1.4, boxstyle="round,pad=0.05",
                              facecolor='#0D1F30', edgecolor='#FF9800', linewidth=2)
ax2.add_patch(posthoc_box)
ax2.text(7.5, 1.2, 'TUKEY HSD', ha='center', fontsize=11, fontweight='bold', color='#FF9800')
ax2.text(7.5, 0.7, 'PFC > NAc > HIPP', ha='center', fontsize=10, color='white', fontfamily='monospace')

# Main figure title
fig.text(0.5, 0.97, 'Figure X. Regional Epigenetic Age Acceleration in Substance Use Disorders',
         ha='center', fontsize=20, fontweight='bold', color='white')
fig.text(0.5, 0.03, 'PMI-corrected Horvath epigenetic clock analysis | Total n=108 postmortem brain samples',
         ha='center', fontsize=11, style='italic', color='#8899AA')

# Save
plt.savefig('figures/brain_region_eaa_pro.png', dpi=300, bbox_inches='tight', 
            facecolor=TECH_BG, edgecolor='none')
plt.savefig('figures/brain_region_eaa_pro.pdf', bbox_inches='tight', 
            facecolor=TECH_BG, edgecolor='none')
print("Brain Region Pro figure saved successfully!")
