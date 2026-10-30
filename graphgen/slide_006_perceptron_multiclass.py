#!/usr/bin/env python3
"""
Generate multi-class perceptron architecture diagram for slide 006.

This recreates the single-layer perceptron visualization showing:
- Input nodes: x₁, x₂, x₃, ..., xₙ, 1 (bias) - TOP TO BOTTOM
- Weight connections to 3 neurons:
  - Neuron 1 (red): w₁₁, w₁₂, w₁₃, ..., w₁ₙ, b₁
  - Neuron 2 (blue): w₂₁, w₂₂, w₂₃, ..., w₂ₙ, b₂
  - Neuron m (green): wₘ₁, wₘ₂, ..., wₘₙ, bₘ
- 3 Summation nodes (Σ)
- 3 Step activation functions (purple boxes)
- 3 Output pairs: >0 Class I / <0 Not Class I, >0 Class II / <0 Not Class II, >0 Class m / <0 Not Class m
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
# Match the original slide's diagram region: right side, middle to bottom, ~60% height
# On a 13.33 x 7.5 inch slide, that's ~6 inches wide x ~4 inches tall
FIG_W, FIG_H = 6.0, 4.0
DPI = 600  # 600 dpi for crisp embedding

fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI)
ax.set_xlim(0, FIG_W)
ax.set_ylim(0, FIG_H)
ax.set_aspect('equal')
ax.axis('off')

# Colors from analysis
WHITE = '#ffffff'
RED = '#ff0000'
BLUE = '#0000ff'
GREEN = '#008000'
BLACK = '#000000'
LIGHT_BLUE = '#c0c0ff'  # Σ circle fill
PURPLE = '#d0b0ff'      # activation box fill
GRAY = '#808080'        # connection lines
INPUT_FILL = '#e6f3ff'  # input node fill

# Layout parameters
LEFT_MARGIN = 0.3
RIGHT_MARGIN = 0.2
TOP_MARGIN = 0.2
BOTTOM_MARGIN = 0.2

# Column positions
X_INPUT = 0.6
X_WEIGHT_1 = 1.4   # Neuron 1 weights (red)
X_WEIGHT_2 = 2.2   # Neuron 2 weights (blue)
X_WEIGHT_M = 3.0   # Neuron m weights (green)
X_SUM_1 = 3.8      # Σ node 1
X_SUM_2 = 4.2      # Σ node 2
X_SUM_M = 4.6      # Σ node m
X_ACT_1 = 5.2      # Activation box 1
X_ACT_2 = 5.2      # Activation box 2
X_ACT_M = 5.2      # Activation box m
X_OUT_1 = 5.9      # Output 1
X_OUT_2 = 5.9      # Output 2
X_OUT_M = 5.9      # Output m

# Row positions (TOP TO BOTTOM to match original)
# 6 inputs: x₁, x₂, x₃, ..., xₙ, 1 (bias)
n_inputs = 6
y_positions = np.linspace(FIG_H - TOP_MARGIN - 0.15, BOTTOM_MARGIN + 0.15, n_inputs)

# Input labels: x₁, x₂, x₃, ..., xₙ, 1
input_labels = ['x₁', 'x₂', 'x₃', '...', 'xₙ', '1']

# Weight labels for 3 neurons
weight_1_labels = ['w₁₁', 'w₁₂', 'w₁₃', '...', 'w₁ₙ', 'b₁']
weight_2_labels = ['w₂₁', 'w₂₂', 'w₂₃', '...', 'w₂ₙ', 'b₂']
weight_m_labels = ['wₘ₁', 'wₘ₂', 'wₘ₃', '...', 'wₘₙ', 'bₘ']

# SUM positions - 3 neurons vertically distributed
# Neuron 1 at top, Neuron 2 in middle, Neuron m at bottom
sum_1_y = y_positions[0]  # Top
sum_2_y = y_positions[2]  # Middle (around 3rd input)
sum_m_y = y_positions[-1]  # Bottom

# Draw input column
for i, (y, x_label) in enumerate(zip(y_positions, input_labels)):
    # Input node - circle
    color = RED if i == n_inputs - 1 else BLACK  # bias '1' in red
    circle = Circle((X_INPUT, y), 0.1, facecolor=INPUT_FILL, edgecolor=BLACK, linewidth=1, zorder=5)
    ax.add_patch(circle)
    ax.text(X_INPUT, y, x_label, ha='center', va='center', fontsize=12, fontweight='bold', color=color, zorder=6)

# Weight columns for 3 neurons
# Neuron 1 (red)
for i, (y, w_label) in enumerate(zip(y_positions, weight_1_labels)):
    ax.text(X_WEIGHT_1, y, w_label, ha='center', va='center', fontsize=10, fontweight='bold', color=RED, zorder=6)
    # Connection from input to Σ1
    arrow = FancyArrowPatch(
        (X_INPUT + 0.1, y), (X_SUM_1 - 0.25, sum_1_y),
        arrowstyle='->', color=GRAY, linewidth=0.4,
        mutation_scale=6, zorder=3
    )
    ax.add_patch(arrow)

# Neuron 2 (blue)
for i, (y, w_label) in enumerate(zip(y_positions, weight_2_labels)):
    ax.text(X_WEIGHT_2, y, w_label, ha='center', va='center', fontsize=10, fontweight='bold', color=BLUE, zorder=6)
    # Connection from input to Σ2
    arrow = FancyArrowPatch(
        (X_INPUT + 0.1, y), (X_SUM_2 - 0.25, sum_2_y),
        arrowstyle='->', color=GRAY, linewidth=0.4,
        mutation_scale=6, zorder=3
    )
    ax.add_patch(arrow)

# Neuron m (green)
for i, (y, w_label) in enumerate(zip(y_positions, weight_m_labels)):
    ax.text(X_WEIGHT_M, y, w_label, ha='center', va='center', fontsize=10, fontweight='bold', color=GREEN, zorder=6)
    # Connection from input to Σm
    arrow = FancyArrowPatch(
        (X_INPUT + 0.1, y), (X_SUM_M - 0.25, sum_m_y),
        arrowstyle='->', color=GRAY, linewidth=0.4,
        mutation_scale=6, zorder=3
    )
    ax.add_patch(arrow)

# Column labels at top
ax.text(X_INPUT, FIG_H - TOP_MARGIN + 0.1, 'Inputs', ha='center', va='bottom', fontsize=9, fontweight='bold', color='#0000ff', style='italic')
ax.text(X_WEIGHT_1, FIG_H - TOP_MARGIN + 0.1, 'Weights 1', ha='center', va='bottom', fontsize=9, fontweight='bold', color=RED, style='italic')
ax.text(X_WEIGHT_2, FIG_H - TOP_MARGIN + 0.1, 'Weights 2', ha='center', va='bottom', fontsize=9, fontweight='bold', color=BLUE, style='italic')
ax.text(X_WEIGHT_M, FIG_H - TOP_MARGIN + 0.1, 'Weights m', ha='center', va='bottom', fontsize=9, fontweight='bold', color=GREEN, style='italic')

# Summation nodes (Σ) - light blue circles
# Neuron 1 (top)
sum_circle_1 = Circle((X_SUM_1, sum_1_y), 0.18, facecolor=LIGHT_BLUE, edgecolor=BLACK, linewidth=1.5, zorder=5)
ax.add_patch(sum_circle_1)
ax.text(X_SUM_1, sum_1_y, 'Σ', ha='center', va='center', fontsize=18, fontweight='bold', zorder=6)

# Neuron 2 (middle)
sum_circle_2 = Circle((X_SUM_2, sum_2_y), 0.18, facecolor=LIGHT_BLUE, edgecolor=BLACK, linewidth=1.5, zorder=5)
ax.add_patch(sum_circle_2)
ax.text(X_SUM_2, sum_2_y, 'Σ', ha='center', va='center', fontsize=18, fontweight='bold', zorder=6)

# Vertical ellipsis between Σ2 and Σm
ellipsis_y = (sum_2_y + sum_m_y) / 2
ax.text(X_SUM_2, ellipsis_y, '⋮', ha='center', va='center', fontsize=20, fontweight='bold', zorder=6)

# Neuron m (bottom)
sum_circle_m = Circle((X_SUM_M, sum_m_y), 0.18, facecolor=LIGHT_BLUE, edgecolor=BLACK, linewidth=1.5, zorder=5)
ax.add_patch(sum_circle_m)
ax.text(X_SUM_M, sum_m_y, 'Σ', ha='center', va='center', fontsize=18, fontweight='bold', zorder=6)

# Arrows from Σ to activation boxes
# Neuron 1
arrow = FancyArrowPatch(
    (X_SUM_1 + 0.18, sum_1_y), (X_ACT_1 - 0.25, sum_1_y),
    arrowstyle='->', color=RED, linewidth=1.5,
    mutation_scale=10, zorder=4
)
ax.add_patch(arrow)

# Neuron 2
arrow = FancyArrowPatch(
    (X_SUM_2 + 0.18, sum_2_y), (X_ACT_2 - 0.25, sum_2_y),
    arrowstyle='->', color=RED, linewidth=1.5,
    mutation_scale=10, zorder=4
)
ax.add_patch(arrow)

# Neuron m
arrow = FancyArrowPatch(
    (X_SUM_M + 0.18, sum_m_y), (X_ACT_M - 0.25, sum_m_y),
    arrowstyle='->', color=RED, linewidth=1.5,
    mutation_scale=10, zorder=4
)
ax.add_patch(arrow)

# Activation boxes - purple rectangles
act_w, act_h = 0.5, 0.35
# Neuron 1
act_rect_1 = Rectangle((X_ACT_1, sum_1_y - act_h/2), act_w, act_h, facecolor=PURPLE, edgecolor=BLACK, linewidth=1, zorder=5)
ax.add_patch(act_rect_1)
# Neuron 2
act_rect_2 = Rectangle((X_ACT_2, sum_2_y - act_h/2), act_w, act_h, facecolor=PURPLE, edgecolor=BLACK, linewidth=1, zorder=5)
ax.add_patch(act_rect_2)
# Neuron m
act_rect_m = Rectangle((X_ACT_M, sum_m_y - act_h/2), act_w, act_h, facecolor=PURPLE, edgecolor=BLACK, linewidth=1, zorder=5)
ax.add_patch(act_rect_m)

# Outputs - two lines per neuron
# Neuron 1 outputs
ax.text(X_OUT_1 + 0.05, sum_1_y + 0.1, '>0 Class I', ha='left', va='center', fontsize=10, fontweight='bold', color=BLACK, zorder=6)
ax.text(X_OUT_1 + 0.05, sum_1_y - 0.1, '<0 Not Class I', ha='left', va='center', fontsize=10, fontweight='bold', color=BLACK, zorder=6)

# Neuron 2 outputs
ax.text(X_OUT_2 + 0.05, sum_2_y + 0.1, '>0 Class II', ha='left', va='center', fontsize=10, fontweight='bold', color=BLACK, zorder=6)
ax.text(X_OUT_2 + 0.05, sum_2_y - 0.1, '<0 Not Class II', ha='left', va='center', fontsize=10, fontweight='bold', color=BLACK, zorder=6)

# Vertical ellipsis between outputs 2 and m
ax.text(X_OUT_1, ellipsis_y, '⋮', ha='center', va='center', fontsize=16, fontweight='bold', zorder=6)

# Neuron m outputs
ax.text(X_OUT_M + 0.05, sum_m_y + 0.1, '>0 Class m', ha='left', va='center', fontsize=10, fontweight='bold', color=BLACK, zorder=6)
ax.text(X_OUT_M + 0.05, sum_m_y - 0.1, '<0 Not Class m', ha='left', va='center', fontsize=10, fontweight='bold', color=BLACK, zorder=6)

# Enclosing box around the diagram area (white background with red border)
box = Rectangle(
    (LEFT_MARGIN, BOTTOM_MARGIN), 
    FIG_W - LEFT_MARGIN - RIGHT_MARGIN, 
    FIG_H - TOP_MARGIN - BOTTOM_MARGIN,
    facecolor=WHITE, edgecolor='#c00000', linewidth=1.5, zorder=1
)
ax.add_patch(box)

# Save
output_path = OUT_DIR / "slide_006_perceptron_multiclass.png"
plt.savefig(output_path, dpi=DPI, transparent=True, bbox_inches='tight', pad_inches=0.02)
plt.close()

print(f"Generated: {output_path}")
print(f"Size: {FIG_W*DPI:.0f} x {FIG_H*DPI:.0f} px at {DPI} dpi")
print(f"Inches at 600dpi embed: {FIG_W:.2f} x {FIG_H:.2f} in")

# Also save a sidecar JSON with metadata for the build script
import json
meta = {
    "image": "slide_006_perceptron_multiclass.png",
    "width_in": FIG_W,
    "height_in": FIG_H,
    "dpi": DPI,
    "position": {
        "x": 7.0,   # Right side (~52% of 13.33)
        "y": 2.8,   # Middle (~37% of 7.5)
        "w": 6.0,
        "h": 4.0
    }
}
with open(OUT_DIR / "slide_006_perceptron_multiclass.json", "w") as f:
    json.dump(meta, f, indent=2)
print(f"Metadata saved to {OUT_DIR}/slide_006_perceptron_multiclass.json")