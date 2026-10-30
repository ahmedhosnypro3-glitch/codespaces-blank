#!/usr/bin/env python3
"""Ink bands inside the slide-019 bottom panels (a11)."""
import sys
import numpy as np
from PIL import Image

img = Image.open(sys.argv[1]).convert("RGB")
a = np.asarray(img).astype(int)
H, W, _ = a.shape
sc = W / 13.333
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
# non-white, non-blue-border, non-cream ink
ink = ~((r > 225) & (g > 225) & (b > 210))

def bands(x0, x1, y0, y1, minpx=2):
    sub = ink[int(y0 * sc):int(y1 * sc), int(x0 * sc):int(x1 * sc)]
    rows = sub.sum(axis=1)
    out = []
    cur = None
    for i, v in enumerate(rows):
        if v >= minpx:
            if cur is None:
                cur = [i, i]
            else:
                cur[1] = i
        else:
            if cur:
                out.append(cur)
                cur = None
    if cur:
        out.append(cur)
    return [(y0 + p / sc, y0 + q / sc) for p, q in out]


def xext(y0, y1, x0, x1, minpx=1):
    sub = ink[int(y0 * sc):int(y1 * sc), int(x0 * sc):int(x1 * sc)]
    cols = sub.sum(axis=0)
    xs = np.where(cols >= minpx)[0]
    if len(xs) == 0:
        return (0.0, 0.0)
    return (x0 + xs[0] / sc, x0 + xs[-1] / sc)


print("== slide019 bottom-left panel (0.69-8.67, 3.31-5.75): ink rows")
for p, q in bands(0.75, 8.6, 3.30, 5.75, minpx=3):
    e = xext(p, q, 0.7, 8.6)
    print(f"  y={p:5.2f}..{q:5.2f} h={q-p:5.3f}  x={e[0]:5.2f}..{e[1]:5.2f}")
print("== slide019 bottom-right panel (9.01-12.68, 3.43-6.46): ink rows")
for p, q in bands(9.05, 12.6, 3.40, 6.46, minpx=3):
    e = xext(p, q, 9.02, 12.6)
    print(f"  y={p:5.2f}..{q:5.2f} h={q-p:5.3f}  x={e[0]:5.2f}..{e[1]:5.2f}")
print("== slide019 cyan box (0.65-5.29, 0.86-3.08): ink rows")
for p, q in bands(0.7, 5.2, 0.80, 3.10, minpx=3):
    e = xext(p, q, 0.66, 5.2)
    print(f"  y={p:5.2f}..{q:5.2f} h={q-p:5.3f}  x={e[0]:5.2f}..{e[1]:5.2f}")
print("== slide019 bottom strip (0.67-12.67, 6.22-7.31): ink rows")
for p, q in bands(0.75, 12.6, 6.20, 7.31, minpx=3):
    e = xext(p, q, 0.7, 12.6)
    print(f"  y={p:5.2f}..{q:5.2f} h={q-p:5.3f}  x={e[0]:5.2f}..{e[1]:5.2f}")
