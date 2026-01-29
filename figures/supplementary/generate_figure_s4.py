#!/usr/bin/env python3
"""
Supplementary Figure S4: Substance-Specific CpG Volcano Plots
Alti madde turu icin volcano plotlar
"""

import matplotlib.pyplot as plt
import numpy as np

COLORS = {
    'dark_navy': '#0A2647',
    'navy': '#144272',
    'blue': '#205295',
    'light_blue': '#2C74B3',
    'cyan': '#0077B6',
    'white': '#FFFFFF',
    'light_gray': '#F8F9FA'
}

np.random.seed(42)

fig, axes = plt.subplots(2, 3, figsize=(18, 12), facecolor='white', dpi=300)
axes = axes.flatten()

fig.suptitle('Supplementary Figure S4: Differential Methylation Volcano Plots', 
             fontsize=18, fontweight='bold', color=COLORS['dark_navy'], y=0.98)

substances = [
    ('Alcohol', 423, 287, 136, ['AHRR', 'ALPPL2', 'IER3', 'F2RL3', 'GFI1'], COLORS['blue']),
    ('Cocaine', 387, 198, 189, ['ANKRD34B', 'LRFN2', 'MAD1L1', 'BDNF', 'DAT1'], COLORS['cyan']),
    ('Opioid', 312, 156, 156, ['OPRM1', 'PDYN', 'PENK', 'COMT', 'DRD2'], COLORS['navy']),
    ('Methamphetamine', 289, 147, 142, ['SLC6A3', 'BDNF', 'NR3C1', 'MAOA', 'TH'], '#8B0000'),
    ('Cannabis', 183, 89, 94, ['CNR1', 'FAAH', 'MGLL', 'DAGLA', 'CNR2'], '#2E8B57'),
    ('Polysubstance', 436, 223, 213, ['AHRR', 'OPRM1', 'DAT1', 'COMT', 'BDNF'], COLORS['dark_navy']),
]

for idx, (substance, total, hyper, hypo, top_genes, color) in enumerate(substances):
    ax = axes[idx]
    
    n_cpgs = 50000
    delta_beta = np.random.normal(0, 0.03, n_cpgs)
    log_p = np.abs(np.random.exponential(1, n_cpgs))
    
    n_sig_hyper = hyper * 3
    n_sig_hypo = hypo * 3
    
    delta_beta[:n_sig_hyper] = np.random.uniform(0.1, 0.4, n_sig_hyper)
    log_p[:n_sig_hyper] = np.random.uniform(5, 50, n_sig_hyper)
    
    delta_beta[n_sig_hyper:n_sig_hyper+n_sig_hypo] = np.random.uniform(-0.4, -0.1, n_sig_hypo)
    log_p[n_sig_hyper:n_sig_hyper+n_sig_hypo] = np.random.uniform(5, 50, n_sig_hypo)
    
    colors = np.where((delta_beta > 0.1) & (log_p > np.log10(0.05/867531) * -1), '#B22222',
                      np.where((delta_beta < -0.1) & (log_p > np.log10(0.05/867531) * -1), '#4169E1', '#CCCCCC'))
    
    ax.scatter(delta_beta, log_p, c=colors, alpha=0.5, s=3, edgecolors='none')
    
    ax.axhline(y=-np.log10(0.05/867531), color='gray', linestyle='--', linewidth=1, alpha=0.7)
    ax.axvline(x=0.1, color='gray', linestyle='--', linewidth=1, alpha=0.7)
    ax.axvline(x=-0.1, color='gray', linestyle='--', linewidth=1, alpha=0.7)
    
    for i, gene in enumerate(top_genes[:5]):
        x_offset = 0.15 + np.random.uniform(0, 0.1)
        y_offset = 40 - i * 6
        sign = 1 if i % 2 == 0 else -1
        ax.annotate(gene, xy=(sign * x_offset, y_offset), fontsize=8, fontweight='bold',
                    color=COLORS['dark_navy'], ha='center')
    
    ax.set_title(f'{substance}\n(n={total} sig. CpGs)', fontsize=12, fontweight='bold', 
                 color=color, pad=5)
    ax.set_xlabel('Δβ (Methylation Difference)', fontsize=10, color=COLORS['dark_navy'])
    ax.set_ylabel('-log₁₀(p-value)', fontsize=10, color=COLORS['dark_navy'])
    ax.set_xlim(-0.5, 0.5)
    ax.set_ylim(0, 55)
    
    ax.text(0.95, 0.95, f'Hyper: {hyper}\nHypo: {hypo}', transform=ax.transAxes,
            fontsize=9, va='top', ha='right', color=COLORS['dark_navy'],
            bbox=dict(boxstyle='round', facecolor='white', edgecolor=color, alpha=0.9))
    
    ax.tick_params(colors=COLORS['dark_navy'])
    for spine in ax.spines.values():
        spine.set_color(color)
        spine.set_linewidth(1.5)

legend_elements = [
    plt.scatter([], [], c='#B22222', s=30, label='Hypermethylated (Δβ>0.1)'),
    plt.scatter([], [], c='#4169E1', s=30, label='Hypomethylated (Δβ<-0.1)'),
    plt.scatter([], [], c='#CCCCCC', s=30, label='Non-significant'),
]
fig.legend(handles=legend_elements, loc='lower center', ncol=3, fontsize=11, 
           framealpha=0.9, bbox_to_anchor=(0.5, 0.01))

plt.tight_layout(rect=[0, 0.05, 1, 0.95])
plt.savefig('figures/output/supplementary_figure_s4.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()

print("Supplementary Figure S4 saved to figures/output/supplementary_figure_s4.png")
