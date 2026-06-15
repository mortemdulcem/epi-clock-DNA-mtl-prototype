"""
EpiClock v4.0 - Figure 2: Substance-Specific EAA
Blue-Black Color Scheme - Publication Ready
"""

import matplotlib.pyplot as plt
import numpy as np

# Blue-Black Color Palette (gradient from dark to light)
COLORS = {
    'primary': '#0A2647',
    'secondary': '#144272',
    'accent': '#205295',
    'light': '#2C74B3',
    'highlight': '#0077B6',
    'text': '#1E293B',
    'bg': '#F8FAFC',
}

# 7 shades of blue for substances
BLUE_GRADIENT = ['#0A2647', '#0D3559', '#144272', '#1A5089', '#205295', '#2667A8', '#2C74B3']

# Data
substances = ['Control', 'Alcohol', 'Opioids', 'Cocaine', 'Polysubstance', 'Cannabis', 'Methamphetamine']
eaa = [0.0, 3.2, 4.8, 5.1, 6.2, 2.1, 7.3]
ci_lower = [0, 2.4, 3.9, 4.2, 5.1, 1.3, 5.8]
ci_upper = [0, 4.0, 5.7, 6.0, 7.3, 2.9, 8.8]
n_samples = [5007, 2183, 1360, 1030, 720, 194, 48]

fig = plt.figure(figsize=(18, 10), facecolor='white')
gs = fig.add_gridspec(2, 3, height_ratios=[1.2, 1], hspace=0.35, wspace=0.25)

# Panel A: Main bar chart
ax1 = fig.add_subplot(gs[0, :2])
ax1.set_facecolor(COLORS['bg'])

x = np.arange(len(substances))
bars = ax1.bar(x, eaa, color=BLUE_GRADIENT, edgecolor='white', linewidth=2, width=0.7)

# Error bars
errors = [[eaa[i] - ci_lower[i] for i in range(len(eaa))],
          [ci_upper[i] - eaa[i] for i in range(len(eaa))]]
ax1.errorbar(x, eaa, yerr=errors, fmt='none', color='black', capsize=5, capthick=2, linewidth=2)

# Labels
for i, (v, n) in enumerate(zip(eaa, n_samples)):
    if v > 0:
        ax1.text(i, v + 0.5, f'+{v}\n(n={n})', ha='center', fontsize=9, fontweight='bold', color=COLORS['text'])
    else:
        ax1.text(i, v + 0.3, f'REF\n(n={n})', ha='center', fontsize=9, fontweight='bold', color=COLORS['text'])

ax1.set_xticks(x)
ax1.set_xticklabels(substances, fontsize=11, fontweight='bold', rotation=15, ha='right')
ax1.set_ylabel('Epigenetic Age Acceleration (years)', fontsize=12, fontweight='bold', color=COLORS['text'])
ax1.set_title('A. Substance-Specific Epigenetic Age Acceleration', fontsize=14, 
              fontweight='bold', color=COLORS['primary'], loc='left', pad=10)
ax1.axhline(y=0, color='#DC2626', linestyle='-', linewidth=2)
ax1.set_ylim(-1, 10)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# Panel B: Effect sizes
ax2 = fig.add_subplot(gs[0, 2])
ax2.set_facecolor(COLORS['bg'])

effect_sizes = [0.0, 0.45, 0.68, 0.72, 0.88, 0.30, 1.03]
y_pos = np.arange(len(substances))
bars = ax2.barh(y_pos, effect_sizes, color=BLUE_GRADIENT, edgecolor='white', linewidth=2, height=0.6)

ax2.axvline(x=0.5, color='#F59E0B', linestyle='--', linewidth=2, label='Medium effect')
ax2.axvline(x=0.8, color='#DC2626', linestyle='--', linewidth=2, label='Large effect')

for i, v in enumerate(effect_sizes):
    ax2.text(v + 0.03, i, f'd={v:.2f}', va='center', fontsize=9, fontweight='bold', color=COLORS['text'])

ax2.set_yticks(y_pos)
ax2.set_yticklabels(substances, fontsize=10)
ax2.set_xlabel("Cohen's d", fontsize=12, fontweight='bold', color=COLORS['text'])
ax2.set_title('B. Effect Sizes', fontsize=14, fontweight='bold', color=COLORS['primary'], loc='left', pad=10)
ax2.set_xlim(0, 1.3)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.legend(loc='lower right', fontsize=9)

# Panel C: Ranking
ax3 = fig.add_subplot(gs[1, 0])
ax3.set_facecolor(COLORS['bg'])

sorted_idx = np.argsort(eaa)[::-1]
sorted_substances = [substances[i] for i in sorted_idx]
sorted_eaa = [eaa[i] for i in sorted_idx]
sorted_colors = [BLUE_GRADIENT[i] for i in sorted_idx]

y_pos = np.arange(len(sorted_substances))
bars = ax3.barh(y_pos, sorted_eaa, color=sorted_colors, edgecolor='white', linewidth=2, height=0.6)

for i, v in enumerate(sorted_eaa):
    label = f'+{v} yr' if v > 0 else 'REF'
    ax3.text(v + 0.1, i, label, va='center', fontsize=10, fontweight='bold', color=COLORS['text'])

ax3.set_yticks(y_pos)
ax3.set_yticklabels(sorted_substances, fontsize=10)
ax3.set_xlabel('EAA (years)', fontsize=11, fontweight='bold', color=COLORS['text'])
ax3.set_title('C. EAA Ranking', fontsize=14, fontweight='bold', color=COLORS['primary'], loc='left', pad=10)
ax3.set_xlim(0, 9)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)

# Panel D: Sample distribution
ax4 = fig.add_subplot(gs[1, 1])
ax4.set_facecolor(COLORS['bg'])

# Pie chart
wedges, texts, autotexts = ax4.pie(n_samples, labels=None, colors=BLUE_GRADIENT,
                                    autopct='%1.1f%%', pctdistance=0.75,
                                    wedgeprops=dict(width=0.5, edgecolor='white', linewidth=2))
for autotext in autotexts:
    autotext.set_fontsize(9)
    autotext.set_fontweight('bold')
    autotext.set_color('white')

ax4.set_title('D. Sample Distribution', fontsize=14, fontweight='bold', color=COLORS['primary'], pad=10)

# Legend outside
ax4.legend(wedges, substances, loc='center left', bbox_to_anchor=(0.95, 0.5), fontsize=9)

# Panel E: Statistics table
ax5 = fig.add_subplot(gs[1, 2])
ax5.axis('off')
ax5.set_title('E. Statistical Summary', fontsize=14, fontweight='bold', color=COLORS['primary'], loc='left', pad=10)

table_data = [
    ['Substance', 'EAA', '95% CI', 'p-value'],
    ['Control', '0.0', '-', 'REF'],
    ['Alcohol', '+3.2', '2.4-4.0', '<0.001'],
    ['Opioids', '+4.8', '3.9-5.7', '<0.001'],
    ['Cocaine', '+5.1', '4.2-6.0', '<0.001'],
    ['Polysubstance', '+6.2', '5.1-7.3', '<0.001'],
    ['Cannabis', '+2.1', '1.3-2.9', '0.003'],
    ['Methamphetamine', '+7.3', '5.8-8.8', '<0.001'],
]

table = ax5.table(cellText=table_data, loc='center', cellLoc='center',
                  colWidths=[0.35, 0.2, 0.25, 0.2])
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1.0, 1.8)

# Header style
for i in range(4):
    table[(0, i)].set_facecolor(COLORS['primary'])
    table[(0, i)].set_text_props(color='white', fontweight='bold')

# Alternating row colors
for row in range(1, 8):
    for col in range(4):
        if row % 2 == 0:
            table[(row, col)].set_facecolor('#E8F4FD')
        else:
            table[(row, col)].set_facecolor('white')

# Main title
fig.suptitle('Figure 2. Substance-Specific Epigenetic Age Acceleration',
             fontsize=18, fontweight='bold', color=COLORS['primary'], y=0.98)
fig.text(0.5, 0.01, 'ANOVA: F(6,10535) = 47.3, p < 0.001 | Error bars: 95% CI | Total n = 10,542',
         ha='center', fontsize=11, style='italic', color='gray')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('figures/output/figure_2_substance_eaa.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('figures/output/figure_2_substance_eaa.pdf', bbox_inches='tight', facecolor='white')
print("Figure 2 saved!")
