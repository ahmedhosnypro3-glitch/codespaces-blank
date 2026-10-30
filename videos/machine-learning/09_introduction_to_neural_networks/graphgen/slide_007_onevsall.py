#!/usr/bin/env python3
"""Generate the One-vs-All 2D classification plot for slide_007."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, Polygon

W, H = 5.0, 4.5
fig, ax = plt.subplots(figsize=(W, H), dpi=200)
ax.set_xlim(-2, 5); ax.set_ylim(-2, 5)
ax.axis("off")

# Decision boundaries:
# d1(x): red line descending upper-left to lower-right
# d2(x): green line ascending lower-left to upper-right
# d3(x): blue line ascending steeper lower-left to upper-right

x = np.linspace(-1, 5, 200)
# d1: y = -x + 2.5 (descending)
y1 = -x + 2.5
# d2: y = 0.8x + 0.5 (ascending shallow)
y2 = 0.8 * x + 0.5
# d3: y = 1.5x - 1.5 (ascending steep)
y3 = 1.5 * x - 1.5

# Plot lines
ax.plot(x, y1, color="#FF0000", lw=2.0)
ax.plot(x, y2, color="#008000", lw=2.0)
ax.plot(x, y3, color="#0000FF", lw=2.0)

# Shaded regions with hatching
# C1 (top): above d1 and d3, left of d2? Actually from plot description: C1 top region (light green)
# Let's fill regions using polygons
# Region C1: bounded by d1 (left/upper), d3 (right/upper) - top area
# Region C2: bounded by d2 (left), d3 (right), d1 (bottom) - right area
# Region C3: bounded by d1 (upper), d2 (lower) - bottom-left

# C1 (top): polygon bounded by d1 from left, d3 from right, top edge
# Actually looking at the plot: d1 descends, d2 ascends shallow, d3 ascends steep
# C1 is the top region (light green hatching)
# C2 is right region (light blue hatching)
# C3 is bottom-left (light pink hatching)

# Create filled polygons for hatching
from matplotlib.patches import Polygon as MplPolygon

# C1: region above d1 and d3, to the left of their intersection
# Intersection of d1 and d3: -x+2.5 = 1.5x-1.5 -> 4 = 2.5x -> x=1.6, y=0.9
# Wait, let me think about this differently
# For each point, determine which side of each boundary it's on

# Actually let's just use the coordinates from the visual layout
# C1 (top) - light green hatching
poly_C1 = MplPolygon([[-1, 5], [5, 5], [5, 2.5], [1.6, 0.9], [-1, 3.5]], 
                     facecolor="#90EE90", alpha=0.4, hatch="///", edgecolor="none", zorder=1)
ax.add_patch(poly_C1)

# C2 (right) - light blue hatching
poly_C2 = MplPolygon([[5, 5], [5, -1], [1.6, -1], [1.6, 0.9]], 
                     facecolor="#ADD8E6", alpha=0.4, hatch="///", edgecolor="none", zorder=1)
ax.add_patch(poly_C2)

# C3 (bottom-left) - light pink hatching  
poly_C3 = MplPolygon([[-1, -1], [1.6, -1], [1.6, 0.9], [-1, 3.5]],
                     facecolor="#FFB6C1", alpha=0.4, hatch="///", edgecolor="none", zorder=1)
ax.add_patch(poly_C3)

# Class labels in yellow boxes
ax.text(-0.5, 4.0, "C\u2081", ha="center", va="center", fontsize=12, fontweight="bold",
        color="#000000",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFFF00", edgecolor="none"))
ax.text(4.2, 4.0, "C\u2082", ha="center", va="center", fontsize=12, fontweight="bold",
        color="#000000",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFFF00", edgecolor="none"))
ax.text(0.5, -0.5, "C\u2083", ha="center", va="center", fontsize=12, fontweight="bold",
        color="#000000",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFFF00", edgecolor="none"))

# Scatter dots for each class
np.random.seed(42)
# C1 dots (green) in top region
for _ in range(8):
    xr = np.random.uniform(-0.5, 2.5)
    yr = np.random.uniform(2.0, 4.5)
    ax.plot(xr, yr, 'o', color="#008000", markersize=6)

# C2 dots (blue) in right region
for _ in range(8):
    xr = np.random.uniform(2.5, 4.5)
    yr = np.random.uniform(-0.5, 3.5)
    ax.plot(xr, yr, 'o', color="#0000FF", markersize=6)

# C3 dots (red) in bottom-left
for _ in range(8):
    xr = np.random.uniform(-0.8, 1.5)
    yr = np.random.uniform(-0.8, 1.5)
    ax.plot(xr, yr, 'o', color="#FF0000", markersize=6)

# Line labels
ax.text(-0.8, 3.2, "d\u2081(x)", color="#FF0000", fontsize=11, style="italic")
ax.text(4.3, 3.8, "d\u2082(x)", color="#008000", fontsize=11, style="italic")
ax.text(1.0, 4.2, "d\u2083(x)", color="#0000FF", fontsize=11, style="italic")

# "+ ve" annotations with arrows
# Red line +ve near lower-right
ax.annotate("+ ve", xy=(3.5, -0.5), xytext=(4.2, -0.8),
            color="#FF0000", fontsize=10,
            arrowprops=dict(arrowstyle="->", color="#FF0000"))
# Green line +ve near left side
ax.annotate("+ ve", xy=(-0.5, 0.1), xytext=(-1.2, 0.5),
            color="#008000", fontsize=10,
            arrowprops=dict(arrowstyle="->", color="#008000"))
# Blue line +ve near upper-right
ax.annotate("+ ve", xy=(2.5, 4.0), xytext=(2.8, 4.5),
            color="#0000FF", fontsize=10,
            arrowprops=dict(arrowstyle="->", color="#0000FF"))

plt.tight_layout(pad=0.2)
fig.savefig("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_007_graph.png",
            transparent=False, facecolor="white")
print("saved slide_007_graph.png")