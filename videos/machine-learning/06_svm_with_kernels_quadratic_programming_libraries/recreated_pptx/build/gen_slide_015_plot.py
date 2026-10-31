#!/usr/bin/env python3
"""Slide 015 plot PNG — real matplotlib render of the spec's lower plot region.

Covers normalized region [0.10, 0.48, 0.87, 0.87] of the 960x540 frame
(x0,y0,x1,y1). Data coords are normalized frame coords with y pointing down.
Output: slide_015_graph.png (transparent bg, 300 dpi).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build/slide_015_graph.png"

X0, Y0, X1, Y1 = 0.10, 0.48, 0.87, 0.87
W_IN = (X1 - X0) * 13.33   # 10.2643 in on the slide
H_IN = (Y1 - Y0) * 7.5     # 2.925 in
DPI = 300

fig = plt.figure(figsize=(W_IN, H_IN), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(X0, X1)
ax.set_ylim(Y1, Y0)  # inverted: normalized y grows downward
ax.axis("off")
fig.patch.set_alpha(0.0)

# Orange non-linear (parabola) decision boundary, spec box
# [0.244,0.497,0.638,0.865], vertex near x=0.48, passing (0.244,0.497).
xs = np.linspace(0.244, 0.638, 300)
k = (0.865 - 0.497) / (0.48 - 0.244) ** 2
ys = 0.865 - k * (xs - 0.48) ** 2
ax.plot(xs, ys, color="#FF8C00", lw=2.5, solid_capstyle="round")

# Blue near-vertical linear decision boundary: (0.395,0.517) -> (0.375,0.915)
ax.plot([0.395, 0.375], [0.517, 0.915], color="#0000FF", lw=2.5,
        solid_capstyle="round")

# Red horizontal x-axis with right arrowhead, y ~ 0.793
ax.annotate("", xy=(0.852, 0.793), xytext=(0.111, 0.793),
            arrowprops=dict(arrowstyle="-|>", color="#FF0000", lw=1.2,
                            mutation_scale=18, shrinkA=0, shrinkB=0))

# Markers, y ~ 0.794, r ~ 6px of 960 -> diameter 0.1667 in = 12 pt -> s ~ 113
cyan_x = [0.298, 0.330, 0.364, 0.590, 0.629, 0.666]
red_x = [0.389, 0.420, 0.453, 0.498, 0.528, 0.559]
ax.scatter(cyan_x, [0.794] * len(cyan_x), s=113, c="#00FFFF",
           edgecolors="#00BFBF", linewidths=1.5, zorder=5)
ax.scatter(red_x, [0.794] * len(red_x), s=113, c="#FF0000",
           edgecolors="#CC0000", linewidths=1.5, zorder=5)

# Red italic serif "x" axis label, centre ~(0.8505, 0.829)
ax.text(0.8505, 0.829, "x", color="#FF0000", style="italic", fontsize=11,
        family="serif", ha="center", va="center")

fig.savefig(OUT, dpi=DPI, transparent=True)
plt.close(fig)

from PIL import Image
im = Image.open(OUT)
print("wrote", OUT, im.size, "expected px:", round(W_IN * DPI), round(H_IN * DPI))
