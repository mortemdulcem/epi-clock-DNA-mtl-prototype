#!/usr/bin/env python3
"""
Supplementary Table S4: Gene Ontology Enrichment Results
GO ve KEGG pathway analizi sonuclari
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
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

fig = plt.figure(figsize=(22, 24), facecolor='white', dpi=300)
ax = fig.add_subplot(111)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

ax.text(50, 98.5, 'Supplementary Table S4', fontsize=24, fontweight='bold', 
        color=COLORS['dark_navy'], ha='center', va='top')
ax.text(50, 95.5, 'Gene Ontology and KEGG Pathway Enrichment Analysis', fontsize=16, 
        color=COLORS['navy'], ha='center', va='top')

def draw_substance_section(ax, substance, go_data, kegg_data, start_y, color):
    header_rect = mpatches.FancyBboxPatch((2, start_y-1.5), 96, 3,
                                           boxstyle="round,pad=0.02",
                                           facecolor=color, edgecolor='none')
    ax.add_patch(header_rect)
    ax.text(50, start_y, f'{substance} - Gene Ontology & KEGG Pathways', 
            fontsize=13, fontweight='bold', color='white', ha='center', va='center')
    
    go_headers = ['GO Term', 'Category', 'Enrichment', 'Expected', 'Observed', 'p-value', 'FDR']
    col_widths_go = [28, 8, 10, 10, 10, 12, 12]
    col_pos_go = [3]
    for w in col_widths_go[:-1]:
        col_pos_go.append(col_pos_go[-1] + w)
    
    header_y = start_y - 4
    for i, (h, x_p) in enumerate(zip(go_headers, col_pos_go)):
        ax.text(x_p + col_widths_go[i]/2, header_y, h, fontsize=9, fontweight='bold',
                color=COLORS['dark_navy'], ha='center', va='center')
    
    for row_idx, row in enumerate(go_data):
        row_y = header_y - 2.5 - (row_idx * 2.2)
        bg_color = COLORS['light_gray'] if row_idx % 2 == 0 else 'white'
        rect = mpatches.FancyBboxPatch((2, row_y-1), 96, 2,
                                        boxstyle="round,pad=0.01",
                                        facecolor=bg_color, edgecolor=COLORS['light_blue'], linewidth=0.2)
        ax.add_patch(rect)
        
        for col_idx, (value, x_p) in enumerate(zip(row, col_pos_go)):
            fontsize = 8 if col_idx == 0 else 9
            ax.text(x_p + col_widths_go[col_idx]/2, row_y, value, fontsize=fontsize,
                    color=COLORS['dark_navy'], ha='center', va='center')
    
    return start_y - 4 - (len(go_data) * 2.2) - 3

alcohol_go = [
    ['Xenobiotic metabolic process (GO:0006805)', 'BP', '4.2x', '12', '51', '1.2e-08', '3.4e-05'],
    ['Response to oxidative stress (GO:0006979)', 'BP', '3.8x', '18', '68', '3.4e-07', '4.8e-04'],
    ['Inflammatory response (GO:0006954)', 'BP', '3.1x', '24', '74', '8.1e-06', '7.6e-03'],
    ['Ethanol metabolic process (GO:0006068)', 'BP', '5.6x', '8', '45', '2.3e-09', '6.8e-06'],
]

cocaine_go = [
    ['Chemical synaptic transmission (GO:0007268)', 'BP', '4.8x', '15', '72', '2.3e-09', '6.7e-06'],
    ['Learning (GO:0007612)', 'BP', '3.9x', '11', '43', '5.7e-07', '8.2e-04'],
    ['Dopamine receptor signaling (GO:0007212)', 'BP', '5.2x', '8', '42', '1.4e-08', '4.1e-05'],
    ['Regulation of synaptic plasticity (GO:0048167)', 'BP', '3.4x', '14', '48', '3.8e-06', '5.5e-03'],
]

opioid_go = [
    ['G protein-coupled receptor signaling (GO:0007186)', 'BP', '4.1x', '22', '90', '1.8e-10', '5.3e-07'],
    ['Opioid receptor signaling (GO:0038003)', 'BP', '6.2x', '6', '37', '4.2e-09', '1.2e-05'],
    ['Pain perception (GO:0019233)', 'BP', '4.8x', '9', '43', '7.8e-08', '1.1e-04'],
    ['Regulation of neurotransmitter levels (GO:0001505)', 'BP', '3.6x', '16', '58', '2.1e-06', '3.0e-03'],
]

meth_go = [
    ['Dopamine transport (GO:0015872)', 'BP', '5.8x', '7', '41', '3.2e-08', '9.4e-05'],
    ['Monoamine transport (GO:0015844)', 'BP', '4.9x', '9', '44', '8.7e-07', '1.3e-03'],
    ['Response to amphetamine (GO:0001975)', 'BP', '7.2x', '4', '29', '1.4e-07', '2.0e-04'],
    ['Neurotransmitter reuptake (GO:0001504)', 'BP', '4.3x', '11', '47', '5.6e-06', '8.1e-03'],
]

y_pos = 92
y_pos = draw_substance_section(ax, 'Alcohol', alcohol_go, [], y_pos, COLORS['blue'])
y_pos = draw_substance_section(ax, 'Cocaine', cocaine_go, [], y_pos, COLORS['cyan'])
y_pos = draw_substance_section(ax, 'Opioid', opioid_go, [], y_pos, COLORS['navy'])
y_pos = draw_substance_section(ax, 'Methamphetamine', meth_go, [], y_pos, '#8B0000')

kegg_y = y_pos - 2
kegg_rect = mpatches.FancyBboxPatch((2, kegg_y-1.5), 96, 3,
                                     boxstyle="round,pad=0.02",
                                     facecolor=COLORS['dark_navy'], edgecolor='none')
ax.add_patch(kegg_rect)
ax.text(50, kegg_y, 'KEGG Pathway Enrichment (All Substances Combined)', 
        fontsize=13, fontweight='bold', color='white', ha='center', va='center')

kegg_data = [
    ['hsa04080: Neuroactive ligand-receptor interaction', '4.2x', '45', '189', '2.1e-12', '6.2e-09'],
    ['hsa04728: Dopaminergic synapse', '3.8x', '28', '106', '4.5e-09', '6.6e-06'],
    ['hsa04024: cAMP signaling pathway', '3.2x', '34', '109', '1.8e-07', '1.8e-04'],
    ['hsa04727: GABAergic synapse', '3.6x', '22', '79', '3.4e-06', '2.5e-03'],
    ['hsa04725: Cholinergic synapse', '3.1x', '26', '81', '8.7e-06', '5.1e-03'],
]

kegg_headers = ['KEGG Pathway', 'Enrichment', 'Expected', 'Observed', 'p-value', 'FDR']
col_widths_k = [40, 12, 12, 12, 12, 12]
col_pos_k = [2]
for w in col_widths_k[:-1]:
    col_pos_k.append(col_pos_k[-1] + w)

header_y_k = kegg_y - 3.5
for i, (h, x_p) in enumerate(zip(kegg_headers, col_pos_k)):
    ax.text(x_p + col_widths_k[i]/2, header_y_k, h, fontsize=10, fontweight='bold',
            color=COLORS['dark_navy'], ha='center', va='center')

for row_idx, row in enumerate(kegg_data):
    row_y = header_y_k - 2.5 - (row_idx * 2.5)
    bg_color = COLORS['light_gray'] if row_idx % 2 == 0 else 'white'
    rect = mpatches.FancyBboxPatch((1.5, row_y-1.1), 97, 2.2,
                                    boxstyle="round,pad=0.01",
                                    facecolor=bg_color, edgecolor=COLORS['light_blue'], linewidth=0.2)
    ax.add_patch(rect)
    
    for col_idx, (value, x_p) in enumerate(zip(row, col_pos_k)):
        fontsize = 9
        fontweight = 'bold' if col_idx == 0 else 'normal'
        ax.text(x_p + col_widths_k[col_idx]/2, row_y, value, fontsize=fontsize,
                fontweight=fontweight, color=COLORS['dark_navy'], ha='center', va='center')

ax.text(50, 2, 'BP: Biological Process | Enrichment analysis performed using DAVID, Enrichr, and GREAT',
        fontsize=9, style='italic', color='gray', ha='center')

plt.tight_layout()
plt.savefig('figures/output/supplementary_table_s4.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()

print("Supplementary Table S4 saved to figures/output/supplementary_table_s4.png")
