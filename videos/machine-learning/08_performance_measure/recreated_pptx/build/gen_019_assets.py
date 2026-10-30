"""Generate line-art assets for slide 019: enemy/safe airplane drawings + step-function icon."""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, FancyBboxPatch

OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets"
os.makedirs(OUT, exist_ok=True)

GRAY = "#808080"
BLACK = "#000000"
PURPLE = "#800080"


def airplane(ax, skull=False):
    """Top-view aircraft line drawing: fuselage, wings, tailplane, engines."""
    # Fuselage (nose at left)
    ax.add_patch(Polygon(
        [(0.06, 0.50), (0.22, 0.42), (0.82, 0.42), (0.95, 0.47),
         (0.95, 0.53), (0.82, 0.58), (0.22, 0.58)],
        closed=True, fill=False, edgecolor=GRAY, linewidth=1.4))
    # Main wings (swept back)
    ax.add_patch(Polygon(
        [(0.42, 0.44), (0.62, 0.10), (0.72, 0.10), (0.66, 0.44)],
        closed=True, fill=False, edgecolor=GRAY, linewidth=1.4))
    ax.add_patch(Polygon(
        [(0.42, 0.56), (0.62, 0.90), (0.72, 0.90), (0.66, 0.56)],
        closed=True, fill=False, edgecolor=GRAY, linewidth=1.4))
    # Tailplane
    ax.add_patch(Polygon(
        [(0.86, 0.45), (0.94, 0.32), (0.98, 0.32), (0.95, 0.45)],
        closed=True, fill=False, edgecolor=GRAY, linewidth=1.2))
    ax.add_patch(Polygon(
        [(0.86, 0.55), (0.94, 0.68), (0.98, 0.68), (0.95, 0.55)],
        closed=True, fill=False, edgecolor=GRAY, linewidth=1.2))
    # Engine nacelles
    for cx in (0.52, 0.63):
        ax.add_patch(Polygon(
            [(cx, 0.38), (cx + 0.05, 0.38), (cx + 0.05, 0.44), (cx, 0.44)],
            closed=True, fill=False, edgecolor=GRAY, linewidth=1.0))
        ax.add_patch(Polygon(
            [(cx, 0.56), (cx + 0.05, 0.56), (cx + 0.05, 0.62), (cx, 0.62)],
            closed=True, fill=False, edgecolor=GRAY, linewidth=1.0))
    # Windows
    for i in range(7):
        ax.add_patch(Circle((0.30 + i * 0.075, 0.50), 0.018,
                            fill=False, edgecolor=BLACK, linewidth=0.7))
    if skull:
        # Skull-and-crossbones insignia on the forward fuselage
        ax.add_patch(Circle((0.26, 0.50), 0.055,
                            fill=False, edgecolor=BLACK, linewidth=1.1))
        ax.add_patch(Circle((0.245, 0.515), 0.011, facecolor=BLACK, edgecolor=BLACK))
        ax.add_patch(Circle((0.275, 0.515), 0.011, facecolor=BLACK, edgecolor=BLACK))
        ax.plot([0.16, 0.34], [0.44, 0.56], color=BLACK, linewidth=1.1)
        ax.plot([0.16, 0.34], [0.56, 0.44], color=BLACK, linewidth=1.1)
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.05, 0.95)
    ax.set_aspect("equal")
    ax.axis("off")


def save_airplane(path, skull):
    fig = plt.figure(figsize=(2.4, 1.1), dpi=600)
    ax = fig.add_axes([0, 0, 1, 1])
    airplane(ax, skull=skull)
    fig.savefig(path, dpi=600, transparent=True, bbox_inches="tight", pad_inches=0.01)
    plt.close(fig)


def save_step(path):
    """Bi-polar step function: -1 level, vertical transition at zero, +1 level."""
    fig = plt.figure(figsize=(1.6, 1.0), dpi=600)
    ax = fig.add_axes([0.10, 0.08, 0.86, 0.84])
    ax.plot([0.0, 0.5], [0.0, 0.0], color=PURPLE, linewidth=2.0)
    ax.plot([0.5, 0.5], [0.0, 1.0], color=PURPLE, linewidth=2.0)
    ax.plot([0.5, 1.0], [1.0, 1.0], color=PURPLE, linewidth=2.0)
    ax.axhline(0.0, color="#999999", linewidth=0.7, linestyle=(0, (4, 3)))
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.18, 1.18)
    ax.axis("off")
    fig.savefig(path, dpi=600, transparent=True, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)


def save_step_small(path):
    """Compact step glyph for the dark-red Model box."""
    fig = plt.figure(figsize=(0.9, 0.9), dpi=600)
    ax = fig.add_axes([0.08, 0.08, 0.84, 0.84])
    ax.plot([0.0, 0.45], [0.05, 0.05], color=PURPLE, linewidth=2.4)
    ax.plot([0.45, 0.45], [0.05, 0.95], color=PURPLE, linewidth=2.4)
    ax.plot([0.45, 0.95], [0.95, 0.95], color=PURPLE, linewidth=2.4)
    ax.set_xlim(-0.02, 1.0)
    ax.set_ylim(-0.05, 1.02)
    ax.axis("off")
    fig.savefig(path, dpi=600, transparent=True, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)


from PIL import Image

assets = []
for name, skull in (("eq_019_airplane_enemy", True), ("eq_019_airplane_safe", False)):
    p = os.path.join(OUT, name + ".png")
    save_airplane(p, skull)
    with Image.open(p) as im:
        w, h = im.size
    assets.append({"image": name + ".png", "w_px": w, "h_px": h,
                   "w_in": round(w / 600, 4), "h_in": round(h / 600, 4)})

for name, fn in (("eq_019_step_icon", save_step), ("eq_019_step_small", save_step_small)):
    p = os.path.join(OUT, name + ".png")
    fn(p)
    with Image.open(p) as im:
        w, h = im.size
    assets.append({"image": name + ".png", "w_px": w, "h_px": h,
                   "w_in": round(w / 600, 4), "h_in": round(h / 600, 4)})

with open(os.path.join(OUT, "eq_019_assets.json"), "w") as f:
    json.dump(assets, f, indent=2)
for a in assets:
    print(a)
