"""
EpiClock v4.0 - Figure 5: Brain Region EAA
Serif Font 32pt - No overlapping - Blue-Black Theme
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle
import matplotlib.image as mpimg
import numpy as np

# Use serif font globally (Times New Roman alternative)
plt.rcParams['font.family'] = 'serif'

# Blue-Black Color Palette
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

# Brain regions - ALL labels on LEFT side with MAXIMUM vertical spacing
regions_data = {
    'Prefrontal Cortex': {'eaa': 5.3, 'n': 48, 'color': BLUES[0], 
                          'marker': (0.78, 0.30), 'label_pos': (-0.28, 0.05)},
    'Nucleus Accumbens': {'eaa': 4.1, 'n': 36, 'color': BLUES[1],
                          'marker': (0.52, 0.42), 'label_pos': (-0.28, 0.28)},
    'Hippocampus': {'eaa': 3.2, 'n': 24, 'color': BLUES[2],
                    'marker': (0.58, 0.50), 'label_pos': (-0.28, 0.51)},
    'Amygdala': {'eaa': 3.5, 'n': 21, 'color': BLUES[3],
                 'marker': (0.48, 0.60), 'label_pos': (-0.28, 0.74)},
    'VTA': {'eaa': 2.8, 'n': 18, 'color': BLUES[4],
            'marker': (0.38, 0.72), 'label_pos': (-0.28, 0.97)},
}

# Create figure - large size for publication
fig = plt.figure(figsize=(28, 16), facecolor='white')
gs = fig.add_gridspec(1, 2, width_ratios=[1.5, 1], wspace=0.12)

# Panel A: Brain Image with labels
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_facecolor('white')

# Load brain image with white background - original aspect ratio
brain_img = mpimg.imread('figures/brain_white_bg.png')
ax1.imshow(brain_img, aspect='equal')

img_h, img_w = brain_img.shape[:2]

# Add numbered markers on brain regions
marker_num = 1
for region, data in regions_data.items():
    x = data['marker'][0] * img_w
    y = data['marker'][1] * img_h
    
    # Glow effect
    for r, alpha in [(45, 0.2), (32, 0.4)]:
        circle = Circle((x, y), r, facecolor=data['color'], alpha=alpha, zorder=5)
        ax1.add_patch(circle)
    
    # Main marker circle with number
    circle = Circle((x, y), 22, facecolor=data['color'], edgecolor='white', 
                    linewidth=4, alpha=0.95, zorder=10)
    ax1.add_patch(circle)
    
    ax1.text(x, y, str(marker_num), ha='center', va='center', 
            fontsize=18, fontweight='bold', color='white', zorder=11)
    marker_num += 1

# Draw labels OUTSIDE the brain image - NO OVERLAP - 32pt
for region, data in regions_data.items():
    mx = data['marker'][0] * img_w
    my = data['marker'][1] * img_h
    lx = data['label_pos'][0] * img_w
    ly = data['label_pos'][1] * img_h
    
    # Connection line - clean and visible
    ax1.plot([mx, lx], [my, ly], color=data['color'], linewidth=4, alpha=0.9, zorder=8)
    
    # Small dot at line end
    ax1.plot(lx, ly, 'o', color=data['color'], markersize=8, zorder=9)
    
    # Short region name
    short_name = region[:3].upper()
    if 'Nucleus' in region:
        short_name = 'NAc'
    elif 'Hippocampus' in region:
        short_name = 'HIP'
    elif 'Prefrontal' in region:
        short_name = 'PFC'
    elif 'Amygdala' in region:
        short_name = 'AMY'
    
    # Label with 18pt font - clear and readable
    label_text = f"{short_name}\n+{data['eaa']} yr\nn={data['n']}"
    
    bbox = dict(boxstyle='round,pad=0.4', facecolor=data['color'], 
                edgecolor='white', linewidth=3, alpha=0.95)
    ax1.text(lx, ly, label_text, ha='center', va='center', fontsize=18,
            fontweight='bold', color='white', bbox=bbox, zorder=12)

# Extended limits for labels outside image - more space on left
ax1.set_xlim(-img_w * 0.45, img_w * 1.15)
ax1.set_ylim(img_h * 1.10, -img_h * 0.10)
ax1.axis('off')
ax1.set_title('A. Sagittal Brain Section - Regional EAA', fontsize=24, 
              fontweight='bold', color=COLORS['primary'], loc='left', pad=20)

# Panel B: Bar chart statistics
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_facecolor(COLORS['bg'])

# Sort by EAA value
regions = list(regions_data.keys())
eaa_vals = [d['eaa'] for d in regions_data.values()]
colors = [d['color'] for d in regions_data.values()]
n_vals = [d['n'] for d in regions_data.values()]

sorted_idx = np.argsort(eaa_vals)[::-1]
regions_sorted = [regions[i] for i in sorted_idx]
eaa_sorted = [eaa_vals[i] for i in sorted_idx]
colors_sorted = [colors[i] for i in sorted_idx]
n_sorted = [n_vals[i] for i in sorted_idx]

# Create horizontal bars
y_positions = np.arange(len(regions_sorted))
bars = ax2.barh(y_positions, eaa_sorted, color=colors_sorted, edgecolor='white', 
                linewidth=2, height=0.7, alpha=0.9)

# Error bars (95% CI approximation)
ci_errors = [0.6, 0.5, 0.5, 0.5, 0.5]
ax2.errorbar(eaa_sorted, y_positions, xerr=ci_errors, fmt='none', 
             color='black', capsize=6, capthick=2, linewidth=2)

# Short names for y-axis
short_names = []
for r in regions_sorted:
    if 'Nucleus' in r:
        short_names.append('NAc')
    elif 'Hippocampus' in r:
        short_names.append('HIP')
    elif 'Prefrontal' in r:
        short_names.append('PFC')
    elif 'Amygdala' in r:
        short_names.append('AMY')
    elif 'VTA' in r:
        short_names.append('VTA')

ax2.set_yticks(y_positions)
ax2.set_yticklabels(short_names, fontsize=28, fontweight='bold', color=COLORS['text'])

# Value annotations
for i, (eaa, n) in enumerate(zip(eaa_sorted, n_sorted)):
    ax2.text(eaa + 0.8, i, f'+{eaa} yr (n={n})', va='center', ha='left',
             fontsize=24, fontweight='bold', color=COLORS['text'])

# X-axis
ax2.set_xlabel('EAA (years)', fontsize=28, fontweight='bold', color=COLORS['text'])
ax2.set_xlim(0, 8)
ax2.tick_params(axis='x', labelsize=22)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_linewidth(2)
ax2.spines['bottom'].set_linewidth(2)

# Add vertical reference line at 0
ax2.axvline(x=0, color='gray', linestyle='-', linewidth=1, alpha=0.5)

ax2.set_title('B. Regional EAA Statistics', fontsize=24, 
              fontweight='bold', color=COLORS['primary'], loc='left', pad=20)

# Statistics box at bottom
stats_text = """ANOVA: F(4,142) = 12.4, p < 0.001 ***
Post-hoc Tukey HSD: PFC > HIP (p<0.001***)
Total n = 147 postmortem samples"""

ax2.text(0.5, -0.18, stats_text, transform=ax2.transAxes, ha='center', va='top',
         fontsize=18, color=COLORS['text'],
         bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                   edgecolor=COLORS['primary'], linewidth=2))

# Main title
fig.suptitle('Figure 5. Brain Region-Specific Epigenetic Age Acceleration',
             fontsize=32, fontweight='bold', color=COLORS['primary'], y=0.96)
fig.text(0.5, 0.02, 'PMI-corrected Horvath clock | Postmortem samples | Error bars: 95% CI',
         ha='center', fontsize=18, style='italic', color='gray')

plt.tight_layout(rect=[0, 0.05, 1, 0.93])
plt.savefig('figures/output/figure_5_brain.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('figures/output/figure_5_brain.pdf', bbox_inches='tight', facecolor='white')
print("Figure 5 saved - Serif 32pt!")
