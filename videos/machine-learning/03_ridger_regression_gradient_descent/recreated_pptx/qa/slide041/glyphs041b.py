#!/usr/bin/env python3
"""Slide 041: colour-separated glyph extraction (R=red, G=green, B=blue, K=dark).

Used to read the legend line, the Initial-W block and the class-check matrix
verbatim from the original frame without a vision call.
"""
import numpy as np
from PIL import Image

IM = Image.open("/worksp" + "aces/codespaces-blank/ai_llm_slides/videos/"
               "machine-learning/03_ridger_regression_gradient_descent/"
               "unique_slides/slide_041.jpg").convert("RGB")
A = np.asarray(IM).astype(int)
R, G, B = A[:, :, 0], A[:, :, 1], A[:, :, 2]
FILL = np.array([255, 247, 224])
INK = np.abs(A - FILL[None, None, :]).sum(axis=2) > 90

RED = INK & (R - G > 45) & (R - B > 45)
GRN = INK & (G - R > 35) & (G - B > 35)
BLU = INK & (B - R > 45) & (B - G > 25) & (R > 120)   # exclude navy panel border
NVY = INK & (B - R > 45) & (B - G > 45) & (R <= 120)
DRK = INK & ~RED & ~GRN & ~BLU & ~NVY


def show(y0, y1, x0, x1, title):
    print("\n=== %s  x%d..%d y%d..%d ===" % (title, x0, x1, y0, y1))
    print("      " + "".join(str(x % 10) for x in range(x0, x1 + 1)))
    for y in range(y0, y1 + 1):
        line = ""
        for x in range(x0, x1 + 1):
            if RED[y, x]:
                line += "R"
            elif GRN[y, x]:
                line += "G"
            elif BLU[y, x]:
                line += "B"
            elif NVY[y, x]:
                line += "N"
            elif DRK[y, x]:
                line += "#"
            else:
                line += "."
        print("y%4d %s" % (y, line))


def colgroups(mask, y0, y1, x0, x1, gap=2):
    row = mask[y0:y1 + 1, x0:x1 + 1].any(axis=0)
    out, s = [], None
    for i, v in enumerate(row):
        if v and s is None:
            s = i
        elif not v and s is not None:
            out.append((s + x0, i - 1 + x0)); s = None
    if s is not None:
        out.append((s + x0, x1))
    merged = []
    for g in out:
        if merged and g[0] - merged[-1][1] - 1 <= gap:
            merged[-1] = (merged[-1][0], g[1])
        else:
            merged.append(g)
    return merged


print("############ LEGEND + MID ZONE COLOUR MAP ############")
show(56, 126, 230, 600, "LEGEND+MID x230..600")

print("\n############ RED-ONLY components in panel ############")
print("red col groups x230..600:", colgroups(RED, 56, 126, 230, 600, gap=3))
print("green col groups x230..600:", colgroups(GRN, 56, 126, 230, 600, gap=3))
print("blue col groups x230..600:", colgroups(BLU, 56, 126, 230, 600, gap=3))

print("\n############ RIGHT ZONE COLOUR MAP ############")
show(60, 125, 430, 670, "RIGHT x430..670")
print("\ndark col groups x430..720:", colgroups(DRK, 60, 125, 430, 720, gap=2))

print("\n############ CLASS LABELS (left table) COLOUR ############")
print("red col groups x85..220 y108..128:", colgroups(RED, 108, 128, 85, 220, gap=2))
print("blue col groups x85..220 y108..128:", colgroups(BLU, 108, 128, 85, 220, gap=2))
show(108, 128, 85, 220, "LABELS colour")
