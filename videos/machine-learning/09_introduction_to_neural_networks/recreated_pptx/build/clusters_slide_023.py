#!/usr/bin/env python3
"""Cluster-based ground truth for slide_023: locate every colored text run."""
from PIL import Image
import numpy as np

img = Image.open("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_023.jpg")
a = np.asarray(img.convert("RGB")).astype(int)
H, W, _ = a.shape

r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
mx = np.max(a, axis=2)
mn = np.min(a, axis=2)
sat = mx - mn

RED = (r - g > 45) & (r - b > 45) & (r > 90)
GREEN = (g - r > 35) & (g - b > 35) & (g > 60)
BLUE = (b - r > 60) & (b - g > 60) & (b > 90)
VIOLET = (b - r > 35) & (b - r <= 70) & (r - g > 10) & (b > 100)
YELLOW = (r > 190) & (g > 190) & (b < 180) & (r - b > 40)
DARK = (mx < 110) & (sat < 55)


def clusters(mask, y0, y1, x0, x1, min_px=6, gap=6):
    """Group mask pixels into clusters (connected by row/column proximity)."""
    m = np.zeros_like(mask)
    m[y0:y1, x0:x1] = mask[y0:y1, x0:x1]
    pts = np.argwhere(m)
    if len(pts) == 0:
        return []
    # simple grid-based clustering: bucket by (y//8, x//8) then merge
    seen = set()
    out = []
    pset = set(map(tuple, pts))
    for p in pts:
        tp = tuple(p)
        if tp in seen:
            continue
        stack = [tp]
        seen.add(tp)
        comp = []
        while stack:
            cy, cx = stack.pop()
            comp.append((cy, cx))
            for dy in range(-gap, gap + 1):
                for dx in range(-gap, gap + 1):
                    q = (cy + dy, cx + dx)
                    if q in pset and q not in seen:
                        seen.add(q)
                        stack.append(q)
        if len(comp) >= min_px:
            ys = [c[0] for c in comp]
            xs = [c[1] for c in comp]
            out.append({"x0": min(xs), "x1": max(xs), "y0": min(ys), "y1": max(ys), "n": len(comp)})
    out.sort(key=lambda d: (d["y0"], d["x0"]))
    return out


def show(title, mask, y0=0, y1=H, x0=0, x1=W, min_px=6, gap=6):
    print(f"\n--- {title} ---")
    for c in clusters(mask, y0, y1, x0, x1, min_px, gap):
        print(f"  x {c['x0']:4d}-{c['x1']:4d} ({c['x0']/W:.3f}-{c['x1']/W:.3f})  "
              f"y {c['y0']:4d}-{c['y1']:4d} ({c['y0']/H:.3f}-{c['y1']/H:.3f})  n={c['n']}")


# Title band (above inner violet frame top y=110)
show("TITLE red text (y 0..110)", RED, 0, 110, 0, 960)
show("YELLOW badge", YELLOW, 0, 120, 700, 960)
show("DARK badge text", DARK, 0, 120, 700, 960)

# Rows: left box and right box regions
ROWS = {
    1: (140, 195, 82, 437, 619, 878),
    2: (221, 276, 84, 437, 619, 878),
    3: (300, 348, 83, 327, 619, 878),
    4: (380, 429, 85, 328, 619, 878),
    5: (460, 497, 85, 238, 619, 746),
}
for n, (y0, y1, lx0, lx1, rx0, rx1) in ROWS.items():
    show(f"ROW{n} LEFT red", RED, y0, y1, lx0, lx1)
    show(f"ROW{n} LEFT green", GREEN, y0, y1, lx0, lx1)
    show(f"ROW{n} LEFT blue", BLUE, y0, y1, lx0, lx1)
    show(f"ROW{n} RIGHT red", RED, y0, y1, rx0, rx1)
    show(f"ROW{n} RIGHT green", GREEN, y0, y1, rx0, rx1)
    show(f"ROW{n} RIGHT blue", BLUE, y0, y1, rx0, rx1)

# Connector band between boxes (x 440..620)
show("CONNECTORS red (all rows)", RED, 110, 510, 440, 620, min_px=8, gap=8)
