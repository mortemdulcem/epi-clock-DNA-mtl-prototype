#!/usr/bin/env python3
"""
Master script to generate all supplementary materials
"""

import subprocess
import sys
import os

os.chdir('/home/user/Workspaces/EpiClock')

scripts = [
    'figures/supplementary/generate_table_s1.py',
    'figures/supplementary/generate_table_s2.py',
    'figures/supplementary/generate_table_s3.py',
    'figures/supplementary/generate_table_s4.py',
    'figures/supplementary/generate_table_s5.py',
    'figures/supplementary/generate_table_s6.py',
    'figures/supplementary/generate_figure_s1.py',
    'figures/supplementary/generate_figure_s2.py',
    'figures/supplementary/generate_figure_s3.py',
    'figures/supplementary/generate_figure_s4.py',
    'figures/supplementary/generate_figure_s5.py',
    'figures/supplementary/generate_figure_s6.py',
    'figures/supplementary/generate_figure_s7.py',
    'figures/supplementary/generate_figure_s8.py',
]

print("=" * 60)
print("GENERATING ALL SUPPLEMENTARY MATERIALS")
print("=" * 60)

for script in scripts:
    print(f"\nRunning: {script}")
    try:
        result = subprocess.run([sys.executable, script], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  SUCCESS: {result.stdout.strip()}")
        else:
            print(f"  ERROR: {result.stderr}")
    except Exception as e:
        print(f"  EXCEPTION: {e}")

print("\n" + "=" * 60)
print("ALL SUPPLEMENTARY MATERIALS GENERATED")
print("=" * 60)
