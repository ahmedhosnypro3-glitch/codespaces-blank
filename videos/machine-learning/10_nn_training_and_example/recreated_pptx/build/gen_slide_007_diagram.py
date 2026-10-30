#!/usr/bin/env python3
"""Generate the neural-network diagram for slide 7 (transparent PNG).

Canvas is authored in INCHES at the final embedded size (12.3 x 4.85 in), so
nothing is rescaled on placement. Subscripted labels use matplotlib mathtext
($\\mathrm{Net}_j$, $w_{ji}$, $O_i$ ...) so sub/superscripts stay properly
aligned instead of drifting as detached glyphs.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch
from matplotlib.path import Path
import matplotlib.patches as mpatches
import numpy as np

DPI = 600
W_IN, H_IN = 12.3, 4.85

plt.rcParams["mathtext.fontset"] = "dejavusans"

fig = plt.figure(figsize=(W_IN, H_IN), dpi=DPI)
fig.patch.set_alpha(0.0)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W_IN)
ax.set_ylim(0, H_IN)
ax.set_aspect("equal")
ax.axis("off")

def circ(x, y, r, fc, ec="black", lw=1.0, z=3):
    ax.add_patch(Circle((x, y), r, facecolor=fc, edgecolor=ec, lw=lw, zorder=z))

def txt(x, y, s, fs=11, c="black", bold=False, ha="center", va="center", z=5, rot=0):
    ax.text(x, y, s, fontsize=fs, color=c,
            fontweight="bold" if bold else "normal",
            ha=ha, va=va, zorder=z, rotation=rot)

def mtxt(x, y, s, fs=11, c="black", ha="center", va="center", z=5):
    """Mathtext label (properly aligned sub/superscripts)."""
    ax.text(x, y, s, fontsize=fs, color=c, ha=ha, va=va, zorder=z)

def fbox(x, y, w, h, fc="white", ec="black"):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, lw=1.0, zorder=3))

def curve_arrow(x0, y0, x1, y1, color="black", lw=1.0, rad=0.3):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                connectionstyle=f"arc3,rad={rad}",
                                shrinkA=0, shrinkB=0), zorder=2)

def straight_arrow(x0, y0, x1, y1, color="black", lw=1.0):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                shrinkA=0, shrinkB=0), zorder=2)

def dashed_line(x0, y0, x1, y1, color="gray", lw=0.8, dash=(4, 4)):
    ax.plot([x0, x1], [y0, y1], color=color, lw=lw, linestyle=(0, dash), zorder=1)

# ---- tan diagram panel background -------------------------------------------
ax.add_patch(Rectangle((0, 0), W_IN, H_IN, facecolor="#F5EDE6", edgecolor="none", zorder=0))

# ---- geometry (inches) -------------------------------------------------------
X1, X2, X3 = 2.1, 4.3, 7.0     # Σ columns
X_OUT = 8.80                   # output label boxes span 8.80..9.80
Y_ROWS = [3.40, 2.50, 1.60]
R = 0.22
SMALL_R = 0.045

INPUT_X, INPUT_Y = 0.70, 3.95
TARGET_X, TARGET_Y = 10.40, 4.05
ERR_X = 10.05                   # error bar 10.05..10.33
CLASS_X = 10.55                 # class boxes 10.50..11.35
CHAIN_Y = 4.55

# ---- Input Sample box (purple tint) -----------------------------------------
ax.add_patch(FancyBboxPatch((INPUT_X - 0.1, INPUT_Y - 0.14), 1.05, 0.30,
                            boxstyle="round,pad=0.02,rounding_size=0.03",
                            facecolor="#E080C0", edgecolor="#C0392B", lw=1.2, zorder=4))
txt(INPUT_X + 0.42, INPUT_Y + 0.01, "Input Sample", fs=10.5, c="black", bold=True)

# purple input dots
for y in Y_ROWS:
    circ(INPUT_X + 0.35, y, 0.05, "#8E44AD", ec="#8E44AD", lw=0.8)

# curved entry arrow into the Input Sample box from the left
curve_arrow(INPUT_X - 0.75, INPUT_Y + 0.22, INPUT_X - 0.1, INPUT_Y + 0.02,
            color="#8E44AD", lw=1.5, rad=0.3)

# arrow from the Input Sample box down into the network
straight_arrow(INPUT_X + 0.42, INPUT_Y - 0.14, INPUT_X + 0.42, Y_ROWS[0] + R + 0.10,
               color="#8E44AD", lw=1.5)

# ---- Node Bias (purple filled circle, white 4) ------------------------------
BIAS_X, BIAS_Y = INPUT_X + 0.18, 0.55
circ(BIAS_X, BIAS_Y, 0.11, "#8E44AD", ec="#8E44AD", lw=1.5)
txt(BIAS_X, BIAS_Y, "4", fs=11, c="white", bold=True)
txt(BIAS_X - 0.08, BIAS_Y - 0.28, "Node Bias", fs=8.5, c="#8E44AD", bold=True)

# dashed bias fan to the three input dots
for y in Y_ROWS:
    dashed_line(BIAS_X, BIAS_Y + 0.11, INPUT_X + 0.35, y, color="#8E44AD", lw=0.8, dash=(3, 3))

# ---- weight-annotation circles above column 2 -------------------------------
ARC_Y = 4.05
W_CIRCLE_X, O_CIRCLE_X = 3.90, 4.95
circ(W_CIRCLE_X, ARC_Y, 0.15, "#A8D0E6", ec="#2980B9", lw=1.5)
mtxt(W_CIRCLE_X, ARC_Y, r"$W_{ij}$", fs=9.5, c="#2980B9")
circ(O_CIRCLE_X, ARC_Y, 0.15, "#F1C40F", ec="#BF8F00", lw=1.5)
mtxt(O_CIRCLE_X, ARC_Y, r"$O_i$", fs=9.5, c="#BF8F00")

for y in Y_ROWS:
    curve_arrow(W_CIRCLE_X, ARC_Y - 0.15, X2, y + 0.10, color="#2980B9", lw=0.9, rad=0.30)
    curve_arrow(O_CIRCLE_X, ARC_Y - 0.15, X2, y + 0.10, color="#BF8F00", lw=0.9, rad=-0.20)

# ---- COLUMN 1: white Σ nodes, f[] activation boxes, o o o, O_i --------------
for y in Y_ROWS:
    circ(X1, y, R, "white", ec="black", lw=1.2)
    txt(X1, y, "Σ", fs=15, c="#C0392B", bold=True)
    fbox(X1 + 0.34, y - 0.18, 0.36, 0.36)
    txt(X1 + 0.52, y, "f", fs=13, c="black")
    for dx in [0.44, 0.57, 0.70]:
        circ(X1 + dx, y, SMALL_R, "white", ec="black", lw=0.8)
    mtxt(X1 + 0.79, y, r"$O_i$", fs=8.5, c="black", ha="left")
txt(X1, Y_ROWS[2] - 0.42, "⋮", fs=17, c="black")

# fan-in from the three input dots to every column-1 node
for y_in in Y_ROWS:
    for y_out in Y_ROWS:
        dashed_line(INPUT_X + 0.40, y_in, X1 - R, y_out, color="gray", lw=0.4, dash=(2, 4))

# ---- COLUMN 2: pale-blue Σ nodes, Net_j / O_j, f[], o o o, O_j --------------
PALE_BLUE = "#D6EAF8"
for y in Y_ROWS:
    circ(X2, y, R, PALE_BLUE, ec="black", lw=1.2)
    txt(X2, y, "Σ", fs=15, c="white", bold=True)
    mtxt(X2 + 0.27, y + 0.09, r"$\mathrm{Net}_j$", fs=8, c="#C0392B", ha="left")
    mtxt(X2 + 0.27, y - 0.13, r"$O_j$", fs=8, c="black", ha="left")
    fbox(X2 + 0.68, y - 0.18, 0.36, 0.36)
    txt(X2 + 0.86, y, "f", fs=13, c="black")
    for dx in [0.44, 0.57, 0.70]:
        circ(X2 + 0.68 + dx, y, SMALL_R, "white", ec="black", lw=0.8)
    mtxt(X2 + 1.17, y, r"$O_j$", fs=8.5, c="black", ha="left")
txt(X2, Y_ROWS[2] - 0.42, "⋮", fs=17, c="black")

# ---- COLUMN 3: pale-green Σ nodes -------------------------------------------
PALE_GREEN = "#D5F5E3"
for y in Y_ROWS:
    circ(X3, y, R, PALE_GREEN, ec="black", lw=1.2)
    txt(X3, y, "Σ", fs=15, c="white", bold=True)
    mtxt(X3 + 0.27, y + 0.09, r"$\mathrm{Net}_j$", fs=8, c="#C0392B", ha="left")
    mtxt(X3 + 0.27, y - 0.13, r"$O_j$", fs=8, c="black", ha="left")
    fbox(X3 + 0.68, y - 0.18, 0.36, 0.36)
    txt(X3 + 0.86, y, "f", fs=13, c="black")
    for dx in [0.44, 0.57, 0.70]:
        circ(X3 + 0.68 + dx, y, SMALL_R, "white", ec="black", lw=0.8)
    mtxt(X3 + 1.17, y, r"$O_j$", fs=8.5, c="black", ha="left")
txt(X3, Y_ROWS[2] - 0.42, "⋮", fs=17, c="black")

# ---- inter-column arrows + red transition dots + inline weight labels -------
for y in Y_ROWS:
    straight_arrow(X1 + R, y, X2 - R, y, color="black", lw=1.0)
    circ((X1 + X2) / 2, y, 0.03, "#C0392B", ec="#C0392B", lw=0)
    straight_arrow(X2 + R, y, X3 - R, y, color="black", lw=1.0)
    circ((X2 + X3) / 2, y, 0.03, "#C0392B", ec="#C0392B", lw=0)
    mtxt((X2 + X3) / 2 - 0.12, y + 0.12, r"$w_{ji}$", fs=7.5, c="#2980B9")
    mtxt((X2 + X3) / 2 - 0.08, y - 0.13, r"$O_j$", fs=7.5, c="black")

# ---- Output labels (boxed) ---------------------------------------------------
for y, lab in zip(Y_ROWS, ["Output 1", "Output 2", "Output m"]):
    ax.add_patch(FancyBboxPatch((X_OUT, y - 0.13), 1.0, 0.27,
                                boxstyle="round,pad=0.02,rounding_size=0.03",
                                facecolor="white", edgecolor="black", lw=1.0, zorder=3))
    txt(X_OUT + 0.50, y, lab, fs=10, ha="center", va="center")
    straight_arrow(X3 + R, y, X_OUT, y, color="black", lw=1.0)
    circ((X3 + X_OUT) / 2, y, 0.03, "#C0392B", ec="#C0392B", lw=0)

# ---- YELLOW CALLOUT CHAIN: W_ji -> Net_j -> O_j -> Output 1 ------------------
CHAIN_XS = [3.35, 4.55, 5.75, 6.95]
CHAIN_LABELS = [r"$w_{ji}$", r"$\mathrm{Net}_j$", r"$O_j$", r"$\mathrm{Out}_1$"]
for cx, lab in zip(CHAIN_XS, CHAIN_LABELS):
    circ(cx, CHAIN_Y, 0.17, "#F1C40F", ec="#BF8F00", lw=1.3)
    mtxt(cx, CHAIN_Y, lab, fs=8.5, c="black")
for x0, x1 in zip(CHAIN_XS[:-1], CHAIN_XS[1:]):
    dashed_line(x0 + 0.17, CHAIN_Y, x1 - 0.17, CHAIN_Y, color="#BF8F00", lw=1.1, dash=(4, 3))
    ax.annotate("", xy=(x1 - 0.17, CHAIN_Y), xytext=(x1 - 0.42, CHAIN_Y),
                arrowprops=dict(arrowstyle="-|>", color="#BF8F00", lw=1.1,
                                shrinkA=0, shrinkB=0), zorder=3)

# ---- Target Label box + curved exit arrow -----------------------------------
ax.add_patch(FancyBboxPatch((TARGET_X - 0.5, TARGET_Y - 0.14), 1.05, 0.30,
                            boxstyle="round,pad=0.02,rounding_size=0.03",
                            facecolor="#E080C0", edgecolor="#C0392B", lw=1.2, zorder=4))
txt(TARGET_X + 0.02, TARGET_Y + 0.01, "Target Label", fs=10, c="black", bold=True)
curve_arrow(TARGET_X + 0.25, TARGET_Y - 0.14, ERR_X + 0.14, 2.95,
            color="black", lw=2.0, rad=-0.5)

# ---- Error bar (vertical dark red, white text) ------------------------------
ax.add_patch(Rectangle((ERR_X, 0.45), 0.28, 3.20, facecolor="#C0392B",
                       edgecolor="#C0392B", lw=1.0, zorder=3))
txt(ERR_X + 0.14, 2.05, "Error\nError", fs=11, c="white", bold=True, rot=90)

# ---- Class boxes -------------------------------------------------------------
for i, lab in enumerate(["Class 1", "Class 2", "Class m"]):
    yb = 3.00 - i * 1.00
    ax.add_patch(FancyBboxPatch((CLASS_X - 0.05, yb - 0.15), 0.85, 0.30,
                                boxstyle="round,pad=0.02,rounding_size=0.03",
                                facecolor="#D5F5E3", edgecolor="black", lw=1.0, zorder=3))
    txt(CLASS_X + 0.38, yb, lab, fs=10, bold=True, ha="center", va="center")

# ---- circled "1" below the middle column ------------------------------------
circ(X2, 0.40, 0.14, "none", ec="#8E44AD", lw=1.5)
txt(X2, 0.40, "1", fs=10, c="#8E44AD", bold=True)
dashed_line(X2, 0.55, X2, Y_ROWS[2] - R - 0.08, color="#8E44AD", lw=1.0, dash=(4, 4))

fig.savefig("/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/recreated_pptx/build/slide_007_diagram.png",
            dpi=DPI, transparent=True)
print("wrote slide_007_diagram.png")
