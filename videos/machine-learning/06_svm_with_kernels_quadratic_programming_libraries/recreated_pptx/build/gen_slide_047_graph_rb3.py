#!/usr/bin/env python3
"""Slide 047 graph (rebuild wave 3) — full-slide transparent PNG.

Geometry measured from qa/rejudge2/orig_png/slide_047.png (960x540):
  plot spines x=207..752, y=64..502  ->  figure-fraction axes rect below.
Content per qa/reanalysis2/slide_047_analysis.txt:
  x 0..35 ticks every 5, y -10..40 ticks every 10,
  light-gray dot lattice over the domain + blue/red/black spiral dot arms.
Run: python3 gen_slide_047_graph_rb3.py <out.png>
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = sys.argv[1] if len(sys.argv) > 1 else "slide_047_graph_rb3.png"
DPI = 200
W_IN, H_IN = 13.33, 7.5

# axes rect in figure fraction (from measured spines)
AX = [207 / 960.0, (540 - 502) / 540.0, (752 - 207) / 960.0, (502 - 64) / 540.0]
XLIM, YLIM = (0, 35), (-10, 40)
CX, CY = 17.5, 15.0

SPIRALS = [
    {"color": "#FF0000", "r0": 1.0, "r1": 24.0, "off": 0.0, "s": 14},
    {"color": "#000000", "r0": 0.7, "r1": 20.0, "off": 2.1, "s": 12},
    {"color": "#0000FF", "r0": 0.4, "r1": 13.5, "off": 4.2, "s": 10},
]


def spiral(r0, r1, off, n=900, turns=2.5):
    t = np.linspace(0, 1, n)
    r = r0 + t * (r1 - r0)
    a = t * turns * 2 * np.pi + off
    return CX + r * np.cos(a), CY + r * np.sin(a)


fig = plt.figure(figsize=(W_IN, H_IN), dpi=DPI)
fig.patch.set_alpha(0.0)
ax = fig.add_axes(AX)
ax.set_xlim(*XLIM)
ax.set_ylim(*YLIM)
ax.set_facecolor("white")

gx, gy = np.meshgrid(np.arange(0, 35.01, 0.75), np.arange(-10, 40.01, 0.75))
ax.scatter(gx, gy, s=4, c="#CCCCCC", marker=".", linewidths=0, zorder=1)

for sp in SPIRALS:
    xs, ys = spiral(sp["r0"], sp["r1"], sp["off"])
    ax.scatter(xs, ys, s=sp["s"], c=sp["color"], marker="o", linewidths=0, zorder=3)

ax.set_xticks(range(0, 36, 5))
ax.set_yticks(range(-10, 41, 10))
ax.tick_params(length=3.5, width=1.0, labelsize=9, colors="black")
for spine in ax.spines.values():
    spine.set_linewidth(1.0)
    spine.set_color("black")

fig.savefig(OUT, dpi=DPI, transparent=True)
plt.close(fig)
print("wrote", OUT)
