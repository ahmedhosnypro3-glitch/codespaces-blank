#!/usr/bin/env python3
"""Slide 041: transcribe every point pair's digits and every label glyph.

Paren-pair x-ranges are taken from the banked connected-component measurement
(dig041_run.txt) rather than re-detected, so pairing is exact.
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

LEFT = [("L1", 89, 92, 101, 103), ("L2", 111, 113, 123, 125), ("L3", 133, 135, 145, 148),
        ("L4", 155, 158, 168, 171), ("L5", 178, 181, 191, 193), ("L6", 201, 203, 213, 215)]
RIGHT = [("R1", 597, 600, 611, 612), ("R2", 621, 623, 633, 635), ("R3", 642, 645, 655, 657)]

DIGIT_BANDS = [(78, 92), (94, 111)]   # row1 / row2 windows


def art(y0, y1, x0, x1):
    return "\n".join("     y%4d %s" % (y, "".join("#" if INK[y, x] else "." for x in range(x0, x1 + 1)))
                     for y in range(y0, y1 + 1))


def bands(y0, y1, x0, x1):
    prof = INK[y0:y1 + 1, x0:x1 + 1].sum(axis=1)
    out, s = [], None
    for i, v in enumerate(prof):
        if v and s is None:
            s = i
        elif not v and s is not None:
            out.append((s + y0, i - 1 + y0)); s = None
    if s is not None:
        out.append((s + y0, y1))
    return [b for b in out if b[1] - b[0] >= 4]


for label, pairs in (("LEFT", LEFT), ("RIGHT", RIGHT)):
    print("\n########## %s POINT PAIRS ##########" % label)
    for name, l0, l1, r0, r1 in pairs:
        ix0, ix1 = l1 + 1, r0 - 1
        print("\n--- %s parens x%d..%d / x%d..%d  interior x%d..%d" % (name, l0, l1, r0, r1, ix0, ix1))
        for i, (a0, a1) in enumerate(bands(76, 112, ix0, ix1)):
            print("  band%d y%d..%d" % (i + 1, a0, a1))
            print(art(a0, a1, ix0, ix1))

print("\n########## CLASS LABELS (left table, y110..126) ##########")
for name, x0, x1 in [("c1", 90, 102), ("c2", 113, 124), ("c3", 134, 146),
                     ("c4", 157, 169), ("c5", 180, 192), ("c6", 203, 214)]:
    print("\n--- %s x%d..%d" % (name, x0, x1))
    print(art(110, 126, x0, x1))
    seg = A[110:127, x0:x1 + 1].reshape(-1, 3)
    # strongest saturated pixels
    sat = seg[(seg.max(axis=1) - seg.min(axis=1)) > 60]
    if len(sat):
        print("   saturated pixels n=%d  median=%s" % (len(sat), np.median(sat, axis=0).tolist()))
    else:
        print("   saturated pixels: none (all dark)")

print("\n########## Z LABELS (right, y62..78) ##########")
for name, x0, x1 in [("z1", 600, 612), ("z2", 622, 634), ("z3", 644, 656)]:
    print("\n--- %s x%d..%d" % (name, x0, x1))
    print(art(62, 78, x0, x1))
    seg = A[62:79, x0:x1 + 1].reshape(-1, 3)
    sat = seg[(seg.max(axis=1) - seg.min(axis=1)) > 60]
    print("   saturated n=%d median=%s" % (len(sat), np.median(sat, axis=0).tolist() if len(sat) else None))
