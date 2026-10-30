#!/usr/bin/env python3
"""
Generate single perceptron diagram for slide 014 (bottom-right yellow box).
Matches the original: inputs x1, x2, weights w1, w2, summation, step function, O/P.
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

FIG_W, FIG_H = 3.0, 1.8
DPI = 600

fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI)
ax.set_xlim(0, FIG_W)
ax.set_ylim(0, FIG_H)
ax.set_aspect('equal')
ax.axis('off')

WHITE = '#ffffff'
BLACK = '#000000'
RED = '#c00000'
PURPLE = '#d0b0d0'
YELLOW_BG = '#fff9c4'

# Layout
X_INPUT = 0.3
X_WEIGHT = 0.8
X_SUM = 1.5
X_STEP = 2.2
X_OP = 2.7

Y_X1 = FIG_H * 0.75
Y_X2 = FIG_H * 0.25
Y_SUM = FIG_H * 0.5
Y_STEP = FIG_H * 0.5
Y_OP = FIG_H * 0.5

# Input nodes
for y, label in [(Y_X1, 'x₁'), (Y_X2, 'x₂')]:
    circle = Circle((X_INPUT, y), 0.08, facecolor=WHITE, edgecolor=BLACK, linewidth=1, zorder=5)
    ax.add_patch(circle)
    ax.text(X_INPUT, y, label, ha='center', va='center', fontsize=10, fontweight='bold', zorder=6)

# Weight labels
ax.text(X_WEIGHT, Y_X1, 'w₁', ha='center', va='center', fontsize=10, fontweight='bold', color=BLACK, zorder=6)
ax.text(X_WEIGHT, Y_X2, 'w₂', ha='center', va='center', fontsize=10, fontweight='bold', color=BLACK, zorder=6)

# Connections x -> weights
for y_src in [Y_X1, Y_X2]:
    arrow = FancyArrowPatch((X_INPUT + 0.08, y_src), (X_WEIGHT - 0.05, y_src),
        arrowstyle='->', color=BLACK, linewidth=0.5, mutation_scale=6, zorder=4)
    ax.add_patch(arrow)

# Connections weights -> summation (fan in)
for y_src in [Y_X1, Y_X2]:
    arrow = FancyArrowPatch((X_WEIGHT + 0.05, y_src), (X_SUM - 0.12, Y_SUM),
        arrowstyle='->', color=BLACK, linewidth=0.5, mutation_scale=6, zorder=4)
    ax.add_patch(arrow)

# Summation node
sum_circle = Circle((X_SUM, Y_SUM), 0.12, facecolor=WHITE, edgecolor=BLACK, linewidth=1.5, zorder=5)
ax.add_patch(sum_circle)
ax.text(X_SUM, Y_SUM, 'Σ', ha='center', va='center', fontsize=16, fontweight='bold', zorder=6)

# Arrow to step function
arrow = FancyArrowPatch((X_SUM + 0.12, Y_SUM), (X_STEP, Y_STEP),
    arrowstyle='->', color=BLACK, linewidth=1.0, mutation_scale=10, zorder=4)
ax.add_patch(arrow)

# Step function box (purple)
step_box = FancyBboxPatch(
    (X_STEP, Y_STEP - 0.1), 0.35, 0.2,
    boxstyle="round,pad=0.02",
    facecolor=PURPLE, edgecolor=BLACK, linewidth=1, zorder=5
)
ax.add_patch(step_box)

# Step icon
step_cx = X_STEP + 0.175
step_cy = Y_STEP
sw, sh = 0.12, 0.08
ax.plot([step_cx - sw/2, step_cx], [step_cy - sh/2, step_cy - sh/2], color=RED, linewidth=1, zorder=6)
ax.plot([step_cx, step_cx], [step_cy - sh/2, step_cy + sh/2], color=RED, linewidth=1, zorder=6)
ax.plot([step_cx, step_cx + sw/2], [step_cy + sh/2, step_cy + sh/2], color=RED, linewidth=1, zorder=6)

# Arrow to O/P
arrow = FancyArrowPatch((X_STEP + 0.35, Y_STEP), (X_OP, Y_OP),
    arrowstyle='->', color=BLACK, linewidth=1.0, mutation_scale=10, zorder=4)
ax.add_patch(arrow)
ax.text(X_OP + 0.05, Y_OP, 'O/P', ha='left', va='center', fontsize=10, fontweight='bold', zorder=6)

# Yellow background box with border
margin = 0.05
box = Rectangle(
    (margin, margin), FIG_W - 2*margin, FIG_H - 2*margin,
    facecolor=YELLOW_BG, edgecolor=BLACK, linewidth=1, zorder=1
)
ax.add_patch(box)

# Save
output_path = OUT_DIR / "slide_014_small_diagram.png"
plt.savefig(output_path, dpi=DPI, transparent=True, bbox_inches='tight', pad_inches=0.02)
plt.close()

print(f"Generated: {output_path}")

import json
meta = {
    "image": "slide_014_small_diagram.png",
    "width_in": FIG_W,
    "height_in": FIG_H,
    "dpi": DPI,
}
with open(OUT_DIR / "slide_014_small_diagram.json", "w") as f:
    json.dump(meta, f, indent=2)
print(f"Metadata saved")