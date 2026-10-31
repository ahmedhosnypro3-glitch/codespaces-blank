#!/usr/bin/env python3
"""Decision-boundary plot for slide_011 of 09_introduction_to_neural_networks.

Reproduces the original frame's upper-right plot: red L-axes (x1 right, x2 up),
the boundary 5*x1 + 3*x2 = 6 (= d(X) = -5x1 - 3x2 + 6 = 0), the four AND truth-table
points, and the intercept labels "2" / "1.2".
Geometry is mapped from the original frame's pixel measurements.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Card measured on the original frame: white area x 539..839, y 111..367 (300 x 256 px).
# 1 original px = 13.03in/844 = 0.0154378 in horizontally, 7.2in/472 = 0.0152542 in vertically.
CARD_W_IN = CARD_W_IN_OUT = 4.631
CARD_H_IN = 3.904
PX_PER_IN = 300.0 / CARD_W_IN_OUT          # 64.79 original px per inch
UNIT_X1_PX = 81.0                          # px per x1 unit (origin px 618 -> x1=0, px 699 -> x1=1)
UNIT_X2_PX = 66.5                          # px per x2 unit (origin px 329 -> x2=0, intercept px 196 -> x2=2)

ORIGIN_X_PX = 618 - 539                    # card-local
ORIGIN_Y_PX = 329 - 111

RED = "#990000"
NAVY = "#000080"
CYAN = "#00FFFF"
GREEN = "#93F63A"

fig = plt.figure(figsize=(CARD_W_IN, CARD_H_IN), dpi=600)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_facecolor("white")

xlim = (-ORIGIN_X_PX / UNIT_X1_PX, (300 - ORIGIN_X_PX) / UNIT_X1_PX)
ylim = ((ORIGIN_Y_PX - 256) / UNIT_X2_PX, ORIGIN_Y_PX / UNIT_X2_PX)
ax.set_xlim(*xlim)
ax.set_ylim(*ylim)
ax.axis("off")

def px2x(px):
    return (px - ORIGIN_X_PX) / UNIT_X1_PX

def px2y(py):
    return (ORIGIN_Y_PX - py) / UNIT_X2_PX

arrow = dict(arrowstyle="-|>", mutation_scale=18, color=RED, lw=2.2,
             shrinkA=0, shrinkB=0, capstyle="butt")
ax.annotate("", xy=(2.63, 0), xytext=(0, 0), arrowprops=arrow)
ax.annotate("", xy=(0, 3.05), xytext=(0, 0), arrowprops=arrow)

# decision boundary: 5*x1 + 3*x2 = 6
xs = [-0.25, 1.40]
ax.plot(xs, [(6 - 5 * x) / 3 for x in xs], color=NAVY, lw=3.6, solid_capstyle="butt")

for x1, x2, col in [(0, 0, CYAN), (0, 1, CYAN), (1, 0, CYAN), (1, 1, GREEN)]:
    ax.plot([x1], [x2], "o", ms=22, mfc=col, mec="none")

lab = dict(color=RED, fontsize=13, family="DejaVu Sans")
ax.text(-0.10, 3.00, "$x_2$", ha="right", va="center", **lab)
ax.text(2.52, -0.29, "$x_1$", ha="center", va="center", **lab)
ax.text(-0.13, 2.00, "2", ha="right", va="center", fontsize=13, color=RED)
ax.text(1.24, -0.36, "1.2", ha="center", va="center", fontsize=13, color=RED)

out = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/plot_s011.png"
fig.savefig(out, dpi=600, facecolor="white")
print("wrote", out)
