#!/usr/bin/env python3
"""Generate the One-vs-All with ambiguity regions for slide_008."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Polygon as MplPolygon

W, H = 5.0, 4.5
fig, ax = plt.subplots(figsize=(W, H), dpi=200)
ax.set_xlim(-2, 5); ax.set_ylim(-2, 5)
ax.axis("off")

# Axes
ax.annotate("", xy=(5, -1.5), xytext=(-1.5, -1.5),
            arrowprops=dict(arrowstyle="->", color="#000000", lw=1.2))
ax.annotate("", xy=(-1.5, 4.5), xytext=(-1.5, -1.5),
            arrowprops=dict(arrowstyle="->", color="#000000", lw=1.2))

# Decision boundaries (same as slide_007 but with d2 unlabeled)
x = np.linspace(-1, 5, 200)
y1 = -x + 2.5  # red d1(x) descending
y2 = 0.8 * x + 0.5  # blue ascending (unlabeled)
y3 = 1.5 * x - 1.5  # green d3(x) ascending shallow

ax.plot(x, y1, color="#c0392b", lw=2.0)  # red
ax.plot(x, y2, color="#2980b9", lw=2.0)  # blue
ax.plot(x, y3, color="#2ecc71", lw=2.0)  # green

# Shaded regions (same as slide_007)
poly_C1 = MplPolygon([[-1, 5], [5, 5], [5, 2.5], [1.6, 0.9], [-1, 3.5]], 
                     facecolor="#90EE90", alpha=0.3, hatch="///", edgecolor="none", zorder=1)
ax.add_patch(poly_C1)
poly_C2 = MplPolygon([[5, 5], [5, -1], [1.6, -1], [1.6, 0.9]], 
                     facecolor="#ADD8E6", alpha=0.3, hatch="///", edgecolor="none", zorder=1)
ax.add_patch(poly_C2)
poly_C3 = MplPolygon([[-1, -1], [1.6, -1], [1.6, 0.9], [-1, 3.5]],
                     facecolor="#FFB6C1", alpha=0.3, hatch="///", edgecolor="none", zorder=1)
ax.add_patch(poly_C3)

# Class labels in yellow boxes
ax.text(-0.5, 4.0, "C1", ha="center", va="center", fontsize=12, fontweight="bold",
        color="#000000", bbox=dict(boxstyle="round,pad=0.3", facecolor="#f1c40f", edgecolor="none"))
ax.text(4.2, 4.0, "C2", ha="center", va="center", fontsize=12, fontweight="bold",
        color="#000000", bbox=dict(boxstyle="round,pad=0.3", facecolor="#f1c40f", edgecolor="none"))
ax.text(0.5, -0.5, "C3", ha="center", va="center", fontsize=12, fontweight="bold",
        color="#000000", bbox=dict(boxstyle="round,pad=0.3", facecolor="#f1c40f", edgecolor="none"))

# Scatter dots
np.random.seed(42)
for _ in range(10):
    ax.plot(np.random.uniform(-0.5, 2.5), np.random.uniform(2.0, 4.5), 'o', color="#2ecc71", markersize=6)
for _ in range(10):
    ax.plot(np.random.uniform(2.5, 4.5), np.random.uniform(-0.5, 3.5), 'o', color="#2980b9", markersize=6)
for _ in range(10):
    ax.plot(np.random.uniform(-0.8, 1.5), np.random.uniform(-0.8, 1.5), 'o', color="#c0392b", markersize=6)

# Line labels
ax.text(-0.8, 3.2, "d1(x)", color="#c0392b", fontsize=11)
ax.text(1.0, 4.2, "d3(x)", color="#2ecc71", fontsize=11)

# "?" boxes (orange) at 4 locations
question_positions = [(0.5, 2.0), (2.0, 2.0), (3.5, 3.0), (1.0, 0.0)]
for xq, yq in question_positions:
    box = Rectangle((xq-0.15, yq-0.15), 0.3, 0.3, facecolor="#e67e22", edgecolor="#000000", lw=0.8)
    ax.add_patch(box)
    ax.text(xq, yq, "?", ha="center", va="center", fontsize=14, fontweight="bold", color="#000000")

# "+ve" labels
ax.annotate("+ve", xy=(-0.5, 0.1), xytext=(-1.5, 0.5),
            color="#000000", fontsize=10,
            arrowprops=dict(arrowstyle="->", color="#2ecc71"))
ax.annotate("+ve", xy=(2.5, 4.0), xytext=(2.8, 4.5),
            color="#000000", fontsize=10,
            arrowprops=dict(arrowstyle="->", color="#2980b9"))
ax.annotate("+ve", xy=(3.5, -0.5), xytext=(4.2, -0.8),
            color="#000000", fontsize=10,
            arrowprops=dict(arrowstyle="->", color="#c0392b"))

# "Undefined" box (top-left outside plot) with leader lines
ax.add_patch(Rectangle((-1.8, 3.0), 1.2, 0.6, facecolor="#d5f5e3", edgecolor="#000000", lw=1.0))
ax.text(-1.2, 3.3, "Undefined", ha="center", va="center", fontsize=10, color="#000000")
# Leader lines from Undefined box to plot
ax.plot([-1.2, 0.0], [3.3, 3.0], color="#c0392b", lw=0.8)
ax.plot([-1.2, 1.0], [3.3, 1.5], color="#c0392b", lw=0.8)

# "New Class" box (middle-right outside plot)
ax.add_patch(Rectangle((5.2, 1.0), 1.2, 0.6, facecolor="#d7bde2", edgecolor="#8e44ad", lw=1.2))
ax.text(5.8, 1.3, "New Class", ha="center", va="center", fontsize=10, color="#000000")

plt.tight_layout(pad=0.2)
fig.savefig("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_008_graph.png",
            transparent=False, facecolor="white")
print("saved slide_008_graph.png")