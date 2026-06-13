"""Shared style for faithful Turkish figure recreation (300 dpi, readable fonts).
Data is sourced verbatim from makale.txt legends / tables.cjs — no invented numbers.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

# DejaVu Sans fully supports Turkish glyphs (ş ğ ı İ ç ö ü)
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "axes.titlesize": 17,
    "axes.titleweight": "bold",
    "axes.labelsize": 14,
    "axes.labelweight": "bold",
    "xtick.labelsize": 12.5,
    "ytick.labelsize": 12.5,
    "legend.fontsize": 12,
    "axes.edgecolor": "#5b6b7b",
    "axes.linewidth": 1.1,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.18,
})

# Sequential dark-navy -> light-blue, matching the originals
PALETTE = ["#0d2a4a", "#1f5c8b", "#2e7cb8", "#4a9bd4", "#79bce6", "#a9d3ef", "#cfe6f6"]
NAVY = "#13294a"
TEAL = "#1f8a8a"
RED = "#c0392b"
GREY_BG = "#f4f8fc"
GREY_TXT = "#7a8896"

TITLE_COLOR = "#15263a"


def panel_title(ax, text):
    ax.set_title(text, loc="left", color=TITLE_COLOR, pad=10)


def style_axes(ax, bg=True):
    if bg:
        ax.set_facecolor(GREY_BG)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(colors="#33414f")
    ax.grid(axis="y", color="#d7e1ea", linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)


def bar_labels(ax, bars, values, fmt="{:.1f}", dy=0.0, fontsize=12.5):
    for b, v in zip(bars, values):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + dy, fmt.format(v),
                ha="center", va="bottom", fontweight="bold", fontsize=fontsize,
                color=TITLE_COLOR)


def footer(fig, text):
    fig.text(0.5, 0.005, text, ha="center", va="bottom", color=GREY_TXT,
             fontsize=11.5, style="italic")


def save(fig, path):
    fig.savefig(path, facecolor="white")
    plt.close(fig)
    return path
