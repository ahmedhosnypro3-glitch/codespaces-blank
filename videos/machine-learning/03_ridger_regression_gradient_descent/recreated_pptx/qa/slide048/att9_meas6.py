#!/usr/bin/env python3
"""att9 measurement pass 6: residual anatomy for the rebuild.

1. 048 row-1 right side at thr<205 (paren strokes + semicolons)
2. 049 row-1 left dx column colors (paren green vs gray anchor)
3. 048 aug-box title word runs (caption fix #4)
4. 048 r1 dx digits darkest core (green pick)
5. 048 r1 result-vector digit x-centres (green 5;-1;-1)
"""
from PIL import Image
import numpy as np

DECK = "videos/machine-learning/03_ridger_regression_gradient_descent"
O48 = np.array(Image.open(f"{DECK}/unique_slides/slide_048.jpg").convert("RGB")).astype(int)
O49 = np.array(Image.open(f"{DECK}/unique_slides/slide_049.jpg").convert("RGB")).astype(int)


def runs(mask, start):
    out, s = [], None
    for i, v in enumerate(mask):
        if v and s is None:
            s = i
        elif not v and s is not None:
            out.append((start + s, start + i - 1)); s = None
    if s is not None:
        out.append((start + s, start + len(mask) - 1))
    return out


def col_bands(a, x0, x1, y0, y1, thr):
    z = a[y0:y1, x0:x1]
    m = z.sum(axis=2) < thr * 3
    res = []
    for (cx0, cx1) in runs(m.any(axis=0), x0):
        sub = m[:, cx0 - x0:cx1 - x0 + 1]
        yb = runs(sub.any(axis=1), y0)
        px = a[y0:y1, cx0:cx1 + 1][sub]
        res.append((cx0, cx1, yb, px.mean(axis=0).round().astype(int), int(len(px))))
    return res


print("===== 1. 048 row-1 RIGHT side thr<205 (x610..812, y144..196) =====")
for b in col_bands(O48, 610, 812, 144, 196, 205):
    print(f"  x{b[0]}..{b[1]} yb={b[2]} mean={tuple(b[3])} npx={b[4]}")

print("===== 1b. same but GREEN/RED classified per column =====")
z = O48[144:196, 610:812]
m = z.sum(axis=2) < 205 * 3
for x in range(610, 812):
    col = m[:, x - 610]
    if not col.any():
        continue
    px = z[:, x - 610][col]
    mean = px.mean(axis=0)
    tag = ""
    if mean[1] > mean[0] + 12 and mean[1] > mean[2] + 12:
        tag = "GREEN"
    elif mean[0] > mean[1] + 30 and mean[0] > mean[2] + 30:
        tag = "RED"
    if tag:
        yb = runs(col, 144)
        print(f"  x{x} {tag} yb={yb} mean={mean.round().astype(int)} npx={int(col.sum())}")

print("===== 2. 049 row-1 left dx column (x370..412, y143..196) thr<205 =====")
for b in col_bands(O49, 370, 412, 143, 196, 205):
    print(f"  x{b[0]}..{b[1]} yb={b[2]} mean={tuple(b[3])} npx={b[4]}")

print("===== 2b. 049 row-2 triplet bars check (x320..385, y206..263) thr<205 =====")
for b in col_bands(O49, 320, 385, 208, 262, 205):
    print(f"  x{b[0]}..{b[1]} yb={b[2]} mean={tuple(b[3])} npx={b[4]}")

print("===== 3. 048 aug title word runs (x72..245, y144..162) thr<205 =====")
z = O48[144:162, 72:245]
m = z.sum(axis=2) < 205 * 3
cols = m.any(axis=0)
print("  x-runs:", runs(cols, 72))
ys = runs(m.any(axis=1), 144)
print("  y-bands:", ys)

print("===== 3b. 049 aug title word runs (same zone) =====")
z = O49[144:162, 72:245]
m = z.sum(axis=2) < 205 * 3
print("  x-runs:", runs(m.any(axis=0), 72))
print("  y-bands:", runs(m.any(axis=1), 144))

print("===== 4. 048 r1 dx digits darkest core (x388..401, y150..194) =====")
z = O48[150:194, 388:402]
m = z.sum(axis=2) < 650
g = m & (z[:, :, 1] > z[:, :, 0] + 12) & (z[:, :, 1] > z[:, :, 2] + 12)
if g.sum():
    px = z[g]
    print(f"  npx={int(g.sum())} mean={px.mean(axis=0).round().astype(int)} "
          f"darkest={px[px.sum(axis=1).argmin()]}")
    # darkest 8 pixels
    s = px.sum(axis=1)
    idx = np.argsort(s)[:8]
    print(f"  darkest-8: {[tuple(px[i]) for i in idx]}")

print("===== 5. 048 r1 result digits per-line x-centres (x736..768) =====")
z = O48[144:196, 736:768]
m = z.sum(axis=2) < 215 * 3
for yb0, yb1 in [(150, 162), (166, 178), (182, 194)]:
    sub = m[yb0 - 144:yb1 - 144]
    xs = np.where(sub.any(axis=0))[0]
    if len(xs):
        print(f"  band y{yb0}..{yb1}: x{736 + xs.min()}..{736 + xs.max()} "
              f"centre={736 + (xs.min() + xs.max()) / 2:.1f}")

print("===== 6. 048 r1 lp/rp paren bow x per vector (thr<210, y156..190) =====")
z = O48[156:190, 615:812]
m = z.sum(axis=2) < 210 * 3
cnt = m.sum(axis=0)
for (a, b) in runs(cnt > 0, 615):
    widths = cnt[a - 615:b - 615 + 1]
    tall = [(615 + i, int(c)) for i, c in enumerate(widths) if c >= 20]
    print(f"  run x{a}..{b}: tall-cols={tall}")
