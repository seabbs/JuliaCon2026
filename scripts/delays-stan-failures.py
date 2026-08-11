#!/usr/bin/env -S uv run --with matplotlib --script
"""Chart the Stan chain failure rates recorded in primarycensored#34.

Every row below is a run reported by Sam Abbott in the issue thread
between 2024-09-05 and 2024-09-12, read back from the issue with

    gh issue view 34 -R epinowcast/primarycensored --json comments

Nothing here is simulated for the talk. The comment timestamp that
carries each number is in the `source` column of the CSV.

The runs are not all on one dataset. The simulated scenario was made
harder in the same PR that landed the ODE, and one run drops the
truncation adjustment, which is a different model. The closest thing
to a like for like pair is the last two rows, both 600 chains.

Usage:
    ./scripts/delays-stan-failures.py
"""

from pathlib import Path

import matplotlib.pyplot as plt

root = Path(__file__).resolve().parent.parent
png = root / "figures" / "delays-stan-failures.png"
csv = root / "figures" / "delays-stan-failures.csv"

blue = "#1f6fd0"
red = "#d02020"
grey = "#8a8a8a"
dark = "#333333"

# label, chains, failed, kind, source comment timestamp
runs = [
    ("integrate_1d, tolerance 1e-6", 256, 243, "quad",
     "2024-09-05T21:19:15Z"),
    ("tolerance dropped to 1e-2", 256, 47, "quad",
     "2024-09-05T21:25:23Z"),
    ("same code, 600 chains", 600, 151, "quad",
     "2024-09-05T21:57:14Z"),
    ("guard on tiny delays", 600, 146, "quad",
     "2024-09-05T21:57:14Z"),
    ("xc boundary at 0.3 pwindow", 600, 135, "quad",
     "2024-09-05T22:11:30Z"),
    ("xc boundary at 0.1 pwindow", 600, 160, "quad",
     "2024-09-05T22:21:58Z"),
    ("truncation dropped, wrong model", 600, 33, "invalid",
     "2024-09-05T22:33:21Z"),
    ("main at e800dfd", 600, 88, "quad", "2024-09-06T21:04:12Z"),
    ("redundant xc removed, 8fb2c03", 600, 70, "quad",
     "2024-09-06T21:28:39Z"),
    ("recast as ode_rk45", 600, 0, "ode", "2024-09-12T20:32:38Z"),
]

colours = {"quad": red, "invalid": grey, "ode": blue}

rows = ["label,chains,failed,rate_percent,kind,source"]
for label, chains, failed, kind, src in runs:
    rate = 100 * failed / chains
    rows.append(f'"{label}",{chains},{failed},{rate:.4f},{kind},{src}')
csv.write_text("\n".join(rows) + "\n")

plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "cm"

fig, ax = plt.subplots(figsize=(13.6, 6.0))

ys = list(range(len(runs)))
rates = [100 * f / c for _, c, f, _, _ in runs]

for y, (label, chains, failed, kind, _), rate in zip(ys, runs, rates):
    ax.barh(y, max(rate, 0.35), height=0.62, color=colours[kind],
            alpha=0.30 if kind == "invalid" else 0.88,
            edgecolor=colours[kind], linewidth=1.3)
    note = f"{rate:.0f}%  ({failed} of {chains} chains)"
    ax.text(rate + 1.8, y, note, va="center", ha="left",
            fontsize=13, color=colours[kind] if kind == "ode" else dark,
            fontweight="bold" if kind == "ode" else "normal")

ax.set_yticks(ys)
ax.set_yticklabels([r[0] for r in runs], fontsize=13.5)
ax.get_yticklabels()[-1].set_color(blue)
ax.get_yticklabels()[-1].set_fontweight("bold")
ax.invert_yaxis()
ax.set_xlim(0, 118)
ax.set_xticks([0, 25, 50, 75, 100])
ax.set_xticklabels(["0", "25", "50", "75", "100%"], fontsize=13)
ax.set_xlabel("chains that died, per cent", fontsize=14.5)
ax.set_title(
    "Nine days of tuning the quadrature, then one change that worked",
    fontsize=17.5, pad=14,
)

ax.text(
    34, 6,
    "not a valid model, shown because\nit located the interaction",
    fontsize=11.5, color=dark, va="center", ha="left", style="italic",
)

for side in ("top", "right"):
    ax.spines[side].set_visible(False)
ax.spines["left"].set_color("#bbbbbb")
ax.spines["bottom"].set_color("#bbbbbb")
ax.tick_params(axis="y", length=0)
ax.grid(axis="x", color="#e2e2e2", linewidth=0.8)
ax.set_axisbelow(True)

fig.tight_layout()
fig.savefig(png, dpi=200, bbox_inches="tight")

print(png)
print(csv)
