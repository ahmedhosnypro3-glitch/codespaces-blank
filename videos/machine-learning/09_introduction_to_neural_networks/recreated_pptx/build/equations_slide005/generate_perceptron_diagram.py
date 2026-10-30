#!/usr/bin/env python3
"""
Generate perceptron architecture diagram for slide 005.
Uses matplotlib/networkx to create the network diagram matching the original frame.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Circle, Rectangle, FancyBboxPatch
import numpy as np
from PIL import Image

# Original frame is 960x540 at 13.33x7.5in -> 72 dpi = 960x540 pixels
# But we want high quality for PPTX embedding, so render at 300 DPI
DPI = 300

# Convert inches to pixels for our render
# The diagram region in the original: bottom left, roughly x=24% to x=64%, y=64% to y=94%
# In inches: 13.33 * 0.24 = 3.2 to 13.33 * 0.64 = 8.53, height 7.5 * (0.94-0.64) = 2.25
# We'll render a slightly larger image and let the PPTX position it precisely

fig, ax = plt.subplots(figsize=(10, 4), dpi=DPI)
ax.set_xlim(0, 10)
ax.set_ylim(0, 4)
ax.axis('off')

# Colors from the original analysis
WHITE = '#ffffff'
RED = '#c00000'
BLUE = '#add8e6'  # light blue for summation circle
PINK = '#ffb6c1'  # pink for step function box
BLACK = '#000000'
GRAY = '#808080'

FONT = 'DejaVu Sans'
MONO_FONT = 'DejaVu Sans Mono'

# ============================================================
# LAYOUT PARAMETERS (matching original visual proportions)
# ============================================================
# Left column: input nodes
input_x = 1.0
input_ys = [3.2, 2.6, 2.0, 1.4, 0.8]
# Middle column: weight nodes
weight_x = 3.5
weight_ys = [3.2, 2.6, 2.0, 1.4, 0.8]
# Summation circle
sum_x = 6.0
sum_y = 2.0
# Step function box
step_x = 8.0
step_y = 2.0
# Output
output_x = 9.5
output_y = 2.0

# ============================================================
# DRAW INPUT NODES (left column)
# ============================================================
input_labels = ['x₁', 'x₂', 'x₃', '...', 'xₙ']
for i, (y, label) in enumerate(zip(input_ys, input_labels)):
    color = RED if label == '...' else BLACK
    ax.text(input_x, y, label, fontsize=14, ha='center', va='center', 
            fontfamily=FONT, color=color, weight='bold' if label == '...' else 'normal')

# Bias input (red '1')
ax.text(input_x, 0.2, '1', fontsize=14, ha='center', va='center',
        fontfamily=FONT, color=RED, weight='bold')

# ============================================================
# DRAW WEIGHT NODES (middle column)
# ============================================================
weight_labels = ['w₁', 'w₂', 'w₃', '...', 'wₙ']
for i, (y, label) in enumerate(zip(weight_ys, weight_labels)):
    color = RED if label == '...' else BLACK
    ax.text(weight_x, y, label, fontsize=14, ha='center', va='center',
            fontfamily=FONT, color=color, weight='bold' if label == '...' else 'normal')

# Bias weight (red 'b')
ax.text(weight_x, 0.2, 'b', fontsize=14, ha='center', va='center',
        fontfamily=FONT, color=RED, weight='bold')

# ============================================================
# DRAW CONNECTIONS (lines from inputs to weights to summation)
# ============================================================
# Input to weight connections (thin gray lines)
for y in input_ys:
    ax.plot([input_x + 0.1, weight_x - 0.1], [y, y], color=GRAY, linewidth=0.5, alpha=0.7)
ax.plot([input_x + 0.1, weight_x - 0.1], [0.2, 0.2], color=GRAY, linewidth=0.5, alpha=0.7)

# Weight to summation (fan in)
for y in weight_ys:
    # Create curved/fan lines
    ax.plot([weight_x + 0.1, sum_x - 0.4], [y, sum_y], color=GRAY, linewidth=0.5, alpha=0.7)
ax.plot([weight_x + 0.1, sum_x - 0.4], [0.2, sum_y], color=GRAY, linewidth=0.5, alpha=0.7)

# ============================================================
# DRAW SUMMATION NODE (light blue circle with Σ)
# ============================================================
sum_circle = Circle((sum_x, sum_y), 0.35, facecolor=BLUE, edgecolor=BLACK, linewidth=1.5, zorder=5)
ax.add_patch(sum_circle)
ax.text(sum_x, sum_y, 'Σ', fontsize=20, ha='center', va='center',
        fontfamily=FONT, color=BLACK, weight='bold')

# "O/P" label above summation
ax.text(sum_x, sum_y + 0.6, 'O/P', fontsize=11, ha='center', va='center',
        fontfamily=FONT, color=BLACK, weight='bold')

# ============================================================
# DRAW ARROW FROM SUMMATION TO STEP FUNCTION
# ============================================================
arrow = FancyArrowPatch(
    (sum_x + 0.35, sum_y), (step_x - 0.5, step_y),
    arrowstyle='->', mutation_scale=20, color=BLACK, linewidth=1.5
)
ax.add_patch(arrow)

# ============================================================
# DRAW STEP FUNCTION BOX (pink rectangle with step icon)
# ============================================================
step_box = FancyBboxPatch(
    (step_x - 0.5, step_y - 0.4), 1.0, 0.8,
    boxstyle="round,pad=0.02",
    facecolor=PINK, edgecolor=BLACK, linewidth=1.5
)
ax.add_patch(step_box)

# Draw step function icon inside the box
# Step: horizontal at bottom, vertical jump, horizontal at top
step_center_x = step_x
step_center_y = step_y
step_width = 0.5
step_height = 0.5

# Bottom horizontal
ax.plot([step_center_x - step_width/2, step_center_x], 
        [step_center_y - step_height/2, step_center_y - step_height/2], 
        color=RED, linewidth=2)
# Vertical jump
ax.plot([step_center_x, step_center_x], 
        [step_center_y - step_height/2, step_center_y + step_height/2], 
        color=RED, linewidth=2)
# Top horizontal
ax.plot([step_center_x, step_center_x + step_width/2], 
        [step_center_y + step_height/2, step_center_y + step_height/2], 
        color=RED, linewidth=2)

# ============================================================
# DRAW ARROW FROM STEP FUNCTION TO OUTPUT
# ============================================================
arrow2 = FancyArrowPatch(
    (step_x + 0.5, step_y), (output_x, output_y),
    arrowstyle='->', mutation_scale=20, color=BLACK, linewidth=1.5
)
ax.add_patch(arrow2)

# Output label
ax.text(output_x, output_y, 'O/P', fontsize=12, ha='center', va='center',
        fontfamily=FONT, color=BLACK, weight='bold')

# ============================================================
# DRAW ENCLOSING BOX (white with red border)
# ============================================================
# The whole diagram is in a white box with red border
encl_x, encl_y = 0.3, -0.2
encl_w, encl_h = 9.6, 4.4
encl_box = FancyBboxPatch(
    (encl_x, encl_y), encl_w, encl_h,
    boxstyle="round,pad=0.05",
    facecolor=WHITE, edgecolor=RED, linewidth=2
)
ax.add_patch(encl_box)

# ============================================================
# LABELS: "Augmented Vector" and "Model Weights"
# ============================================================
# These are blue italic labels to the right of the columns
ax.text(input_x + 1.8, 3.5, 'Augmented Vector', fontsize=12, ha='left', va='center',
        fontfamily=FONT, color=BLUE, style='italic', weight='bold')
ax.text(weight_x + 1.8, 3.5, 'Model Weights', fontsize=12, ha='left', va='center',
        fontfamily=FONT, color=BLUE, style='italic', weight='bold')

# ============================================================
# SAVE
# ============================================================
output_path = '/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/equations_slide005/perceptron_diagram.png'
plt.tight_layout(pad=0)
plt.savefig(output_path, dpi=DPI, bbox_inches='tight', pad_inches=0.1, transparent=False, facecolor=WHITE)
plt.close()

# Also save a version with exact dimensions for reference
print(f"Saved to {output_path}")
