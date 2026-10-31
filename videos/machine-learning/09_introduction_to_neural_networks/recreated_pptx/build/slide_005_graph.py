#!/usr/bin/env python3
"""Generate the single-perceptron schematic for slide 005.

The canvas is mapped 1:1 to the original lecture frame pixels so every element
lands on its measured position.  Colours are taken from the original frame:
inputs black (bias "1" red), weights blue, sum circle pale cyan, step box pale
pink with a blue staircase, arrows red, O/P black.
"""
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["mathtext.fontset"] = "stix"
matplotlib.rcParams["font.family"] = "STIXGeneral"
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
from matplotlib.lines import Line2D

OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_005_graph.png"

# measured panel bounds in original-frame pixels (y grows downward)
X0, X1, Y_TOP, Y_BOT = 227, 614, 349, 508
W_IN = (X1 - X0) / 72.0
H_IN = (Y_BOT - Y_TOP) / 72.0
DPI = 600

BLACK = "#000000"
BLUE = "#0000C0"
RED = "#C00000"
FAN = "#D9D2D2"
CIRCLE_FILL = "#E0FCF9"
BOX_FILL = "#FBE5FA"
BOX_EDGE = "#B48CB4"
STEP_BLUE = "#241478"
MAUVE = "#C089C0"

fig = plt.figure(figsize=(W_IN, H_IN), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(X0, X1)
ax.set_ylim(Y_BOT, Y_TOP)
ax.set_aspect("equal")
ax.axis("off")
fig.patch.set_facecolor("white")

IN_X, WT_X = 257, 296

inputs = [("x_1", 361), ("x_2", 384), ("x_3", 406),
          (r"\ldots", 430), (r"\ldots", 452), ("x_n", 474)]
weights = [("w_1", 362), ("w_2", 381), ("w_3", 402), ("w_n", 453), ("b", 493)]

SIG_CX, SIG_CY, SIG_R = 425, 421, 18

for _, y in inputs + weights:
    ax.add_line(Line2D([IN_X + 14, SIG_CX - SIG_R], [y, SIG_CY],
                       color=FAN, linewidth=0.6, zorder=1))
for _, y in weights:
    ax.add_line(Line2D([WT_X + 12, SIG_CX - SIG_R], [y, SIG_CY],
                       color=FAN, linewidth=0.6, zorder=1))

for label, y in inputs:
    ax.text(IN_X, y, f"${label}$", ha="center", va="center",
            fontsize=14, color=BLACK, zorder=4)
ax.text(IN_X, 494, "1", ha="center", va="center", fontsize=14,
        color=RED, zorder=4)

for label, y in weights:
    ax.text(WT_X, y, f"${label}$", ha="center", va="center",
            fontsize=14, color=BLUE, zorder=4)

ax.add_patch(Circle((SIG_CX, SIG_CY), SIG_R, facecolor=CIRCLE_FILL,
                    edgecolor=BLACK, linewidth=0.8, zorder=3))
ax.text(SIG_CX, SIG_CY, r"$\Sigma$", ha="center", va="center",
        fontsize=25, color=BLACK, zorder=4)

BOX_L, BOX_R, BOX_T, BOX_B = 461, 513, 406, 439
ax.add_patch(Rectangle((BOX_L, BOX_B), BOX_R - BOX_L, BOX_T - BOX_B,
                       facecolor=BOX_FILL, edgecolor=BOX_EDGE, linewidth=0.8, zorder=3))
# staircase glyph, measured in the original frame
ax.add_line(Line2D([476, 486], [429, 429], color=STEP_BLUE, linewidth=1.3, zorder=4))
ax.add_line(Line2D([486, 486], [429, 413], color=STEP_BLUE, linewidth=1.3, zorder=4))
ax.add_line(Line2D([486, 504], [413, 413], color=STEP_BLUE, linewidth=1.3, zorder=4))
ax.add_line(Line2D([488, 488], [408, 437], color=MAUVE, linewidth=0.8, zorder=4))

# red arrows: fan-in head, sum -> box, box -> O/P
ax.annotate("", xy=(SIG_CX - SIG_R + 1, SIG_CY), xytext=(396, SIG_CY),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.0,
                            mutation_scale=11), zorder=5)
ax.annotate("", xy=(BOX_L, 420), xytext=(SIG_CX + SIG_R, 420),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.2,
                            mutation_scale=10), zorder=5)
ax.annotate("", xy=(577, 420), xytext=(BOX_R, 420),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.2,
                            mutation_scale=10), zorder=5)
ax.text(593, 420, "O/P", ha="center", va="center", fontsize=13,
        color=BLACK, family="DejaVu Sans", weight="bold", zorder=5)

fig.savefig(OUT, dpi=DPI, facecolor="white")
plt.close(fig)
print(f"saved {OUT}  ({int(W_IN * DPI)}x{int(H_IN * DPI)} px)")
