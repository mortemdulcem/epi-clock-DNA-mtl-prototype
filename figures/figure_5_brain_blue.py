"""
EpiClock v4.0 - Figure 5: Brain Region EAA
Blue-Black Color Scheme - Using provided anatomical illustration
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, Ellipse, Rectangle
import matplotlib.image as mpimg
import numpy as np

# Blue-Black Color Palette (gradient)
BLUES = ['#0A2647', '#144272', '#205295', '#2C74B3', '#0077B6']
COLORS = {
    'primary': '#0A2647',
    'secondary': '#144272',
    'accent': '#205295',
    'light': '#2C74B3',
    'highlight': '#0077B6',
    'text': '#1E293B',
    'bg': '#F8FAFC',
}

# Data - positions with CLEAR SEPARATION - labels far outside for visibility
regions_data = {
    'Prefrontal Cortex': {'eaa': 5.3, 'ci': (4.2, 6.5), 'n': 48, 'color': BLUES[0], 
                          'pos': (0.18, 0.32), 'label_pos': (-0.20, 0.25)},  # Far left bottom
    'Nucleus Accumbens': {'eaa': 4.1, 'ci': (3.2, 5.1), 'n': 36, 'color': BLUES[1],
                          'pos': (0.32, 0.48), 'label_pos': (-0.20, 0.55)},  # Left middle
    'Hippocampus': {'eaa': 3.2, 'ci': (2.3, 4.2), 'n': 24, 'color': BLUES[2],
                    'pos': (0.65, 0.52), 'label_pos': (1.15, 0.45)},  # Right lower
    'Amygdala': {'eaa': 3.5, 'ci': (2.6, 4.4), 'n': 21, 'color': BLUES[3],
                 'pos': (0.48, 0.58), 'label_pos': (1.15, 0.72)},  # Right upper
    'VTA': {'eaa': 2.8, 'ci': (1.9, 3.7), 'n': 18, 'color': BLUES[4],
            'pos': (0.45, 0.72), 'label_pos': (-0.20, 0.85)},  # Left top
}

fig = plt.figure(figsize=(24, 14), facecolor='white')
gs = fig.add_gridspec(1, 2, width_ratios=[1.4, 1], wspace=0.08)

# Panel A: Brain Image
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_facecolor('white')

brain_img = mpimg.imread('figures/brain_realistic.png')
ax1.imshow(brain_img, aspect='auto')

img_h, img_w = brain_img.shape[:2]

# Region markers - simple numbered circles
marker_num = 1
for region, data in regions_data.items():
    x = data['pos'][0] * img_w
    y = (1 - data['pos'][1]) * img_h
    
    # Glow effect (blue tones)
    for r, alpha in [(35, 0.15), (25, 0.3)]:
        circle = Circle((x, y), r, facecolor=data['color'], alpha=alpha, zorder=5)
        ax1.add_patch(circle)
    
    # Inner marker with number only
    circle = Circle((x, y), 18, facecolor=data['color'], edgecolor='white', 
                    linewidth=3, alpha=0.95, zorder=10)
    ax1.add_patch(circle)
    
    ax1.text(x, y, str(marker_num), ha='center', va='center', 
            fontsize=14, fontweight='bold', color='white', zorder=11)
    marker_num += 1

# Labels with connection lines
for region, data in regions_data.items():
    x = data['pos'][0] * img_w
    y = (1 - data['pos'][1]) * img_h
    lx = data['label_pos'][0] * img_w
    ly = (1 - data['label_pos'][1]) * img_h
    
    # Connection line
    ax1.plot([x, lx], [y, ly], color=data['color'], linewidth=2, alpha=0.8, zorder=8)
    
    short_name = region[:3].upper()
    if 'Nucleus' in region:
        short_name = 'NAc'
    elif 'Hippocampus' in region:
        short_name = 'HIP'
    elif 'Prefrontal' in region:
        short_name = 'PFC'
    elif 'Amygdala' in region:
        short_name = 'AMY'
    
    label_text = f"{short_name}\n+{data['eaa']} yr\nn={data['n']}"
    
    bbox = dict(boxstyle='round,pad=0.8', facecolor=data['color'], 
                edgecolor='white', linewidth=4, alpha=0.95)
    ax1.text(lx, ly, label_text, ha='center', va='center', fontsize=18,
            fontweight='bold', color='white', bbox=bbox, zorder=12)

# Extended limits to show labels outside brain - expanded for larger labels
ax1.set_xlim(-img_w * 0.35, img_w * 1.25)
ax1.set_ylim(img_h * 1.08, -img_h * 0.08)
ax1.axis('off')
ax1.set_title('A. Sagittal Brain Section - Regional EAA Mapping', fontsize=14, 
              fontweight='bold', color=COLORS['primary'], loc='left', pad=15)

# Panel B: Statistics
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_facecolor(COLORS['bg'])
ax2.set_xlim(0, 10)
ax2.set_ylim(-4, 12)
ax2.axis('off')
ax2.set_title('B. Regional EAA Statistics', fontsize=14, 
              fontweight='bold', color=COLORS['primary'], loc='left', pad=15)

# Sorted bars
regions = list(regions_data.keys())
eaa_vals = [d['eaa'] for d in regions_data.values()]
colors = [d['color'] for d in regions_data.values()]
ci_vals = [d['ci'] for d in regions_data.values()]
n_vals = [d['n'] for d in regions_data.values()]

sorted_idx = np.argsort(eaa_vals)[::-1]
regions_sorted = [regions[i] for i in sorted_idx]
eaa_sorted = [eaa_vals[i] for i in sorted_idx]
colors_sorted = [colors[i] for i in sorted_idx]
ci_sorted = [ci_vals[i] for i in sorted_idx]
n_sorted = [n_vals[i] for i in sorted_idx]

bar_height = 1.2
y_positions = [10 - i*2 for i in range(len(regions_sorted))]

for i, (y_pos, region, eaa, color, ci, n) in enumerate(zip(y_positions, regions_sorted, 
                                                            eaa_sorted, colors_sorted, ci_sorted, n_sorted)):
    bar = Rectangle((0.5, y_pos - bar_height/2), eaa * 1.2, bar_height,
                    facecolor=color, edgecolor='white', linewidth=2, alpha=0.9)
    ax2.add_patch(bar)
    
    ci_low = (eaa - ci[0]) * 1.2
    ci_high = (ci[1] - eaa) * 1.2
    ax2.errorbar(0.5 + eaa * 1.2, y_pos, xerr=[[ci_low], [ci_high]], 
                fmt='none', color='black', capsize=4, capthick=2, linewidth=2)
    
    # Short name
    short_name = region[:3].upper()
    if 'Nucleus' in region:
        short_name = 'NAc'
    elif 'Hippocampus' in region:
        short_name = 'HIP'
    elif 'Prefrontal' in region:
        short_name = 'PFC'
    elif 'Amygdala' in region:
        short_name = 'AMY'
        
    ax2.text(0.3, y_pos, short_name, ha='right', va='center', fontsize=14, fontweight='bold', color=COLORS['text'])
    ax2.text(0.5 + eaa * 1.2 + 0.8, y_pos, f'+{eaa} yr (n={n})', 
            ha='left', va='center', fontsize=13, fontweight='bold', color=COLORS['text'])

# X-axis
ax2.plot([0.5, 8], [0.3, 0.3], color='black', linewidth=1.5)
for tick in [0, 2, 4, 6]:
    ax2.plot([0.5 + tick*1.2, 0.5 + tick*1.2], [0.2, 0.4], color='black', linewidth=1)
    ax2.text(0.5 + tick*1.2, -0.1, f'{tick}', ha='center', fontsize=12, color=COLORS['text'])
ax2.text(4, -0.6, 'EAA (years)', ha='center', fontsize=13, fontweight='bold', color=COLORS['text'])

# Stats box
stats_box = FancyBboxPatch((0.3, -3.5), 9.4, 2.8, boxstyle='round,pad=0.05',
                            facecolor='white', edgecolor=COLORS['primary'], linewidth=2)
ax2.add_patch(stats_box)

stats_text = """ANOVA: F(4,142) = 12.4, p < 0.001 ***
Post-hoc Tukey HSD:
  PFC > NAc (p=0.021*)  |  PFC > HIP (p<0.001***)
Total n = 147 postmortem samples"""

ax2.text(5, -2.1, stats_text, ha='center', va='center', fontsize=11,
        fontfamily='monospace', color=COLORS['text'])

# Main title
fig.suptitle('Figure 5. Brain Region-Specific Epigenetic Age Acceleration',
             fontsize=18, fontweight='bold', color=COLORS['primary'], y=0.97)
fig.text(0.5, 0.02, 'PMI-corrected Horvath clock | Postmortem samples | Error bars: 95% CI',
         ha='center', fontsize=11, style='italic', color='gray')

plt.tight_layout(rect=[0, 0.04, 1, 0.94])
plt.savefig('figures/output/figure_5_brain.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('figures/output/figure_5_brain.pdf', bbox_inches='tight', facecolor='white')
print("Figure 5 saved!")
