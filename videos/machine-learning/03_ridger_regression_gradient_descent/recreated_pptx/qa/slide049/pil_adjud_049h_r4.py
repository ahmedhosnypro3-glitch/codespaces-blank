#!/usr/bin/env python3
# Round 4: Initial-W column values, label, top-table paren runs, box extent,
# render d(x1) PNG bounds, render REPEAT wrap.
import numpy as np
from PIL import Image
from collections import deque

DECK = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = DECK + "/recreated_pptx/qa/slide049"
orig = np.asarray(Image.open(DECK + "/unique_slides/slide_049.jpg").convert("RGB")).astype(int)
rend = np.asarray(Image.open(QA + "/render_9.png").convert("RGB")).astype(int)
H, W = orig.shape[:2]
rh, rw = rend.shape[:2]
sx, sy = rw / W, rh / H
olum = (orig[:, :, 0] * 299 + orig[:, :, 1] * 587 + orig[:, :, 2] * 114) // 1000
rlum = (rend[:, :, 0] * 299 + rend[:, :, 1] * 587 + rend[:, :, 2] * 114) // 1000
x0s = np.minimum((np.arange(W) * sx).astype(int), rw - 1)
y0s = np.minimum((np.arange(H) * sy).astype(int), rh - 1)
rmin = np.minimum.reduceat(np.minimum.reduceat(rlum, y0s, axis=0), x0s, axis=1)
r_ink = rmin < 150
o_ink = olum < 205


def dump(ink, x0, x1, y0, y1, label):
    print(f"\n--- {label} frame x{x0}..{x1} y{y0}..{y1} ---")
    print("     " + "".join(str((x // 10) % 10) if x % 10 == 0 else " " for x in range(x0, x1)))
    print("     " + "".join("." if x % 10 else "+" for x in range(x0, x1)))
    for y in range(y0, y1):
        print(f"{y:4d} " + "".join("#" if ink[y, x] else "." for x in range(x0, x1)))


# 1) Initial column values, zoomed
dump(o_ink, 326, 356, 56, 108, "R4 ORIG Initial column values")
# 2) Initial label
dump(o_ink, 358, 430, 56, 80, "R4 ORIG Initial label")
# 3) top-table col-1 paren continuity: longest vertical run per column x85..110, y74..127
print("\n--- R4 ORIG top-table col1 vertical runs y74..127 ---")
for x in range(85, 112):
    col = o_ink[74:127, x]
    run = best = 0
    for v in col:
        run = run + 1 if v else 0
        best = max(best, run)
    if best >= 5:
        print(f"  x{x}: run={best}")
# 4) box rules right extent
print("\n--- R4 ORIG rule extents ---")
for yy in (54, 55, 56, 128, 129, 130, 140, 197, 206):
    xs = np.where(o_ink[yy, :])[0]
    if len(xs):
        print(f"  y{yy}: x{xs.min()}..{xs.max()} n={len(xs)}")
# vertical borders of top zone and calc table
for xx in (70, 71, 274, 775, 776, 777, 778, 779, 780):
    ys = np.where(o_ink[40:510, xx])[0]
    if len(ys) > 30:
        print(f"  x{xx}: y{40+ys.min()}..{40+ys.max()} n={len(ys)}")
# 5) render d(x1) matrix PNG bounds (tall comps)
print("\n--- R4 RENDER d(x1) row1 ink clusters y142..196 ---")
sp = []
cur = None
for x in range(276, 700):
    n = int(r_ink[142:196, x].sum())
    if n:
        if cur is None:
            cur = [x, x]
        else:
            cur[1] = x
    else:
        if cur is not None:
            sp.append(cur)
            cur = None
if cur:
    sp.append(cur)
print("  " + "  ".join(f"x{s[0]}..{s[1]}" for s in sp))
# 6) render REPEAT zone
dump(r_ink, 415, 560, 50, 85, "R4 RENDER REPEAT zone")
dump(o_ink, 415, 560, 50, 85, "R4 ORIG REPEAT zone")
# 7) render row-box check: any horizontal rule y135..505 x300..780?
rows = []
for y in range(135, 505):
    seg = r_ink[y, 300:780]
    run = best = 0
    for v in seg:
        run = run + 1 if v else 0
        best = max(best, run)
    if best >= 100:
        rows.append(y)
print("\n--- R4 RENDER horizontal runs>=100 x300..780 ---", rows if rows else "none")
# 8) orig: does the top table have tall parens on EVERY value column? scan x86..232
print("\n--- R4 ORIG top-table tall verticals (run>=25) y74..127, x86..232 ---")
sp = []
for x in range(86, 232):
    col = o_ink[74:127, x]
    run = best = 0
    for v in col:
        run = run + 1 if v else 0
        best = max(best, run)
    if best >= 25:
        if sp and x == sp[-1][1] + 1:
            sp[-1][1] = x
        else:
            sp.append([x, x])
print("  " + "  ".join(f"x{s[0]}..{s[1]}" for s in sp) if sp else "  none")
# 9) augmented table tall paren span exact
print("\n--- R4 ORIG aug-table tall verticals (run>=25) y176..228, x86..232 ---")
sp = []
for x in range(86, 232):
    col = o_ink[176:228, x]
    run = best = 0
    for v in col:
        run = run + 1 if v else 0
        best = max(best, run)
    if best >= 25:
        if sp and x == sp[-1][1] + 1:
            sp[-1][1] = x
        else:
            sp.append([x, x])
print("  " + "  ".join(f"x{s[0]}..{s[1]}" for s in sp) if sp else "  none")
