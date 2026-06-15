"""
EpiClock v4.0 - Figure 4: Sample Characteristics
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

BLUE_GRADIENT = ['#0A2647', '#0D3559', '#144272', '#1A5089', '#205295', '#2667A8', '#2C74B3']

# Data
groups = ['Control', 'Alcohol', 'Opioids', 'Cocaine', 'Polysubstance', 'Cannabis', 'Methamphetamine']
n_samples = [5007, 2183, 1360, 1030, 720, 194, 48]
mean_age = [42.3, 45.7, 38.4, 41.2, 36.8, 32.5, 34.1]
sd_age = [14.2, 12.8, 10.5, 11.3, 9.7, 8.9, 7.8]
female_pct = [48.2, 32.1, 38.7, 28.4, 35.2, 41.2, 33.3]
duration_yrs = [0, 12.4, 8.2, 10.1, 11.3, 7.8, 6.5]
sd_duration = [0, 8.3, 5.7, 6.8, 7.2, 4.5, 3.9]

fig = plt.figure(figsize=(18, 12), facecolor='white')
gs = fig.add_gridspec(2, 3, hspace=0.35, wspace=0.3)

# Panel A: Sample Distribution Bar
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_facecolor(COLORS['bg'])

x = np.arange(len(groups))
bars = ax1.bar(x, n_samples, color=BLUE_GRADIENT, edgecolor='white', linewidth=2)

for i, (v, pct) in enumerate(zip(n_samples, [n/sum(n_samples)*100 for n in n_samples])):
    ax1.text(i, v + 100, f'{v}\n({pct:.1f}%)', ha='center', fontsize=8, fontweight='bold', color=COLORS['text'])

ax1.set_xticks(x)
ax1.set_xticklabels(groups, fontsize=9, rotation=30, ha='right')
ax1.set_ylabel('Sample Size (n)', fontsize=11, fontweight='bold', color=COLORS['text'])
ax1.set_title('A. Sample Distribution', fontsize=14, fontweight='bold', 
              color=COLORS['primary'], loc='left', pad=10)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# Panel B: Donut Chart
ax2 = fig.add_subplot(gs[0, 1])

wedges, texts, autotexts = ax2.pie(n_samples, colors=BLUE_GRADIENT,
                                    autopct='%1.1f%%', pctdistance=0.75,
                                    wedgeprops=dict(width=0.5, edgecolor='white', linewidth=2))
for autotext in autotexts:
    autotext.set_fontsize(8)
    autotext.set_fontweight('bold')
    autotext.set_color('white')

ax2.text(0, 0, f'Total\nn={sum(n_samples):,}', ha='center', va='center', 
         fontsize=14, fontweight='bold', color=COLORS['primary'])
ax2.set_title('B. Cohort Composition', fontsize=14, fontweight='bold', 
              color=COLORS['primary'], pad=10)
ax2.legend(wedges, groups, loc='center left', bbox_to_anchor=(1.0, 0.5), fontsize=8)

# Panel C: Age Distribution
ax3 = fig.add_subplot(gs[0, 2])
ax3.set_facecolor(COLORS['bg'])

y_pos = np.arange(len(groups))
bars = ax3.barh(y_pos, mean_age, xerr=sd_age, color=BLUE_GRADIENT, 
                edgecolor='white', linewidth=2, height=0.6, capsize=4)

for i, (m, s) in enumerate(zip(mean_age, sd_age)):
    ax3.text(m + s + 2, i, f'{m:.1f}±{s:.1f}', va='center', fontsize=9, fontweight='bold', color=COLORS['text'])

ax3.set_yticks(y_pos)
ax3.set_yticklabels(groups, fontsize=9)
ax3.set_xlabel('Age (years)', fontsize=11, fontweight='bold', color=COLORS['text'])
ax3.set_title('C. Age Distribution', fontsize=14, fontweight='bold', 
              color=COLORS['primary'], loc='left', pad=10)
ax3.set_xlim(0, 70)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)

# Panel D: Sex Distribution
ax4 = fig.add_subplot(gs[1, 0])
ax4.set_facecolor(COLORS['bg'])

x = np.arange(len(groups))
width = 0.35
male_pct = [100 - f for f in female_pct]

bars1 = ax4.bar(x - width/2, female_pct, width, color=COLORS['light'], 
                edgecolor='white', linewidth=2, label='Female')
bars2 = ax4.bar(x + width/2, male_pct, width, color=COLORS['primary'], 
                edgecolor='white', linewidth=2, label='Male')

for i, (f, m) in enumerate(zip(female_pct, male_pct)):
    ax4.text(i - width/2, f + 1, f'{f:.0f}%', ha='center', fontsize=8, fontweight='bold', color=COLORS['text'])
    ax4.text(i + width/2, m + 1, f'{m:.0f}%', ha='center', fontsize=8, fontweight='bold', color=COLORS['text'])

ax4.set_xticks(x)
ax4.set_xticklabels(groups, fontsize=9, rotation=30, ha='right')
ax4.set_ylabel('Percentage (%)', fontsize=11, fontweight='bold', color=COLORS['text'])
ax4.set_title('D. Sex Distribution', fontsize=14, fontweight='bold', 
              color=COLORS['primary'], loc='left', pad=10)
ax4.legend(loc='upper right', fontsize=9)
ax4.set_ylim(0, 85)
ax4.spines['top'].set_visible(False)
ax4.spines['right'].set_visible(False)

# Panel E: Duration of Use
ax5 = fig.add_subplot(gs[1, 1])
ax5.set_facecolor(COLORS['bg'])

substance_groups = groups[1:]  # Exclude control
dur = duration_yrs[1:]
sd_dur = sd_duration[1:]
colors_dur = BLUE_GRADIENT[1:]

y_pos = np.arange(len(substance_groups))
bars = ax5.barh(y_pos, dur, xerr=sd_dur, color=colors_dur, 
                edgecolor='white', linewidth=2, height=0.6, capsize=4)

for i, (d, s) in enumerate(zip(dur, sd_dur)):
    ax5.text(d + s + 0.5, i, f'{d:.1f}±{s:.1f} yr', va='center', fontsize=9, fontweight='bold', color=COLORS['text'])

ax5.set_yticks(y_pos)
ax5.set_yticklabels(substance_groups, fontsize=9)
ax5.set_xlabel('Duration (years)', fontsize=11, fontweight='bold', color=COLORS['text'])
ax5.set_title('E. Duration of Use', fontsize=14, fontweight='bold', 
              color=COLORS['primary'], loc='left', pad=10)
ax5.set_xlim(0, 25)
ax5.spines['top'].set_visible(False)
ax5.spines['right'].set_visible(False)

# Panel F: Summary Table
ax6 = fig.add_subplot(gs[1, 2])
ax6.axis('off')
ax6.set_title('F. Summary Statistics', fontsize=14, fontweight='bold', 
              color=COLORS['primary'], loc='left', pad=10)

table_data = [['Group', 'n', 'Age', 'Female%', 'Duration'],
              ['Control', '5,007', '42.3±14.2', '48.2%', '-'],
              ['Alcohol', '2,183', '45.7±12.8', '32.1%', '12.4±8.3'],
              ['Opioids', '1,360', '38.4±10.5', '38.7%', '8.2±5.7'],
              ['Cocaine', '1,030', '41.2±11.3', '28.4%', '10.1±6.8'],
              ['Polysubstance', '720', '36.8±9.7', '35.2%', '11.3±7.2'],
              ['Cannabis', '194', '32.5±8.9', '41.2%', '7.8±4.5'],
              ['Methamphetamine', '48', '34.1±7.8', '33.3%', '6.5±3.9'],
              ['TOTAL', '10,542', '-', '-', '-']]

table = ax6.table(cellText=table_data, loc='center', cellLoc='center',
                  colWidths=[0.32, 0.15, 0.2, 0.16, 0.17])
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1.0, 1.6)

# Header and total row styling
for i in range(5):
    table[(0, i)].set_facecolor(COLORS['primary'])
    table[(0, i)].set_text_props(color='white', fontweight='bold')
    table[(8, i)].set_facecolor(COLORS['accent'])
    table[(8, i)].set_text_props(color='white', fontweight='bold')

for row in range(1, 8):
    for col in range(5):
        if row % 2 == 0:
            table[(row, col)].set_facecolor('#E8F4FD')

# Main title
fig.suptitle('Figure 4. Study Cohort Characteristics',
             fontsize=18, fontweight='bold', color=COLORS['primary'], y=0.98)
fig.text(0.5, 0.01, 'Data sources: GEO, UK Biobank, MESA, WHI, FHS, KORA, Rotterdam Study | Values: Mean±SD',
         ha='center', fontsize=11, style='italic', color='gray')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('figures/output/figure_4_sample.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('figures/output/figure_4_sample.pdf', bbox_inches='tight', facecolor='white')
print("Figure 4 saved!")
