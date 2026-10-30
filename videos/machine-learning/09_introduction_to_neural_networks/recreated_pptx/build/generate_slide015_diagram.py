#!/usr/bin/env python3
"""
Generate two-layer perceptron with non-linearity diagram for slide 015.
Matches the original frame: inputs x1, x2; hidden S1, S2 with step activations Z1, Z2;
output S3 with step activation Z3/O/P. Weights: x1->S1=-1 (red), x1->S2=1 (blue),
x2->S1=1 (red), x2->S2=-1 (blue), Z1->S3=-1 (red), Z2->S3=1 (green).
Truth table and data table are shown on original.
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

FIG_W, FIG_H = 8.0, 4.5
DPI = 600

fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI)
ax.set_xlim(0, FIG_W)
ax.set_ylim(0, FIG_H)
ax.set_aspect('equal')
ax.axis('off')

# Colors from analysis
WHITE = '#ffffff'
BLACK = '#000000'
RED = '#ff0000'
BLUE = '#0000ff'
GREEN = '#008000'
YELLOW = '#ffff00'
PURPLE = '#d2b48c'
LIGHT_BLUE = '#add8e6'

# Layout columns
X_INPUT = 0.6
X_HIDDEN = 2.2
X_Z = 4.0
X_OUTPUT = 5.8
X_Z3 = 7.2
X_OP = 8.0

# Row positions
Y_X1 = FIG_H * 0.75
Y_X2 = FIG_H * 0.25
Y_S1 = FIG_H * 0.75
Y_S2 = FIG_H * 0.25
Y_Z1 = FIG_H * 0.75
Y_Z2 = FIG_H * 0.25
Y_S3 = FIG_H * 0.5
Y_Z3 = FIG_H * 0.5
Y_OP = FIG_H * 0.5

# Input nodes
for y, label in [(Y_X1, 'x₁'), (Y_X2, 'x₂')]:
    circle = Circle((X_INPUT, y), 0.12, facecolor=WHITE, edgecolor=BLACK, linewidth=1, zorder=5)
    ax.add_patch(circle)
    ax.text(X_INPUT, y, label, ha='center', va='center', fontsize=14, fontweight='bold', zorder=6)

# Hidden neurons S1, S2
for y, label in [(Y_S1, 'S₁'), (Y_S2, 'S₂')]:
    circle = Circle((X_HIDDEN, y), 0.15, facecolor=WHITE, edgecolor=BLACK, linewidth=1.5, zorder=5)
    ax.add_patch(circle)
    ax.text(X_HIDDEN, y, 'Σ', ha='center', va='center', fontsize=18, fontweight='bold', zorder=6)
    ax.text(X_HIDDEN - 0.3, y, label, ha='right', va='center', fontsize=12, fontweight='bold', zorder=6)

# Connections input -> hidden with weights
# x1 -> S1: -1 (red)
arrow = FancyArrowPatch((X_INPUT + 0.12, Y_X1), (X_HIDDEN - 0.15, Y_S1),
    arrowstyle='->', color=RED, linewidth=1.0, mutation_scale=10, zorder=4)
ax.add_patch(arrow)
ax.text((X_INPUT + X_HIDDEN)/2, (Y_X1 + Y_S1)/2 + 0.1, '-1', ha='center', va='bottom', fontsize=10, fontweight='bold', color=RED, zorder=6)

# x1 -> S2: 1 (blue)
arrow = FancyArrowPatch((X_INPUT + 0.12, Y_X1), (X_HIDDEN - 0.15, Y_S2),
    arrowstyle='->', color=BLUE, linewidth=1.0, mutation_scale=10, zorder=4)
ax.add_patch(arrow)
ax.text((X_INPUT + X_HIDDEN)/2, (Y_X1 + Y_S2)/2 - 0.1, '1', ha='center', va='top', fontsize=10, fontweight='bold', color=BLUE, zorder=6)

# x2 -> S1: 1 (red)
arrow = FancyArrowPatch((X_INPUT + 0.12, Y_X2), (X_HIDDEN - 0.15, Y_S1),
    arrowstyle='->', color=RED, linewidth=1.0, mutation_scale=10, zorder=4)
ax.add_patch(arrow)
ax.text((X_INPUT + X_HIDDEN)/2, (Y_X2 + Y_S1)/2 - 0.1, '1', ha='center', va='top', fontsize=10, fontweight='bold', color=RED, zorder=6)

# x2 -> S2: -1 (blue)
arrow = FancyArrowPatch((X_INPUT + 0.12, Y_X2), (X_HIDDEN - 0.15, Y_S2),
    arrowstyle='->', color=BLUE, linewidth=1.0, mutation_scale=10, zorder=4)
ax.add_patch(arrow)
ax.text((X_INPUT + X_HIDDEN)/2, (Y_X2 + Y_S2)/2 + 0.1, '-1', ha='center', va='bottom', fontsize=10, fontweight='bold', color=BLUE, zorder=6)

# Step function boxes Z1, Z2
for x, y, label, rules in [
    (X_Z, Y_Z1, 'Z₁', [('>0.5 ⇒ 1', YELLOW), ('<0.5 ⇒ 0', RED)]),
    (X_Z, Y_Z2, 'Z₂', [('≥-0.5 ⇒ 1', GREEN), ('<-0.5 ⇒ 0', RED)]),
]:
    box = FancyBboxPatch((x - 0.15, y - 0.2), 0.3, 0.4,
        boxstyle="round,pad=0.02", facecolor=PURPLE, edgecolor=BLACK, linewidth=1.5, zorder=5)
    ax.add_patch(box)
    # Step icon
    cx = x
    cy = y
    sw, sh = 0.12, 0.1
    ax.plot([cx - sw/2, cx], [cy - sh/2, cy - sh/2], color=RED, linewidth=1.5, zorder=6)
    ax.plot([cx, cx], [cy - sh/2, cy + sh/2], color=RED, linewidth=1.5, zorder=6)
    ax.plot([cx, cx + sw/2], [cy + sh/2, cy + sh/2], color=RED, linewidth=1.5, zorder=6)
    ax.text(x + 0.3, y, label, ha='left', va='center', fontsize=14, fontweight='bold', zorder=6)
    for i, (text, color) in enumerate(rules):
        ax.text(x + 0.3, y + 0.25 - i*0.25, text, ha='left', va='center', fontsize=8, color=color, zorder=6)

# Connections hidden -> Z
for y_src, y_dst in [(Y_S1, Y_Z1), (Y_S2, Y_Z2)]:
    arrow = FancyArrowPatch((X_HIDDEN + 0.15, y_src), (X_Z - 0.15, y_dst),
        arrowstyle='->', color=BLACK, linewidth=1.0, mutation_scale=10, zorder=4)
    ax.add_patch(arrow)

# Output neuron S3
circle3 = Circle((X_OUTPUT, Y_S3), 0.15, facecolor=WHITE, edgecolor=BLACK, linewidth=1.5, zorder=5)
ax.add_patch(circle3)
ax.text(X_OUTPUT, Y_S3, 'Σ', ha='center', va='center', fontsize=18, fontweight='bold', zorder=6)
ax.text(X_OUTPUT - 0.3, Y_S3, 'S₃', ha='right', va='center', fontsize=12, fontweight='bold', zorder=6)

# Connections Z1, Z2 -> S3
arrow = FancyArrowPatch((X_Z + 0.15, Y_Z1), (X_OUTPUT - 0.15, Y_S3),
    arrowstyle='->', color=RED, linewidth=1.0, mutation_scale=10, zorder=4)
ax.add_patch(arrow)
ax.text((X_Z + X_OUTPUT)/2, (Y_Z1 + Y_S3)/2 + 0.1, '-1', ha='center', va='bottom', fontsize=10, fontweight='bold', color=RED, zorder=6)

arrow = FancyArrowPatch((X_Z + 0.15, Y_Z2), (X_OUTPUT - 0.15, Y_S3),
    arrowstyle='->', color=GREEN, linewidth=1.0, mutation_scale=10, zorder=4)
ax.add_patch(arrow)
ax.text((X_Z + X_OUTPUT)/2, (Y_Z2 + Y_S3)/2 - 0.1, '1', ha='center', va='top', fontsize=10, fontweight='bold', color=GREEN, zorder=6)

# Step function box Z3 / O/P
box = FancyBboxPatch((X_Z3 - 0.15, Y_Z3 - 0.2), 0.3, 0.4,
    boxstyle="round,pad=0.02", facecolor=PURPLE, edgecolor=BLACK, linewidth=1.5, zorder=5)
ax.add_patch(box)
cx = X_Z3
cy = Y_Z3
sw, sh = 0.12, 0.1
ax.plot([cx - sw/2, cx], [cy - sh/2, cy - sh/2], color=RED, linewidth=1.5, zorder=6)
ax.plot([cx, cx], [cy - sh/2, cy + sh/2], color=RED, linewidth=1.5, zorder=6)
ax.plot([cx, cx + sw/2], [cy + sh/2, cy + sh/2], color=RED, linewidth=1.5, zorder=6)
ax.text(X_Z3 + 0.3, Y_Z3, 'Z₃ / O/P', ha='left', va='center', fontsize=12, fontweight='bold', zorder=6)
ax.text(X_Z3 + 0.3, Y_Z3 + 0.25, '>0 ⇒ 1', ha='left', va='center', fontsize=8, color=YELLOW, zorder=6)
ax.text(X_Z3 + 0.3, Y_Z3 - 0.25, '<0 ⇒ 0', ha='left', va='center', fontsize=8, color=RED, zorder=6)

# Arrow to O/P
arrow = FancyArrowPatch((X_Z3 + 0.15, Y_Z3), (X_OP, Y_OP),
    arrowstyle='->', color=BLACK, linewidth=1.5, mutation_scale=12, zorder=4)
ax.add_patch(arrow)
ax.text(X_OP + 0.1, Y_OP, 'O/P', ha='left', va='center', fontsize=14, fontweight='bold', zorder=6)

# Enclosing blue-bordered box
margin = 0.15
box = Rectangle((margin, margin), FIG_W - 2*margin, FIG_H - 2*margin,
    facecolor=WHITE, edgecolor=BLUE, linewidth=2, zorder=1)
ax.add_patch(box)

# Save
output_path = OUT_DIR / "slide_015_main_diagram.png"
plt.savefig(output_path, dpi=DPI, transparent=True, bbox_inches='tight', pad_inches=0.02)
plt.close()

print(f"Generated: {output_path}")
print(f"Size: {FIG_W*DPI:.0f} x {FIG_H*DPI:.0f} px at {DPI} dpi")

import json
meta = {"image": "slide_015_main_diagram.png", "width_in": FIG_W, "height_in": FIG_H, "dpi": DPI}
with open(OUT_DIR / "slide_015_main_diagram.json", "w") as f:
    json.dump(meta, f, indent=2)
print(f"Metadata saved")