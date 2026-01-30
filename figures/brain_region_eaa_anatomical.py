"""
EpiClock v4.0 - Anatomical Brain Region Visualization
Realistic brain schematic with regional EAA overlay
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, Ellipse, Polygon, PathPatch, Arc
from matplotlib.path import Path
import numpy as np

# UNODC Color Palette
UNODC_PRIMARY = '#0050A0'
UNODC_SECONDARY = '#003366'
UNODC_ACCENT = '#00A7D8'

# Region colors with gradients
COLOR_PFC = '#E53935'      # Prefrontal Cortex - red
COLOR_NAC = '#8E24AA'      # Nucleus Accumbens - purple  
COLOR_HIPP = '#43A047'     # Hippocampus - green
COLOR_VTA = '#FB8C00'      # VTA - orange
COLOR_AMY = '#1E88E5'      # Amygdala - blue

# Brain base colors
BRAIN_FILL = '#F5E6D3'
BRAIN_OUTLINE = '#5D4037'
BRAIN_SULCI = '#C4A484'

# Data
regions_data = {
    'Prefrontal Cortex': {'eaa': 5.3, 'ci': (4.2, 6.5), 'n': 48, 'color': COLOR_PFC},
    'Nucleus Accumbens': {'eaa': 4.1, 'ci': (3.2, 5.1), 'n': 36, 'color': COLOR_NAC},
    'Hippocampus': {'eaa': 3.2, 'ci': (2.3, 4.2), 'n': 24, 'color': COLOR_HIPP},
    'VTA': {'eaa': 2.8, 'ci': (1.9, 3.7), 'n': 18, 'color': COLOR_VTA},
    'Amygdala': {'eaa': 3.5, 'ci': (2.6, 4.4), 'n': 21, 'color': COLOR_AMY},
}

fig = plt.figure(figsize=(20, 14), facecolor='white')
gs = fig.add_gridspec(2, 2, height_ratios=[1.8, 1], width_ratios=[1.2, 1], 
                       hspace=0.25, wspace=0.2)

# === PANEL A: Sagittal Brain View ===
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_xlim(0, 20)
ax1.set_ylim(0, 14)
ax1.set_aspect('equal')
ax1.axis('off')
ax1.set_title('A. Sagittal View - Regional EAA Distribution', fontsize=14, 
              fontweight='bold', color=UNODC_SECONDARY, loc='left', pad=10)

# Brain outline - realistic sagittal shape
theta = np.linspace(0, 2*np.pi, 200)

# Main cerebrum
cerebrum_x = 10 + 7 * np.cos(theta) * (1 + 0.2*np.cos(theta))
cerebrum_y = 8.5 + 4.5 * np.sin(theta) * (1 + 0.15*np.sin(2*theta))
ax1.fill(cerebrum_x, cerebrum_y, facecolor=BRAIN_FILL, edgecolor=BRAIN_OUTLINE, 
         linewidth=2.5, zorder=1)

# Sulci lines (brain folds)
for i in range(5):
    sulci_start = 5 + i * 2.5
    sulci_x = np.linspace(sulci_start, sulci_start + 2, 20)
    sulci_y = 10 + 1.5*np.sin((sulci_x - sulci_start) * np.pi / 2) + np.random.uniform(-0.2, 0.2, 20)
    ax1.plot(sulci_x, sulci_y, color=BRAIN_SULCI, linewidth=1.5, alpha=0.6, zorder=2)

# Central sulcus
central_x = np.array([9, 9.5, 10, 10.5])
central_y = np.array([12.5, 10, 8, 6])
ax1.plot(central_x, central_y, color=BRAIN_SULCI, linewidth=2, alpha=0.8, zorder=2)

# Lateral fissure
lateral_x = np.array([4, 6, 8, 10])
lateral_y = np.array([7, 7.5, 7.2, 6.5])
ax1.plot(lateral_x, lateral_y, color=BRAIN_SULCI, linewidth=2, alpha=0.8, zorder=2)

# Cerebellum
cerebellum_theta = np.linspace(0, np.pi, 50)
cerebellum_x = 15 + 2.5 * np.cos(cerebellum_theta)
cerebellum_y = 4 + 1.5 * np.sin(cerebellum_theta)
cerebellum_path = np.column_stack([cerebellum_x, cerebellum_y])
ax1.fill(cerebellum_x, cerebellum_y, facecolor='#E8D4C4', edgecolor=BRAIN_OUTLINE, 
         linewidth=2, zorder=1)
# Cerebellar folia
for i in range(4):
    folia_y = 3.5 + i * 0.4
    ax1.plot([13, 17], [folia_y, folia_y], color=BRAIN_SULCI, linewidth=1, alpha=0.5)

# Brain stem
brainstem = Polygon([(14, 4), (15, 2), (16, 2), (16.5, 4)], 
                    facecolor='#E0C8B8', edgecolor=BRAIN_OUTLINE, linewidth=2, zorder=1)
ax1.add_patch(brainstem)

# Corpus callosum
cc_x = np.linspace(6, 14, 50)
cc_y = 7.5 + 0.8*np.sin((cc_x - 6) * np.pi / 8)
ax1.fill_between(cc_x, cc_y - 0.4, cc_y + 0.4, color='#FFFFFF', edgecolor=BRAIN_SULCI, 
                  linewidth=1.5, zorder=3)

# === BRAIN REGIONS WITH HOTSPOTS ===

# PREFRONTAL CORTEX (anterior)
pfc_x = 4.5 + 2.2 * np.cos(theta)
pfc_y = 9 + 2.5 * np.sin(theta)
ax1.fill(pfc_x, pfc_y, facecolor=COLOR_PFC, edgecolor='white', linewidth=3, 
         alpha=0.75, zorder=5)
ax1.text(4.5, 9.3, 'PFC', ha='center', va='center', fontsize=14, fontweight='bold', 
         color='white', zorder=6)
ax1.text(4.5, 8.3, '+5.3 yr', ha='center', va='center', fontsize=11, 
         fontweight='bold', color='white', zorder=6)

# NUCLEUS ACCUMBENS (ventral striatum)
nac = Ellipse((8, 5.5), 1.8, 1.2, facecolor=COLOR_NAC, edgecolor='white', 
              linewidth=3, alpha=0.85, zorder=5)
ax1.add_patch(nac)
ax1.text(8, 5.7, 'NAc', ha='center', va='center', fontsize=12, fontweight='bold', 
         color='white', zorder=6)
ax1.text(8, 5, '+4.1 yr', ha='center', va='center', fontsize=10, 
         fontweight='bold', color='white', zorder=6)

# HIPPOCAMPUS (curved shape)
hipp_t = np.linspace(0, np.pi, 50)
hipp_x = 12 + 2 * np.cos(hipp_t)
hipp_y = 5.5 + 0.8 * np.sin(hipp_t) - 0.3 * np.sin(2*hipp_t)
hipp_x_full = np.concatenate([hipp_x, hipp_x[::-1]])
hipp_y_full = np.concatenate([hipp_y + 0.4, hipp_y[::-1] - 0.4])
ax1.fill(hipp_x_full, hipp_y_full, facecolor=COLOR_HIPP, edgecolor='white', 
         linewidth=3, alpha=0.85, zorder=5)
ax1.text(12, 5.5, 'HIPP', ha='center', va='center', fontsize=11, fontweight='bold', 
         color='white', zorder=6)
ax1.text(12, 4.8, '+3.2 yr', ha='center', va='center', fontsize=9, 
         fontweight='bold', color='white', zorder=6)

# AMYGDALA
amy = Ellipse((10, 4.5), 1.4, 1.0, facecolor=COLOR_AMY, edgecolor='white', 
              linewidth=3, alpha=0.85, zorder=5)
ax1.add_patch(amy)
ax1.text(10, 4.7, 'AMY', ha='center', va='center', fontsize=10, fontweight='bold', 
         color='white', zorder=6)
ax1.text(10, 4.1, '+3.5 yr', ha='center', va='center', fontsize=9, 
         fontweight='bold', color='white', zorder=6)

# VTA (midbrain)
vta = Ellipse((14.5, 4.5), 1.2, 0.8, facecolor=COLOR_VTA, edgecolor='white', 
              linewidth=3, alpha=0.85, zorder=5)
ax1.add_patch(vta)
ax1.text(14.5, 4.7, 'VTA', ha='center', va='center', fontsize=10, fontweight='bold', 
         color='white', zorder=6)
ax1.text(14.5, 4.1, '+2.8 yr', ha='center', va='center', fontsize=9, 
         fontweight='bold', color='white', zorder=6)

# Neural pathway arrows
arrow_style = dict(arrowstyle='->', color='#333333', lw=2, 
                   connectionstyle='arc3,rad=0.2')
ax1.annotate('', xy=(7, 5.5), xytext=(5.5, 8), arrowprops=arrow_style, zorder=4)
ax1.annotate('', xy=(10, 4.8), xytext=(8.5, 5.3), arrowprops=arrow_style, zorder=4)
ax1.annotate('', xy=(11, 5.2), xytext=(10.5, 4.8), arrowprops=arrow_style, zorder=4)

# Scale bar
ax1.plot([1, 3], [2, 2], color='black', linewidth=2)
ax1.text(2, 1.5, '2 cm', ha='center', fontsize=10, color='black')

# Legend
legend_y = 13
for i, (region, data) in enumerate(regions_data.items()):
    rect = plt.Rectangle((1, legend_y - i*0.7), 0.5, 0.4, facecolor=data['color'], 
                          edgecolor='black', linewidth=1)
    ax1.add_patch(rect)
    ax1.text(1.7, legend_y - i*0.7 + 0.2, f'{region}', fontsize=9, va='center')

# === PANEL B: Coronal View ===
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_xlim(0, 14)
ax2.set_ylim(0, 12)
ax2.set_aspect('equal')
ax2.axis('off')
ax2.set_title('B. Coronal View - Subcortical Structures', fontsize=14, 
              fontweight='bold', color=UNODC_SECONDARY, loc='left', pad=10)

# Coronal brain outline
coronal_x = 7 + 5 * np.cos(theta)
coronal_y = 7 + 4.5 * np.sin(theta) * (1 + 0.1*np.cos(2*theta))
ax2.fill(coronal_x, coronal_y, facecolor=BRAIN_FILL, edgecolor=BRAIN_OUTLINE, 
         linewidth=2.5, zorder=1)

# Ventricles (bilateral)
vent_left = Polygon([(5.5, 7), (6, 8), (6.5, 7), (6, 6)], 
                    facecolor='#B3E5FC', edgecolor='#0288D1', linewidth=1.5)
vent_right = Polygon([(7.5, 7), (8, 8), (8.5, 7), (8, 6)], 
                     facecolor='#B3E5FC', edgecolor='#0288D1', linewidth=1.5)
ax2.add_patch(vent_left)
ax2.add_patch(vent_right)

# Corpus callosum (coronal)
cc = Ellipse((7, 9), 6, 1, facecolor='white', edgecolor=BRAIN_SULCI, linewidth=2)
ax2.add_patch(cc)

# Bilateral structures
# NAc left & right
nac_l = Ellipse((5, 5), 1.2, 0.8, facecolor=COLOR_NAC, edgecolor='white', linewidth=2, alpha=0.85)
nac_r = Ellipse((9, 5), 1.2, 0.8, facecolor=COLOR_NAC, edgecolor='white', linewidth=2, alpha=0.85)
ax2.add_patch(nac_l)
ax2.add_patch(nac_r)
ax2.text(5, 5, 'NAc', ha='center', va='center', fontsize=9, fontweight='bold', color='white')
ax2.text(9, 5, 'NAc', ha='center', va='center', fontsize=9, fontweight='bold', color='white')

# Amygdala left & right
amy_l = Ellipse((4, 4), 1.0, 0.7, facecolor=COLOR_AMY, edgecolor='white', linewidth=2, alpha=0.85)
amy_r = Ellipse((10, 4), 1.0, 0.7, facecolor=COLOR_AMY, edgecolor='white', linewidth=2, alpha=0.85)
ax2.add_patch(amy_l)
ax2.add_patch(amy_r)
ax2.text(4, 4, 'AMY', ha='center', va='center', fontsize=8, fontweight='bold', color='white')
ax2.text(10, 4, 'AMY', ha='center', va='center', fontsize=8, fontweight='bold', color='white')

# Hippocampus left & right
hipp_l = Ellipse((3.5, 5.5), 1.4, 0.8, angle=-30, facecolor=COLOR_HIPP, 
                 edgecolor='white', linewidth=2, alpha=0.85)
hipp_r = Ellipse((10.5, 5.5), 1.4, 0.8, angle=30, facecolor=COLOR_HIPP, 
                 edgecolor='white', linewidth=2, alpha=0.85)
ax2.add_patch(hipp_l)
ax2.add_patch(hipp_r)
ax2.text(3.5, 5.5, 'H', ha='center', va='center', fontsize=9, fontweight='bold', color='white')
ax2.text(10.5, 5.5, 'H', ha='center', va='center', fontsize=9, fontweight='bold', color='white')

# Labels
ax2.text(7, 2, 'L                    R', ha='center', fontsize=12, fontweight='bold')
ax2.text(7, 9, 'CC', ha='center', va='center', fontsize=10, color=BRAIN_SULCI)

# === PANEL C: EAA Bar Chart ===
ax3 = fig.add_subplot(gs[1, 0])
regions = list(regions_data.keys())
eaa_vals = [d['eaa'] for d in regions_data.values()]
colors = [d['color'] for d in regions_data.values()]
ci_errors = [(d['eaa'] - d['ci'][0], d['ci'][1] - d['eaa']) for d in regions_data.values()]
ci_lower = [e[0] for e in ci_errors]
ci_upper = [e[1] for e in ci_errors]

y_pos = np.arange(len(regions))
bars = ax3.barh(y_pos, eaa_vals, color=colors, edgecolor='black', linewidth=1.5, height=0.6)
ax3.errorbar(eaa_vals, y_pos, xerr=[ci_lower, ci_upper], fmt='none', 
             color='black', capsize=5, capthick=2, linewidth=2)

ax3.set_yticks(y_pos)
ax3.set_yticklabels(regions, fontsize=11)
ax3.set_xlabel('Epigenetic Age Acceleration (years)', fontsize=12, fontweight='bold')
ax3.set_title('C. Regional EAA Comparison', fontsize=14, fontweight='bold', 
              color=UNODC_SECONDARY, loc='left')
ax3.axvline(x=0, color='black', linewidth=1)
ax3.set_xlim(0, 8)

# Add value labels
for i, (v, n) in enumerate(zip(eaa_vals, [d['n'] for d in regions_data.values()])):
    ax3.text(v + 0.3, i, f'+{v} yr (n={n})', va='center', fontsize=10, fontweight='bold')

ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)

# === PANEL D: Statistics Table ===
ax4 = fig.add_subplot(gs[1, 1])
ax4.axis('off')
ax4.set_title('D. Statistical Summary', fontsize=14, fontweight='bold', 
              color=UNODC_SECONDARY, loc='left')

table_data = [
    ['Region', 'n', 'EAA (yr)', '95% CI', 'Function'],
    ['Prefrontal Cortex', '48', '+5.3', '4.2-6.5', 'Executive control'],
    ['Nucleus Accumbens', '36', '+4.1', '3.2-5.1', 'Reward processing'],
    ['Amygdala', '21', '+3.5', '2.6-4.4', 'Emotional memory'],
    ['Hippocampus', '24', '+3.2', '2.3-4.2', 'Memory formation'],
    ['VTA', '18', '+2.8', '1.9-3.7', 'Dopamine source'],
]

colors_table = [['#D6EAF8'] * 5] + [[c, 'white', 'white', 'white', 'white'] 
                                    for c in [COLOR_PFC, COLOR_NAC, COLOR_AMY, COLOR_HIPP, COLOR_VTA]]

table = ax4.table(cellText=table_data, cellColours=colors_table,
                  loc='center', cellLoc='center',
                  colWidths=[0.28, 0.1, 0.15, 0.17, 0.3])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 2)

# Header style
for i in range(5):
    table[(0, i)].set_text_props(fontweight='bold', color='black')
    table[(0, i)].set_facecolor('#0050A0')
    table[(0, i)].set_text_props(color='white', fontweight='bold')

# Stats box
stats_text = """ANOVA: F(4,142) = 12.4, p < 0.001***
Post-hoc (Tukey HSD):
  PFC > NAc (p = 0.021*)
  PFC > HIPP (p < 0.001***)
  NAc > VTA (p = 0.043*)"""
ax4.text(0.5, 0.08, stats_text, transform=ax4.transAxes, fontsize=10,
         fontfamily='monospace', ha='center', va='bottom',
         bbox=dict(boxstyle='round', facecolor='#F0F4F8', edgecolor=UNODC_PRIMARY, linewidth=2))

# Main title
fig.suptitle('Figure X. Brain Region-Specific Epigenetic Age Acceleration in Substance Use Disorders',
             fontsize=18, fontweight='bold', color=UNODC_SECONDARY, y=0.98)
fig.text(0.5, 0.01, 'PMI-corrected Horvath clock analysis | Total n=108 postmortem samples | Error bars: 95% CI',
         ha='center', fontsize=11, style='italic', color='gray')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('figures/brain_region_eaa_anatomical.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('figures/brain_region_eaa_anatomical.pdf', bbox_inches='tight', facecolor='white')
print("Anatomical brain region figure saved!")
