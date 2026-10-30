#!/usr/bin/env python3
"""Locate the slide-019 network-diagram elements by color (a11)."""
import sys
from PIL import Image
from collections import defaultdict

TARGETS = {
    "magenta": (204, 0, 204),
    "dblue": (31, 78, 121),
    "cred": (192, 0, 0),
    "green": (0, 128, 0),
    "red": (255, 0, 0),
    "blue": (68, 114, 196),
    "orgreen": (112, 173, 71),
    "orange": (237, 125, 49),
    "yellow": (255, 192, 0),
}

def near(px, t, tol=45):
    return all(abs(px[i] - t[i]) <= tol for i in range(3))

img = Image.open(sys.argv[1]).convert("RGB")
W, H = img.size
px = img.load()
scale = W / 13.333
print(f"{sys.argv[1]} {W}x{H} scale={scale:.2f}px/in")

for name, t in TARGETS.items():
    pts = []
    for y in range(H):
        for x in range(W):
            if near(px[x, y], t):
                pts.append((x, y))
    if not pts:
        print(f"  {name:9s} NOT FOUND")
        continue
    xs = sorted(set(p[0] for p in pts))
    # cluster columns
    clusters = []
    cur = [xs[0]]
    for v in xs[1:]:
        if v - cur[-1] <= 5:
            cur.append(v)
        else:
            clusters.append((cur[0], cur[-1], len(cur)))
            cur = [v]
    clusters.append((cur[0], cur[-1], len(cur)))
    ys = sorted(set(p[1] for p in pts))
    print(f"  {name:9s} n={len(pts):5d} x={xs[0]/scale:5.2f}..{xs[-1]/scale:5.2f} "
          f"y={ys[0]/scale:5.2f}..{ys[-1]/scale:5.2f}")
    for a, b, n in clusters:
        if n < 2:
            continue
        sub = [p for p in pts if a <= p[0] <= b]
        sy = sorted(set(p[1] for p in sub))
        print(f"      col x={a/scale:5.2f}..{b/scale:5.2f} w={(b-a)/scale:4.2f} "
              f"y={sy[0]/scale:5.2f}..{sy[-1]/scale:5.2f} n={len(sub)}")
