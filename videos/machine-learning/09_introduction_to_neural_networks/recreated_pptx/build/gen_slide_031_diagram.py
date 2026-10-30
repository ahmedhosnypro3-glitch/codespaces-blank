#!/usr/bin/env python3
"""
Generate neural network architecture diagram for slide 031 (Example / Better Weights).

This recreates the 2-layer neural network visualization showing:
- Input layer: x1=7, x2=4 (2 inputs)
- Hidden layer: 3 nodes (3, 4, 5) with outputs O3=0.895, O4=0.836, O5=0.828
- Output layer: 2 nodes (6, 7) with outputs O6=0.32, O7=0.855
- Green weights from inputs to hidden
- Red weights from hidden to output
- Output/Target column on right: O6, O7 with target [0; 1] labeled t6, t7
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch, Circle, Rectangle
import numpy as np
from pathlib import Path
import json

# Output directory
OUT_DIR = Path("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Figure size in inches (will be embedded at exact size in PPTX)
# Match the original slide's diagram region
FIG_W, FIG_H = 7.5, 3.5
DPI = 600  # 600 dpi for crisp embedding

fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI)
ax.set_xlim(0, FIG_W)
ax.set_ylim(0, FIG_H)
ax.set_aspect('equal')
ax.axis('off')

# Colors from analysis
WHITE = '#ffffff'
RED = '#c00000'
GREEN = '#008000'
ORANGE = '#ffa500'
YELLOW = '#ffff00'
BLACK = '#000000'
LIGHT_GRAY = '#f0f0f0'
BLUE = '#0000ff'

# Layout parameters
LEFT_MARGIN = 0.2
RIGHT_MARGIN = 0.2
TOP_MARGIN = 0.15
BOTTOM_MARGIN = 0.15

# Column positions
X_INPUT = 0.6
X_HIDDEN = 2.5
X_OUTPUT = 4.5
X_WEIGHTS_IH = 1.5   # weights between input and hidden
X_WEIGHTS_HO = 3.5   # weights between hidden and output
X_TARGET = 5.5

# Row positions (TOP TO BOTTOM)
# Hidden layer: 3 nodes
hidden_y = np.linspace(FIG_H - TOP_MARGIN - 0.3, BOTTOM_MARGIN + 0.3, 3)
# Output layer: 2 nodes
output_y = np.linspace(FIG_H - TOP_MARGIN - 0.2, BOTTOM_MARGIN + 0.2, 2)
# Input layer: 2 inputs
input_y = np.array([hidden_y[0], hidden_y[-1]])  # align with top/bottom hidden

# Draw input column - x1=7, x2=4
input_labels = ['x₁', 'x₂']
input_values = ['7', '4']
for i, (y, label, val) in enumerate(zip(input_y, input_labels, input_values)):
    # Input node - white circle with label
    circle = Circle((X_INPUT, y), 0.12, facecolor=WHITE, edgecolor=BLACK, linewidth=1, zorder=5)
    ax.add_patch(circle)
    ax.text(X_INPUT, y, label, ha='center', va='center', fontsize=14, fontweight='bold', zorder=6)
    # Input value to the right of circle
    ax.text(X_INPUT + 0.25, y, val, ha='left', va='center', fontsize=12, fontweight='bold', color=BLACK, zorder=6)

# Draw hidden layer - yellow circles labeled 3, 4, 5
hidden_labels = ['3', '4', '5']
hidden_outputs = ['O₃=0.895', 'O₄=0.836', 'O₅=0.828']
for i, (y, label, out) in enumerate(zip(hidden_y, hidden_labels, hidden_outputs)):
    # Hidden node - yellow circle
    circle = Circle((X_HIDDEN, y), 0.16, facecolor=YELLOW, edgecolor=BLACK, linewidth=1.5, zorder=5)
    ax.add_patch(circle)
    ax.text(X_HIDDEN, y, label, ha='center', va='center', fontsize=16, fontweight='bold', zorder=6)
    # Output label above
    ax.text(X_HIDDEN, y + 0.22, out, ha='center', va='bottom', fontsize=9, color=BLACK, zorder=6)

# Draw output layer - orange circles labeled 6, 7
output_labels = ['6', '7']
output_values = ['O₆=0.32', 'O₇=0.855']
for i, (y, label, val) in enumerate(zip(output_y, output_labels, output_values)):
    # Output node - orange circle
    circle = Circle((X_OUTPUT, y), 0.16, facecolor=ORANGE, edgecolor=BLACK, linewidth=1.5, zorder=5)
    ax.add_patch(circle)
    ax.text(X_OUTPUT, y, label, ha='center', va='center', fontsize=16, fontweight='bold', zorder=6)
    # Output value to the right
    ax.text(X_OUTPUT + 0.25, y, val, ha='left', va='center', fontsize=10, color=BLACK, zorder=6)

# Draw Target column on right
target_y = output_y  # align with output nodes
target_labels = ['t₆', 't₇']
target_vals = ['0', '1']
ax.text(X_TARGET, FIG_H - TOP_MARGIN, 'Target', ha='center', va='bottom', fontsize=10, fontweight='bold', color=BLACK)
for i, (y, t_label, t_val) in enumerate(zip(target_y, target_labels, target_vals)):
    ax.text(X_TARGET - 0.2, y, t_label, ha='right', va='center', fontsize=10, fontweight='bold', color=BLACK)
    ax.text(X_TARGET + 0.15, y, t_val, ha='left', va='center', fontsize=10, fontweight='bold', color=BLACK)

# Draw Output column label
ax.text(X_OUTPUT, FIG_H - TOP_MARGIN, 'Output', ha='center', va='bottom', fontsize=10, fontweight='bold', color=BLACK)

# Draw weights Input -> Hidden (GREEN)
# Weights: to node 3: 0.121 (from x1), 0.405 (from x2)
#          to node 4: 0.101 (from x1), 0.305 (from x2)
#          to node 5: 0.099 (from x1), 0.295 (from x2)
w_ih = [
    [0.121, 0.405],  # to node 3
    [0.101, 0.305],  # to node 4
    [0.099, 0.295],  # to node 5
]
for h_idx, h_y in enumerate(hidden_y):
    for i_idx, i_y in enumerate(input_y):
        # Arrow from input to hidden
        arrow = FancyArrowPatch(
            (X_INPUT + 0.12, i_y), (X_HIDDEN - 0.16, h_y),
            arrowstyle='->', color=GREEN, linewidth=1.5,
            mutation_scale=10, zorder=3
        )
        ax.add_patch(arrow)
        # Weight label at midpoint
        mid_x = (X_INPUT + 0.12 + X_HIDDEN - 0.16) / 2
        mid_y = (i_y + h_y) / 2
        ax.text(mid_x, mid_y, f'{w_ih[h_idx][i_idx]}', ha='center', va='center', fontsize=9, fontweight='bold', color=GREEN, zorder=6,
                bbox=dict(boxstyle='round,pad=0.1', facecolor=WHITE, edgecolor='none', alpha=0.8))

# Draw weights Hidden -> Output (RED)
# From node 3: -0.399 (to 6), 0.598 (to 7)
# From node 4: -0.288 (to 6), 0.696 (to 7)
# From node 5: -0.187 (to 6), 0.795 (to 7)
w_ho = [
    [-0.399, 0.598],  # from node 3
    [-0.288, 0.696],  # from node 4
    [-0.187, 0.795],  # from node 5
]
for h_idx, h_y in enumerate(hidden_y):
    for o_idx, o_y in enumerate(output_y):
        # Arrow from hidden to output
        arrow = FancyArrowPatch(
            (X_HIDDEN + 0.16, h_y), (X_OUTPUT - 0.16, o_y),
            arrowstyle='->', color=RED, linewidth=1.5,
            mutation_scale=10, zorder=3
        )
        ax.add_patch(arrow)
        # Weight label at midpoint
        mid_x = (X_HIDDEN + 0.16 + X_OUTPUT - 0.16) / 2
        mid_y = (h_y + o_y) / 2
        ax.text(mid_x, mid_y, f'{w_ho[h_idx][o_idx]}', ha='center', va='center', fontsize=9, fontweight='bold', color=RED, zorder=6,
                bbox=dict(boxstyle='round,pad=0.1', facecolor=WHITE, edgecolor='none', alpha=0.8))

# Column labels
ax.text(X_INPUT, FIG_H - TOP_MARGIN, 'Input', ha='center', va='bottom', fontsize=10, fontweight='bold', color=BLUE, style='italic')
ax.text(X_HIDDEN, FIG_H - TOP_MARGIN, 'Hidden', ha='center', va='bottom', fontsize=10, fontweight='bold', color=BLUE, style='italic')
ax.text(X_OUTPUT, FIG_H - TOP_MARGIN, 'Output', ha='center', va='bottom', fontsize=10, fontweight='bold', color=BLUE, style='italic')

# Enclosing red border box around the diagram
box = Rectangle(
    (LEFT_MARGIN, BOTTOM_MARGIN),
    FIG_W - LEFT_MARGIN - RIGHT_MARGIN,
    FIG_H - TOP_MARGIN - BOTTOM_MARGIN,
    facecolor='none', edgecolor=RED, linewidth=1.5, zorder=1
)
ax.add_patch(box)

# Save
output_path = OUT_DIR / "slide_031_nn_diagram.png"
plt.savefig(output_path, dpi=DPI, transparent=True, bbox_inches='tight', pad_inches=0.02)
plt.close()

print(f"Generated: {output_path}")
print(f"Size: {FIG_W*DPI:.0f} x {FIG_H*DPI:.0f} px at {DPI} dpi")
print(f"Inches at 600dpi embed: {FIG_W:.2f} x {FIG_H:.2f} in")

# Also save a sidecar JSON with metadata for the build script
meta = {
    "image": "slide_031_nn_diagram.png",
    "width_in": FIG_W,
    "height_in": FIG_H,
    "dpi": DPI,
    "position": {
        "x": 1.5,
        "y": 1.2,
        "w": 7.5,
        "h": 3.5
    }
}
with open(OUT_DIR / "slide_031_nn_diagram.json", "w") as f:
    json.dump(meta, f, indent=2)
print(f"Metadata saved to {OUT_DIR}/slide_031_nn_diagram.json")