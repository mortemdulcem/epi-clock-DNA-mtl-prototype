"""
EpiClock v4.0 - Brain Region EAA with Real Anatomical Image
Professional Publication-Ready Visualization
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, Ellipse, Rectangle
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
import numpy as np

# UNODC Color Palette
UNODC_PRIMARY = '#0050A0'
UNODC_SECONDARY = '#003366'
UNODC_ACCENT = '#00A7D8'

# Region colors
COLOR_PFC = '#FF1744'      # Prefrontal Cortex - red
COLOR_NAC = '#AA00FF'      # Nucleus Accumbens - purple  
COLOR_HIPP = '#00E676'     # Hippocampus - green
COLOR_VTA = '#FF9100'      # VTA - orange
COLOR_AMY = '#2979FF'      # Amygdala - blue

# Data
regions_data = {
    'Prefrontal Cortex (PFC)': {'eaa': 5.3, 'ci': (4.2, 6.5), 'n': 48, 'color': COLOR_PFC, 
                                 'pos': (0.78, 0.72), 'label_pos': (0.92, 0.88)},
    'Nucleus Accumbens (NAc)': {'eaa': 4.1, 'ci': (3.2, 5.1), 'n': 36, 'color': COLOR_NAC,
                                 'pos': (0.52, 0.42), 'label_pos': (0.15, 0.55)},
    'Hippocampus (HIPP)': {'eaa': 3.2, 'ci': (2.3, 4.2), 'n': 24, 'color': COLOR_HIPP,
                           'pos': (0.38, 0.48), 'label_pos': (0.08, 0.35)},
    'Amygdala (AMY)': {'eaa': 3.5, 'ci': (2.6, 4.4), 'n': 21, 'color': COLOR_AMY,
                       'pos': (0.48, 0.35), 'label_pos': (0.15, 0.15)},
    'VTA': {'eaa': 2.8, 'ci': (1.9, 3.7), 'n': 18, 'color': COLOR_VTA,
            'pos': (0.28, 0.38), 'label_pos': (0.08, 0.68)},
}

# Create figure
fig = plt.figure(figsize=(20, 12), facecolor='white')
gs = fig.add_gridspec(1, 2, width_ratios=[1.4, 1], wspace=0.08)

# === PANEL A: Brain Image with Overlays ===
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_facecolor('black')

# Load brain image
brain_img = mpimg.imread('figures/brain_anatomy.jpg')
ax1.imshow(brain_img, aspect='auto')

# Get image dimensions for coordinate mapping
img_h, img_w = brain_img.shape[:2]

# Add region markers with glow effect
for region, data in regions_data.items():
    x = data['pos'][0] * img_w
    y = (1 - data['pos'][1]) * img_h  # Flip y for image coords
    
    # Outer glow
    for r, alpha in [(45, 0.15), (35, 0.25), (25, 0.4)]:
        circle = Circle((x, y), r, facecolor=data['color'], alpha=alpha, zorder=5)
        ax1.add_patch(circle)
    
    # Inner marker
    circle = Circle((x, y), 18, facecolor=data['color'], edgecolor='white', 
                    linewidth=3, alpha=0.95, zorder=10)
    ax1.add_patch(circle)
    
    # EAA value on marker
    ax1.text(x, y, f"+{data['eaa']}", ha='center', va='center', 
            fontsize=9, fontweight='bold', color='white', zorder=11)

# Add annotation lines and labels
for region, data in regions_data.items():
    x = data['pos'][0] * img_w
    y = (1 - data['pos'][1]) * img_h
    lx = data['label_pos'][0] * img_w
    ly = (1 - data['label_pos'][1]) * img_h
    
    # Connection line
    ax1.plot([x, lx], [y, ly], color='white', linewidth=1.5, alpha=0.8, zorder=8)
    
    # Label box
    short_name = region.split('(')[1].rstrip(')') if '(' in region else region
    label_text = f"{short_name}\n+{data['eaa']} yr\nn={data['n']}"
    
    bbox = dict(boxstyle='round,pad=0.4', facecolor=data['color'], 
                edgecolor='white', linewidth=2, alpha=0.9)
    ax1.text(lx, ly, label_text, ha='center', va='center', fontsize=9,
            fontweight='bold', color='white', bbox=bbox, zorder=12)

ax1.set_xlim(0, img_w)
ax1.set_ylim(img_h, 0)
ax1.axis('off')
ax1.set_title('A. Sagittal Brain Section - Regional EAA Mapping', fontsize=14, 
              fontweight='bold', color=UNODC_SECONDARY, loc='left', pad=15)

# === PANEL B: Statistics Dashboard ===
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_facecolor('#F8F9FA')
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 12)
ax2.axis('off')
ax2.set_title('B. Regional EAA Statistics', fontsize=14, 
              fontweight='bold', color=UNODC_SECONDARY, loc='left', pad=15)

# Bar chart
regions = list(regions_data.keys())
eaa_vals = [d['eaa'] for d in regions_data.values()]
colors = [d['color'] for d in regions_data.values()]
ci_vals = [d['ci'] for d in regions_data.values()]
n_vals = [d['n'] for d in regions_data.values()]

# Sort by EAA
sorted_idx = np.argsort(eaa_vals)[::-1]
regions_sorted = [regions[i] for i in sorted_idx]
eaa_sorted = [eaa_vals[i] for i in sorted_idx]
colors_sorted = [colors[i] for i in sorted_idx]
ci_sorted = [ci_vals[i] for i in sorted_idx]
n_sorted = [n_vals[i] for i in sorted_idx]

# Draw horizontal bars
bar_height = 1.2
y_positions = [10 - i*2 for i in range(len(regions_sorted))]

for i, (y_pos, region, eaa, color, ci, n) in enumerate(zip(y_positions, regions_sorted, 
                                                            eaa_sorted, colors_sorted, ci_sorted, n_sorted)):
    # Bar
    bar = Rectangle((0.5, y_pos - bar_height/2), eaa * 1.2, bar_height,
                    facecolor=color, edgecolor='white', linewidth=2, alpha=0.9)
    ax2.add_patch(bar)
    
    # Error bar
    ci_low = (eaa - ci[0]) * 1.2
    ci_high = (ci[1] - eaa) * 1.2
    ax2.errorbar(0.5 + eaa * 1.2, y_pos, xerr=[[ci_low], [ci_high]], 
                fmt='none', color='black', capsize=4, capthick=2, linewidth=2)
    
    # Region name
    short_name = region.split('(')[1].rstrip(')') if '(' in region else region
    ax2.text(0.3, y_pos, short_name, ha='right', va='center', fontsize=11, fontweight='bold')
    
    # Value and n
    ax2.text(0.5 + eaa * 1.2 + 0.8, y_pos, f'+{eaa} yr (n={n})', 
            ha='left', va='center', fontsize=10, fontweight='bold', color=UNODC_SECONDARY)

# X-axis
ax2.plot([0.5, 8], [0.3, 0.3], color='black', linewidth=1.5)
for tick in [0, 2, 4, 6]:
    ax2.plot([0.5 + tick*1.2, 0.5 + tick*1.2], [0.2, 0.4], color='black', linewidth=1)
    ax2.text(0.5 + tick*1.2, -0.1, f'{tick}', ha='center', fontsize=9)
ax2.text(4, -0.6, 'EAA (years)', ha='center', fontsize=11, fontweight='bold')

# Statistics box
stats_box = FancyBboxPatch((0.3, -3.5), 9.4, 2.8, boxstyle='round,pad=0.05',
                            facecolor='white', edgecolor=UNODC_PRIMARY, linewidth=2)
ax2.add_patch(stats_box)

stats_text = """STATISTICAL ANALYSIS
────────────────────────────────────────
ANOVA: F(4,142) = 12.4, p < 0.001 ***
Post-hoc Tukey HSD:
  PFC > NAc (p = 0.021*)  |  PFC > HIPP (p < 0.001***)
  NAc > VTA (p = 0.043*)  |  AMY vs HIPP (p = 0.52, ns)
Total n = 147 postmortem samples"""

ax2.text(5, -2.1, stats_text, ha='center', va='center', fontsize=9,
        fontfamily='monospace', color=UNODC_SECONDARY)

# Extend y limits to show stats box
ax2.set_ylim(-4, 12)

# Main title
fig.suptitle('Figure X. Brain Region-Specific Epigenetic Age Acceleration in Substance Use Disorders',
             fontsize=18, fontweight='bold', color=UNODC_SECONDARY, y=0.97)

# Footer
fig.text(0.5, 0.02, 
         'PMI-corrected Horvath epigenetic clock | Postmortem brain samples | Error bars: 95% CI | '
         'Image: Human brain sagittal section',
         ha='center', fontsize=10, style='italic', color='gray')

plt.tight_layout(rect=[0, 0.04, 1, 0.94])

# Save
plt.savefig('figures/brain_region_eaa_real.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('figures/brain_region_eaa_real.pdf', bbox_inches='tight', facecolor='white')
print("Real brain EAA figure saved!")
