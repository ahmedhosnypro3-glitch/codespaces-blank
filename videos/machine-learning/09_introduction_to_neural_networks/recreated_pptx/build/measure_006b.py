#!/usr/bin/env python3
"""Precise geometry probe for slide 006 original (PIL only, no vision)."""
from PIL import Image
import numpy as np
from pathlib import Path

V = Path("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks")
a = np.array(Image.open(V / "unique_slides/slide_006.jpg").convert("RGB")).astype(int)
H, W, _ = a.shape

def near(rgb, tol):
    return np.abs(a - np.array(rgb)).sum(axis=2) <= tol

def runs_row(m, y, min_len):
    xs = np.where(m[y])[0]
    if len(xs) == 0:
        return []
    split = np.where(np.diff(xs) > 1)[0]
    return [r for r in np.split(xs, split + 1) if len(r) >= min_len]

def runs_col(m, x, min_len):
    ys = np.where(m[:, x])[0]
    if len(ys) == 0:
        return []
    split = np.where(np.diff(ys) > 1)[0]
    return [r for r in np.split(ys, split + 1) if len(r) >= min_len]

print("=== 1. equation box (white panel, x<500, y 90..235) ===")
bg = a[250, 100]  # outside box background sample
print("bg sample at (250,100):", a[250, 100], " at (500,300):", a[500, 300])
# boundary = pixel differing from local bg
reg = a[90:240, 60:500].copy()
for y in range(90, 240):
    row = a[y, 60:500]
    d = np.abs(row - a[y, 60]).sum(axis=1)
    xs = np.where(d > 90)[0]
    xs = xs[(xs > 5)]
    if len(xs) > 100:
        r = runs_row(np.ones((1, 440), bool), 0, 0)  # placeholder
        # find longest contiguous change-run
        segs = np.split(xs, np.where(np.diff(xs) > 3)[0] + 1)
        segs = [s for s in segs if len(s) > 60]
        if segs:
            s = max(segs, key=len)
            print(f"  y={y}: change-run x {60+s[0]}-{60+s[-1]} n={len(s)}")

print("\n=== 2. panel border (steel-blue thin) right region ===")
steel = near((154, 168, 224), 90)
for y in range(120, 500):
    for r in runs_row(steel, y, 200):
        print(f"  panel-top/bottom row y={y} x {r[0]}-{r[-1]}")
for x in range(380, 900):
    for r in runs_col(steel, x, 60):
        print(f"  panel-left/right col x={x} y {r[0]}-{r[-1]}")

print("\n=== 3. activation boxes: magenta border / pink fill components ===")
pink = near((255, 204, 255), 90)
mag = near((255, 68, 255), 110)
ys, xs = np.where(mag)
if len(ys):
    print(f"  magenta border ink bbox x {xs.min()}-{xs.max()} y {ys.min()}-{ys.max()} px={len(ys)}")
# cluster magenta ink by simple grid (label components by flood fill via numpy)
lab, n = None, 0
try:
    from scipy import ndimage
    lab, n = ndimage.label(mag)
    for i in range(1, n + 1):
        yy, xx = np.where(lab == i)
        if len(yy) < 40:
            continue
        print(f"  mag comp {i}: x {xx.min()}-{xx.max()} y {yy.min()}-{yy.max()} px={len(yy)}")
except ImportError:
    print("  (scipy unavailable)")

print("\n=== 4. sigma circles: cyan fill + teal outline ===")
cyan = near((204, 255, 255), 110)
try:
    from scipy import ndimage
    lab, n = ndimage.label(cyan)
    for i in range(1, n + 1):
        yy, xx = np.where(lab == i)
        if len(yy) < 100:
            continue
        print(f"  cyan comp {i}: x {xx.min()}-{xx.max()} y {yy.min()}-{yy.max()} px={len(yy)}"
              f" center ({(xx.min()+xx.max())/2:.0f},{(yy.min()+yy.max())/2:.0f})")
    teal = near((64, 160, 160), 110)
    lab, n = ndimage.label(teal)
    for i in range(1, n + 1):
        yy, xx = np.where(lab == i)
        if len(yy) < 30:
            continue
        print(f"  teal comp {i}: x {xx.min()}-{xx.max()} y {yy.min()}-{yy.max()} px={len(yy)}")
except ImportError:
    pass

print("\n=== 5. callout box: yellow fill / olive border ===")
yellow = near((255, 255, 204), 60)
try:
    from scipy import ndimage
    lab, n = ndimage.label(yellow)
    for i in range(1, n + 1):
        yy, xx = np.where(lab == i)
        if len(yy) < 300:
            continue
        print(f"  yellow comp {i}: x {xx.min()}-{xx.max()} y {yy.min()}-{yy.max()} px={len(yy)}")
    olive = near((184, 180, 0), 90)
    lab, n = ndimage.label(olive)
    for i in range(1, n + 1):
        yy, xx = np.where(lab == i)
        if len(yy) < 60:
            continue
        print(f"  olive comp {i}: x {xx.min()}-{xx.max()} y {yy.min()}-{yy.max()} px={len(yy)}")
except ImportError:
    pass

print("\n=== 6. colored fan-in lines (sample colors along diagonals) ===")
for name, rgb, tol in (("red", (204, 0, 0), 80), ("blue", (26, 52, 200), 80), ("green", (0, 166, 0), 80)):
    m = near(rgb, tol)
    # only inside diagram panel
    m[:150, :] = False
    m[:, :420] = False
    ys, xs = np.where(m)
    if len(ys) < 10:
        print(f"  {name}: none in panel")
        continue
    print(f"  {name}: x {xs.min()}-{xs.max()} y {ys.min()}-{ys.max()} px={len(ys)}")
