#!/usr/bin/env -S uv run --with matplotlib --script
"""Draw the right truncation figure used in the delays talk.

Reads figures/delays-right-truncation.csv, which is written by
scripts/delays-right-truncation.jl from CensoredDistributions.jl output.

Usage:
    julia --project=/path/to/CensoredDistributions.jl \\
        scripts/delays-right-truncation.jl
    ./scripts/delays-right-truncation.py
"""

import csv
from pathlib import Path

import matplotlib.pyplot as plt

root = Path(__file__).resolve().parent.parent
src = root / "figures" / "delays-right-truncation.csv"
out = root / "figures" / "delays-right-truncation.png"

blue = "#1f6fd0"
red = "#d02020"
grey = "#4d4d4d"

plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "cm"

series = {}
with src.open() as fh:
    for row in csv.DictReader(fh):
        key = (row["kind"], row["series"])
        series.setdefault(key, []).append((float(row["x"]), float(row["y"])))


def xy(kind, name):
    pairs = sorted(series[(kind, name)])
    return [p[0] for p in pairs], [p[1] for p in pairs]


fig, (ax, bx) = plt.subplots(1, 2, figsize=(13.4, 4.4),
                             gridspec_kw={"width_ratios": [1.15, 1]})

x_full, y_full = xy("pmf", "full")
ax.step(x_full, y_full, where="mid", color=grey, lw=2.0,
        label="true delay distribution")
ax.fill_between(x_full, y_full, step="mid", color=grey, alpha=0.10)

for cut, colour in ((7, red), (14, blue)):
    x_cut, y_cut = xy("pmf", f"cut{cut}")
    ax.step(x_cut, y_cut, where="mid", color=colour, lw=2.0,
            label=f"seen by day {cut}")
    ax.plot([cut, cut], [0, 0.235], color=colour, lw=1.4,
            linestyle=(0, (5, 4)))

ax.set_xlim(-0.6, 24)
ax.set_ylim(0, 0.26)
ax.set_xlabel("delay (days)", fontsize=13)
ax.set_ylabel("probability", fontsize=13)
ax.set_title("Only short delays have had time to appear",
             fontsize=14, pad=10)
ax.legend(frameon=False, fontsize=12, loc="upper right")

x_mean, y_mean = xy("mean", "truncated")
true_mean = series[("mean", "full")][0][1]

bx.axhline(true_mean, color=grey, lw=1.6, linestyle=(0, (5, 4)))
bx.text(38.5, true_mean + 0.13, f"true mean {true_mean:.1f} days",
        color=grey, ha="right", va="bottom", fontsize=12)
bx.plot(x_mean, y_mean, color="black", lw=2.2)

for cut, colour in ((7, red), (14, blue)):
    value = dict(zip(x_mean, y_mean))[cut]
    bx.plot([cut], [value], "o", color=colour, ms=8)
    drop = 100 * (1 - value / true_mean)
    bx.annotate(f"{value:.1f} days, {drop:.0f}% low",
                xy=(cut, value), xytext=(cut + 1.4, value - 0.85),
                color=colour, fontsize=12,
                arrowprops=dict(arrowstyle="-", color=colour, lw=1.0))

bx.set_xlim(2, 40)
bx.set_ylim(1.6, 6.6)
bx.set_xlabel("days since the primary event (cutoff $C$)", fontsize=13)
bx.set_ylabel("mean estimated delay (days)", fontsize=13)
bx.set_title("The bias grows the closer the cutoff is to now",
             fontsize=14, pad=10)

for panel in (ax, bx):
    panel.spines["top"].set_visible(False)
    panel.spines["right"].set_visible(False)
    panel.tick_params(labelsize=11)

fig.tight_layout(pad=0.6)
fig.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
print(out)
