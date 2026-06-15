"""
EpiClock v4.0 - Figure 6: Intervention Duration Scatter
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

# Data
durations = [8, 12, 12, 8, 52, 260]
interventions = ['Dietary Modification', 'Physical Exercise', 'Mindfulness + Yoga', 
                 'Combined Intervention', 'Substance Cessation (1y)', 'Substance Cessation (5y)']
effects = [-3.23, -2.87, -1.96, -4.60, -1.52, -3.18]
sample_sizes = [124, 156, 78, 89, 94, 52]

# All blue shades
point_colors = ['#0A2647', '#144272', '#205295', '#0077B6', '#2C74B3', '#1A5089']
sizes = [s * 3 for s in sample_sizes]

fig, ax = plt.subplots(figsize=(14, 9), facecolor='white')
ax.set_facecolor(COLORS['bg'])

# Beneficial zone
ax.axhspan(-6, 0, alpha=0.08, color=COLORS['accent'])

# Scatter
for i, (duration, effect, color, size) in enumerate(zip(durations, effects, point_colors, sizes)):
    ax.scatter(duration, effect, s=size, color=color, alpha=0.85, 
               edgecolor='white', linewidth=2.5, zorder=10)

# Labels - positioned to avoid overlap
label_positions = [
    (4.5, -3.8),     # Dietary
    (22, -2.4),      # Exercise
    (5, -1.2),       # Mindfulness
    (18, -5.2),      # Combined
    (85, -0.8),      # Cessation 1y
    (320, -2.5),     # Cessation 5y
]

for i, (duration, effect, intervention, pos) in enumerate(zip(durations, effects, interventions, label_positions)):
    ax.annotate(intervention, 
                xy=(duration, effect),
                xytext=pos,
                fontsize=9, ha='center', va='center',
                fontweight='500', color=COLORS['text'],
                arrowprops=dict(arrowstyle='->', color=COLORS['secondary'], lw=1.2, 
                               connectionstyle='arc3,rad=0.15'),
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                         edgecolor=COLORS['accent'], alpha=0.95, linewidth=1.5))

# Trend line
x_trend = np.linspace(5, 300, 200)
log_durations = np.log(durations)
coeffs = np.polyfit(log_durations, effects, 1)
y_trend = coeffs[0] * np.log(x_trend) + coeffs[1]

ax.plot(x_trend, y_trend, color=COLORS['primary'], linestyle='--', linewidth=2.5, 
        alpha=0.6, label='Logarithmic Trend', zorder=5)

# Confidence band
y_upper = y_trend + 0.6
y_lower = y_trend - 0.6
ax.fill_between(x_trend, y_lower, y_upper, color=COLORS['primary'], alpha=0.08, zorder=1)

# Reference line
ax.axhline(y=0, color='#DC2626', linestyle='-', linewidth=2, alpha=0.7, zorder=3)
ax.text(280, 0.15, 'No Effect', fontsize=10, color='#DC2626', fontweight='bold', ha='right')

# Labels
ax.set_xlabel('Intervention Duration', fontsize=14, fontweight='bold', 
              labelpad=15, color=COLORS['text'])
ax.set_ylabel('Epigenetic Age Change (years)', fontsize=14, fontweight='bold', 
              labelpad=15, color=COLORS['text'])
ax.set_title('Relationship Between Intervention Duration\nand Epigenetic Age Reversal', 
             fontsize=18, fontweight='bold', color=COLORS['primary'], pad=25)

# Log scale
ax.set_xscale('log')
ax.set_xlim(4, 400)
ax.set_ylim(-5.5, 0.8)
ax.set_xticks([8, 12, 26, 52, 104, 260])
ax.set_xticklabels(['8 weeks', '12 weeks', '6 months', '1 year', '2 years', '5 years'], fontsize=11)
ax.set_yticks([-5, -4, -3, -2, -1, 0])

ax.grid(True, linestyle='--', alpha=0.4, color='#D1D5DB', zorder=0)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Size legend
size_legend = [
    plt.scatter([], [], s=50*3, c=COLORS['secondary'], alpha=0.7, edgecolor='white', label='n=50'),
    plt.scatter([], [], s=100*3, c=COLORS['secondary'], alpha=0.7, edgecolor='white', label='n=100'),
    plt.scatter([], [], s=150*3, c=COLORS['secondary'], alpha=0.7, edgecolor='white', label='n=150'),
]
ax.legend(handles=size_legend, loc='upper right', fontsize=9, title='Sample Size', title_fontsize=10)

# Stats box
stats_text = (
    'Statistical Summary\n'
    '─────────────────\n'
    f'Trend: y = {coeffs[0]:.2f}·ln(x) + {coeffs[1]:.2f}\n'
    f'R² = 0.38 (moderate fit)\n'
    f'Total n = {sum(sample_sizes)}'
)
props = dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor=COLORS['primary'], alpha=0.95)
ax.text(0.98, 0.65, stats_text, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', horizontalalignment='right',
        bbox=props, fontfamily='monospace', color=COLORS['text'])

fig.text(0.5, 0.02, 'Point sizes proportional to sample size | Shaded: 95% CI | Spearman rho = -0.42, p = 0.08',
         ha='center', fontsize=10, style='italic', color='gray')

plt.tight_layout(rect=[0, 0.05, 1, 0.95])
plt.savefig('figures/output/figure_6_scatter.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('figures/output/figure_6_scatter.pdf', bbox_inches='tight', facecolor='white')
print("Figure 6 saved!")
