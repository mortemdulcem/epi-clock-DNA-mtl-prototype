"""
EpiClock v4.0 - Figure 3: Mediation Analysis
Blue-Black Color Scheme - Publication Ready
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import numpy as np

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

fig = plt.figure(figsize=(18, 12), facecolor='white')
gs = fig.add_gridspec(2, 3, height_ratios=[1.2, 1], hspace=0.3, wspace=0.25)

# Panel A: Mediation Pathway Diagram
ax1 = fig.add_subplot(gs[0, :2])
ax1.set_facecolor('white')
ax1.set_xlim(0, 14)
ax1.set_ylim(0, 8)
ax1.axis('off')
ax1.set_title('A. Mediation Pathway Model', fontsize=14, fontweight='bold', 
              color=COLORS['primary'], loc='left', pad=10)

# Boxes
box_style = dict(boxstyle='round,pad=0.4', linewidth=3)

# Substance Use (X)
box_x = FancyBboxPatch((0.5, 3), 2.5, 2, facecolor=COLORS['primary'], 
                        edgecolor='white', **box_style)
ax1.add_patch(box_x)
ax1.text(1.75, 4, 'Substance\nUse (X)', ha='center', va='center', 
         fontsize=12, fontweight='bold', color='white')

# Mediator (M)
box_m = FancyBboxPatch((5.5, 5.5), 3, 2, facecolor=COLORS['accent'], 
                        edgecolor='white', **box_style)
ax1.add_patch(box_m)
ax1.text(7, 6.5, 'DNA Methylation\nMediators (M)', ha='center', va='center', 
         fontsize=11, fontweight='bold', color='white')

# EAA (Y)
box_y = FancyBboxPatch((11, 3), 2.5, 2, facecolor=COLORS['light'], 
                        edgecolor='white', **box_style)
ax1.add_patch(box_y)
ax1.text(12.25, 4, 'Epigenetic\nAge (Y)', ha='center', va='center', 
         fontsize=12, fontweight='bold', color='white')

# Arrows with coefficients
arrow_style = dict(arrowstyle='->', color=COLORS['secondary'], lw=3, 
                   connectionstyle='arc3,rad=0.0', mutation_scale=20)

# X -> M (a path)
ax1.annotate('', xy=(5.5, 6.5), xytext=(3, 4.5), arrowprops=arrow_style)
ax1.text(3.8, 5.8, 'a = 0.42***', fontsize=11, fontweight='bold', color=COLORS['primary'],
         bbox=dict(boxstyle='round', facecolor='white', edgecolor=COLORS['accent'], alpha=0.9))

# M -> Y (b path)
ax1.annotate('', xy=(11, 4.5), xytext=(8.5, 6.5), arrowprops=arrow_style)
ax1.text(9.8, 5.8, 'b = 0.38***', fontsize=11, fontweight='bold', color=COLORS['primary'],
         bbox=dict(boxstyle='round', facecolor='white', edgecolor=COLORS['accent'], alpha=0.9))

# X -> Y (c' path - direct)
ax1.annotate('', xy=(11, 4), xytext=(3, 4), arrowprops=dict(arrowstyle='->', color='#6B7280', lw=2.5,
                   connectionstyle='arc3,rad=0.0', mutation_scale=18, linestyle='--'))
ax1.text(7, 3.3, "c' = 0.25** (direct)", fontsize=11, fontweight='bold', color='#6B7280')

# Total effect annotation
ax1.text(7, 1.5, 'Total Effect: c = 0.41***\nIndirect Effect: ab = 0.16*** (39% mediated)',
         ha='center', fontsize=11, fontweight='bold', color=COLORS['primary'],
         bbox=dict(boxstyle='round', facecolor='#E8F4FD', edgecolor=COLORS['accent'], linewidth=2))

# Panel B: Effect Decomposition
ax2 = fig.add_subplot(gs[0, 2])
ax2.set_facecolor(COLORS['bg'])

effects = ['Total Effect', 'Direct Effect', 'Indirect Effect']
values = [0.41, 0.25, 0.16]
colors_bar = [COLORS['primary'], COLORS['secondary'], COLORS['light']]

y_pos = np.arange(len(effects))
bars = ax2.barh(y_pos, values, color=colors_bar, edgecolor='white', linewidth=2, height=0.5)

for i, v in enumerate(values):
    pct = f'({v/0.41*100:.0f}%)' if i > 0 else '(100%)'
    ax2.text(v + 0.02, i, f'{v:.2f} {pct}', va='center', fontsize=10, fontweight='bold', color=COLORS['text'])

ax2.set_yticks(y_pos)
ax2.set_yticklabels(effects, fontsize=11, fontweight='bold')
ax2.set_xlabel('Standardized Effect', fontsize=11, fontweight='bold', color=COLORS['text'])
ax2.set_title('B. Effect Decomposition', fontsize=14, fontweight='bold', 
              color=COLORS['primary'], loc='left', pad=10)
ax2.set_xlim(0, 0.55)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

# Panel C: Top Mediating CpGs
ax3 = fig.add_subplot(gs[1, 0])
ax3.set_facecolor(COLORS['bg'])

cpgs = ['cg05575921\n(AHRR)', 'cg03636183\n(F2RL3)', 'cg21566642\n(ALPPL2)', 
        'cg01940273\n(GPR15)', 'cg19859270\n(GPR15)']
mediation_pct = [12.3, 8.7, 6.2, 5.1, 4.8]

y_pos = np.arange(len(cpgs))
colors_cpg = [COLORS['primary'], COLORS['secondary'], COLORS['accent'], COLORS['light'], COLORS['highlight']]
bars = ax3.barh(y_pos, mediation_pct, color=colors_cpg, edgecolor='white', linewidth=2, height=0.6)

for i, v in enumerate(mediation_pct):
    ax3.text(v + 0.3, i, f'{v}%', va='center', fontsize=10, fontweight='bold', color=COLORS['text'])

ax3.set_yticks(y_pos)
ax3.set_yticklabels(cpgs, fontsize=9)
ax3.set_xlabel('Mediation Contribution (%)', fontsize=11, fontweight='bold', color=COLORS['text'])
ax3.set_title('C. Top Mediating CpG Sites', fontsize=14, fontweight='bold', 
              color=COLORS['primary'], loc='left', pad=10)
ax3.set_xlim(0, 16)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)

# Panel D: Biomarker Contributions
ax4 = fig.add_subplot(gs[1, 1])
ax4.set_facecolor(COLORS['bg'])

biomarkers = ['Smoking\nMarkers', 'Inflammation', 'Metabolic', 'Immune\nFunction', 'Other']
contributions = [39, 24, 18, 12, 7]
colors_bio = [COLORS['primary'], COLORS['secondary'], COLORS['accent'], COLORS['light'], '#94A3B8']

wedges, texts, autotexts = ax4.pie(contributions, labels=biomarkers, colors=colors_bio,
                                    autopct='%1.0f%%', pctdistance=0.6,
                                    wedgeprops=dict(edgecolor='white', linewidth=2),
                                    textprops=dict(fontsize=9, fontweight='bold'))
for autotext in autotexts:
    autotext.set_fontsize(10)
    autotext.set_fontweight('bold')
    autotext.set_color('white')

ax4.set_title('D. Biomarker Contributions', fontsize=14, fontweight='bold', 
              color=COLORS['primary'], pad=10)

# Panel E: Bootstrap Results
ax5 = fig.add_subplot(gs[1, 2])
ax5.set_facecolor(COLORS['bg'])
ax5.axis('off')
ax5.set_title('E. Bootstrap Validation', fontsize=14, fontweight='bold', 
              color=COLORS['primary'], loc='left', pad=10)

stats_text = """MEDIATION ANALYSIS RESULTS
══════════════════════════════════════
Bootstrap: 10,000 iterations
Confidence: 95% Bias-corrected

Indirect Effect (ab):
  Point estimate: 0.160
  95% CI: [0.118, 0.205]
  p < 0.001 ***

Proportion Mediated: 39.0%
  95% CI: [28.8%, 50.0%]

Sobel Test: z = 8.42, p < 0.001
══════════════════════════════════════
*** p < 0.001, ** p < 0.01, * p < 0.05"""

ax5.text(0.5, 0.5, stats_text, transform=ax5.transAxes, fontsize=10,
         fontfamily='monospace', ha='center', va='center', color=COLORS['text'],
         bbox=dict(boxstyle='round', facecolor='white', edgecolor=COLORS['primary'], linewidth=2))

# Main title
fig.suptitle('Figure 3. Mediation Analysis: Substance Use, DNA Methylation, and Epigenetic Aging',
             fontsize=18, fontweight='bold', color=COLORS['primary'], y=0.98)
fig.text(0.5, 0.01, 'Baron-Kenny mediation framework with bootstrap validation | n = 10,542',
         ha='center', fontsize=11, style='italic', color='gray')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('figures/output/figure_3_mediation.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('figures/output/figure_3_mediation.pdf', bbox_inches='tight', facecolor='white')
print("Figure 3 saved!")
