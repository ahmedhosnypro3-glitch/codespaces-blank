#!/usr/bin/env python3
"""Generate perceptron diagram for slide 013 (XOR slide).

This recreates the single perceptron visualization showing:
- Input nodes: x1, x2, 1 (bias) - each with blue '?' weight
- Summation node (Σ)
- Step activation function (purple outline)
- Output O/P
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
# Match the original slide's diagram region: roughly bottom left, x=0.5-5.5, y=4.5-6.8
# On a 13.33 x 7.5 inch slide, that's ~5 inches wide x ~2.3 inches tall
FIG_W, FIG_H = 5.0, 2.3
DPI = 600  # 600 dpi for crisp embedding

fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI)
ax.set_xlim(0, FIG_W)
ax.set_ylim(0, FIG_H)
ax.set_aspect('equal')
ax.axis('off')

# Colors from analysis
WHITE = '#ffffff'
RED = '#B22222'
BLACK = '#000000'
PURPLE = '#9370DB'
BLUE = '#0000FF'
GRAY = '#808080'

# Layout parameters
LEFT_MARGIN = 0.2
RIGHT_MARGIN = 0.2
TOP_MARGIN = 0.15
BOTTOM_MARGIN = 0.15

# Column positions
X_INPUT = 0.5
X_WEIGHT = 1.3
X_SUM = 2.8
X_ACTIVATION = 3.7
X_OUTPUT = 4.5

# Row positions - three inputs: x1, x2, 1 (bias) - TOP TO BOTTOM
y_positions = np.linspace(FIG_H - TOP_MARGIN - 0.15, BOTTOM_MARGIN + 0.15, 3)

# Draw input column - TOP TO BOTTOM: x1, x2, 1
input_labels = ['x\u2081', 'x\u2082', '1']

for i, (y, label) in enumerate(zip(y_positions, input_labels)):
    # Input label
    ax.text(X_INPUT, y, label, ha='right', va='center', fontsize=14, fontweight='normal', color=BLACK, zorder=6)
    
    # Blue '?' weight label
    ax.text(X_WEIGHT, y, '?', ha='center', va='center', fontsize=14, fontweight='bold', color=BLUE, zorder=6)
    
    # Connection line from input to sum (converging to middle)
    sum_y = y_positions[1]  # middle row
    arrow = FancyArrowPatch(
        (X_WEIGHT + 0.15, y), (X_SUM - 0.3, sum_y),
        arrowstyle='->', color=GRAY, linewidth=1.0,
        mutation_scale=10, zorder=3
    )
    ax.add_patch(arrow)

# Summation node (Σ) - white circle with black border at middle height
sum_y = y_positions[1]
sum_circle = Circle((X_SUM, sum_y), 0.25, facecolor=WHITE, edgecolor=BLACK, linewidth=1.5, zorder=5)
ax.add_patch(sum_circle)
ax.text(X_SUM, sum_y, '\u03a3', ha='center', va='center', fontsize=22, fontweight='bold', color=BLACK, zorder=6)

# Arrow from sum to activation box
arrow = FancyArrowPatch(
    (X_SUM + 0.3, sum_y), (X_ACTIVATION - 0.2, sum_y),
    arrowstyle='->', color=BLACK, linewidth=1.5,
    mutation_scale=12, zorder=4
)
ax.add_patch(arrow)

# Activation box - purple outline, white fill
act_rect = Rectangle((X_ACTIVATION, sum_y - 0.15), 0.4, 0.3, facecolor=WHITE, edgecolor=PURPLE, linewidth=1.5, zorder=5)
ax.add_patch(act_rect)
# Step function symbol inside
step_x = X_ACTIVATION + 0.2
step_y = sum_y
# Horizontal line, vertical riser, horizontal line (step function)
ax.plot([step_x - 0.12, step_x], [step_y, step_y], 'k-', linewidth=1.5, zorder=6)
ax.plot([step_x, step_x], [step_y - 0.1, step_y + 0.1], 'k-', linewidth=1.5, zorder=6)
ax.plot([step_x, step_x + 0.12], [step_y + 0.1, step_y + 0.1], 'k-', linewidth=1.5, zorder=6)

# Arrow from activation to output
arrow = FancyArrowPatch(
    (X_ACTIVATION + 0.4, sum_y), (X_OUTPUT, sum_y),
    arrowstyle='->', color=BLACK, linewidth=1.5,
    mutation_scale=12, zorder=4
)
ax.add_patch(arrow)

# Output O/P
ax.text(X_OUTPUT + 0.15, sum_y, 'O/P', ha='left', va='center', fontsize=14, fontweight='bold', color=BLACK, zorder=6)

# Enclosing red border box around the diagram
box = Rectangle(
    (LEFT_MARGIN, BOTTOM_MARGIN), 
    FIG_W - LEFT_MARGIN - RIGHT_MARGIN, 
    FIG_H - TOP_MARGIN - BOTTOM_MARGIN,
    facecolor=WHITE, edgecolor=RED, linewidth=1.5, zorder=1
)
ax.add_patch(box)

# Save
output_path = OUT_DIR / "slide_013_perceptron_diagram.png"
plt.savefig(output_path, dpi=DPI, transparent=True, bbox_inches='tight', pad_inches=0.02)
plt.close()

print(f"Generated: {output_path}")
print(f"Size: {FIG_W*DPI:.0f} x {FIG_H*DPI:.0f} px at {DPI} dpi")
print(f"Inches at 600dpi embed: {FIG_W:.2f} x {FIG_H:.2f} in")

# Also save a sidecar JSON with metadata for the build script
import json
meta = {
    "image": "slide_013_perceptron_diagram.png",
    "width_in": FIG_W,
    "height_in": FIG_H,
    "dpi": DPI,
    "position": {
        "x": 0.5,
        "y": 4.5,
        "w": 5.0,
        "h": 2.3
    }
}
with open(OUT_DIR / "slide_013_perceptron_diagram.json", "w") as f:
    json.dump(meta, f, indent=2)
print(f"Metadata saved to {OUT_DIR}/slide_013_perceptron_diagram.json")