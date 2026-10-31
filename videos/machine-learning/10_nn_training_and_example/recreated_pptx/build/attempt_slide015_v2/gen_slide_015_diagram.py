#!/usr/bin/env python3
"""Slide 15 neural-network diagram. Canvas == placed image area exactly.

Placed in pptx at x=0.5, y=1.35, w=12.3, h=4.9 -> canvas in = 12.3 x 4.9.
All coordinates below are inches in that local space; save with bbox=None so
the PNG is pixel-exact to the placement (no tight-crop distortion).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch

W_IN, H_IN = 12.3, 4.9
fig = plt.figure(figsize=(W_IN, H_IN), dpi=600)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W_IN)
ax.set_ylim(0, H_IN)
ax.axis("off")
fig.patch.set_alpha(0.0)

SIGMA = "#C0392B"
WTXT = "#2980B9"
BIAS = "#8E44AD"
CY = 2.45
R = 0.26
COL1, COL2, COL3 = 1.6, 5.9, 10.2

rowy = [CY - 0.85, CY, CY + 0.85]

# Input column (white + sigma, f[] boxes, ellipsis)
for i, y in enumerate(rowy):
    ax.add_patch(Circle((COL1, y), R, facecolor="white", edgecolor="black", linewidth=1.4, zorder=5))
    ax.text(COL1, y, r"$\Sigma$", fontsize=23, fontweight="bold", color=SIGMA, ha="center", va="center", zorder=6)
    ax.add_patch(FancyBboxPatch((COL1 + 0.42, y - 0.14), 0.52, 0.28, boxstyle="round,pad=0.02",
                                facecolor="none", edgecolor="black", linewidth=1.1, zorder=4))
    ax.text(COL1 + 0.68, y, "f", fontsize=12, fontweight="bold", color="black", ha="center", va="center", zorder=5)
    if i == 1:
        ax.text(COL1 + 1.15, y, "...", fontsize=15, color="black", ha="center", va="center", zorder=5)

# Hidden column (green + sigma), Net_j / O_j labels, bias circles
for i, y in enumerate(rowy):
    ax.add_patch(Circle((COL2, y), R, facecolor="#90EE90", edgecolor="black", linewidth=1.4, zorder=5))
    ax.text(COL2, y, r"$\Sigma$", fontsize=23, fontweight="bold", color=SIGMA, ha="center", va="center", zorder=6)
    ax.text(COL2 - 0.75, y + 0.42, r"$Net_j$", fontsize=13, fontweight="bold", color=SIGMA, ha="center", va="center", zorder=6)
    ax.text(COL2 + 0.72, y + 0.42, r"$O_j$", fontsize=13, color="black", ha="center", va="center", zorder=6)
    ax.add_patch(FancyBboxPatch((COL2 + 0.42, y - 0.14), 0.52, 0.28, boxstyle="round,pad=0.02",
                                facecolor="none", edgecolor="black", linewidth=1.1, zorder=4))
    ax.text(COL2 + 0.68, y, "f", fontsize=12, fontweight="bold", color="black", ha="center", va="center", zorder=5)
    ax.add_patch(Circle((COL2 - 1.15, y - 0.55), 0.17, facecolor=BIAS, edgecolor="black", linewidth=1, zorder=5))
    ax.text(COL2 - 1.15, y - 0.55, "1", fontsize=8, fontweight="bold", color="white", ha="center", va="center", zorder=6)

# Output column (orange + sigma), Net_k / O_k labels, bias circles
for i, y in enumerate(rowy):
    ax.add_patch(Circle((COL3, y), R, facecolor="#FFA07A", edgecolor="black", linewidth=1.4, zorder=5))
    ax.text(COL3, y, r"$\Sigma$", fontsize=23, fontweight="bold", color=SIGMA, ha="center", va="center", zorder=6)
    ax.text(COL3 - 0.75, y + 0.42, r"$Net_k$", fontsize=13, fontweight="bold", color=SIGMA, ha="center", va="center", zorder=6)
    ax.text(COL3 + 0.72, y + 0.42, r"$O_k$", fontsize=13, color="black", ha="center", va="center", zorder=6)
    ax.add_patch(FancyBboxPatch((COL3 + 0.42, y - 0.14), 0.52, 0.28, boxstyle="round,pad=0.02",
                                facecolor="none", edgecolor="black", linewidth=1.1, zorder=4))
    ax.text(COL3 + 0.68, y, "f", fontsize=12, fontweight="bold", color="black", ha="center", va="center", zorder=5)
    ax.add_patch(Circle((COL3 - 1.15, y - 0.55), 0.17, facecolor=BIAS, edgecolor="black", linewidth=1, zorder=5))
    ax.text(COL3 - 1.15, y - 0.55, "1", fontsize=8, fontweight="bold", color="white", ha="center", va="center", zorder=6)

# Inter-layer arrows
for iy in rowy:
    for hy in rowy:
        ax.add_patch(FancyArrowPatch((COL1 + R + 0.55, iy), (COL2 - R, hy),
                                     connectionstyle="arc3,rad=0.06",
                                     arrowstyle="->", mutation_scale=8, linewidth=0.7,
                                     color="#808080", zorder=3))
for hy in rowy:
    for oy in rowy:
        ax.add_patch(FancyArrowPatch((COL2 + R + 0.55, hy), (COL3 - R, oy),
                                     connectionstyle="arc3,rad=-0.06",
                                     arrowstyle="->", mutation_scale=8, linewidth=0.7,
                                     color="#808080", zorder=3))

# Weight labels on the arrows
for dx, lab in [((COL1 + COL2) / 2, r"$w_{ji}$"), ((COL2 + COL3) / 2, r"$w_{kj}$")]:
    ax.text(dx, CY + 1.22, lab, fontsize=12, fontweight="bold", color=WTXT, ha="center", va="center", zorder=6)
    ax.text(dx + 0.35, CY - 1.22, lab, fontsize=12, fontweight="bold", color=WTXT, ha="center", va="center", zorder=6)

# Input-dot cluster + Input Sample arrow
for dy in (-0.22, 0, 0.22):
    ax.add_patch(Circle((0.42, CY + dy / 3.2), 0.075, facecolor=BIAS, edgecolor="black", linewidth=0.8, zorder=5))
ax.add_patch(FancyArrowPatch((0.6, CY), (COL1 - R, CY),
                             connectionstyle="arc3,rad=0",
                             arrowstyle="->", mutation_scale=12, linewidth=1.6,
                             color=BIAS, zorder=3))
ax.text(0.45, CY + 0.5, "Input\nSample", fontsize=11, fontweight="bold", color=BIAS,
        ha="center", va="center", zorder=6)

# Target-label feed from output column
ax.add_patch(FancyArrowPatch((COL3 + 0.95, CY), (W_IN - 0.45, CY),
                             connectionstyle="arc3,rad=0",
                             arrowstyle="->", mutation_scale=12, linewidth=1.6,
                             color=BIAS, zorder=3))
ax.text(W_IN - 0.05, CY + 0.5, "Target\nLabel", fontsize=11, fontweight="bold", color=BIAS,
        ha="right", va="center", zorder=6)

# Output labels
for i, lab in enumerate(["Output 1", "Output 2", "Output m"]):
    ax.add_patch(FancyBboxPatch((COL3 + 1.0, rowy[i] - 0.16), 1.05, 0.32, boxstyle="round,pad=0.02",
                                facecolor="#FFA07A", edgecolor="#FF4500", linewidth=1.3, zorder=4))
    ax.text(COL3 + 1.52, rowy[i], lab, fontsize=10, fontweight="bold", color="#FF4500",
            ha="center", va="center", zorder=5)

# Dashed backprop error curves
for i, oy in enumerate(rowy):
    ax.add_patch(FancyArrowPatch((COL3 + 0.6, oy), (COL2 - 0.45, rowy[i]),
                                 connectionstyle="arc3,rad=0.35",
                                 arrowstyle="->", mutation_scale=8, linewidth=1.1,
                                 color="#C00000", linestyle="--", zorder=3))

# Node Bias label
ax.text(COL1 - 0.05, 0.18, "Node Bias", fontsize=10, color="black", ha="center", va="center", zorder=6)

# Two purple circled-1 markers
for x in (2.6, 7.9):
    ax.add_patch(Circle((x, 0.18), 0.19, facecolor=BIAS, edgecolor="black", linewidth=1.1, zorder=5))
    ax.text(x, 0.18, "1", fontsize=9, fontweight="bold", color="white", ha="center", va="center", zorder=6)

fig.savefig("slide_015_diagram.png", dpi=600, transparent=True)
plt.close(fig)
print("ok slide_015_diagram.png", int(W_IN * 600), int(H_IN * 600))
