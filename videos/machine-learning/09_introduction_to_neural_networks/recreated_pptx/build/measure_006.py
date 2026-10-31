#!/usr/bin/env python3
"""Measure slide 006 original frame geometry with PIL (no vision calls).

Prints bounding boxes of every colored region so the rebuild can be
pixel-matched. 1px = 1pt in the build (960x540 -> 13.33x7.5 in => 72 px/in).
"""
from PIL import Image
import numpy as np
from pathlib import Path

V = Path("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks")
im = Image.open(V / "unique_slides/slide_006.jpg").convert("RGB")
a = np.array(im).astype(int)
H, W, _ = a.shape
print(f"image {W}x{H}")


def mask_rect(rgb, tol=40):
    d = np.abs(a - np.array(rgb)).sum(axis=2)
    return d <= tol


def bbox(m, label, area_min=30):
    ys, xs = np.where(m)
    if len(ys) < area_min:
        print(f"{label:28s} MISSING ({len(ys)} px)")
        return None
    print(f"{label:28s} bbox x {xs.min():4d}-{xs.max():4d} y {ys.min():4d}-{ys.max():4d}"
          f"  (w{xs.max()-xs.min()+1} h{ys.max()-ys.min()+1}) px={len(ys)}")
    return (xs.min(), ys.min(), xs.max(), ys.max())


def rows_runs(m, label, min_len=50):
    """Rows of the mask whose run length exceeds min_len -> horizontal edge lines."""
    out = []
    for y in range(H):
        row = m[y]
        xs = np.where(row)[0]
        if len(xs) >= min_len:
            # longest contiguous run
            split = np.where(np.diff(xs) > 1)[0]
            runs = np.split(xs, split + 1)
            best = max(runs, key=len)
            out.append((y, best[0], best[-1]))
    if out:
        ys = [r[0] for r in out]
        x0 = min(r[1] for r in out)
        x1 = max(r[2] for r in out)
        print(f"{label:28s} rows y {min(ys)}-{max(ys)} (n={len(out)}) x {x0}-{x1}")
    else:
        print(f"{label:28s} none")


print("\n== frame / panels ==")
bbox(mask_rect((214, 75, 126), 60), "magenta frame")
bbox(mask_rect((255, 255, 204), 40), "callout yellow")
rows_runs(mask_rect((154, 168, 224), 70), "panel steel-blue rows")
bbox(mask_rect((154, 168, 224), 70), "panel steel-blue")
bbox(mask_rect((255, 204, 255), 40), "activation pink", area_min=100)
bbox(mask_rect((204, 255, 255), 30), "sigma cyan", area_min=100)
bbox(mask_rect((0, 0, 238), 60), "step-glyph blue", area_min=30)
bbox(mask_rect((204, 0, 0), 60), "red ink", area_min=30)
bbox(mask_rect((26, 52, 200), 60), "blue weight ink", area_min=30)
bbox(mask_rect((0, 166, 0), 60), "green weight ink", area_min=30)

print("\n== equation box: pink/rose border runs by region (x<500, y 80-240) ==")
rose = mask_rect((214, 75, 126), 70)
sub = rose[80:240, 60:520]
ys, xs = np.where(sub)
print("rose ink in region:", "x", 60 + xs.min(), "-", 60 + xs.max(),
      "y", 80 + ys.min(), "-", 80 + ys.max(), "px", len(ys))
# horizontal border rows
for y in range(80, 240):
    xs = np.where(rose[y])[0]
    if len(xs) > 200:
        print(f"  row y={y} x {xs.min()}-{xs.max()} n={len(xs)}")
for x in range(60, 520):
    ys2 = np.where(rose[:, x])[0]
    if len(ys2) > 80:
        print(f"  col x={x} y {ys2.min()}-{ys2.max()} n={len(ys2)}")

print("\n== dark text ink per region (original text, excluding black letterbox) ==")
dark = (a.sum(axis=2) < 240)
dark[487:, :] = False  # drop black capture band

def region_ink(label, x0, x1, y0, y1):
    m = dark[y0:y1, x0:x1]
    ys, xs = np.where(m)
    if len(ys) == 0:
        print(f"{label:34s} no ink")
        return
    print(f"{label:34s} x {x0+xs.min():4d}-{x0+xs.max():4d} y {y0+ys.min():4d}-{y0+ys.max():4d} px={len(ys)}")

region_ink("title", 0, 960, 40, 95)
region_ink("equation line1", 60, 500, 100, 130)
region_ink("equation line2", 60, 500, 135, 170)
region_ink("equation line3", 60, 500, 175, 215)
region_ink("class label", 100, 420, 340, 430)
region_ink("input column", 390, 440, 150, 460)
region_ink("class labels right", 740, 860, 150, 460)

print("\n== done ==")
