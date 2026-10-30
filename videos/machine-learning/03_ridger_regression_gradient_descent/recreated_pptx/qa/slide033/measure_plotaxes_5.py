#!/usr/bin/env python3
"""Locate the plot's axis rules and white background box precisely (slide 033).

Answers, with numbers:
  1. exact x/y extent of the WHITE plot background box
  2. exact rows of the x-axis rules and cols of the y-axis rules (dark horizontal
     and vertical strokes near the plot)
"""
from PIL import Image
import numpy as np, collections

ORIG = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent/unique_slides/slide_033.jpg")
o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
R, G, B = o[:, :, 0], o[:, :, 1], o[:, :, 2]

print("=== 1) WHITE background box ===")
W = (R >= 240) & (G >= 240) & (B >= 240)
# per-row: contiguous white runs inside the panel, ignoring the badge area
print("rows y58..315: first/last white x inside x600..903")
edges = []
for y in range(58, 316):
    xs = [x for x in range(600, 904) if W[y, x]]
    if xs: edges.append((y, xs[0], xs[-1]))
for y, a, b in edges[::20]:
    print(f"  y{y} x{a}..x{b}")
ys_ = [e[0] for e in edges]
print(f"  -> white rows y{min(ys_)}..y{max(ys_)}")
xs0 = [e[1] for e in edges]; xs1 = [e[2] for e in edges]
print(f"  -> left edge (mode of first-white): {collections.Counter(xs0).most_common(3)}")
print(f"  -> right edge (mode of last-white): {collections.Counter(xs1).most_common(3)}")

print()
print("=== 2) dark horizontal rules near the plot bottom (y300..325) ===")
for y in range(298, 326):
    dk = (R[y, :] < 150) & (G[y, :] < 150) & (B[y, :] < 150)
    xs = np.where(dk[540:910])[0] + 540
    if len(xs) > 100:
        print(f"  y{y}: dark px {len(xs)}  x{xs.min()}..x{xs.max()}")

print()
print("=== 3) dark vertical rules in the plot x-range (x600..620 and x700..740) ===")
for x0, x1 in [(598, 625), (700, 745), (838, 850)]:
    print(f"  cols x{x0}..{x1}:")
    for x in range(x0, x1):
        dk = (R[:, x] < 150) & (G[:, x] < 150) & (B[:, x] < 150)
        ys = np.where(dk[55:315])[0] + 55
        if len(ys) > 80:
            print(f"    x{x}: dark px {len(ys)}  y{ys.min()}..y{ys.max()}")
