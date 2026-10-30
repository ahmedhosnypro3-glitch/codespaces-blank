#!/usr/bin/env python3
"""
Generate perceptron architecture diagram for slide 005.

This recreates the single perceptron visualization showing:
- Input nodes: x1, x2, x3, ..., xn, 1 (bias) - TOP TO BOTTOM
- Weight connections: w1, w2, w3, ..., wn, b - TOP TO BOTTOM (matching inputs)
- Summation node (Σ)
- Step activation function
- Output O/P with classification rules
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch, Circle, Rectangle
import numpy as np
from pathlib import Path

# Output directory
OUT_DIR = Path("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Figure size in inches (will be embedded at exact size in PPTX)
# Match the original slide's diagram region: roughly x=24% to x=64%, y=64% to y=94%
# On a 13.33 x 7.5 inch slide, that's ~4 inches wide x ~2.25 inches tall
FIG_W, FIG_H = 4.5, 2.5
DPI = 600  # 600 dpi for crisp embedding

fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI)
ax.set_xlim(0, FIG_W)
ax.set_ylim(0, FIG_H)
ax.set_aspect('equal')
ax.axis('off')

# Colors from analysis
WHITE = '#ffffff'
RED = '#c00000'
BLACK = '#000000'
LIGHT_BLUE = '#add8e6'
PINK = '#ffb6c1'
GRAY = '#808080'
BLUE = '#0000ff'

# Layout parameters
LEFT_MARGIN = 0.2
RIGHT_MARGIN = 0.2
TOP_MARGIN = 0.15
BOTTOM_MARGIN = 0.15

# Column positions
X_INPUT = 0.5
X_WEIGHT = 1.5
X_SUM = 3.0
X_ACTIVATION = 4.0
X_OUTPUT = 4.8

# Row positions (TOP TO BOTTOM to match original)
# y=FIG_H - TOP_MARGIN is top, y=BOTTOM_MARGIN is bottom
n_inputs = 5  # x1, x2, x3, ..., xn, 1 (bias) = 5 visible rows
# Generate from TOP to BOTTOM
y_positions = np.linspace(FIG_H - TOP_MARGIN - 0.2, BOTTOM_MARGIN + 0.2, n_inputs)

# Draw input column - TOP TO BOTTOM: x₁, x₂, x₃, ..., xₙ, 1
input_labels = ['x₁', 'x₂', 'x₃', '...', 'xₙ']
weight_labels = ['w₁', 'w₂', 'w₃', '...', 'wₙ']

for i, (y, x_label, w_label) in enumerate(zip(y_positions, input_labels, weight_labels)):
    # Input node
    circle = Circle((X_INPUT, y), 0.12, facecolor=WHITE, edgecolor=BLACK, linewidth=1, zorder=5)
    ax.add_patch(circle)
    ax.text(X_INPUT, y, x_label, ha='center', va='center', fontsize=14, fontweight='bold', zorder=6)
    
    # Weight label (matching position)
    ax.text(X_WEIGHT, y, w_label, ha='center', va='center', fontsize=14, fontweight='bold', zorder=6)
    
    # Connection line from input to sum
    arrow = FancyArrowPatch(
        (X_INPUT + 0.12, y), (X_SUM - 0.3, y_positions[2]),  # all converge to summation center (middle)
        arrowstyle='->', color=GRAY, linewidth=0.5,
        mutation_scale=8, zorder=3
    )
    ax.add_patch(arrow)

# Bias input (1) - in RED, at BOTTOM
bias_y = y_positions[-1]
circle = Circle((X_INPUT, bias_y), 0.12, facecolor=WHITE, edgecolor=BLACK, linewidth=1, zorder=5)
ax.add_patch(circle)
ax.text(X_INPUT, bias_y, '1', ha='center', va='center', fontsize=14, fontweight='bold', color=RED, zorder=6)

# Bias weight (b) - in RED, at BOTTOM matching bias
ax.text(X_WEIGHT, bias_y, 'b', ha='center', va='center', fontsize=14, fontweight='bold', color=RED, zorder=6)

# Connection from bias to sum
arrow = FancyArrowPatch(
    (X_INPUT + 0.12, bias_y), (X_SUM - 0.3, y_positions[2]),
    arrowstyle='->', color=GRAY, linewidth=0.5,
    mutation_scale=8, zorder=3
)
ax.add_patch(arrow)

# Labels for columns (at top)
ax.text(X_INPUT, FIG_H - TOP_MARGIN, 'Inputs', ha='center', va='bottom', fontsize=10, fontweight='bold', color=BLUE, style='italic')
ax.text(X_WEIGHT, FIG_H - TOP_MARGIN, 'Weights', ha='center', va='bottom', fontsize=10, fontweight='bold', color=BLUE, style='italic')

# Summation node (Σ) - light blue circle at middle height
sum_y = y_positions[2]  # middle row
sum_circle = Circle((X_SUM, sum_y), 0.3, facecolor=LIGHT_BLUE, edgecolor=BLACK, linewidth=1.5, zorder=5)
ax.add_patch(sum_circle)
ax.text(X_SUM, sum_y, 'Σ', ha='center', va='center', fontsize=22, fontweight='bold', zorder=6)

# Arrow from sum to activation
arrow = FancyArrowPatch(
    (X_SUM + 0.3, sum_y), (X_ACTIVATION - 0.25, sum_y),
    arrowstyle='->', color=BLACK, linewidth=1.5,
    mutation_scale=12, zorder=4
)
ax.add_patch(arrow)

# Activation function - pink rectangle
act_rect = Rectangle((X_ACTIVATION, sum_y - 0.2), 0.5, 0.4, facecolor=PINK, edgecolor=BLACK, linewidth=1, zorder=5)
ax.add_patch(act_rect)
# Step function icon inside
step_x = X_ACTIVATION + 0.25
step_y = sum_y
ax.plot([step_x - 0.12, step_x], [step_y, step_y], 'k-', linewidth=1.5, zorder=6)
ax.plot([step_x, step_x], [step_y - 0.1, step_y + 0.1], 'k-', linewidth=1.5, zorder=6)
ax.plot([step_x, step_x + 0.12], [step_y + 0.1, step_y + 0.1], 'k-', linewidth=1.5, zorder=6)

# Arrow from activation to output
arrow = FancyArrowPatch(
    (X_ACTIVATION + 0.5, sum_y), (X_OUTPUT, sum_y),
    arrowstyle='->', color=BLACK, linewidth=1.5,
    mutation_scale=12, zorder=4
)
ax.add_patch(arrow)

# Output O/P
ax.text(X_OUTPUT + 0.15, sum_y, 'O/P', ha='left', va='center', fontsize=14, fontweight='bold', zorder=6)

# Enclosing red border box around the diagram
box = Rectangle(
    (LEFT_MARGIN, BOTTOM_MARGIN), 
    FIG_W - LEFT_MARGIN - RIGHT_MARGIN, 
    FIG_H - TOP_MARGIN - BOTTOM_MARGIN,
    facecolor=WHITE, edgecolor=RED, linewidth=1.5, zorder=1
)
ax.add_patch(box)

# Save
output_path = OUT_DIR / "slide_005_perceptron_diagram.png"
plt.savefig(output_path, dpi=DPI, transparent=True, bbox_inches='tight', pad_inches=0.02)
plt.close()

print(f"Generated: {output_path}")
print(f"Size: {FIG_W*DPI:.0f} x {FIG_H*DPI:.0f} px at {DPI} dpi")
print(f"Inches at 600dpi embed: {FIG_W:.2f} x {FIG_H:.2f} in")

# Also save a sidecar JSON with metadata for the build script
import json
meta = {
    "image": "slide_005_perceptron_diagram.png",
    "width_in": FIG_W,
    "height_in": FIG_H,
    "dpi": DPI,
    "position": {
        "x": 3.2,  # ~24% of 13.33
        "y": 4.8,  # ~64% of 7.5
        "w": 4.5,
        "h": 2.5
    }
}
with open(OUT_DIR / "slide_005_perceptron_diagram.json", "w") as f:
    json.dump(meta, f, indent=2)
print(f"Metadata saved to {OUT_DIR}/slide_005_perceptron_diagram.json")