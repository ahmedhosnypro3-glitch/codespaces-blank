#!/usr/bin/env python3
"""Generate slide 16 neural network diagram — 3-layer network with backprop error paths."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch

fig, ax = plt.subplots(figsize=(13.33, 7.5), dpi=600)
ax.set_xlim(0, 13.33)
ax.set_ylim(0, 7.5)
ax.axis('off')
fig.patch.set_alpha(0.0)

# Colors
BG = "#F5E8D0"
INPUT_NODE_COLOR = "#FFFFFF"
HIDDEN_NODE_COLOR = "#00FF00"
OUTPUT_NODE_COLOR = "#FFA500"
SIGMA_COLOR = "#C0392B"
WEIGHT_COLOR_1 = "#2980B9"
WEIGHT_COLOR_2 = "#800080"
BIAS_COLOR = "#800080"
ERROR_COLOR = "#8B0000"
INPUT_BOX_COLOR = "#DDA0DD"
INPUT_BOX_BORDER = "#800080"
CLASS_COLOR = "#90EE90"
CLASS_BORDER = "#006400"
OUTPUT_LABEL_COLOR = "#FFA07A"
OUTPUT_LABEL_BORDER = "#FF4500"
ANNO_BOX_COLORS = [
    "#E6F3FF",  # Previous Layer (l) - blue
    "#E6FFE6",  # Current Layer (You are here) - green
    "#FFE6CC",  # Next Layer (K) - orange
    "#FFFFFF",  # Note - white with red border
]
ANNO_BORDERS = ["#0000FF", "#008000", "#FF8C00", "#FF0000"]

# Layout constants
LEFT_MARGIN = 0.5
RIGHT_MARGIN = 12.83
TOP_DIAGRAM = 1.8
BOTTOM_DIAGRAM = 6.2
DIAGRAM_H = BOTTOM_DIAGRAM - TOP_DIAGRAM
CENTER_Y = (TOP_DIAGRAM + BOTTOM_DIAGRAM) / 2

# Three columns
COL1_X = 2.0   # Input layer
COL2_X = 6.5   # Hidden layer
COL3_X = 11.0  # Output layer
NODE_R = 0.25

# --- Input nodes (left column) ---
input_y_positions = [CENTER_Y - 0.8, CENTER_Y, CENTER_Y + 0.8]
for i, y in enumerate(input_y_positions):
    circle = Circle((COL1_X, y), NODE_R, facecolor=INPUT_NODE_COLOR, edgecolor='black', linewidth=1.5, zorder=5)
    ax.add_patch(circle)
    ax.text(COL1_X, y, r'$\Sigma$', fontsize=24, fontweight='bold', color=SIGMA_COLOR,
            ha='center', va='center', zorder=6)
    # f[] box
    fbox = FancyBboxPatch((COL1_X + 0.4, y - 0.15), 0.5, 0.3, boxstyle="round,pad=0.02",
                           facecolor='white', edgecolor='black', linewidth=1, zorder=4)
    ax.add_patch(fbox)
    ax.text(COL1_X + 0.65, y, 'f', fontsize=12, fontweight='bold', color='black',
            ha='center', va='center', zorder=5)

# --- Hidden nodes (middle column) ---
hidden_y_positions = [CENTER_Y - 0.8, CENTER_Y, CENTER_Y + 0.8]
for i, y in enumerate(hidden_y_positions):
    circle = Circle((COL2_X, y), NODE_R, facecolor=HIDDEN_NODE_COLOR, edgecolor='black', linewidth=1.5, zorder=5)
    ax.add_patch(circle)
    ax.text(COL2_X, y, r'$\Sigma$', fontsize=24, fontweight='bold', color=SIGMA_COLOR,
            ha='center', va='center', zorder=6)
    # O_j label
    ax.text(COL2_X - 0.7, y + 0.35, r'$O_j$', fontsize=12, color='black',
            ha='center', va='center', zorder=6)
    # f[] box
    fbox = FancyBboxPatch((COL2_X + 0.4, y - 0.15), 0.5, 0.3, boxstyle="round,pad=0.02",
                           facecolor='white', edgecolor='black', linewidth=1, zorder=4)
    ax.add_patch(fbox)
    ax.text(COL2_X + 0.65, y, 'f', fontsize=12, fontweight='bold', color='black',
            ha='center', va='center', zorder=5)
    # Purple bias circle with '1'
    bias_circle = Circle((COL2_X - 1.0, y - 0.6), 0.15, facecolor=BIAS_COLOR, edgecolor='black', linewidth=1, zorder=5)
    ax.add_patch(bias_circle)
    ax.text(COL2_X - 1.0, y - 0.6, '1', fontsize=8, fontweight='bold', color='white',
            ha='center', va='center', zorder=6)

# --- Output nodes (right column) ---
output_y_positions = [CENTER_Y - 0.8, CENTER_Y, CENTER_Y + 0.8]
for i, y in enumerate(output_y_positions):
    circle = Circle((COL3_X, y), NODE_R, facecolor=OUTPUT_NODE_COLOR, edgecolor='black', linewidth=1.5, zorder=5)
    ax.add_patch(circle)
    ax.text(COL3_X, y, r'$\Sigma$', fontsize=24, fontweight='bold', color=SIGMA_COLOR,
            ha='center', va='center', zorder=6)
    # O_k label
    ax.text(COL3_X - 0.7, y + 0.35, r'$O_k$', fontsize=12, color='black',
            ha='center', va='center', zorder=6)
    # f[] box
    fbox = FancyBboxPatch((COL3_X + 0.4, y - 0.15), 0.5, 0.3, boxstyle="round,pad=0.02",
                           facecolor='white', edgecolor='black', linewidth=1, zorder=4)
    ax.add_patch(fbox)
    ax.text(COL3_X + 0.65, y, 'f', fontsize=12, fontweight='bold', color='black',
            ha='center', va='center', zorder=5)
    # Output labels (Output 1, Output 2, Output m)
    out_labels = ['Output 1', 'Output 2', 'Output m']
    out_box = FancyBboxPatch((COL3_X + 1.1, y - 0.15), 1.2, 0.3, boxstyle="round,pad=0.02",
                              facecolor=OUTPUT_LABEL_COLOR, edgecolor=OUTPUT_LABEL_BORDER, linewidth=1.5, zorder=4)
    ax.add_patch(out_box)
    ax.text(COL3_X + 1.7, y, out_labels[i], fontsize=10, fontweight='bold', color=OUTPUT_LABEL_BORDER,
            ha='center', va='center', zorder=5)

# --- Connections: Input to Hidden (w_ji) ---
for iy in input_y_positions:
    for hy in hidden_y_positions:
        arrow = FancyArrowPatch((COL1_X + NODE_R + 0.5, iy), (COL2_X - NODE_R, hy),
                                 connectionstyle="arc3,rad=0.1",
                                 arrowstyle='->', mutation_scale=10, linewidth=0.8,
                                 color='gray', zorder=3)
        ax.add_patch(arrow)
# w_ji labels
ax.text((COL1_X + COL2_X) / 2, CENTER_Y + 1.1, r'$w_{ji}$', fontsize=11, fontweight='bold',
        color=WEIGHT_COLOR_1, ha='center', va='center', zorder=6)
ax.text((COL1_X + COL2_X) / 2 + 0.3, CENTER_Y - 1.1, r'$w_{ji}$', fontsize=11, fontweight='bold',
        color=WEIGHT_COLOR_1, ha='center', va='center', zorder=6)

# --- Connections: Hidden to Output (w_kj) ---
for hy in hidden_y_positions:
    for oy in output_y_positions:
        arrow = FancyArrowPatch((COL2_X + NODE_R + 0.5, hy), (COL3_X - NODE_R, oy),
                                 connectionstyle="arc3,rad=-0.1",
                                 arrowstyle='->', mutation_scale=10, linewidth=0.8,
                                 color='gray', zorder=3)
        ax.add_patch(arrow)
# w_kj labels
ax.text((COL2_X + COL3_X) / 2, CENTER_Y + 1.1, r'$w_{kj}$', fontsize=11, fontweight='bold',
        color=WEIGHT_COLOR_1, ha='center', va='center', zorder=6)
ax.text((COL2_X + COL3_X) / 2 - 0.3, CENTER_Y - 1.1, r'$w_{kj}$', fontsize=11, fontweight='bold',
        color=WEIGHT_COLOR_1, ha='center', va='center', zorder=6)

# --- Bias inputs (purple dots on far left) ---
for i, y in enumerate(input_y_positions):
    bias = Circle((COL1_X - 0.8, y), 0.1, facecolor=BIAS_COLOR, edgecolor='black', linewidth=1, zorder=5)
    ax.add_patch(bias)
    ax.text(COL1_X - 0.8, y, '1', fontsize=7, fontweight='bold', color='white',
            ha='center', va='center', zorder=6)
ax.text(COL1_X - 0.8, CENTER_Y + 1.2, 'Node Bias', fontsize=10, color='black',
        ha='center', va='center', zorder=6)

# --- Input Sample box (top left) ---
in_box = FancyBboxPatch((0.5, TOP_DIAGRAM + 2.5), 1.8, 0.5, boxstyle="round,pad=0.05",
                         facecolor=INPUT_BOX_COLOR, edgecolor=INPUT_BOX_BORDER, linewidth=2, zorder=4)
ax.add_patch(in_box)
ax.text(1.4, TOP_DIAGRAM + 2.75, 'Input Sample', fontsize=14, fontweight='bold', color=INPUT_BOX_BORDER,
        ha='center', va='center', zorder=5)
# Arrow from Input Sample to input nodes
arrow = FancyArrowPatch((2.3, TOP_DIAGRAM + 2.75), (COL1_X - NODE_R, input_y_positions[1]),
                         connectionstyle="arc3,rad=-0.3",
                         arrowstyle='->', mutation_scale=15, linewidth=2,
                         color=INPUT_BOX_BORDER, zorder=3)
ax.add_patch(arrow)

# --- Target Label box (top right) ---
target_box = FancyBboxPatch((11.03, TOP_DIAGRAM + 2.5), 1.8, 0.5, boxstyle="round,pad=0.05",
                             facecolor=INPUT_BOX_COLOR, edgecolor=INPUT_BOX_BORDER, linewidth=2, zorder=4)
ax.add_patch(target_box)
ax.text(11.93, TOP_DIAGRAM + 2.75, 'Target Label', fontsize=14, fontweight='bold', color=INPUT_BOX_BORDER,
        ha='center', va='center', zorder=5)
# Arrow from output to Target Label
arrow = FancyArrowPatch((COL3_X + 2.5, output_y_positions[1]), (11.03, TOP_DIAGRAM + 2.75),
                         connectionstyle="arc3,rad=0.3",
                         arrowstyle='->', mutation_scale=15, linewidth=2,
                         color=INPUT_BOX_BORDER, zorder=3)
ax.add_patch(arrow)

# --- Error bar (vertical red bar on right) ---
error_bar_x = 12.5
error_bar_y = 2.0
error_bar_h = 3.5
error_bar = plt.Rectangle((error_bar_x, error_bar_y), 0.4, error_bar_h,
                           facecolor=ERROR_COLOR, edgecolor='none', zorder=4)
ax.add_patch(error_bar)
ax.text(error_bar_x + 0.2, error_bar_y + error_bar_h / 2, 'Error Error',
        fontsize=10, fontweight='bold', color='white',
        ha='center', va='center', rotation=90, zorder=5)

# --- Class labels ---
class_labels = ['Class 1', 'Class 2', 'Class m']
for i, label in enumerate(class_labels):
    class_box = FancyBboxPatch((12.93, error_bar_y + i * 1.0), 1.0, 0.8,
                                boxstyle="round,pad=0.02",
                                facecolor=CLASS_COLOR, edgecolor=CLASS_BORDER, linewidth=1.5, zorder=4)
    ax.add_patch(class_box)
    ax.text(13.43, error_bar_y + i * 1.0 + 0.4, label, fontsize=11, fontweight='bold', color=CLASS_BORDER,
            ha='center', va='center', zorder=5)

# --- Bottom annotation boxes ---
box_y = 6.4
box_h = 1.0
gap = 0.15
b1_x, b1_w = 0.5, 2.0
b2_x, b2_w = b1_x + b1_w + gap, 2.0
b3_x, b3_w = b2_x + b2_w + gap, 2.0
b4_x, b4_w = b3_x + b3_w + gap, 2.0

anno_texts = [
    'Previous Layer (l)',
    'Current Layer (You are here)',
    'Next Layer (K)',
    'Note: Layer "j" is NOT Output Layer',
]

for i, (bx, bw, text, fc, bc) in enumerate(zip(
    [b1_x, b2_x, b3_x, b4_x],
    [b1_w, b2_w, b3_w, b4_w],
    anno_texts,
    ANNO_BOX_COLORS,
    ANNO_BORDERS
)):
    box = FancyBboxPatch((bx, box_y), bw, box_h, boxstyle="round,pad=0.05",
                          facecolor=fc, edgecolor=bc, linewidth=1.5 if i < 3 else 2, zorder=4)
    ax.add_patch(box)
    ax.text(bx + bw/2, box_y + box_h/2 + 0.1, text, fontsize=10, fontweight='bold', color='black',
            ha='center', va='center', zorder=5)
    # Up arrows with labels
    if i == 0:
        ax.text(bx + bw/2, box_y - 0.15, '↑ i', fontsize=14, color='black', ha='center', va='bottom', zorder=5)
    elif i == 1:
        ax.text(bx + bw/2, box_y - 0.15, '↑ j', fontsize=14, color='black', ha='center', va='bottom', zorder=5)
    elif i == 2:
        ax.text(bx + bw/2, box_y - 0.15, '↑ k', fontsize=14, color='black', ha='center', va='bottom', zorder=5)

# --- Dashed error backprop arrows (curved from output back toward left) ---
for i, oy in enumerate(output_y_positions):
    arrow = FancyArrowPatch((COL3_X + 1.0, oy), (COL2_X - 0.5, hidden_y_positions[i]),
                             connectionstyle="arc3,rad=0.4",
                             arrowstyle='->', mutation_scale=10, linewidth=1.2,
                             color='red', linestyle='--', zorder=3)
    ax.add_patch(arrow)

# Save
plt.savefig('slide_016_diagram.png', dpi=600, transparent=True, bbox_inches='tight', pad_inches=0)
plt.close()
print("Generated slide_016_diagram.png")