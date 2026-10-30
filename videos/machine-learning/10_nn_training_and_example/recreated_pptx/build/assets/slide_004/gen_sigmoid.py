#!/usr/bin/env python3
"""Generate sigmoid function graph for slide 4."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Region from original (measured): upper-right blue-bordered box
# From analysis: "upper-right inside blue-bordered box"
# Let's measure from the original image
REGION_PX = (700, 80, 920, 300)  # approximate - will adjust
BG = "#FFFFFF"
LINE_COLOR = "#0000FF"
GRID_COLOR = "#CCCCCC"
AXIS_COLOR = "#000000"
BORDER_COLOR = "#0000FF"
BORDER_WIDTH = 2

# Generate sigmoid
x = np.linspace(-6, 6, 400)
y = 1 / (1 + np.exp(-x))

w = REGION_PX[2] - REGION_PX[0]
h = REGION_PX[3] - REGION_PX[1]
fig = plt.figure(figsize=(w / 72, h / 72), dpi=72)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_facecolor(BG)

# Plot sigmoid curve
ax.plot(x, y, color=LINE_COLOR, linewidth=2)

# Grid
ax.grid(True, color=GRID_COLOR, linewidth=0.5, linestyle='-')

# Axes
ax.axhline(y=0, color=AXIS_COLOR, linewidth=0.8)
ax.axvline(x=0, color=AXIS_COLOR, linewidth=0.8)
ax.axhline(y=1, color=AXIS_COLOR, linewidth=0.8, linestyle='--')

# Ticks
ax.set_xticks(np.arange(-6, 7, 2))
ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
ax.tick_params(colors=AXIS_COLOR, labelsize=8)

# Limits
ax.set_xlim(-6, 6)
ax.set_ylim(-0.1, 1.1)

# Blue border
for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_color(BORDER_COLOR)
    spine.set_linewidth(BORDER_WIDTH)

# Remove tick labels (original may not have visible labels)
ax.set_xticklabels([])
ax.set_yticklabels([])

fig.savefig("/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/recreated_pptx/build/assets/slide_004/sigmoid_graph.png", dpi=72, facecolor=BG)
print("wrote sigmoid_graph.png")
print(f"Region: {w}x{h} px")