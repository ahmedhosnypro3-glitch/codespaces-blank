"""Generate line-art assets for slide 020: varied aircraft sketches + sigmoid-circle insets."""
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon

OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure/recreated_pptx/build/assets"
os.makedirs(OUT, exist_ok=True)

GRAY = "#606060"
BLACK = "#000000"
PURPLE = "#800080"
LAV = "#E6C8F0"


def rot(pts, deg, cx=0.5, cy=0.5):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * ca - (y - cy) * sa, cy + (x - cx) * sa + (y - cy) * ca) for x, y in pts]


def airplane(ax, enemy=False, tilt=0.0, stretch=1.0, flip=False):
    """Sketch-style side-view aircraft: fuselage, wings, tail, windows; optional target mark."""
    def P(pts):
        p = [(x, 0.5 + (y - 0.5) / stretch) for x, y in pts]
        if flip:
            p = [(1.0 - x, y) for x, y in p]
        return rot(p, tilt)

    # fuselage
    ax.add_patch(Polygon(P([(0.04, 0.50), (0.18, 0.40), (0.80, 0.40), (0.95, 0.46),
                            (0.95, 0.54), (0.80, 0.60), (0.18, 0.60)]),
                         closed=True, fill=False, edgecolor=GRAY, linewidth=1.6))
    # main wings (swept)
    ax.add_patch(Polygon(P([(0.38, 0.42), (0.56, 0.12), (0.66, 0.12), (0.60, 0.42)]),
                         closed=True, fill=False, edgecolor=GRAY, linewidth=1.6))
    ax.add_patch(Polygon(P([(0.38, 0.58), (0.56, 0.88), (0.66, 0.88), (0.60, 0.58)]),
                         closed=True, fill=False, edgecolor=GRAY, linewidth=1.6))
    # tailplane
    ax.add_patch(Polygon(P([(0.84, 0.45), (0.93, 0.30), (0.99, 0.30), (0.95, 0.45)]),
                         closed=True, fill=False, edgecolor=GRAY, linewidth=1.3))
    ax.add_patch(Polygon(P([(0.84, 0.55), (0.93, 0.70), (0.99, 0.70), (0.95, 0.55)]),
                         closed=True, fill=False, edgecolor=GRAY, linewidth=1.3))
    # propeller
    px, py = P([(1.00, 0.50)])[0]
    ax.plot([px], [py], marker="|", markersize=14,
            markeredgewidth=1.6, color=GRAY)
    # windows
    for i in range(6):
        ax.add_patch(Circle((0.30 + i * 0.072, 0.50), 0.016,
                            fill=False, edgecolor=BLACK, linewidth=0.7))
    if enemy:
        # pencil target / cross-hair mark on the forward fuselage
        c = P([(0.24, 0.50)])[0]
        ax.add_patch(Circle(c, 0.052, fill=False, edgecolor=BLACK, linewidth=1.1))
        ax.plot([c[0] - 0.062, c[0] + 0.062], [c[1], c[1]], color=BLACK, linewidth=1.0)
        ax.plot([c[0], c[0]], [c[1] - 0.062, c[1] + 0.062], color=BLACK, linewidth=1.0)
    ax.set_xlim(0.0, 1.02)
    ax.set_ylim(0.05, 0.95)
    ax.set_aspect("auto")
    ax.axis("off")


def save_plane(path, enemy, tilt, stretch, flip):
    fig = plt.figure(figsize=(2.6, 1.0), dpi=600)
    ax = fig.add_axes([0, 0, 1, 1])
    airplane(ax, enemy=enemy, tilt=tilt, stretch=stretch, flip=flip)
    fig.savefig(path, dpi=600, transparent=True, bbox_inches="tight", pad_inches=0.01)
    plt.close(fig)


def save_sigmoid_circle(path, size_in):
    """Pink/lavender circle with cross-axes and a hand-drawn sigmoid S-curve."""
    fig = plt.figure(figsize=(size_in, size_in), dpi=600)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.add_patch(Circle((0.5, 0.5), 0.46, facecolor=LAV, edgecolor=PURPLE, linewidth=2.0))
    ax.plot([0.10, 0.90], [0.50, 0.50], color=PURPLE, linewidth=1.1)
    ax.plot([0.50, 0.50], [0.10, 0.90], color=PURPLE, linewidth=1.1)
    xs = [i / 60 for i in range(61)]
    ys = [1 / (1 + math.exp(-(x - 0.5) * 9)) for x in xs]
    ax.plot([0.12 + x * 0.76 for x in xs], [0.16 + y * 0.68 for y in ys],
            color=PURPLE, linewidth=2.4)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.savefig(path, dpi=600, transparent=True)
    plt.close(fig)


enemy_specs = [
    ("eq_020_plane_enemy_a.png", 0.0, 1.0, False),
    ("eq_020_plane_enemy_b.png", -7.0, 1.05, False),
    ("eq_020_plane_enemy_c.png", 6.0, 0.95, False),
]
safe_specs = [
    ("eq_020_plane_safe_a.png", 0.0, 1.0, False),
    ("eq_020_plane_safe_b.png", 8.0, 1.0, True),
    ("eq_020_plane_safe_c.png", -6.0, 1.05, False),
]
for name, tilt, stretch, flip in enemy_specs:
    save_plane(os.path.join(OUT, name), True, tilt, stretch, flip)
for name, tilt, stretch, flip in safe_specs:
    save_plane(os.path.join(OUT, name), False, tilt, stretch, flip)

save_sigmoid_circle(os.path.join(OUT, "eq_020_sigmoid_circle.png"), 1.2)
save_sigmoid_circle(os.path.join(OUT, "eq_020_sigmoid_circle_small.png"), 0.9)

print("assets written to", OUT)
