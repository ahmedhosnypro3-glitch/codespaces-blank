"""Slide 019 assets v2 — side-view propeller aircraft line art + activation step plot.

The original frames show hand-drawn SIDE-VIEW propeller planes (nose with propeller,
cockpit window, swept wing, tailplane + vertical fin), enemy ones carrying a small
target marking on the fuselage. Judge attempt 6 flagged the v1 top-view jet icons as a
MAJOR imagery mismatch, so the drawings are redrawn in side view with per-row pitch.
"""
import json
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Polygon, Rectangle

OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets"
os.makedirs(OUT, exist_ok=True)

GRAY = "#7A7A7A"
BLACK = "#000000"
PINK = "#F7A8C4"
MAROON = "#8B1030"


def rotate(pts, deg, cx=0.5, cy=0.5):
    r = math.radians(deg)
    c, s = math.cos(r), math.sin(r)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def plane(ax, pitch=0.0, enemy=False, style="prop"):
    """Side-view propeller aircraft, nose at left, rotated by `pitch` degrees."""
    def P(pts):
        return rotate(pts, pitch)

    # Fuselage: nose -> tail, tapering
    ax.add_patch(Polygon(P([
        (0.07, 0.50), (0.13, 0.44), (0.55, 0.44), (0.80, 0.455), (0.94, 0.48),
        (0.96, 0.52), (0.94, 0.545), (0.80, 0.565), (0.55, 0.575), (0.13, 0.575),
        (0.07, 0.53),
    ]), closed=True, fill=False, edgecolor=GRAY, linewidth=1.3))
    # Cockpit window
    ax.add_patch(Ellipse(rotate([(0.235, 0.485)], pitch)[0], 0.055, 0.045,
                         fill=False, edgecolor=BLACK, linewidth=0.8))
    # Side windows
    for i in range(4):
        x = 0.31 + i * 0.065
        ax.add_patch(Circle(rotate([(x, 0.493)], pitch)[0], 0.016,
                            fill=False, edgecolor=BLACK, linewidth=0.6))
    # Near wing sweeping down-back (side view)
    ax.add_patch(Polygon(P([
        (0.36, 0.575), (0.50, 0.80), (0.60, 0.80), (0.52, 0.575),
    ]), closed=True, fill=False, edgecolor=GRAY, linewidth=1.2))
    # Far wing tip peeking above
    ax.add_patch(Polygon(P([
        (0.40, 0.44), (0.50, 0.30), (0.58, 0.30), (0.54, 0.44),
    ]), closed=True, fill=False, edgecolor=GRAY, linewidth=1.0))
    # Tailplane
    ax.add_patch(Polygon(P([
        (0.78, 0.565), (0.90, 0.66), (0.97, 0.66), (0.92, 0.565),
    ]), closed=True, fill=False, edgecolor=GRAY, linewidth=1.1))
    # Vertical fin
    ax.add_patch(Polygon(P([
        (0.82, 0.50), (0.90, 0.28), (0.97, 0.28), (0.95, 0.50),
    ]), closed=True, fill=False, edgecolor=GRAY, linewidth=1.1))
    # Propeller: spinner + two blades
    ax.add_patch(Circle(rotate([(0.065, 0.515)], pitch)[0], 0.022,
                        facecolor=GRAY, edgecolor=GRAY))
    ax.plot(*zip(*P([(0.062, 0.30), (0.062, 0.73)])), color=GRAY, linewidth=1.4)
    # Engine nacelle hint under fuselage
    ax.add_patch(Rectangle(rotate([(0.42, 0.575)], pitch)[0], 0.10, 0.035,
                           fill=False, edgecolor=GRAY, linewidth=0.8, angle=pitch))
    if enemy:
        # Target marking on the fuselage
        ax.add_patch(Circle(rotate([(0.30, 0.535)], pitch)[0], 0.030,
                            fill=False, edgecolor=MAROON, linewidth=1.0))
        ax.add_patch(Circle(rotate([(0.30, 0.535)], pitch)[0], 0.014,
                            facecolor=MAROON, edgecolor=MAROON))


def save_plane(path, pitch, enemy):
    fig = plt.figure(figsize=(2.2, 1.2), dpi=600)
    ax = fig.add_axes([0, 0, 1, 1])
    plane(ax, pitch, enemy)
    ax.set_xlim(0.0, 1.02)
    ax.set_ylim(0.20, 0.88)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.savefig(path, dpi=600, transparent=True, bbox_inches="tight", pad_inches=0.01)
    plt.close(fig)


def save_step_plot(path, small=False):
    """Bipolar step function inside a small axis box (px/600 asset)."""
    w, h = (1.1, 0.85) if small else (1.5, 1.0)
    fig = plt.figure(figsize=(w, h), dpi=600)
    ax = fig.add_axes([0.16, 0.14, 0.76, 0.78])
    ax.plot([0.0, 0.5], [0.0, 0.0], color=MAROON, linewidth=1.8)
    ax.plot([0.5, 0.5], [0.0, 1.0], color=MAROON, linewidth=1.8)
    ax.plot([0.5, 1.0], [1.0, 1.0], color=MAROON, linewidth=1.8)
    # axes frame
    for s in ("top", "bottom", "left", "right"):
        ax.spines[s].set_visible(True)
        ax.spines[s].set_color(GRAY)
        ax.spines[s].set_linewidth(0.6)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.10, 1.10)
    fig.savefig(path, dpi=600, transparent=True, bbox_inches="tight", pad_inches=0.01)
    plt.close(fig)


from PIL import Image

assets = []
for name, pitch, enemy in [
    ("eq_019_plane_enemy_a", -7, True),
    ("eq_019_plane_enemy_b", 0, True),
    ("eq_019_plane_enemy_c", 5, True),
    ("eq_019_plane_safe_a", -6, False),
    ("eq_019_plane_safe_b", 0, False),
    ("eq_019_plane_safe_c", 4, False),
]:
    p = os.path.join(OUT, name + ".png")
    save_plane(p, pitch, enemy)
    with Image.open(p) as im:
        assets.append({"image": name + ".png", "w_px": im.size[0], "h_px": im.size[1],
                       "w_in": round(im.size[0] / 600, 4), "h_in": round(im.size[1] / 600, 4)})

for name, small in (("eq_019_step_plot", False), ("eq_019_step_plot_small", True)):
    p = os.path.join(OUT, name + ".png")
    save_step_plot(p, small)
    with Image.open(p) as im:
        assets.append({"image": name + ".png", "w_px": im.size[0], "h_px": im.size[1],
                       "w_in": round(im.size[0] / 600, 4), "h_in": round(im.size[1] / 600, 4)})

with open(os.path.join(OUT, "eq_019_assets_v2.json"), "w") as f:
    json.dump(assets, f, indent=2)
for a in assets:
    print(a)

# preview contact strip for the zoom check
prev = Image.new("RGB", (1400, 400), "white")
x = 0
for nm in ("eq_019_plane_enemy_a", "eq_019_plane_enemy_b", "eq_019_plane_safe_b", "eq_019_step_plot"):
    im = Image.open(os.path.join(OUT, nm + ".png")).convert("RGBA")
    bg = Image.new("RGB", im.size, "white")
    bg.paste(im, mask=im.split()[3])
    s = 300 / bg.height
    bg = bg.resize((int(bg.width * s), 300), Image.LANCZOS)
    prev.paste(bg, (x, 40))
    x += bg.width + 30
prev.save("/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/qa/slide019/crops/assets_v2_preview.png")
print("preview written")
