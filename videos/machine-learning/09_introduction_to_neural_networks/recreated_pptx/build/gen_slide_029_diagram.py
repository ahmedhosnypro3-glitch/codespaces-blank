#!/usr/bin/env python3
"""Generate slide 029 neural network diagram."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os
import json

outdir = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build"
os.makedirs(outdir, exist_ok=True)

# Colors from vision analysis
BEIGE_PANEL = "#E8E0D0"
WHITE = "#FFFFFF"
RED = "#FF0000"
BLUE = "#0070C0"
GREEN = "#00B050"
PINK = "#E8A0A0"
GRAY = "#808080"
MAGENTA = "#CC66CC"
DARK_RED = "#C00000"
LIGHT_BLUE = "#DDEBF7"
LIGHT_GREEN = "#E2EFDA"
BLACK = "#000000"
GRAY_LINES = "#BFBFBF"

# Figure setup - will save at high DPI
# The diagram panel is approx x 7%-58%, y 24%-72% of slide
# That's ~51% width, ~48% height of 13.33x7.5in = ~6.8x3.6in
# We'll generate at 150 DPI for the diagram (since it's not text math)
fig, ax = plt.subplots(figsize=(6.8, 3.6), dpi=150)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')
fig.patch.set_facecolor(WHITE)

# Panel background (beige)
panel = patches.Rectangle((0.0, 0.0), 1.0, 1.0, facecolor=BEIGE_PANEL, edgecolor=GRAY, linewidth=1)
ax.add_patch(panel)

# Coordinates (normalized 0-1 within the panel)
# Input dots: 4 dots at far left
input_x = 0.03
input_ys = [0.20, 0.32, 0.44, 0.56]
for iy in input_ys:
    circle = patches.Circle((input_x, iy), 0.015, facecolor=MAGENTA, edgecolor=MAGENTA)
    ax.add_patch(circle)

# Column 1 nodes (red sigma + red sigmoid): 3 nodes
col1_x = 0.15
col1_ys = [0.25, 0.40, 0.55]
node_radius = 0.035

for iy in col1_ys:
    # White circle
    circle = patches.Circle((col1_x, iy), node_radius, facecolor=WHITE, edgecolor=BLACK, linewidth=1.5)
    ax.add_patch(circle)
    # Vertical split line
    ax.plot([col1_x, col1_x], [iy - node_radius, iy + node_radius], color=RED, linewidth=1.5)
    # Red sigma symbol (left half)
    ax.text(col1_x - 0.022, iy, r"$\Sigma$", fontsize=20, color=RED, ha='center', va='center', fontweight='bold')
    # Red sigmoid squiggle (right half) - draw S shape
    # We'll use a text approximation
    ax.text(col1_x + 0.022, iy, "S", fontsize=14, color=RED, ha='center', va='center', fontweight='bold', style='italic')
    # Three small hollow gray circles to the right (omitted nodes)
    for offset in [0.045, 0.055, 0.065]:
        dot = patches.Circle((col1_x + offset, iy), 0.008, facecolor='none', edgecolor=GRAY, linewidth=1)
        ax.add_patch(dot)

# Red italic bold "Net_j" above column 1
ax.text(col1_x, col1_ys[0] + 0.06, r"$\mathit{Net}_j$", fontsize=14, color=RED, ha='center', va='bottom', fontweight='bold', style='italic')

# Red italic bold "O_j" to the right of each column 1 node
for iy in col1_ys:
    ax.text(col1_x + 0.085, iy, r"$\mathit{O}_j$", fontsize=12, color=RED, ha='left', va='center', fontweight='bold', style='italic')

# Lines from input dots to column 1 nodes
for ix in input_ys:
    for iy in col1_ys:
        ax.plot([input_x + 0.015, col1_x - node_radius], [ix, iy], color=GRAY_LINES, linewidth=0.5, alpha=0.6)

# Column 2 nodes (blue outline, red sigma, blue sigmoid): 3 nodes
col2_x = 0.30
col2_ys = [0.25, 0.40, 0.55]

for iy in col2_ys:
    circle = patches.Circle((col2_x, iy), node_radius, facecolor=WHITE, edgecolor=BLUE, linewidth=2)
    ax.add_patch(circle)
    # Vertical split line
    ax.plot([col2_x, col2_x], [iy - node_radius, iy + node_radius], color=RED, linewidth=1.5)
    # Red sigma
    ax.text(col2_x - 0.022, iy, r"$\Sigma$", fontsize=20, color=RED, ha='center', va='center', fontweight='bold')
    # Blue sigmoid
    ax.text(col2_x + 0.022, iy, "S", fontsize=14, color=BLUE, ha='center', va='center', fontweight='bold', style='italic')
    # Small filled red dot on right edge
    dot = patches.Circle((col2_x + node_radius, iy), 0.006, facecolor=RED, edgecolor=RED)
    ax.add_patch(dot)

# Red italic bold "Net_j" above column 2
ax.text(col2_x, col2_ys[0] + 0.06, r"$\mathit{Net}_j$", fontsize=14, color=RED, ha='center', va='bottom', fontweight='bold', style='italic')

# Red italic bold "O_j" to the right of each column 2 node
for iy in col2_ys:
    ax.text(col2_x + 0.085, iy, r"$\mathit{O}_j$", fontsize=12, color=RED, ha='left', va='center', fontweight='bold', style='italic')

# Column 3 nodes (green outline, red sigma, green sigmoid): 3 nodes
col3_x = 0.50
col3_ys = [0.25, 0.40, 0.55]

for iy in col3_ys:
    circle = patches.Circle((col3_x, iy), node_radius, facecolor=WHITE, edgecolor=GREEN, linewidth=2)
    ax.add_patch(circle)
    # Vertical split line
    ax.plot([col3_x, col3_x], [iy - node_radius, iy + node_radius], color=RED, linewidth=1.5)
    # Red sigma
    ax.text(col3_x - 0.022, iy, r"$\Sigma$", fontsize=20, color=RED, ha='center', va='center', fontweight='bold')
    # Green sigmoid
    ax.text(col3_x + 0.022, iy, "S", fontsize=14, color=GREEN, ha='center', va='center', fontweight='bold', style='italic')
    # Small filled red dot on left edge
    dot = patches.Circle((col3_x - node_radius, iy), 0.006, facecolor=RED, edgecolor=RED)
    ax.add_patch(dot)

# Red italic bold "Net_j" above column 3
ax.text(col3_x, col3_ys[0] + 0.06, r"$\mathit{Net}_j$", fontsize=14, color=RED, ha='center', va='bottom', fontweight='bold', style='italic')

# Red italic bold "O_j" to the right of each column 3 node
for iy in col3_ys:
    ax.text(col3_x + 0.085, iy, r"$\mathit{O}_j$", fontsize=12, color=RED, ha='left', va='center', fontweight='bold', style='italic')

# Fully connected: 9 pink/red lines from col2 to col3
for iy2 in col2_ys:
    for iy3 in col3_ys:
        ax.plot([col2_x + node_radius, col3_x - node_radius], [iy2, iy3], color=PINK, linewidth=1, alpha=0.8)

# Three blue w_ji labels on specific connections
# One above top horizontal link (col2_ys[0] to col3_ys[0])
mid_x = (col2_x + col3_x) / 2
ax.text(mid_x, col2_ys[0] + 0.02, r"$w_{ji}$", fontsize=12, color=BLUE, ha='center', va='bottom', fontweight='bold', style='italic')
# Two on descending diagonals
ax.text(mid_x, (col2_ys[0] + col3_ys[1]) / 2, r"$w_{ji}$", fontsize=12, color=BLUE, ha='center', va='center', fontweight='bold', style='italic')
ax.text(mid_x, (col2_ys[1] + col3_ys[2]) / 2, r"$w_{ji}$", fontsize=12, color=BLUE, ha='center', va='center', fontweight='bold', style='italic')

# Output boxes to the right of column 3
output_x = 0.62
output_labels = ["Output 1", "Output 2", "Output m"]
for iy, label in zip(col3_ys, output_labels):
    rect = patches.Rectangle((output_x, iy - 0.02), 0.12, 0.04, facecolor=WHITE, edgecolor=BLACK, linewidth=1)
    ax.add_patch(rect)
    ax.text(output_x + 0.06, iy, label, fontsize=11, color=BLACK, ha='center', va='center', style='italic')

# Vertical dark-red "Error Error Error" bar (just right of diagram)
error_x = 0.78
error_rect = patches.Rectangle((error_x, 0.15), 0.03, 0.7, facecolor=DARK_RED, edgecolor=DARK_RED)
ax.add_patch(error_rect)
# Rotated text - matplotlib doesn't easily do rotated text in normalized coords, use transform
ax.text(error_x + 0.015, 0.5, "Error Error Error", fontsize=14, color=WHITE, ha='center', va='center', rotation=90, fontweight='bold')

# Class labels to the right of error bar
class_x = 0.83
class_labels = ["Class 1", "Class 2", "Class m"]
for iy, label in zip(col3_ys, class_labels):
    rect = patches.Rectangle((class_x, iy - 0.02), 0.12, 0.04, facecolor="#D9EAD3", edgecolor=GREEN, linewidth=1.5)
    ax.add_patch(rect)
    ax.text(class_x + 0.06, iy, label, fontsize=11, color=BLACK, ha='center', va='center')

# Save
out_path = f"{outdir}/slide_029_diagram.png"
plt.tight_layout(pad=0)
plt.savefig(out_path, dpi=150, facecolor=WHITE, edgecolor='none', bbox_inches='tight', pad_inches=0)
plt.close()

# Also save metadata
meta = {
    "position": {"x": 0.6, "y": 1.1, "w": 6.8, "h": 3.6},  # approx in inches on slide
    "dpi": 150
}
with open(f"{outdir}/slide_029_diagram.json", "w") as f:
    json.dump(meta, f, indent=2)

print(f"Generated {out_path}")