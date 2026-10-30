"""Connected-component ink inventory for slide_004 boxes (pure numpy/python)."""
from PIL import Image
import numpy as np
from collections import deque

ORIG = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_004.jpg"
o = Image.open(ORIG).convert("RGB")
a = np.asarray(o).astype(int)
R, G, B = a[..., 0], a[..., 1], a[..., 2]
ink = (R < 150) | (G < 150) | (B < 150)


def cls(px):
    r_, g_, b_ = px
    if r_ - g_ > 45 and r_ - b_ > 45:
        return "RED"
    if b_ - r_ > 30:
        return "BLUE"
    return "BLK"


def components(x0, x1, y0, y1, minpx=6):
    seen = np.zeros((y1 - y0, x1 - x0), bool)
    out = []
    sub = ink[y0:y1, x0:x1]
    for yy in range(sub.shape[0]):
        for xx in range(sub.shape[1]):
            if sub[yy, xx] and not seen[yy, xx]:
                q = deque([(yy, xx)])
                seen[yy, xx] = True
                pix = []
                while q:
                    cy, cx = q.popleft()
                    pix.append((cy, cx))
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = cy + dy, cx + dx
                            if 0 <= ny < sub.shape[0] and 0 <= nx < sub.shape[1] \
                               and sub[ny, nx] and not seen[ny, nx]:
                                seen[ny, nx] = True
                                q.append((ny, nx))
                if len(pix) < minpx:
                    continue
                ys = [p[0] + y0 for p in pix]
                xs = [p[1] + x0 for p in pix]
                counts = {}
                for p in pix:
                    c = cls(a[p[0] + y0, p[1] + x0])
                    counts[c] = counts.get(c, 0) + 1
                out.append({
                    "bbox": (min(xs), min(ys), max(xs), max(ys)),
                    "n": len(pix),
                    "cls": max(counts, key=counts.get),
                    "clsall": counts,
                })
    return sorted(out, key=lambda c: (c["bbox"][1], c["bbox"][0]))


for name, bx0, bx1 in [("LEFT Let Y box", 84, 392), ("RIGHT Let Yh box", 431, 742)]:
    print("=" * 76)
    print(f"{name}: components >6px, y103..218, sorted by y then x")
    print("=" * 76)
    print(f"{'bbox x0..x1 / y0..y1':30s} {'px':>5s} {'cls':5s} detail")
    for c in components(bx0, bx1, 103, 219):
        x0, y0, x1, y1 = c["bbox"]
        print(f"x{x0:3d}..{x1:3d} y{y0:3d}..{y1:3d} ({x1-x0+1:3d}x{y1-y0+1:3d}) "
              f"{c['n']:5d} {c['cls']:5s} {c['clsall']}")
