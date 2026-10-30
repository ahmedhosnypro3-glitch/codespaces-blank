#!/usr/bin/env python3
"""probe64 - slide 009 annotation group: colour + geometry read on the frame.

Questions:
  1. Are the annotation strokes (parallel stroke, dimension shaft) RED or ROSE?
  2. Is there a faint shaft trace, and does it follow the OLD (70 deg) path or
     the PERPENDICULAR (62.8 deg) path?
  3. Where is the label ink exactly (bbox / centroid) and how steep is it?
"""
import math
import numpy as np
from PIL import Image

FRAME = ("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
         "03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg")

im = Image.open(FRAME).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
print(f"frame {W}x{H}")


def sat(px):
    r, g, b = px
    return r - max(g, b)


def path(label, p0, p1, n=14, win=2):
    """Sample along a segment: report the most-saturated pixel in a small window."""
    print(f"-- {label}  {p0} -> {p1}")
    (x0, y0), (x1, y1) = p0, p1
    for i in range(n + 1):
        t = i / n
        cx = x0 + (x1 - x0) * t
        cy = y0 + (y1 - y0) * t
        best = None
        for dy in range(-win, win + 1):
            for dx in range(-win, win + 1):
                x, y = int(round(cx)) + dx, int(round(cy)) + dy
                if 0 <= x < W and 0 <= y < H:
                    px = tuple(a[y, x])
                    if best is None or sat(px) > sat(best):
                        best = px
        print(f"   t={t:4.2f} ({cx:6.1f},{cy:6.1f}) maxsat rgb={best}")


def bbox(label, x0, y0, x1, y1, test):
    sub = a[y0:y1 + 1, x0:x1 + 1]
    m = np.zeros(sub.shape[:2], dtype=bool)
    for yy in range(sub.shape[0]):
        for xx in range(sub.shape[1]):
            m[yy, xx] = test(sub[yy, xx])
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        print(f"-- {label}: NO MATCH")
        return
    print(f"-- {label}: n={len(xs)} bbox x{x0+xs.min()}..{x0+xs.max()} "
          f"y{y0+ys.min()}..{y0+ys.max()} centroid=({x0+xs.mean():.1f},{y0+ys.mean():.1f})")
    # steepest ink: PCA axis of the ink
    pts = np.stack([xs, ys]).astype(float)
    pts -= pts.mean(axis=1, keepdims=True)
    cov = pts @ pts.T / pts.shape[1]
    vals, vecs = np.linalg.eigh(cov)
    ax = vecs[:, -1]
    ang = math.degrees(math.atan2(ax[1], ax[0]))
    print(f"      PCA axis {ang:.1f} deg (mod 180), elongation "
          f"{math.sqrt(vals[-1]/max(vals[0],1e-9)):.2f}")


# ---------------------------------------------------------------- strokes
path("LEFT parallel stroke", (168, 159), (191, 147))
path("RIGHT parallel stroke", (585, 152), (607, 142))
path("LEFT OLD shaft (197,146)->(249,292)", (197, 146), (249, 292), n=12)
path("LEFT PERP shaft (197.5,145)->(270.2,284.5)", (197.5, 145), (270.2, 284.5), n=12)
path("RIGHT OLD shaft (611,147)->(682,324)", (611, 147), (682, 324), n=12)
path("RIGHT PERP shaft (611,145)->(696.0,321.4)", (611, 145), (696.0, 321.4), n=12)

# ---------------------------------------------------------------- heads / disc
path("LEFT bottom head", (244, 286), (249, 292), n=4, win=1)
path("RIGHT bottom head", (677, 317), (681, 323), n=4, win=1)
path("LEFT old tail head", (185, 153), (190, 159), n=4, win=1)
path("RIGHT old tail head", (601, 147), (605, 153), n=4, win=1)

# ---------------------------------------------------------------- labels
bbox("LEFT label ink (red+rose)", 192, 188, 240, 232,
     lambda p: p[0] > 150 and p[0] - p[1] > 25 and p[0] - p[2] > 15)
bbox("LEFT label ink (strong red only)", 192, 188, 240, 232,
     lambda p: p[0] > 120 and p[0] - p[1] > 60 and p[0] - p[2] > 50)
bbox("RIGHT label ink (red+rose)", 618, 198, 660, 270,
     lambda p: p[0] > 150 and p[0] - p[1] > 25 and p[0] - p[2] > 15)
bbox("RIGHT label ink (strong red only)", 618, 198, 660, 270,
     lambda p: p[0] > 120 and p[0] - p[1] > 60 and p[0] - p[2] > 50)

# ---------------------------------------------------------------- blue lines
for name, (xa, ya), (xb, yb) in {
    "LEFT blue": ((141, 351), (433, 201)),
    "RIGHT blue": ((555, 387), (849, 247)),
}.items():
    ys = []
    for x in range(min(xa, xb) + 6, max(xa, xb) - 6):
        col = a[max(0, int(ya + (yb - ya) * (x - xa) / (xb - xa)) - 4):
                 int(ya + (yb - ya) * (x - xa) / (xb - xa)) + 5, x]
        idx = np.argmax(col[:, 2])
        ys.append((col[idx][2], x))
    blues = [(c, x) for c, x in ys if c > 90]
    if blues:
        cs = np.array([c for c, _ in blues], float)
        xs = np.array([x for _, x in blues], float)
        m, b = np.polyfit(xs, cs, 1)
        print(f"-- {name}: n={len(blues)} core slope={m:.5f} (y = {m:.5f}x {b:+.2f})")
