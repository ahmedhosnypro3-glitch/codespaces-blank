#!/usr/bin/env python3
"""Measure unique_slides/slide_004.jpg (960x540, 1px=1pt) — broad census pass 1.

Goal: locate every content element — colored box borders (red/blue/yellow),
salmon fill, text ink bands, equation ink — and dump per-region bboxes so the
build can be placed from measurement, never intuition.
"""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_004.jpg"
im = np.asarray(Image.open(F).convert("RGB")).astype(int)
H, W = im.shape[:2]
print(f"frame {W}x{H}")
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

# --- masks -------------------------------------------------------------------
# red ink (C00000 family, JPEG-darkened; r much greater than g,b)
red = (r > 100) & ((r - g) > 50) & ((r - b) > 30)
# blue ink (#0000FF family; b much greater than r)
blue = (b > 90) & ((b - r) > 50) & ((b - g) > 40)
# yellow borders (#FFFF00 family: r,g high, b low)
yellow = (r > 180) & (g > 180) & (b < 140) & (abs(r - g) < 60)
# salmon fill (#FAEBD7 family: high r, mid g, low-ish b, warm)
salmon = (r > 235) & (g > 200) & (g < 240) & (b > 180) & (b < 225) & ((r - b) > 25)
# dark ink (text): sum low
dark = (r + g + b) < 330

print("\n=== counts (frame px) ===")
for name, m in [("red", red), ("blue", blue), ("yellow", yellow), ("salmon", salmon), ("dark", dark)]:
    print(f"  {name:8s}: {int(m.sum())}")


def runs_of(mask_1d, min_len=1):
    """Return list of (start, end_inclusive) runs of True in a 1-D bool array."""
    out = []
    d = np.diff(np.concatenate(([0], mask_1d.astype(int), [0])))
    starts = np.where(d == 1)[0]
    ends = np.where(d == -1)[0] - 1
    for s, e in zip(starts, ends):
        if e - s + 1 >= min_len:
            out.append((int(s), int(e)))
    return out


def bbox_of(mask):
    ys, xs = np.where(mask)
    if not len(ys):
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def region_report(name, mask, min_area=30):
    """Connected-ish region report via row/col projections (simple, robust)."""
    if mask.sum() < min_area:
        print(f"  [{name}] empty")
        return
    x0, y0, x1, y1 = bbox_of(mask)
    print(f"  [{name}] bbox x {x0}..{x1} (w {x1-x0+1}), y {y0}..{y1} (h {y1-y0+1}), px {int(mask.sum())}")
    # row bands
    rowsum = mask.sum(axis=1)
    bands = runs_of(rowsum > 0, min_len=2)
    print(f"    row bands: {bands[:24]}{' ...' if len(bands) > 24 else ''}")
    return (x0, y0, x1, y1)


print("\n=== red ink (borders + red text + title red) ===")
region_report("red", red)
print("\n=== blue ink ===")
region_report("blue", blue)
print("\n=== yellow ink (borders) ===")
region_report("yellow", yellow)
print("\n=== salmon fill ===")
region_report("salmon", salmon)

# The house strokes are red too — separate interior-content red from stroke red
# by excluding the stroke columns/rows.
inner = np.zeros_like(red)
inner[48:536, 62:898] = red[48:536, 62:898]
print("\n=== red EXCLUDING house strokes (content red) ===")
region_report("red-content", inner)

# --- vertical structure of content: dark-ink row bands inside the panel ------
print("\n=== dark-ink row bands inside panel (x 60..900) ===")
dp = dark[:, 60:900]
rowsum = dp.sum(axis=1)
bands = runs_of(rowsum > 0, min_len=1)
for s, e in bands:
    seg = dp[s:e + 1]
    cols = np.where(seg.sum(axis=0) > 0)[0]
    print(f"  y {s}..{e} (h {e-s+1})  x {60+cols.min()}..{60+cols.max()}  px {int(seg.sum())}")

print("\n=== color samples ===")
for (x, y) in [(480, 20), (480, 535), (60, 300), (570, 300), (700, 300), (876, 73), (100, 100)]:
    print(f"  px({x},{y}) = {tuple(im[y, x])}")
