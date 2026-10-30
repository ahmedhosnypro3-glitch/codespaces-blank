#!/usr/bin/env python3
"""Compact targeted structure probe: bl box, both images, one line per question."""
import numpy as np
from PIL import Image

B = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
     "03_ridger_regression_gradient_descent")
o = np.asarray(Image.open(B + "/unique_slides/slide_003.jpg").convert(
    "RGB")).astype(int)
r = np.asarray(Image.open(B + "/recreated_pptx/qa/slide003/render_9.png").convert(
    "RGB").resize((960, 540), Image.LANCZOS)).astype(int)


def cl(px):
    R, G, Bc = int(px[0]), int(px[1]), int(px[2])
    s = R + G + Bc
    if s > 735:
        return "."
    if R > 200 and G > 200 and Bc < 215 and Bc > 90:
        return "Y"
    if G > 195 and Bc > 195 and R < 215 and R > 95:
        return "C"
    if R > 195 and Bc > 175 and G < 225 and G > 105:
        return "P"
    if R > 135 and G < 110 and Bc < 110:
        return "R"
    if Bc > 135 and R < 110 and G < 135:
        return "B"
    if abs(R - G) < 26 and abs(G - Bc) < 26 and 80 < R < 215:
        return "g"
    return "#"


def colprofile(a, x0, x1, y0, y1, label):
    """Which x-columns in [x0,x1) have ink in y-range."""
    res = []
    for x in range(x0, x1):
        has = any(cl(a[y, x]) != "." for y in range(y0, y1))
        res.append("|" if has else " ")
    print(f"  {label:22s} x{x0}..{x1-1} y{y0}..{y1-1}: " + "".join(res))


print("=== BOTTOM-LEFT: column ink profiles (| = has ink) ===")
for nm, a in (("ORIG", o), ("REN ", r)):
    print(f"-- {nm}")
    colprofile(a, 75, 200, 330, 500, "yvec zone")
    colprofile(a, 200, 460, 330, 500, "matrix zone")
    colprofile(a, 455, 545, 330, 500, "wvec zone")

print("\n=== '=' sign location: dark-ink runs x130..200 by row ===")
for nm, a in (("ORIG", o), ("REN ", r)):
    print(f"-- {nm}")
    for y in range(360, 420, 2):
        hits = [x for x in range(128, 200) if cl(a[y, x]) not in (".", "Y", "C", "P")]
        if hits:
            print(f"    y{y}: x{min(hits)}..{max(hits)} n={len(hits)}")

print("\n=== dimension-label rows y470..520: red/dark runs ===")
for nm, a in (("ORIG", o), ("REN ", r)):
    print(f"-- {nm}")
    for y in range(468, 520, 2):
        hits = [(x, cl(a[y, x])) for x in range(75, 545)
                if cl(a[y, x]) in ("R", "#", "g")]
        if hits:
            xs = [x for x, _ in hits]
            print(f"    y{y}: x{min(xs)}..{max(xs)} n={len(hits)} "
                  f"{''.join(c for _, c in hits[:80])}")
