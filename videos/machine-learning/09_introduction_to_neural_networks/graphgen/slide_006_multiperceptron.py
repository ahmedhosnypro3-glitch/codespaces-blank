#!/usr/bin/env python3
"""Generate the single-layer perceptron (multi-output) diagram for slide_006."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from matplotlib.path import Path
import matplotlib.patches as patches

W, H = 5.0, 4.0
fig, ax = plt.subplots(figsize=(W, H), dpi=200)
ax.set_xlim(0, 12); ax.set_ylim(0, 8)
ax.axis("off")

# Input column (left)
inputs = ["$x_1$", "$x_2$", "$x_3$", "...", "$x_n$", "$1$"]
ys = [7.0, 6.0, 5.0, 4.0, 3.0, 2.0]

for y, lab in zip(ys, inputs):
    ax.text(1.0, y, lab, ha="center", va="center", fontsize=11, color="#000000", style="italic")
    # input node circles
    circ = Circle((1.0, y), 0.25, facecolor="#e6f3ff", edgecolor="#000000", lw=0.8, zorder=3)
    ax.add_patch(circ)

# Three summation nodes (right side)
sigmas_y = [6.5, 4.5, 2.5]
sigmas_colors = ["#c0c0ff", "#c0c0ff", "#c0c0ff"]
sigmas_labels = [r"$\Sigma$", r"$\Sigma$", r"$\Sigma$"]

# Weight lines: red for neuron 1, blue for neuron 2, green for neuron m
# red lines to top sigma
for y in ys:
    ax.plot([1.25, 4.5], [y, sigmas_y[0]], color="#ff0000", lw=0.6, zorder=1)
# blue lines to middle sigma
for y in ys:
    ax.plot([1.25, 4.5], [y, sigmas_y[1]], color="#0000ff", lw=0.6, zorder=1)
# green lines to bottom sigma
for y in ys:
    ax.plot([1.25, 4.5], [y, sigmas_y[2]], color="#008000", lw=0.6, zorder=1)

# Vertical ellipsis between middle and bottom sigma
ax.text(4.5, 3.5, "...", ha="center", va="center", fontsize=14, color="#000000")

# Summation nodes
for i, (y, lab) in enumerate(zip(sigmas_y, sigmas_labels)):
    circ = Circle((4.5, y), 0.3, facecolor="#c0c0ff", edgecolor="#000000", lw=1.0, zorder=3)
    ax.add_patch(circ)
    ax.text(4.5, y, lab, ha="center", va="center", fontsize=14, color="#000000", zorder=4)

# Arrow from each sigma to activation box
for y in sigmas_y:
    ax.annotate("", xy=(6.0, y), xytext=(4.85, y),
                arrowprops=dict(arrowstyle="->", color="#ff0000", lw=1.2))

# Activation boxes (purple)
for y in sigmas_y:
    box = Rectangle((6.0, y-0.25), 1.2, 0.5, facecolor="#d0b0ff", edgecolor="#000000", lw=1.0, zorder=3)
    ax.add_patch(box)

# Outputs
outputs = [
    [">0 Class I", "<0 Not Class I"],
    [">0 Class II", "<0 Not Class II"],
    [">0 Class m", "<0 Not Class m"]
]
for i, (y, out_pair) in enumerate(zip(sigmas_y, outputs)):
    ax.text(7.4, y + 0.15, out_pair[0], ha="left", va="center", fontsize=9, color="#000000")
    ax.text(7.4, y - 0.15, out_pair[1], ha="left", va="center", fontsize=9, color="#000000")

# Vertical ellipsis between 2nd and last output
ax.text(8.0, 3.5, "...", ha="center", va="center", fontsize=14, color="#000000")

plt.tight_layout(pad=0.2)
fig.savefig("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_006_graph.png",
            transparent=False, facecolor="white")
print("saved slide_006_graph.png")