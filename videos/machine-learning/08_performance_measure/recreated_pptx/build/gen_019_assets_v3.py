"""Slide 019 assets v3 — DISTINCT aircraft per row (judge attempt 8 MAJOR: repeated
identical clip-art). Original shows a mix of sleek jet (no propeller) and propeller
planes with different fuselage markings (target ring, X crosshair, skull), varied
pitch/scale. Enemy rows get markings; safe rows plain. 5 enemy + 6 safe variants."""
import json
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, Polygon

OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets"
os.makedirs(OUT, exist_ok=True)

GRAY = "#7A7A7A"
BLACK = "#000000"
MAROON = "#8B1030"


def rotate(pts, deg, cx=0.5, cy=0.5):
    r = math.radians(deg)
    c, s = math.cos(r), math.sin(r)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def base_fuselage(ax, P, jet=False):
    if jet:
        ax.add_patch(Polygon(P([
            (0.05, 0.50), (0.20, 0.455), (0.60, 0.45), (0.88, 0.47), (0.97, 0.50),
            (0.88, 0.53), (0.60, 0.55), (0.20, 0.545), (0.05, 0.52),
        ]), closed=True, fill=False, edgecolor=GRAY, linewidth=1.3))
    else:
        ax.add_patch(Polygon(P([
            (0.07, 0.50), (0.13, 0.44), (0.55, 0.44), (0.80, 0.455), (0.94, 0.48),
            (0.96, 0.52), (0.94, 0.545), (0.80, 0.565), (0.55, 0.575), (0.13, 0.575),
            (0.07, 0.53),
        ]), closed=True, fill=False, edgecolor=GRAY, linewidth=1.3))


def plane(ax, pitch=0.0, jet=False, marking=None, scale=1.0):
    """Side-view aircraft. marking: None | 'ring' | 'x' | 'skull'."""
    def P(pts):
        return rotate(pts, pitch)

    base_fuselage(ax, P, jet)
    # cockpit + windows
    ax.add_patch(Ellipse(rotate([(0.235, 0.485)], pitch)[0], 0.055 * scale, 0.045 * scale,
                         fill=False, edgecolor=BLACK, linewidth=0.8))
    for i in range(4):
        x = 0.31 + i * 0.065
        ax.add_patch(Circle(rotate([(x, 0.493)], pitch)[0], 0.016 * scale,
                            fill=False, edgecolor=BLACK, linewidth=0.6))
    # wings
    ax.add_patch(Polygon(P([(0.36, 0.575), (0.50, 0.80), (0.60, 0.80), (0.52, 0.575)]),
                         closed=True, fill=False, edgecolor=GRAY, linewidth=1.2))
    ax.add_patch(Polygon(P([(0.40, 0.44), (0.50, 0.30), (0.58, 0.30), (0.54, 0.44)]),
                         closed=True, fill=False, edgecolor=GRAY, linewidth=1.0))
    # tail
    ax.add_patch(Polygon(P([(0.78, 0.565), (0.90, 0.66), (0.97, 0.66), (0.92, 0.565)]),
                         closed=True, fill=False, edgecolor=GRAY, linewidth=1.1))
    ax.add_patch(Polygon(P([(0.82, 0.50), (0.90, 0.28), (0.97, 0.28), (0.95, 0.50)]),
                         closed=True, fill=False, edgecolor=GRAY, linewidth=1.1))
    if jet:
        # swept wing only, no propeller
        ax.add_patch(Polygon(P([(0.45, 0.575), (0.62, 0.86), (0.70, 0.86), (0.56, 0.575)]),
                             closed=True, fill=False, edgecolor=GRAY, linewidth=1.2))
    else:
        # propeller
        ax.add_patch(Circle(rotate([(0.065, 0.515)], pitch)[0], 0.022,
                            facecolor=GRAY, edgecolor=GRAY))
        ax.plot(*zip(*P([(0.062, 0.30), (0.062, 0.73)])), color=GRAY, linewidth=1.4)
    if marking == "ring":
        c = rotate([(0.32, 0.535)], pitch)[0]
        ax.add_patch(Circle(c, 0.032, fill=False, edgecolor=MAROON, linewidth=1.1))
        ax.add_patch(Circle(c, 0.012, facecolor=MAROON, edgecolor=MAROON))
    elif marking == "x":
        c = rotate([(0.32, 0.535)], pitch)[0]
        ax.plot([c[0] - 0.028, c[0] + 0.028], [c[1] - 0.028, c[1] + 0.028],
                color=MAROON, linewidth=1.4)
        ax.plot([c[0] - 0.028, c[0] + 0.028], [c[1] + 0.028, c[1] - 0.028],
                color=MAROON, linewidth=1.4)
    elif marking == "skull":
        c = rotate([(0.32, 0.535)], pitch)[0]
        ax.add_patch(Circle(c, 0.024, fill=False, edgecolor=BLACK, linewidth=1.2))
        ax.plot([c[0] - 0.014, c[0] + 0.014], [c[1] + 0.030, c[1] + 0.030], color=BLACK, linewidth=1.4)
        ax.plot([c[0] - 0.020, c[0] + 0.020], [c[1] + 0.038, c[1] + 0.038], color=BLACK, linewidth=1.2)


def save_plane(path, pitch, jet, marking, scale=1.0):
    fig = plt.figure(figsize=(2.2, 1.2), dpi=600)
    ax = fig.add_axes([0, 0, 1, 1])
    plane(ax, pitch, jet, marking, scale)
    ax.set_xlim(0.0, 1.02)
    ax.set_ylim(0.20, 0.88)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.savefig(path, dpi=600, transparent=True, bbox_inches="tight", pad_inches=0.01)
    plt.close(fig)


from PIL import Image

specs = [
    # 5 enemy: jet+ring, prop+x, prop+skull, prop+ring, jet+skull — varied pitch/scale
    ("p019_enemy_1", -7, True, "ring", 1.00),
    ("p019_enemy_2", 3, False, "x", 0.95),
    ("p019_enemy_3", -2, False, "skull", 1.00),
    ("p019_enemy_4", 6, False, "ring", 0.90),
    ("p019_enemy_5", 0, True, "skull", 0.95),
    # 6 safe: jet + props, no markings, varied pitch/scale
    ("p019_safe_1", -6, True, None, 0.95),
    ("p019_safe_2", 2, False, None, 1.00),
    ("p019_safe_3", -3, False, None, 0.90),
    ("p019_safe_4", 5, True, None, 0.90),
    ("p019_safe_5", 0, False, None, 1.00),
    ("p019_safe_6", -5, False, None, 0.95),
]
assets = []
for name, pitch, jet, marking, scale in specs:
    p = os.path.join(OUT, name + ".png")
    save_plane(p, pitch, jet, marking, scale)
    with Image.open(p) as im:
        assets.append({"image": name + ".png", "w_px": im.size[0], "h_px": im.size[1],
                       "w_in": round(im.size[0] / 600, 4), "h_in": round(im.size[1] / 600, 4)})
with open(os.path.join(OUT, "p019_assets_v3.json"), "w") as f:
    json.dump(assets, f, indent=2)
for a in assets:
    print(a)
