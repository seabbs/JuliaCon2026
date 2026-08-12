#!/usr/bin/env -S uv run --with matplotlib --script
"""Draw the natural history timeline used to open the delays talk.

Usage:
    ./scripts/delays-natural-history.py
"""

from pathlib import Path

import matplotlib.pyplot as plt

root = Path(__file__).resolve().parent.parent
out = root / "figures" / "delays-natural-history.png"

blue = "#1f6fd0"
red = "#d02020"
grey = "#4d4d4d"
faint = "#9a9a9a"

plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "cm"

fig, ax = plt.subplots(figsize=(12.2, 4.6))

events = [
    (1.0, "infection", blue),
    (4.4, "symptom\nonset", red),
    (7.4, "hospitalisation", grey),
    (11.0, "death", grey),
]

for x, label, colour in events:
    ax.plot([x, x], [-0.16, 0.16], color=colour, lw=2.4,
            solid_capstyle="butt")
    ax.text(x, -0.42, label, color=colour, ha="center", va="top",
            fontsize=14, linespacing=1.35)

delays = [
    (1.0, 4.4, 0.95, "incubation period", blue),
    (4.4, 7.4, 1.85, "onset to hospitalisation", grey),
    (4.4, 11.0, 2.75, "onset to death", grey),
]

for x0, x1, y, label, colour in delays:
    for x in (x0, x1):
        ax.plot([x, x], [0.1, y], color=faint, lw=0.9,
                linestyle=(0, (2, 3)))
    ax.annotate("", xy=(x1, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle="<->", color=colour, lw=2.0))
    ax.text((x0 + x1) / 2, y + 0.1, label, color=colour, ha="center",
            va="bottom", fontsize=14)

ax.annotate("", xy=(12.6, 0), xytext=(0.1, 0),
            arrowprops=dict(arrowstyle="-|>", color="black", lw=1.8,
                            mutation_scale=18))
ax.text(12.75, 0, "time", ha="left", va="center", fontsize=14)

ax.set_xlim(0, 13.8)
ax.set_ylim(-1.5, 3.5)
ax.axis("off")

fig.tight_layout(pad=0.2)
fig.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
print(out)
