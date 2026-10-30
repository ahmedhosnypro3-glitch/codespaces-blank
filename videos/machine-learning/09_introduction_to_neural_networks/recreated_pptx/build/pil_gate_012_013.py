"""Objective pre-check gate: measured facts, render-vs-original.

Per visual-judge doctrine, mechanical measurements are banked before any
vision call. Vision-model claims that contradict a measured value are
adjudicated as HIGH findings.
"""
from PIL import Image
import numpy as np
import os
import json

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
ORIG = f"{BASE}/unique_slides"
REND = f"{BASE}/recreated_pptx/build"
OUT = f"{BASE}/recreated_pptx/build"

def px(v, total):
    return v / total


def census(path, n=32, label=""):
    """Dominant-color census of an image at coarse quantization."""
    a = np.array(Image.open(path).convert("RGB").resize((160, 90)))
    q = (a // 24 * 24).reshape(-1, 3)
    import collections
    c = collections.Counter(map(tuple, q))
    return c.most_common(n)


def measure(num, label, regions):
    """Measure region occupancy in the original and the render."""
    o = Image.open(f"{ORIG}/slide_{num:03d}.jpg").convert("RGB")
    r = Image.open(f"{REND}/slide_{num:03d}_rendered.png").convert("RGB")
    oW, oH = o.size
    rW, rH = r.size
    print(f"\n{'='*60}\n{label} (slide_{num:03d})\n  orig {oW}x{oH}  rendered {rW}x{rH}")
    oa = np.array(o).astype(int)
    ra = np.array(r).astype(int)

    facts = {}

    # 1. Background mean (should be light gray ~E6/E8)
    facts["orig_bg_mean"] = [round(float(x), 1) for x in oa.mean(axis=(0, 1))]
    facts["rend_bg_mean"] = [round(float(x), 1) for x in ra.mean(axis=(0, 1))]

    # 2. House frame: detect near-bg-colored long horizontal/vertical runs
    #    Non-gray pixels = frame ink
    for name, arr, W, H in (("orig", oa, oW, oH), ("rend", ra, rW, rH)):
        gray = np.abs(arr.max(axis=2) - arr.min(axis=2)) < 14  # achromatic
        notgray = ~gray
        hcols = [x for x in range(W) if notgray[:, x].sum() > H * 0.55]
        hrows = [y for y in range(H) if notgray[y, :].sum() > W * 0.55]
        facts[f"{name}_frame_vcols"] = (min(hcols), max(hcols)) if hcols else None
        facts[f"{name}_frame_hrows"] = (min(hrows), max(hrows)) if hrows else None

    # 3. Region checks: for each expected region, confirm the RED frame ink exists
    for region_name, (x0, y0, x1, y1), expected in regions:
        ox0, ox1 = int(x0 * oW), int(x1 * oW)
        oy0, oy1 = int(y0 * oH), int(y1 * oH)
        rx0, rx1 = int(x0 * rW), int(x1 * rW)
        ry0, ry1 = int(y0 * rH), int(y1 * rH)
        oR = np.abs(oa[oy0:oy1, ox0:ox1] - outer_box(ox0, ox1, oy0, oy1, oW, oH, oa))
        print(f"  region {region_name}: orig x[{x0:.2f}-{x1:.2f}] y[{y0:.2f}-{y1:.2f}] -> "
              f"px x[{ox0}-{ox1}] y[{oy0}-{oy1}]")

    # 4. Table cell-fill colors: sample expected highlight pixels
    return facts


def outer_box(x0, x1, y0, y1, W, H, arr):
    return arr[y0:y1, x0:x1].reshape(-1, 3).mean(axis=0)


def sample_table_cell(path, num, row, col, ncols=3, nrows=5,
                      tx0=0.10, tx1=0.33, ty0=0.25, ty1=0.58):
    """Sample the O/P highlight cell of a table."""
    im = Image.open(path).convert("RGB")
    W, H = im.size
    a = np.array(im).astype(int)
    cw = (tx1 - tx0) / ncols
    ch = (ty1 - ty0) / nrows
    cx0 = tx0 + col * cw
    cy0 = ty0 + row * ch
    x0, x1 = int((cx0 + 0.1 * cw) * W), int((cx0 + 0.9 * cw) * W)
    y0, y1 = int((cy0 + 0.2 * ch) * H), int((cy0 + 0.8 * ch) * H)
    patch = a[y0:y1, x0:x1]
    return [round(float(v), 1) for v in patch.mean(axis=(0, 1))]


# ---- slide 012 ----
print("=" * 60)
print("SLIDE 012 - objective pre-check gate")
print("=" * 60)
print("\n[orig] truth-table O/P cell fills (rows 1-4, col 2):")
for row in range(1, 5):
    m = sample_table_cell(f"{ORIG}/slide_012.jpg", 12, row, 2)
    print(f"  row {row}: RGB {m}")
print("\n[rend] truth-table O/P cell fills (rows 1-4, col 2):")
for row in range(1, 5):
    m = sample_table_cell(f"{REND}/slide_012_rendered.png", 12, row, 2)
    print(f"  row {row}: RGB {m}")

# frame check
oa = np.array(Image.open(f"{ORIG}/slide_012.jpg").convert("RGB")).astype(int)
ra = np.array(Image.open(f"{REND}/slide_012_rendered.png").convert("RGB")).astype(int)
oHb, oWb = oa.shape[:2]
rHb, rWb = ra.shape[:2]
def frame_pixels(a, W, H, label):
    gray = np.abs(a.max(axis=2) - a.min(axis=2)) < 20
    ng = ~gray
    vcols = [x for x in range(W) if ng[:, x].sum() > H * 0.60]
    hrows = [y for y in range(H) if ng[y, :].sum() > W * 0.60]
    print(f"  {label}: vertical frame cols {vcols[:4]}{'...' if len(vcols)>4 else ''} count={len(vcols)}; "
          f"horizontal frame rows {hrows[:4]}{'...' if len(hrows)>4 else ''} count={len(hrows)}")
    if vcols:
        print(f"    left frame x = {vcols[0]/W*13.333:.3f} in ; right frame x = {vcols[-1]/W*13.333:.3f} in")
    if hrows:
        print(f"    top frame y = {hrows[0]/H*7.5:.3f} in ; bottom frame y = {hrows[-1]/H*7.5:.3f} in")
    return vcols, hrows

print("\n[orig] frame ink columns/rows:")
frame_pixels(oa, oWb, oHb, "orig")
print("[rend] frame ink columns/rows:")
frame_pixels(ra, rWb, rHb, "rend")

# ---- slide 013 ----
print("\n" + "=" * 60)
print("SLIDE 013 - objective pre-check gate")
print("=" * 60)
print("\n[orig] truth-table O/P cell fills (rows 1-4, col 2):")
for row in range(1, 5):
    m = sample_table_cell(f"{ORIG}/slide_013.jpg", 13, row, 2)
    print(f"  row {row}: RGB {m}")
print("\n[rend] truth-table O/P cell fills (rows 1-4, col 2):")
for row in range(1, 5):
    m = sample_table_cell(f"{REND}/slide_013_rendered.png", 13, row, 2)
    print(f"  row {row}: RGB {m}")

oa = np.array(Image.open(f"{ORIG}/slide_013.jpg").convert("RGB")).astype(int)
ra = np.array(Image.open(f"{REND}/slide_013_rendered.png").convert("RGB")).astype(int)
oHb, oWb = oa.shape[:2]
rHb, rWb = ra.shape[:2]
print("\n[orig] frame ink columns/rows:")
frame_pixels(oa, oWb, oHb, "orig")
print("[rend] frame ink columns/rows:")
frame_pixels(ra, rWb, rHb, "rend")
