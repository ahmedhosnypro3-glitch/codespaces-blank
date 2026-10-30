#!/usr/bin/env python3
"""Comprehensive chart measurement for slide 050 — marker clusters, gridlines, ticks,
decision line, arrowhead. All in frame px (960x540, 1px=1pt)."""
from PIL import Image
import numpy as np
from collections import defaultdict

IMG = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_050.jpg'
im = Image.open(IMG).convert('RGB')
a = np.asarray(im).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

# chart interior (exclude the red border ring)
CX0, CX1, CY0, CY1 = 318, 818, 180, 475

BLUE = (B - R > 25) & (B > 60) & (G < 140)
MAG = (R > 110) & (B > 110) & (R - G > 20) & (B - G > 20)
RED = (R > 110) & (R - G > 30) & (R - B > 30)


def clusters(mask, minpix=20, band=8):
    sub = mask[CY0:CY1, CX0:CX1]
    ys, xs = np.where(sub)
    if len(xs) == 0:
        return []
    pts = [(int(x + CX0), int(y + CY0)) for x, y in zip(xs, ys)]
    grid = defaultdict(list)
    for i, (x, y) in enumerate(pts):
        grid[(x // band, y // band)].append(i)
    seen = set()
    out = []
    for i in range(len(pts)):
        if i in seen:
            continue
        stack = [i]; seen.add(i); comp = []
        while stack:
            j = stack.pop(); comp.append(pts[j]); px, py = pts[j]
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    for k in grid.get(((px + dx) // band, (py + dy) // band), ()):
                        if k not in seen:
                            seen.add(k); stack.append(k)
        if len(comp) >= minpix:
            cxs = [p[0] for p in comp]; cys = [p[1] for p in comp]
            out.append((min(cxs), min(cys), max(cxs), max(cys), len(comp)))
    return sorted(out, key=lambda c: -c[4])


XP = lambda x: 362.7 + 52.725 * x
YP = lambda y: 428.7 - 30.671 * y
DX = lambda px: (px - 362.7) / 52.725
DY = lambda py: (428.7 - py) / 30.671

print("=== BLUE clusters (squares, class C1) ===")
for c in clusters(BLUE, 15):
    cx, cy = (c[0] + c[2]) / 2, (c[1] + c[3]) / 2
    print(f"  bbox {c[:4]} centre ({cx:.1f},{cy:.1f}) n={c[4]} -> data ({DX(cx):.2f},{DY(cy):.2f})")

print("=== MAGENTA clusters (diamonds, class C2) ===")
for c in clusters(MAG, 15):
    cx, cy = (c[0] + c[2]) / 2, (c[1] + c[3]) / 2
    print(f"  bbox {c[:4]} centre ({cx:.1f},{cy:.1f}) n={c[4]} -> data ({DX(cx):.2f},{DY(cy):.2f})")

print("=== RED clusters (decision line + markers + arrowhead) ===")
for c in clusters(RED, 25):
    cx, cy = (c[0] + c[2]) / 2, (c[1] + c[3]) / 2
    w = c[2] - c[0] + 1; h = c[3] - c[1] + 1
    print(f"  bbox {c[:4]} w={w} h={h} centre ({cx:.1f},{cy:.1f}) n={c[4]} -> data ({DX(cx):.2f},{DY(cy):.2f})")

print("=== HORIZONTAL gridlines (rows with long light-grey runs) ===")
# grid colour measured ~(207,209,206): neutral, mid-light
NEU = (np.abs(R - G) < 10) & (np.abs(G - B) < 10) & (R > 180) & (R < 245)
for y in range(CY0, CY1):
    row = NEU[y, CX0:CX1]
    if row.sum() > 380:
        print(f"  y={y} count={row.sum()} data_y={DY(y):.2f}")

print("=== VERTICAL spines ===")
for x in range(CX0, CX1):
    col = NEU[CY0:CY1, x]
    if col.sum() > 250:
        print(f"  x={x} count={col.sum()} data_x={DX(x):.2f}")

print("=== decision line: red px per row (interior, excl markers) ===")
pts = []
for y in range(CY0, CY1):
    for x in range(CX0, CX1):
        if RED[y, x]:
            pts.append((x, y))
# bin by y
byy = defaultdict(list)
for x, y in pts:
    byy[y].append(x)
ys = sorted(byy)
print(f"  red y range {ys[0]}..{ys[-1]}, n={len(pts)}")
for y in ys:
    xs = byy[y]
    print(f"   y={y} data_y={DY(y):+.2f} x {min(xs)}..{max(xs)} (data_x {DX(min(xs)):+.2f}..{DX(max(xs)):+.2f}) n={len(xs)}")
