#!/usr/bin/env python3
"""Compare green 'predicted y' ink between the original frame and the build render.

The original frame is 960x540 (1 px == 1 pt). The 150 dpi render is 2001x1125
(2.0833 px == 1 pt), so render pixels are mapped back into frame space before
any comparison. Green is isolated as the channel where G dominates R and B.
"""
from PIL import Image

DECK = "videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = f"{DECK}/unique_slides/slide_019.jpg"
REND = f"{DECK}/recreated_pptx/qa/slide019/render_8.png"
SCALE = 150 / 72.0


def is_green(c):
    r, g, b = c
    return g > 60 and g - r > 35 and g - b > 35


def green_points(path, scale_to_frame):
    im = Image.open(path).convert("RGB")
    W, H = im.size
    px = im.load()
    pts = []
    for y in range(H):
        for x in range(W):
            if is_green(px[x, y]):
                pts.append((x / scale_to_frame, y / scale_to_frame))
    return im.size, pts


def clusters(pts, gap=4):
    """Cluster points into boxes by y-gap then x-gap."""
    ys = sorted(set(round(p[1], 1) for p in pts))
    ybands = []
    if ys:
        start = prev = ys[0]
        for v in ys[1:]:
            if v - prev > gap:
                ybands.append((start, prev))
                start = v
            prev = v
        ybands.append((start, prev))
    out = []
    for y0, y1 in ybands:
        sel = [p for p in pts if y0 - 0.1 <= p[1] <= y1 + 0.1]
        xs = sorted(set(round(p[0], 1) for p in sel))
        xb = []
        if xs:
            s = pv = xs[0]
            for v in xs[1:]:
                if v - pv > gap:
                    xb.append((s, pv))
                    s = v
                pv = v
            xb.append((s, pv))
        for x0, x1 in xb:
            n = sum(1 for p in sel if x0 - 0.1 <= p[0] <= x1 + 0.1)
            out.append((round(x0, 1), round(y0, 1), round(x1, 1), round(y1, 1), n))
    return out


for name, path, sc in [("ORIGINAL (frame px)", ORIG, 1.0),
                       ("RENDER_8 (mapped to frame px)", REND, SCALE)]:
    size, pts = green_points(path, sc)
    print(f"===== {name}: native size {size}, green px {len(pts)} =====")
    for c in clusters(pts):
        x0, y0, x1, y1, n = c
        print(f"  box x {x0:7.1f}..{x1:7.1f}   y {y0:6.1f}..{y1:6.1f}   n={n:5d}"
              f"   h={y1-y0+1:4.1f} w={x1-x0+1:5.1f}")
    print()
