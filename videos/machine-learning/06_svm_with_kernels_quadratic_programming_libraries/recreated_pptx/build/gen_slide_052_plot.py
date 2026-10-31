#!/usr/bin/env python3
# Generate the slide_052 scatter plot exactly at the spec plot region size.
# Spec plot area [0.22, 0.12, 0.79, 0.84] -> 7.5981 x 5.4 in at 13.33x7.5 slide.
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
OUT = NS + "/recreated_pptx/build/slide_052_plot_rb4.png"

W_IN, H_IN = 7.5981, 5.4
DPI = 200

rng = np.random.default_rng(52)

fig = plt.figure(figsize=(W_IN, H_IN), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_facecolor("white")

ax.set_xlim(-3, 21)
ax.set_ylim(-5, 35)
ax.set_xticks([0, 5, 10, 15, 20])
ax.set_yticks(list(range(-5, 36, 5)))
ax.tick_params(labelbottom=False, labelleft=False, length=0)
for spine in ax.spines.values():
    spine.set_color("black")
    spine.set_linewidth(1.0)
ax.grid(True, color="#E0E0E0", linewidth=1.0)
ax.set_axisbelow(True)

# Blue dots: ~100 points forming a U-shape, #0000FF, x in [-2, 18], y in [14, 23]
bx = rng.uniform(-2, 18, 100)
by = 14 + 9 * ((bx - 8) / 10.0) ** 2 + rng.normal(0, 0.6, 100)
by = np.clip(by, 14, 23)
ax.scatter(bx, by, s=45, c="#0000FF", edgecolors="none", zorder=3)

# Red dots: ~50 points clustered above the U, #FF0000, x in [3, 11], y in [23, 28]
rx = np.clip(rng.normal(7, 1.8, 50), 3, 11)
ry = np.clip(rng.normal(25.5, 1.2, 50), 23, 28)
ax.scatter(rx, ry, s=45, c="#FF0000", edgecolors="none", zorder=3)

# Black vertical line at x=0, from y=10 to y=32
ax.plot([0, 0], [10, 32], color="#000000", linewidth=2.0, zorder=4)

fig.savefig(OUT, dpi=DPI, facecolor="white")
print("wrote", OUT)
from PIL import Image
im = Image.open(OUT)
print("size px:", im.size, "-> inches at 200dpi:", im.size[0] / 200, im.size[1] / 200)
