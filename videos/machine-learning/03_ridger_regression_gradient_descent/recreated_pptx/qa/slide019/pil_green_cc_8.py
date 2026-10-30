#!/usr/bin/env python3
"""Connected-component census of green 'predicted y' ink, original frame vs build render.

The original frame is 960x540 (1 px == 1 pt). The 150 dpi render is 2001x1125
(2.0833 px == 1 pt); render pixels are mapped back into frame space before
comparison. Components smaller than 3 px are rejected (phantom-trap law).
"""
from collections import deque

from PIL import Image

DECK = "videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = f"{DECK}/unique_slides/slide_019.jpg"
REND = f"{DECK}/recreated_pptx/qa/slide019/render_8.png"
SCALE = 150 / 72.0
MIN_PX = 3


def is_green(c):
    r, g, b = c
    return g > 60 and g - r > 35 and g - b > 35


def components(path, to_frame):
    im = Image.open(path).convert("RGB")
    W, H = im.size
    px = im.load()
    mask = bytearray(W * H)
    for y in range(H):
        base = y * W
        for x in range(W):
            if is_green(px[x, y]):
                mask[base + x] = 1
    seen = bytearray(W * H)
    comps = []
    for y in range(H):
        for x in range(W):
            i = y * W + x
            if not mask[i] or seen[i]:
                continue
            q = deque([(x, y)])
            seen[i] = 1
            pts = []
            while q:
                cx, cy = q.popleft()
                pts.append((cx, cy))
                for nx, ny in ((cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)):
                    if 0 <= nx < W and 0 <= ny < H:
                        j = ny * W + nx
                        if mask[j] and not seen[j]:
                            seen[j] = 1
                            q.append((nx, ny))
            if len(pts) < MIN_PX:
                continue
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            comps.append({
                "n": len(pts),
                "x0": min(xs) / to_frame, "x1": max(xs) / to_frame,
                "y0": min(ys) / to_frame, "y1": max(ys) / to_frame,
            })
    return im.size, comps


for name, path, sc in [("ORIGINAL (frame px)", ORIG, 1.0),
                       ("RENDER_8 (mapped to frame px)", REND, SCALE)]:
    size, comps = components(path, sc)
    comps.sort(key=lambda c: (round(c["y0"]), c["x0"]))
    print(f"===== {name}: native {size}, {len(comps)} green components (>= {MIN_PX} px) =====")
    for c in comps:
        print(f"  n={c['n']:6d}  x {c['x0']:7.1f}..{c['x1']:7.1f}  "
              f"y {c['y0']:6.1f}..{c['y1']:6.1f}  "
              f"h={c['y1']-c['y0']+1:5.1f} w={c['x1']-c['x0']+1:5.1f}")
    print()
