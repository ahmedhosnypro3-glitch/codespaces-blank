#!/usr/bin/env python3
"""Generate the single-perceptron architecture diagram for slide_005.
Native pptxgenjs shapes/lines cannot fan-in cleanly; matplotlib draws the
measured colors/orientation exactly as the original slide shows."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

W, H = 6.0, 3.0  # inches (matches measured diagram region aspect)
fig, ax = plt.subplots(figsize=(W, H), dpi=200)
ax.set_xlim(0, 10); ax.set_ylim(0, 5)
ax.axis("off")

inputs = ["$x_1$", "$x_2$", "$x_3$", "...", "$x_n$", "$1$"]
weights = ["$w_1$", "$w_2$", "$w_3$", "...", "$w_n$", "$b$"]
ys = [4.5, 3.7, 2.9, 2.1, 1.3, 0.5]

# input labels (left) and weight labels
for y, lab in zip(ys, inputs):
    color = "#ff0000" if lab == "$1$" else "#000000"
    ax.text(0.8, y, lab, ha="center", va="center", fontsize=11, color=color, style="italic")
for y, lab in zip(ys, weights):
    color = "#ff0000" if lab == "$b$" else "#000000"
    ax.text(3.0, y, lab, ha="center", va="center", fontsize=11, color=color, style="italic")

# fan-in lines from weight column into the summation node
for y in ys:
    ax.plot([3.4, 4.9], [y, 2.5], color="#888888", lw=0.8, zorder=1)

# summation node
sigma = Circle((5.3, 2.5), 0.42, facecolor="#add8e6", edgecolor="#000000", lw=1.2, zorder=3)
ax.add_patch(sigma)
ax.text(5.3, 2.5, r"$\Sigma$", ha="center", va="center", fontsize=16, color="#000000", zorder=4)

# arrow Sigma -> step-function box
ax.annotate("", xy=(6.6, 2.5), xytext=(5.75, 2.5),
            arrowprops=dict(arrowstyle="->", color="#000000", lw=1.4))

# step-function (activation) box
step = Rectangle((6.6, 1.9), 1.1, 1.2, facecolor="#ffb6c1", edgecolor="#000000", lw=1.0, zorder=3)
ax.add_patch(step)
# Heaviside staircase inside the box
ax.plot([6.75, 7.05], [2.05, 2.05], color="#000000", lw=1.6, zorder=4)
ax.plot([7.05, 7.05], [2.05, 2.95], color="#000000", lw=1.6, zorder=4)
ax.plot([7.05, 7.55], [2.95, 2.95], color="#000000", lw=1.6, zorder=4)

# arrow box -> O/P
ax.annotate("", xy=(8.6, 2.5), xytext=(7.75, 2.5),
            arrowprops=dict(arrowstyle="->", color="#000000", lw=1.4))
ax.text(8.75, 2.5, "O/P", ha="left", va="center", fontsize=11, color="#000000")

plt.tight_layout(pad=0.2)
fig.savefig("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_005_graph.png",
            transparent=False, facecolor="white")
print("saved slide_005_graph.png")