#!/usr/bin/env python3
"""
Generate two-layer perceptron architecture diagram for slide 014.
Matches the original frame's visual: two hidden neurons (1, 2), output neuron (3),
with step activation function, weights w11, w12, w21, w22, w31, w32.
Colors: red neuron numbers, green weights w31/w32, purple step box.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch, Circle, Rectangle, FancyBboxPatch
import numpy as np
from pathlib import Path

OUT_DIR = Path("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build")
OUT_DIR.mkdir(parents=True, exist_ok=True)

FIG_W, FIG_H = 5.0, 3.0
DPI = 600

fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI)
ax.set_xlim(0, FIG_W)
ax.set_ylim(0, FIG_H)
ax.set_aspect('equal')
ax.axis('off')

# Colors from analysis
WHITE = '#ffffff'
RED = '#c00000'
BLACK = '#000000'
GREEN = '#008000'
BLUE = '#0000ff'
PURPLE = '#d0b0d0'
LIGHT_GRAY = '#e6e6e6'

# Layout
# Inputs on left: x1 (top), x2 (bottom)
# Hidden layer: neuron 1 (top), neuron 2 (bottom)
# Output layer: neuron 3 (right)
# Step function box: right of neuron 3
# Output: far right

X_INPUT = 0.5
X_HIDDEN = 1.8
X_OUTPUT = 3.2
X_STEP = 4.0
X_OP = 4.7

# Y positions
Y_X1 = FIG_H * 0.75
Y_X2 = FIG_H * 0.25
Y_N1 = FIG_H * 0.75
Y_N2 = FIG_H * 0.25
Y_N3 = FIG_H * 0.5
Y_STEP = FIG_H * 0.5
Y_OP = FIG_H * 0.5

# Input nodes
for y, label in [(Y_X1, 'x₁'), (Y_X2, 'x₂')]:
    circle = Circle((X_INPUT, y), 0.1, facecolor=WHITE, edgecolor=BLACK, linewidth=1, zorder=5)
    ax.add_patch(circle)
    ax.text(X_INPUT, y, label, ha='center', va='center', fontsize=12, fontweight='bold', zorder=6)

# Hidden neuron 1
circle1 = Circle((X_HIDDEN, Y_N1), 0.18, facecolor=WHITE, edgecolor=BLACK, linewidth=1.5, zorder=5)
ax.add_patch(circle1)
ax.text(X_HIDDEN, Y_N1, 'Σ', ha='center', va='center', fontsize=18, fontweight='bold', zorder=6)
# Neuron number in red circle
num_circle1 = Circle((X_HIDDEN - 0.25, Y_N1 + 0.2), 0.12, facecolor=RED, edgecolor='none', zorder=7)
ax.add_patch(num_circle1)
ax.text(X_HIDDEN - 0.25, Y_N1 + 0.2, '1', ha='center', va='center', fontsize=10, fontweight='bold', color=WHITE, zorder=8)

# Hidden neuron 2
circle2 = Circle((X_HIDDEN, Y_N2), 0.18, facecolor=WHITE, edgecolor=BLACK, linewidth=1.5, zorder=5)
ax.add_patch(circle2)
ax.text(X_HIDDEN, Y_N2, 'Σ', ha='center', va='center', fontsize=18, fontweight='bold', zorder=6)
num_circle2 = Circle((X_HIDDEN - 0.25, Y_N2 + 0.2), 0.12, facecolor=RED, edgecolor='none', zorder=7)
ax.add_patch(num_circle2)
ax.text(X_HIDDEN - 0.25, Y_N2 + 0.2, '2', ha='center', va='center', fontsize=10, fontweight='bold', color=WHITE, zorder=8)

# Output neuron 3
circle3 = Circle((X_OUTPUT, Y_N3), 0.18, facecolor=WHITE, edgecolor=BLACK, linewidth=1.5, zorder=5)
ax.add_patch(circle3)
ax.text(X_OUTPUT, Y_N3, 'Σ', ha='center', va='center', fontsize=18, fontweight='bold', zorder=6)
num_circle3 = Circle((X_OUTPUT - 0.25, Y_N3 + 0.2), 0.12, facecolor=RED, edgecolor='none', zorder=7)
ax.add_patch(num_circle3)
ax.text(X_OUTPUT - 0.25, Y_N3 + 0.2, '3', ha='center', va='center', fontsize=10, fontweight='bold', color=WHITE, zorder=8)

# Connections: x1 -> n1 (w11), x2 -> n1 (w12)
for y_src, y_dst, weight_label, weight_color in [
    (Y_X1, Y_N1, 'w₁₁', BLACK),
    (Y_X2, Y_N1, 'w₁₂', BLACK),
]:
    arrow = FancyArrowPatch((X_INPUT + 0.1, y_src), (X_HIDDEN - 0.18, y_dst),
        arrowstyle='->', color=weight_color, linewidth=0.8, mutation_scale=8, zorder=4)
    ax.add_patch(arrow)
    mid_x = (X_INPUT + 0.1 + X_HIDDEN - 0.18) / 2
    mid_y = (y_src + y_dst) / 2
    ax.text(mid_x, mid_y + 0.1, weight_label, ha='center', va='bottom', fontsize=9, color=weight_color, zorder=6)

# Connections: x1 -> n2 (w21), x2 -> n2 (w22)
for y_src, y_dst, weight_label, weight_color in [
    (Y_X1, Y_N2, 'w₂₁', BLACK),
    (Y_X2, Y_N2, 'w₂₂', BLACK),
]:
    arrow = FancyArrowPatch((X_INPUT + 0.1, y_src), (X_HIDDEN - 0.18, y_dst),
        arrowstyle='->', color=weight_color, linewidth=0.8, mutation_scale=8, zorder=4)
    ax.add_patch(arrow)
    mid_x = (X_INPUT + 0.1 + X_HIDDEN - 0.18) / 2
    mid_y = (y_src + y_dst) / 2
    ax.text(mid_x, mid_y - 0.1, weight_label, ha='center', va='top', fontsize=9, color=weight_color, zorder=6)

# Connections: n1 -> n3 (w31, green), n2 -> n3 (w32, green)
for y_src, weight_label in [(Y_N1, 'w₃₁'), (Y_N2, 'w₃₂')]:
    arrow = FancyArrowPatch((X_HIDDEN + 0.18, y_src), (X_OUTPUT - 0.18, Y_N3),
        arrowstyle='->', color=GREEN, linewidth=1.0, mutation_scale=10, zorder=4)
    ax.add_patch(arrow)
    mid_x = (X_HIDDEN + 0.18 + X_OUTPUT - 0.18) / 2
    mid_y = (y_src + Y_N3) / 2
    ax.text(mid_x, mid_y + 0.1, weight_label, ha='center', va='bottom', fontsize=10, fontweight='bold', color=GREEN, zorder=6)

# Step function box (purple)
step_box = FancyBboxPatch(
    (X_STEP, Y_STEP - 0.15), 0.5, 0.3,
    boxstyle="round,pad=0.02",
    facecolor=PURPLE, edgecolor=BLACK, linewidth=1.5, zorder=5
)
ax.add_patch(step_box)

# Step function icon inside box
step_center_x = X_STEP + 0.25
step_center_y = Y_STEP
step_width = 0.2
step_height = 0.15
# Bottom horizontal
ax.plot([step_center_x - step_width/2, step_center_x],
        [step_center_y - step_height/2, step_center_y - step_height/2],
        color=RED, linewidth=1.5, zorder=6)
# Vertical jump
ax.plot([step_center_x, step_center_x],
        [step_center_y - step_height/2, step_center_y + step_height/2],
        color=RED, linewidth=1.5, zorder=6)
# Top horizontal
ax.plot([step_center_x, step_center_x + step_width/2],
        [step_center_y + step_height/2, step_center_y + step_height/2],
        color=RED, linewidth=1.5, zorder=6)

# Text above step box
ax.text(X_STEP + 0.25, Y_STEP + 0.3, '>0 ⇒ 1', ha='center', va='bottom', fontsize=8, color=BLACK, zorder=6)
ax.text(X_STEP + 0.25, Y_STEP - 0.35, '≤0 ⇒ 0', ha='center', va='top', fontsize=8, color=BLACK, zorder=6)

# Arrow from step to O/P
arrow = FancyArrowPatch((X_STEP + 0.5, Y_STEP), (X_OP, Y_OP),
    arrowstyle='->', color=BLACK, linewidth=1.5, mutation_scale=12, zorder=4)
ax.add_patch(arrow)
ax.text(X_OP + 0.1, Y_OP, 'O/P', ha='left', va='center', fontsize=12, fontweight='bold', zorder=6)

# Enclosing white box with dark border (matches original)
margin = 0.15
box = Rectangle(
    (margin, margin), FIG_W - 2*margin, FIG_H - 2*margin,
    facecolor=WHITE, edgecolor=BLACK, linewidth=1.5, zorder=1
)
ax.add_patch(box)

# Save
output_path = OUT_DIR / "slide_014_main_diagram.png"
plt.savefig(output_path, dpi=DPI, transparent=True, bbox_inches='tight', pad_inches=0.02)
plt.close()

print(f"Generated: {output_path}")
print(f"Size: {FIG_W*DPI:.0f} x {FIG_H*DPI:.0f} px at {DPI} dpi")

import json
meta = {
    "image": "slide_014_main_diagram.png",
    "width_in": FIG_W,
    "height_in": FIG_H,
    "dpi": DPI,
}
with open(OUT_DIR / "slide_014_main_diagram.json", "w") as f:
    json.dump(meta, f, indent=2)
print(f"Metadata saved")