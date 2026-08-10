#!/usr/bin/env -S uv run --with matplotlib --script
"""Draw the double censoring diagram used in the delays talk.

Usage:
    ./scripts/delays-double-censoring.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

root = Path(__file__).resolve().parent.parent
out = root / "figures" / "delays-double-censoring.png"

blue = "#1f6fd0"
red = "#d02020"
grey = "#4d4d4d"

plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "cm"

fig, ax = plt.subplots(figsize=(12.2, 3.9))

p0, p1 = 1.2, 2.6
s0, s1 = 7.8, 9.2
cutoff = 11.0

ax.add_patch(Rectangle((p0, 0), p1 - p0, 1.7, facecolor=blue,
                       edgecolor=blue, alpha=0.18, linewidth=1.4))
ax.add_patch(Rectangle((p0, 0), p1 - p0, 1.7, facecolor="none",
                       edgecolor=blue, linewidth=1.4))
ax.add_patch(Rectangle((s0, 0), s1 - s0, 1.7, facecolor=red,
                       edgecolor=red, alpha=0.14, linewidth=1.4))
ax.add_patch(Rectangle((s0, 0), s1 - s0, 1.7, facecolor="none",
                       edgecolor=red, linewidth=1.4))

ax.annotate("", xy=(p1, 1.45), xytext=(p0, 1.45),
            arrowprops=dict(arrowstyle="<->", color=blue, lw=1.4))
ax.text((p0 + p1) / 2, 1.52, r"$w_P$", color=blue, ha="center",
        va="bottom", fontsize=13)
ax.annotate("", xy=(s1, 1.45), xytext=(s0, 1.45),
            arrowprops=dict(arrowstyle="<->", color=red, lw=1.4))
ax.text((s0 + s1) / 2, 1.52, r"$w_S$", color=red, ha="center",
        va="bottom", fontsize=13)

ax.text((p0 + p1) / 2, 2.35, "primary event\nwindow", color=blue,
        ha="center", va="bottom", fontsize=14, linespacing=1.4)
ax.text((s0 + s1) / 2, 2.35, "secondary event\nwindow",
        color=red, ha="center", va="bottom", fontsize=14, linespacing=1.4)

ax.annotate("", xy=(s0 + 0.45, 0.85), xytext=(p0 + 0.45, 0.85),
            arrowprops=dict(arrowstyle="<->", color=grey, lw=2.0))
ax.text((p0 + s0) / 2 + 0.45, 0.95, r"delay $T = S - P$", color=grey,
        ha="center", va="bottom", fontsize=14)

ax.plot([cutoff, cutoff], [-0.15, 3.0], color="#333333", lw=1.8,
        linestyle=(0, (6, 4)))
ax.text(cutoff, 3.15, "observation\ncutoff $C$", color="#333333",
        ha="center", va="bottom", fontsize=14, linespacing=1.4)

ax.text(12.1, 1.15, "longer delays\nnot yet seen", color="#555555",
        ha="center", va="bottom", fontsize=12.5, linespacing=1.4)
ax.annotate("", xy=(12.6, 0.85), xytext=(11.6, 0.85),
            arrowprops=dict(arrowstyle="->", color="#555555", lw=1.2))

ax.annotate("", xy=(13.3, 0), xytext=(0.1, 0),
            arrowprops=dict(arrowstyle="-|>", color="black", lw=1.8,
                            mutation_scale=18))
ax.text(13.45, 0, "time", ha="left", va="center", fontsize=14)

ax.set_xlim(0, 14.2)
ax.set_ylim(-0.6, 4.0)
ax.axis("off")

fig.tight_layout(pad=0.2)
fig.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
print(out)
