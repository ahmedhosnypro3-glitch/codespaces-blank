#!/usr/bin/env python3
"""Row-by-row colour-run scan of the bottom-left box, both images."""
import numpy as np
from PIL import Image

B = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
     "03_ridger_regression_gradient_descent")
o = np.asarray(Image.open(B + "/unique_slides/slide_003.jpg").convert(
    "RGB")).astype(int)
r = np.asarray(Image.open(B + "/recreated_pptx/qa/slide003/render_9.png").convert(
    "RGB").resize((960, 540), Image.LANCZOS)).astype(int)


def classify(px):
    R, G, Bc = px
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


def runs_of(a, y, x0=75, x1=545):
    """Return list of (x_start, x_end, label) for colour/ink runs."""
    out = []
    cur = None
    for x in range(x0, x1):
        c = classify(a[y, x])
        if c == ".":
            if cur:
                out.append(cur)
                cur = None
        else:
            if cur is None:
                cur = [x, x, c]
            elif cur[2] == c and x - cur[1] <= 2:
                cur[1] = x
            else:
                out.append(cur)
                cur = [x, x, c]
    if cur:
        out.append(cur)
    return [(s, e, c) for s, e, c in out]


print("=== BOTTOM-LEFT BOX colour runs (frame px) ===")
print("=== ORIGINAL ===")
for y in range(322, 520, 3):
    rr = runs_of(o, y)
    print(f" y{y:>3}: " + "  ".join(f"{s}-{e}:{c}" for s, e, c in rr))
print("=== RENDER ===")
for y in range(322, 520, 3):
    rr = runs_of(r, y)
    print(f" y{y:>3}: " + "  ".join(f"{s}-{e}:{c}" for s, e, c in rr))
