#!/usr/bin/env python3
"""Detect slide_024 panel border rectangles precisely (per border color)."""
from PIL import Image
import numpy as np

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
o = np.array(Image.open(V + "/unique_slides/slide_024.jpg").convert("RGB")).astype(int)
H, W, _ = o.shape
r, g, b = o[:, :, 0], o[:, :, 1], o[:, :, 2]

def near(hexc, tol=42):
    c = np.array([int(hexc[i:i+2], 16) for i in (1, 3, 5)])
    d = np.abs(o - c).sum(axis=2)
    return d < tol

for label, hexc in [("pink#FF7C80", "#FF7C80"), ("blue#4472C4", "#4472C4"),
                    ("gray#BFBFBF", "#BFBFBF"), ("orange#ED7D31", "#ED7D31"),
                    ("orange2#E36C0A", "#E36C0A")]:
    m = near(hexc)
    ys, xs = np.nonzero(m)
    if not len(xs):
        print(f"{label}: none n=0"); continue
    # row/col profile to isolate panel borders (long runs)
    rowsum = m.sum(axis=1); colsum = m.sum(axis=0)
    rows = np.nonzero(rowsum > 40)[0]
    cols = np.nonzero(colsum > 15)[0]
    print(f"{label}: n={len(xs)} bbox x={xs.min()}..{xs.max()} y={ys.min()}..{ys.max()}")
    if len(rows):
        # group contiguous rows
        grp, start = [], rows[0]
        for i in range(1, len(rows)):
            if rows[i] - rows[i-1] > 3:
                grp.append((start, rows[i-1])); start = rows[i]
        grp.append((start, rows[-1]))
        print(f"   long-row groups: {grp}")
    if len(cols):
        grp, start = [], cols[0]
        for i in range(1, len(cols)):
            if cols[i] - cols[i-1] > 3:
                grp.append((start, cols[i-1])); start = cols[i]
        grp.append((start, cols[-1]))
        print(f"   long-col groups: {grp}")

# white fill panels (P3, P4, P6, P2)
print("\n=== white-fill panel bboxes (r>246,g>246,b>246) ===")
wm = (r > 246) & (g > 246) & (b > 246)
# restrict to interior of the frame, y 95..480
sub = wm[95:480, 70:900]
ys, xs = np.nonzero(sub)
print("white total bbox x", xs.min()+70, "..", xs.max()+70, " y", ys.min()+95, "..", ys.max()+95)
# connected-ish: per-row extents
for y in [105, 125, 175, 200, 220, 250, 300, 340, 370, 400, 440, 465]:
    row = wm[y, 70:900]
    xx = np.nonzero(row)[0]
    if len(xx):
        # groups
        grp, st = [], xx[0]
        for i in range(1, len(xx)):
            if xx[i] - xx[i-1] > 4:
                grp.append((st+70, xx[i-1]+70)); st = xx[i]
        grp.append((st+70, xx[-1]+70))
        print(y, grp)
