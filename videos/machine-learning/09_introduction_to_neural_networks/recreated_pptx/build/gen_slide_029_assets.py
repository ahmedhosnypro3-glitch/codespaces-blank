#!/usr/bin/env python3
"""Generate slide 029 overlay assets: rotated error-bar label and callout arrows."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

outdir = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build"
os.makedirs(outdir, exist_ok=True)

DPI = 600

# --- rotated "Error Error Error" label (bar interior 0.223 x 2.931 in) ---
W, H = 0.223, 2.931
fig = plt.figure(figsize=(W, H), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.axis("off")
ax.text(W / 2, H / 2, "Error Error Error", fontsize=9, color="white",
        ha="center", va="center", rotation=90, fontweight="bold")
fig.savefig(f"{outdir}/slide_029_errlabel.png", dpi=DPI, transparent=True)
plt.close(fig)

# --- hollow up-arrows for the layer callouts ---
for name, color in [("slide_029_arrow_blue.png", "#0070C0"),
                    ("slide_029_arrow_green.png", "#00B050")]:
    aw, ah = 0.18, 0.21
    fig = plt.figure(figsize=(aw, ah), dpi=DPI)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, aw)
    ax.set_ylim(0, ah)
    ax.axis("off")
    shaft_w = aw * 0.42
    head_y = ah * 0.55
    head_hw = aw * 0.5
    head_h = ah * 0.45
    shaft_x = (aw - shaft_w) / 2
    ax.add_patch(patches.Rectangle((shaft_x, 0), shaft_w, head_y,
                                   facecolor="none", edgecolor=color,
                                   linewidth=1.8))
    ax.add_patch(patches.Polygon(
        [(aw / 2, ah), (aw / 2 - head_hw, head_y), (aw / 2 + head_hw, head_y)],
        closed=True, facecolor="none", edgecolor=color, linewidth=1.8))
    fig.savefig(f"{outdir}/{name}", dpi=DPI, transparent=True)
    plt.close(fig)

print("generated errlabel + arrows")
