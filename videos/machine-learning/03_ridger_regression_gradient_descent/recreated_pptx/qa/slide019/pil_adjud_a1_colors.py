#!/usr/bin/env python3
"""PIL adjudication of the template-A attempt_1 colour findings.
F1: Test1/Test2/Test3 test-table headers (build: Test1/Test3 red, Test2 blue)
F2: "W =" label (build: "W" red, " =" black)
Compare original frame ink vs render ink at the measured build coordinates.
"""
import numpy as np
from PIL import Image

ORIG = Image.open(
    "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_019.jpg"
).convert("RGB")
REND = Image.open(
    "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide019/render_1.png"
).convert("RGB")

O = np.asarray(ORIG).astype(int)
R = np.asarray(REND).astype(int)
SY = R.shape[0] / O.shape[0]   # 1125/540 = 2.0833
SX = R.shape[1] / O.shape[1]  # 2001/960 = 2.0844

COLX = [124, 384, 644]
GROUPY = [205, 310, 420]


def classify(px):
    """Classify an ink pixel: red / blue / green / black / gray."""
    r, g, b = px
    if r > 120 and g < 110 and b < 110 and (r - max(g, b)) > 45:
        return "red"
    if b > 120 and r < 110 and (b - max(r, g)) > 30:
        return "blue"
    if g > 110 and r < 130 and b < 110 and (g - max(r, b)) > 40:
        return "green"
    if r < 90 and g < 90 and b < 90:
        return "black"
    return "other"


def census(img, sfy, sfx, x0, y0, x1, y1, thresh=170, label=""):
    """Count dark-ink pixels in a frame-px box and return colour census + median."""
    X0, Y0 = int(x0 * sfx), int(y0 * sfy)
    X1, Y1 = int(x1 * sfx), int(y1 * sfy)
    sub = img[Y0:Y1, X0:X1]
    lum = sub.sum(axis=2) / 3.0
    mask = lum < thresh
    if mask.sum() == 0:
        print(f"  {label}: NO DARK INK ({mask.size} px checked)")
        return
    from collections import Counter
    cnt = Counter()
    for py, ppx in zip(*np.where(mask)):
        cnt[classify(sub[py, ppx])] += 1
    tot = sum(cnt.values())
    parts = ", ".join(f"{k}:{v} ({100*v/tot:.0f}%)" for k, v in cnt.most_common())
    print(f"  {label}: {tot} ink px | {parts}")


print("=== F1: Test table headers (build places TestN at v0=x0+142, gy+5..+20) ===")
for ci, x0 in enumerate(COLX):
    for gi, gy in enumerate(GROUPY):
        for ti in range(3):
            colW = 44  # approx build colW (gx1-v0)/3
            v0 = x0 + 142
            bx0, bx1 = v0 + ti * colW + 3, v0 + (ti + 1) * colW - 3
            by0, by1 = gy + 4, gy + 21
            print(f" col{ci} g{gi} Test{ti+1}:")
            census(O, 1.0, 1.0, bx0, by0, bx1, by1, label="  orig")
            census(R, SY, SX, bx0, by0, bx1, by1, label="  rend")

print()
print("=== F2: 'W =' label (build places at x0+16..x0+46, gy+22..+38) ===")
for ci, x0 in enumerate(COLX):
    for gi, gy in enumerate(GROUPY):
        print(f" col{ci} g{gi}:")
        census(O, 1.0, 1.0, x0 + 16, gy + 22, x0 + 46, gy + 38, label="  orig")
        census(R, SY, SX, x0 + 16, gy + 22, x0 + 46, gy + 38, label="  rend")
