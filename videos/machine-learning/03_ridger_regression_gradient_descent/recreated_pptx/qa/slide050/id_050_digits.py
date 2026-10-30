#!/usr/bin/env python3
"""Identify the math-zone digit glyphs by bitmap-clustering them against the
KNOWN digits in the top-left data table (whose values are measured directly).

Known reference digits (top-left table, rows y80..89 and y96..105):
  row1: (1) (2) (1) (5) (6) (6)   cols x88..228
  row2: (1) (1) (2) (4) (5) (6)
Reference bitmaps are extracted at the same ink threshold and compared to
each math-zone glyph by normalised overlap; the best match names the digit.
"""
import numpy as np
from PIL import Image

IMG = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_050.jpg"
a = np.asarray(Image.open(IMG).convert("RGB")).astype(int)
LUM = a.mean(axis=2)
INK = LUM < 175


def glyph(x0, y0, x1, y1):
    g = INK[y0:y1 + 1, x0:x1 + 1]
    return g


def norm(g, H=12, W=9):
    im = Image.fromarray((~g * 255).astype(np.uint8)).resize((W, H), Image.LANCZOS)
    return np.asarray(im) < 128


def sim(g1, g2):
    n1, n2 = norm(g1), norm(g2)
    return float((n1 == n2).sum()) / float(n1.size)


# ---- reference digits: top-left table cells (measured values) ----
REF = {}
TBL = {
    "1": [(88, 80, 105, 89), (88, 96, 105, 105), (110, 80, 131, 89), (110, 96, 131, 105),
          (132, 80, 153, 89), (132, 96, 153, 105)],
    "2": [(110, 80, 131, 89), (132, 96, 153, 105)],
    "4": [(155, 96, 178, 105)],
    "5": [(155, 80, 178, 89), (178, 96, 202, 105)],
    "6": [(178, 80, 202, 89), (203, 80, 226, 89), (203, 96, 226, 105)],
}
for d, boxes in TBL.items():
    REF.setdefault(d, [])
    for b in boxes:
        REF[d].append(glyph(*b))

# the reference boxes above include the parens; isolate the digit by taking the
# central ink columns of each box
def digit_only(g):
    cols = g.any(axis=0)
    xs = np.where(cols)[0]
    if len(xs) == 0:
        return g
    return g[:, xs.min():(xs.max() + 1)]


REF2 = {d: [digit_only(g) for g in gs] for d, gs in REF.items()}

# ---- math-zone digit glyphs: the Z column vector numbers ----
# G1 x641..656, G2 x664..678, G3 x686..700 ; row1 y71..77, row2 y78..84
ZGLYPHS = []
for gi, (x0, x1) in enumerate([(641, 656), (664, 678), (686, 700)], start=1):
    for ri, (y0, y1) in enumerate([(71, 77), (78, 84)], start=1):
        g = glyph(x0, y0, x1, y1)
        g = digit_only(g)
        scores = [(sim(g, r), d) for d, rs in REF2.items() for r in rs]
        scores.sort(reverse=True)
        best = scores[:3]
        ZGLYPHS.append((gi, ri, best))

for gi, ri, best in ZGLYPHS:
    print("Z%d row%d -> %s" % (gi, ri,
          ", ".join("%s:%.2f" % (d, s) for s, d in best)))

# ---- the 4/-2 stack in the Initial-W column vector ----
print()
print("Initial W column vector digits:")
for nm, (x0, y0, x1, y1) in [("row1", (338, 60, 350, 72)), ("row2", (338, 76, 350, 88)),
                             ("row3?", (338, 92, 350, 104))]:
    g = digit_only(glyph(x0, y0, x1, y1))
    scores = sorted(((sim(g, r), d) for d, rs in REF2.items() for r in rs), reverse=True)
    print("  %s -> %s" % (nm, ", ".join("%s:%.2f" % (d, s) for s, d in scores[:3])))
