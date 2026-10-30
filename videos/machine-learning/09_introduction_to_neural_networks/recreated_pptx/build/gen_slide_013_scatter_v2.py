#!/usr/bin/env python3
"""Slide 013 XOR scatter plot.

Geometry/colors follow analysis/reanalysis_v2/slide_013_reanalysis.txt (fresh
visual re-analysis of unique_slides/slide_013.jpg), section 5a.

The PNG is rendered in ORIGINAL-FRAME PIXEL COORDINATES (960x540 frame) so every
feature lands at the measured original position; the build embeds it at the
mapped panel size.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = ("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/"
       "recreated_pptx/build/slide_013_scatter_v2.png")

# Original-frame panel bbox (px) and the slide-space size it maps to.
PANEL_X0, PANEL_X1 = 510, 800
PANEL_Y0, PANEL_Y1 = 107, 355
W_IN = 4.723
H_IN = 3.986

RED = "#C00000"
NAVY = "#1414B4"
X_RED = "#FF0000"
GREEN = "#66CC00"
CYAN = "#00CED1"

fig = plt.figure(figsize=(W_IN, H_IN), dpi=300)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(PANEL_X0, PANEL_X1)
ax.set_ylim(PANEL_Y1, PANEL_Y0)   # inverted: image coords, y grows downward
ax.set_aspect("auto")
ax.axis("off")
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

# --- axes (red, with arrowheads) --------------------------------------------
ax.annotate("", xy=(785, 317), xytext=(585, 317),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.9, mutation_scale=13))
ax.annotate("", xy=(585, 122), xytext=(585, 317),
            arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.9, mutation_scale=13))

# small unlabeled ticks
for tx in (630, 690):
    ax.plot([tx, tx], [317, 310], color=RED, lw=1.1, solid_capstyle="butt")
ax.plot([578, 585], [310, 310], color=RED, lw=1.1, solid_capstyle="butt")

# --- two parallel decision lines (navy) -------------------------------------
ax.plot([570, 708], [185, 330], color=NAVY, lw=3.2, solid_capstyle="round", zorder=2)
ax.plot([528, 648], [222, 355], color=NAVY, lw=3.2, solid_capstyle="round", zorder=2)

# --- data marks --------------------------------------------------------------
ax.plot([555 - 10, 555 + 10], [178 - 10, 178 + 10], color=X_RED, lw=3.0, zorder=3)
ax.plot([555 - 10, 555 + 10], [178 + 10, 178 - 10], color=X_RED, lw=3.0, zorder=3)
ax.plot([522 - 10, 522 + 10], [212 - 10, 212 + 10], color=X_RED, lw=3.0, zorder=3)
ax.plot([522 - 10, 522 + 10], [212 + 10, 212 - 10], color=X_RED, lw=3.0, zorder=3)

for cx, cy, col in ((585, 250, GREEN), (663, 319, GREEN), (663, 251, CYAN), (585, 319, CYAN)):
    ax.plot([cx], [cy], marker="o", ms=20.4, mfc=col, mec="white", mew=1.2, zorder=4)

fig.savefig(OUT, dpi=300, facecolor="white")
plt.close(fig)
print("wrote", OUT)
