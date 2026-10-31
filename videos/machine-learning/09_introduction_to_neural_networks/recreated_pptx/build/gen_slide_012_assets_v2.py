#!/usr/bin/env python3
"""Regenerate slide 012 assets at exact measured original-frame geometry.

Original frame is 960x540 px where 1 px = 1 pt = 1/72 in, so every figure is
built in "frame-pixel" axes and placed at (geom_px / 72) inches -> 1:1, no
rescaling. All coordinates below were measured from
videos/.../unique_slides/slide_012.jpg with PIL/connected components.
"""
import os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle, Polygon

BUILD = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build"
SCRIPTS = "/home/codespace/ai_llm_slides/scripts"
sys.path.insert(0, SCRIPTS)

RED = "#F03A3A"          # axes / red arrows (measured bright red)
LBL_RED = "#C00000"      # plot annotation + axis labels
NAVY = "#1F1FA0"         # decision boundary
GREEN = "#3FE63F"        # class-1 points
CYAN = "#00DCDC"         # class-0 point
BLUE = "#2A2AC8"         # weights / step glyph
STEP_RED = "#D03030"
PANEL_PINK = "#E9A9A9"
STRIP_FILL = "#FFFCE0"
ACT_FILL = "#FAE1FE"     # measured step-box fill
ACT_EDGE = "#EEDAF1"     # measured step-box edge

def new_fig(w_pt, h_pt):
    """Figure whose data units are slide points (1 unit = 1 pt)."""
    fig = plt.figure(figsize=(w_pt / 72.0, h_pt / 72.0), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w_pt)
    ax.set_ylim(h_pt, 0)          # y grows downward = frame pixel rows
    ax.axis("off")
    return fig, ax

# ---------------------------------------------------------------- plot -------
# Panel: x 537..843, y 109..370  -> 307 x 262 pt
PW, PH = 307, 262
fig, ax = new_fig(PW, PH)
OX, OY = 537, 109           # frame origin of the panel
def f(x, y):               # frame px -> fig coords
    return x - OX, PH - (y - OY)

ax.add_patch(Rectangle((0, 0), PW, PH, facecolor="white",
                       edgecolor=PANEL_PINK, lw=1, zorder=1))

# origin of the Cartesian frame: (619, 330)
ox, oy = f(619, 330)
# vertical axis 619, from y=330 up to the arrowhead at y=125
ax.annotate("", xy=f(619, 125), xytext=(ox, oy),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.8,
                            shrinkA=0, shrinkB=0, mutation_scale=8), zorder=3)
# horizontal axis y=330, from origin right to the arrowhead at x=831
ax.annotate("", xy=f(831, 330), xytext=(ox, oy),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.8,
                            shrinkA=0, shrinkB=0, mutation_scale=8), zorder=3)

# decision boundary: measured (558,235) -> (683,364)
ax.plot(*zip(*[f(558, 235), f(683, 364)]), color=NAVY, lw=4,
        solid_capstyle="butt", zorder=4)

# data points: three green + one cyan, radius ~9 pt
for (px, py) in [(618, 258.5), (699.5, 259), (699.5, 327.5)]:
    ax.add_patch(Circle(f(px, py), 9, facecolor=GREEN,
                        edgecolor="white", lw=0.6, zorder=5))
ax.add_patch(Circle(f(618, 328), 9.5, facecolor=CYAN,
                    edgecolor="white", lw=0.6, zorder=5))

ax.text(*f(600 + 11, 124 + 10), r"$x_2$", fontsize=9, color=LBL_RED,
        style="italic", ha="center", va="center", zorder=6)
ax.text(*f(810 + 11, 327 + 12), r"$x_1$", fontsize=9, color=LBL_RED,
        style="italic", ha="center", va="center", zorder=6)
ax.text(*f(577 + 10, 289 + 6), "0.4", fontsize=9, color=LBL_RED, ha="center",
        va="center", fontweight="bold", zorder=6)
ax.text(*f(629 + 14, 344 + 5), "0.28", fontsize=9, color=LBL_RED, ha="center",
        va="center", fontweight="bold", zorder=6)

fig.savefig(f"{BUILD}/slide_012_decision_boundary.png", dpi=300, facecolor="white")
plt.close(fig)
print("wrote slide_012_decision_boundary.png")

# --------------------------------------------------------- perceptron -------
# Panel: x 141..515, y 352..492  -> 375 x 141 pt
CW, CH = 375, 141
fig2, ax2 = new_fig(CW, CH)
CX, CY = 141, 352
def p(x, y):
    return x - CX, CH - (y - CY)

# thin gray connectors from the inputs into the Sigma circle
IN_Y = [379, 418, 470]
for iy in IN_Y:
    ax2.plot(*zip(p(33, iy), p(158, 420.5)), color="#B8B8B8", lw=0.8, zorder=1)

# inputs + bias
ax2.text(*p(166, 379), r"$x_1$", fontsize=8, color="black",
         ha="left", va="center", zorder=6)
ax2.text(*p(166, 418), r"$x_2$", fontsize=8, color="black",
         ha="left", va="center", zorder=6)
ax2.text(*p(166, 466), "1", fontsize=8, color="#E02B38", fontweight="bold",
         ha="left", va="center", zorder=6)
# weights in blue, above the connector lines, nearer the inputs
ax2.text(*p(207, 372), "-7", fontsize=8, color=BLUE, ha="left",
         va="center", zorder=6)
ax2.text(*p(207, 429), "-5", fontsize=8, color=BLUE, ha="left",
         va="center", zorder=6)
ax2.text(*p(207, 472), "2", fontsize=8, color=BLUE, ha="left",
         va="center", zorder=6)

# Sigma node: fill bbox x 299..333, y 403..438
ax2.add_patch(Circle(p(316, 420.5), 17, facecolor="#ADD8E6",
                     edgecolor="#8FB8C8", lw=1.2, zorder=3))
ax2.text(*p(315, 420.5), r"$\Sigma$", fontsize=15, color="black",
         ha="center", va="center", zorder=6)

# small red triangle immediately left of the circle rim (x 292..298)
ax2.add_patch(Polygon([p(292, 417), p(292, 425), p(300, 421)],
                      closed=True, facecolor=RED, edgecolor="none", zorder=6))

# red arrow Sigma -> activation box
ax2.annotate("", xy=p(360, 420.5), xytext=p(334, 420.5),
             arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.4, shrinkA=0,
                             shrinkB=0, mutation_scale=8), zorder=6)

# activation box (measured x 360..399, y 405..436) with ONLY the step pictogram
bx, by = p(360, 405)
ax2.add_patch(Rectangle((bx, by), 39, 31, facecolor=ACT_FILL,
                        edgecolor=ACT_EDGE, lw=1.4, zorder=2))
# step pictogram (measured ink inside the box)
ax2.plot(*zip(p(239, 60 + 52), p(239, 78 + 52)), color=BLUE, lw=3,
         solid_capstyle="butt", zorder=5)                      # vertical jump
ax2.plot(*zip(p(242, 61 + 52), p(253, 61 + 52)), color=BLUE, lw=3,
         solid_capstyle="butt", zorder=5)                      # top horizontal
ax2.plot(*zip(p(226, 77 + 52), p(238, 77 + 52)), color=BLUE, lw=3,
         solid_capstyle="butt", zorder=5)                      # bottom horizontal
ax2.plot(*zip(p(227, 69 + 52), p(236, 69 + 52)), color=STEP_RED, lw=3,
         solid_capstyle="butt", zorder=5)
ax2.plot(*zip(p(243, 69 + 52), p(253, 69 + 52)), color=STEP_RED, lw=3,
         solid_capstyle="butt", zorder=5)

# rule legend on its pale strip, ABOVE the activation box (measured x 344..408,
# y 365..396)  ->  it ends 9 pt above the box top
sx, sy = p(344, 396)
ax2.add_patch(FancyBboxPatch((sx, sy), 64, 31,
                             boxstyle="round,pad=0,rounding_size=3",
                             facecolor=STRIP_FILL, edgecolor="#D8D8A0",
                             lw=0.8, zorder=1))
ax2.text(*p(235, 373), r">0 $\Rightarrow$ 1", fontsize=8, color="#00A000",
         ha="center", va="center", zorder=6)
ax2.text(*p(235, 386), r"$\leq$0 $\Rightarrow$ 0", fontsize=8,
         color="#E07B00", ha="center", va="center", zorder=6)

# red arrow activation box -> O/P, then the label
ax2.annotate("", xy=p(461, 420.5), xytext=p(402, 420.5),
             arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.4, shrinkA=0,
                             shrinkB=0, mutation_scale=8), zorder=6)
ax2.text(*p(473, 420.5), "O/P", fontsize=9, color="black",
         ha="left", va="center", zorder=6)

fig2.savefig(f"{BUILD}/slide_012_perceptron.png", dpi=300, transparent=True)
plt.close(fig2)
print("wrote slide_012_perceptron.png")

# ------------------------------------------------------------- equation -----
import render_eq
info = render_eq.render(r"d(X) = -7 x_1 - 5 x_2 + 2",
                        f"{BUILD}/eq_s012_dX.png", 29, "#000000")
print("eq:", info)
print("PLACE x=%.5f y=%.5f w=%.5f h=%.5f" % (
    8.04167 + (3.22222 - info["w_in"]) / 2,
    5.79167 + (0.65278 - info["h_in"]) / 2,
    info["w_in"], info["h_in"]))
