import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build"

# Spec slide_043: plot area [0.23, 0.14, 0.76, 0.82]; y labels left of it
# [0.20, 0.12, 0.23, 0.82]; x labels below [0.23, 0.82, 0.76, 0.87].
# Render one PNG covering [0.20, 0.12, 0.76, 0.87] so tick labels are real plot text.
W, H = 13.33, 7.5
X0, Y0, X1, Y1 = 0.20 * W, 0.12 * H, 0.76 * W, 0.87 * H
FIG_W, FIG_H = X1 - X0, Y1 - Y0
DPI = 200

PX0, PY0, PX1, PY1 = 0.23, 0.14, 0.76, 0.82  # plot area, normalized (y down)

def to_data(x, y):
    dx = (x - PX0) / (PX1 - PX0) * 40.0          # x data 0..40
    dy = 40.0 - (y - PY0) / (PY1 - PY0) * 50.0   # y data 40 (top) .. -10 (bottom)
    return dx, dy

clusters = [
    ([0.25, 0.28, 0.45, 0.48], "#0000FF"),
    ([0.28, 0.52, 0.34, 0.62], "#00FF00"),
    ([0.30, 0.42, 0.37, 0.52], "#FFFF00"),
    ([0.38, 0.50, 0.58, 0.72], "#FF00FF"),
    ([0.48, 0.30, 0.56, 0.42], "#FF0000"),
    ([0.61, 0.25, 0.70, 0.48], "#00FFFF"),
    ([0.61, 0.50, 0.70, 0.68], "#000000"),
]

rng = np.random.default_rng(43)
fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
fig.patch.set_facecolor("white")
# axes rect within figure: leave left margin for y labels, bottom for x labels
ax = fig.add_axes([0.075, 0.09, 0.90, 0.885])
ax.set_facecolor("white")
ax.set_xlim(0, 40)
ax.set_ylim(-10, 40)
ax.set_xticks([0, 10, 20, 30, 40])
ax.set_yticks([40, 30, 20, 10, 0, -10])
ax.tick_params(colors="#000000", labelsize=9, length=3, width=0.8)
for lbl in list(ax.get_xticklabels()) + list(ax.get_yticklabels()):
    lbl.set_color("#000000")
for sp in ax.spines.values():
    sp.set_color("#808080")
    sp.set_linewidth(1.0)
ax.grid(True, linestyle=":", color="#C0C0C0", linewidth=0.8)
ax.set_axisbelow(True)

for (box, color) in clusters:
    x0, y0 = to_data(box[0], box[3])  # bottom-left in data coords
    x1, y1 = to_data(box[2], box[1])  # top-right
    n = 20
    xs = rng.uniform(min(x0, x1), max(x0, x1), n)
    ys = rng.uniform(min(y0, y1), max(y0, y1), n)
    ax.scatter(xs, ys, s=150, c=color, marker="o", edgecolors="none", linewidths=0, zorder=3)

out = BASE + "/slide_043_graph.png"
fig.savefig(out, dpi=DPI, facecolor="white", pad_inches=0)
plt.close(fig)
from PIL import Image
im = Image.open(out)
print("wrote", out, im.size, "px ->", im.size[0] / DPI, "x", im.size[1] / DPI, "in")
