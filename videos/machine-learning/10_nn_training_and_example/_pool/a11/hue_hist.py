#!/usr/bin/env python3
"""Per-hue x/y histogram of diagram node columns (a11)."""
from PIL import Image
import sys

def hue_class(p):
    r, g, b = p[:3]
    mx, mn = max(p[:3]), min(p[:3])
    if mx - mn < 55 or mx < 80:
        return None
    if r > 150 and g < 110 and b < 150: return "red_or_magenta" if b > 130 else "red"
    if b > 120 and r < 130 and g < 170: return "blue"
    if g > 110 and r < 150 and b < 140: return "green"
    if r > 180 and 120 < g < 200 and b < 110: return "orange"
    if r > 180 and g > 170 and b < 140: return "yellow"
    if r > 150 and g < 130 and b > 140: return "magenta"
    return None

def scan(path, x0i, x1i, y0i, y1i):
    img = Image.open(path).convert("RGB")
    W, H = img.size
    px = img.load()
    scale = W / 13.333
    X0, X1 = int(x0i*scale), int(x1i*scale)
    Y0, Y1 = int(y0i*scale), int(y1i*scale)
    hist = {}
    for y in range(Y0, Y1):
        for x in range(X0, X1):
            c = hue_class(px[x, y])
            if c:
                hist.setdefault(c, {}).setdefault(x, 0)
                hist[c][x] += 1
    for c, hx in sorted(hist.items()):
        xs = sorted(hx)
        clusters = []
        cur = [xs[0]]
        for x in xs[1:]:
            if x - cur[-1] <= 6:
                cur.append(x)
            else:
                clusters.append(cur); cur = [x]
        clusters.append(cur)
        out = []
        for cl in clusters:
            n = sum(hx[x] for x in cl)
            if n < 12: continue
            out.append(f"x={cl[0]/scale:.2f}-{cl[-1]/scale:.2f}(n={n})")
        print(f"  {c:16s} " + " ".join(out))

scan(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]))
