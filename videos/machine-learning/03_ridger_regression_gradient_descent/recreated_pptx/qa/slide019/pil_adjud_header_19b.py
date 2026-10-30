#!/usr/bin/env python3
"""Follow-up: RIDGE3 header ink runs + background class map (orig vs render_18)."""
from PIL import Image
import os
from collections import Counter

os.chdir("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent")
o = Image.open("unique_slides/slide_019.jpg").convert("RGB")
r = Image.open("recreated_pptx/qa/slide019/render_18.png").convert("RGB")
S = r.size[0] / o.size[0]
op, rp = o.load(), r.load()

print("== RIDGE3 header per-x ink (y181..200) ==")
runs = []
for x in range(380, 645):
    nr = nb = 0
    for y in range(181, 200):
        R, G, B = op[x, y]
        if R > 150 and G < 110 and B < 110:
            nr += 1
        elif B > 120 and R < 120 and G < 120:
            nb += 1
    runs.append((x, nr, nb))
# compress into segments
seg = None
out = []
for x, nr, nb in runs:
    cls = "r" if nr > 0 else ("b" if nb > 0 else ".")
    if seg and seg[0] == cls:
        seg[2] = x
    else:
        seg = [cls, x, x]
        out.append(seg)
print("segments (class, x0..x1):", [(c, a, b) for c, a, b in out])

def bgclass(px_tuple):
    R, G, B = px_tuple
    if R > 245 and G > 245 and B > 245:
        return "W"  # white
    if R > 230 and G > 230 and B < 160:
        return "Y"  # yellow
    if abs(R - 233) < 12 and abs(G - 233) < 12 and abs(B - 231) < 12:
        return "G"  # gray panel
    if R > 200 and G < 180 and B < 160:
        return "p"  # peach tint
    if R > 215 and G > 245 and B > 215:
        return "m"  # mint tint
    if R > 240 and G > 245 and B > 215:
        return "c"  # cream tint
    return "?"

print("\n== BG CLASS MAP orig (rows y210..530 step 8, cols x60..905 step 10) ==")
for y in range(210, 531, 16):
    line_o = "".join(bgclass(op[x, y]) for x in range(60, 906, 10))
    print(f"y{y:3d} O {line_o}")
print("\n== BG CLASS MAP render_18 (same frame coords) ==")
for y in range(210, 531, 16):
    line_r = "".join(bgclass(rp[int(x * S), int(y * S)]) for x in range(60, 906, 10))
    print(f"y{y:3d} R {line_r}")
