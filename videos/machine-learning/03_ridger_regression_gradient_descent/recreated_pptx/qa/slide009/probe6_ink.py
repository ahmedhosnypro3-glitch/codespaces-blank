#!/usr/bin/env python3
"""Probe 6: locate annotation-box borders (dark navy strokes) + full element map."""
import numpy as np
from PIL import Image
from collections import Counter

FRAME = ("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
         "03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg")
a = np.asarray(Image.open(FRAME).convert("RGB")).astype(int)
H, W = a.shape[:2]
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def runs(idx, gap=1):
    idx = [int(v) for v in idx]
    if not idx:
        return []
    out, s, p = [], idx[0], idx[0]
    for v in idx[1:]:
        if v <= p + gap:
            p = v
            continue
        out.append((s, p))
        s = p = v
    out.append((s, p))
    return out

# "not near-white and not panel-gray and not faint" = strong ink
ink = ~(((r > 245) & (g > 243) & (b > 240)) |
        ((abs(r - 233) < 12) & (abs(g - 231) < 14) & (abs(b - 230) < 16)))

print("=== ROW scan: strong-ink runs at key rows ===")
for y in (100, 105, 106, 108, 110, 115, 130, 145, 150, 155, 158, 160, 165, 170,
          175, 178, 180, 182, 185, 190, 195, 240, 300, 380, 430, 433, 434, 436,
          440, 460, 470, 475, 480, 488, 490, 495, 500, 505, 510, 515, 519, 521,
          526, 530):
    xs = np.where(ink[y])[0]
    print(f"  y={y:3d}: {runs(xs, gap=2)}")

print("\n=== COL scan: strong-ink runs at key cols ===")
for x in (56, 60, 70, 90, 94, 96, 100, 110, 126, 150, 200, 250, 300, 350, 400,
          440, 450, 460, 466, 470, 480, 490, 500, 540, 560, 600, 650, 700, 750,
          800, 850, 870, 900):
    ys = np.where(ink[:, x])[0]
    print(f"  x={x:3d}: {runs(ys, gap=2)}")

print("\n=== Find the navy/blue border strokes of annotation boxes ===")
# navy-ish: blue dominant, darkish
navy = (b - r > 30) & (b > 60) & (b < 200) & (r < 160)
print("  navy-ish px:", int(navy.sum()))
for nm, c0, c1 in (("LEFT", 60, 470), ("RIGHT", 480, 910)):
    m = navy[:, c0:c1]
    ys, xs = np.where(m)
    if len(ys):
        print(f"  {nm}: bbox x {xs.min()+c0}..{xs.max()+c0} y {ys.min()}..{ys.max()} n={len(ys)}")
# long vertical navy runs
nc = navy.sum(axis=0)
print("  navy cols >15: {[(x,int(nc[x])) for x in range(W) if nc[x] > 15]}")
nr = navy.sum(axis=1)
print("  navy rows >15: {[(y,int(nr[y])) for y in range(H) if nr[y] > 15]}")

print("\n=== Full strong-ink element map (coarse 8px blocks) ===")
for y0 in range(45, 540, 8):
    row = ""
    for x0 in range(0, W, 8):
        blk = ink[y0:y0 + 8, x0:x0 + 8]
        row += "#" if blk.mean() > 0.35 else ("+" if blk.mean() > 0.08 else " ")
    print(f"{y0:4d}|{row}|")

print("\n=== Colors of the long vertical navy strokes ===")
for x in (94, 95, 96, 97):
    col = a[:, x]
    dark = [(y, tuple(int(v) for v in col[y])) for y in range(H) if col[y].sum() < 500]
    print(f"  x={x}: {dark[:40]}")

print("\n=== LEFT box right edge: strong ink at row 170 x>300 ===")
for y in (160, 170, 175):
    xs = np.where(ink[y, 250:470])[0] + 250
    print(f"  y={y}: {runs(xs, gap=2)}")

print("\n=== RIGHT box edges at rows 150..180 ===")
for y in (150, 160, 170, 180):
    xs = np.where(ink[y, 480:910])[0] + 480
    print(f"  y={y}: {runs(xs, gap=2)}")

print("\n=== TOP of boxes: scan rows 90..115 for long horizontal dark runs ===")
for y in range(90, 120):
    xs = np.where(navy[y])[0]
    if len(xs) > 10:
        print(f"  y={y}: navy cols {runs(xs, gap=2)}")
print("  --- bottom of boxes ---")
for y in range(170, 200):
    xs = np.where(navy[y])[0]
    if len(xs) > 10:
        print(f"  y={y}: navy cols {runs(xs, gap=2)}")
