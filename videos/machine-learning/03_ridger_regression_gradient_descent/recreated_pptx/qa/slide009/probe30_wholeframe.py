#!/usr/bin/env python3
"""Probe 30: whole-frame text-ink census. Finds every connected cluster of
'dark text' ink (any hue, but clearly darker than the local background) on the
entire 960x540 frame, so nothing (especially the 'mm' labels) is missed.
"""
import numpy as np
from PIL import Image
from collections import deque

SRC = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
mx = np.maximum(np.maximum(r, g), b)
mn = np.minimum(np.minimum(r, g), b)

# dark text ink: clearly dark (<=560 total) — catches black, dark red, dark blue
DARK = (r + g + b) <= 560
# the red caption keyword (129,37,41) sums to 207 -> caught.
# the black caption (49,51,37) sums to 137 -> caught.
# the equation text: caught.
# the badge numeral 333333 sums to 153 -> caught.

H, W = DARK.shape
seen = np.zeros_like(DARK, bool)
comps = []
for yy in range(H):
    for xx in range(W):
        if DARK[yy, xx] and not seen[yy, xx]:
            q = deque([(yy, xx)])
            seen[yy, xx] = True
            pts = []
            while q:
                cy, cx = q.popleft()
                pts.append((cy, cx))
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < H and 0 <= nx < W and DARK[ny, nx] and not seen[ny, nx]:
                            seen[ny, nx] = True
                            q.append((ny, nx))
            if len(pts) >= 10:
                ys = [p[0] for p in pts]
                xss = [p[1] for p in pts]
                comps.append((len(pts), min(xss), max(xss), min(ys), max(ys)))
comps.sort(key=lambda c: -c[0])
print(f"total dark-ink clusters (n>=10): {len(comps)}")
for n, xa, xb, ya, yb in comps:
    print(f"  n={n:6d}  x {xa:4d}..{xb:4d}  y {ya:4d}..{yb:4d}  w={xb-xa+1:4d} h={yb-ya+1:3d}")
