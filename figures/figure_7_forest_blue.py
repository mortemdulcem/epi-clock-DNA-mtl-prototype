"""
EpiClock v4.0 - Figure 7: Intervention Forest Plot
Blue-Black Color Scheme - Publication Ready
"""

import matplotlib.pyplot as plt
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

# Intervention data
interventions = [
    'Combined Lifestyle Intervention',
    'Dietary Modification',
    'Substance Cessation (5y)',
    'Physical Exercise',
    'Mindfulness + Yoga',
    'Substance Cessation (1y)',
]

effects = [-4.60, -3.23, -3.18, -2.87, -1.96, -1.52]
ci_lower = [-5.82, -4.15, -4.21, -3.68, -2.74, -2.28]
ci_upper = [-3.38, -2.31, -2.15, -2.06, -1.18, -0.76]
weights = [15, 21, 9, 26, 13, 16]
n_samples = [89, 124, 52, 156, 78, 94]

fig, ax = plt.subplots(figsize=(14, 10), facecolor='white')
ax.set_facecolor(COLORS['bg'])

y_positions = np.arange(len(interventions))[::-1]

# Forest plot elements
for i, (y, effect, ci_l, ci_u, weight, n) in enumerate(zip(y_positions, effects, ci_lower, ci_upper, weights, n_samples)):
    # CI line
    ax.plot([ci_l, ci_u], [y, y], color=COLORS['primary'], linewidth=2, zorder=5)
    
    # CI caps
    ax.plot([ci_l, ci_l], [y-0.1, y+0.1], color=COLORS['primary'], linewidth=2)
    ax.plot([ci_u, ci_u], [y-0.1, y+0.1], color=COLORS['primary'], linewidth=2)
    
    # Point estimate (size by weight)
    size = weight * 15
    ax.scatter(effect, y, s=size, color=COLORS['accent'], edgecolor='white', 
              linewidth=2, zorder=10, marker='s')

# Reference line
ax.axvline(x=0, color='#DC2626', linestyle='-', linewidth=2, alpha=0.7, zorder=3)
ax.text(0.1, len(interventions) + 0.3, 'No Effect', fontsize=10, color='#DC2626', fontweight='bold')

# Pooled effect (diamond)
pooled_effect = -2.89
pooled_ci_l = -3.42
pooled_ci_u = -2.36

diamond_y = -1
diamond_x = [pooled_ci_l, pooled_effect, pooled_ci_u, pooled_effect]
diamond_y_pts = [diamond_y, diamond_y + 0.25, diamond_y, diamond_y - 0.25]
ax.fill(diamond_x, diamond_y_pts, color=COLORS['primary'], edgecolor='white', linewidth=2, zorder=10)

# Separator line
ax.axhline(y=-0.5, color=COLORS['secondary'], linestyle='-', linewidth=1.5, alpha=0.5)

# Labels
ax.set_yticks(list(y_positions) + [-1])
ax.set_yticklabels(interventions + ['POOLED EFFECT'], fontsize=11, fontweight='bold')

ax.set_xlabel('Epigenetic Age Change (years)', fontsize=14, fontweight='bold', 
              color=COLORS['text'], labelpad=15)
ax.set_title('Figure 7. Forest Plot: Intervention Effects on Epigenetic Age',
             fontsize=18, fontweight='bold', color=COLORS['primary'], pad=20)

ax.set_xlim(-7, 2)
ax.set_ylim(-1.8, len(interventions) + 0.5)

# Right side annotations
ax.text(1.5, len(interventions) + 0.3, 'Effect [95% CI]', fontsize=10, fontweight='bold', ha='center')
for i, (y, effect, ci_l, ci_u, n) in enumerate(zip(y_positions, effects, ci_lower, ci_upper, n_samples)):
    text = f'{effect:.2f} [{ci_l:.2f}, {ci_u:.2f}]'
    ax.text(1.5, y, text, fontsize=9, ha='center', va='center', fontfamily='monospace')

# Pooled annotation
ax.text(1.5, -1, f'{pooled_effect:.2f} [{pooled_ci_l:.2f}, {pooled_ci_u:.2f}]', 
        fontsize=10, ha='center', va='center', fontweight='bold', fontfamily='monospace')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(True, axis='x', linestyle='--', alpha=0.4, color='#D1D5DB')

# Heterogeneity stats
het_text = """Heterogeneity: I² = 42%, τ² = 0.31, Q = 8.6 (p = 0.13)
Test for effect: Z = -8.42 (p < 0.001)
Random-effects meta-analysis (DerSimonian-Laird)"""

fig.text(0.5, 0.02, het_text, ha='center', fontsize=10, style='italic', 
         color='gray', fontfamily='monospace')

plt.tight_layout(rect=[0, 0.06, 1, 0.98])
plt.savefig('figures/output/figure_7_forest.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('figures/output/figure_7_forest.pdf', bbox_inches='tight', facecolor='white')
print("Figure 7 saved!")
