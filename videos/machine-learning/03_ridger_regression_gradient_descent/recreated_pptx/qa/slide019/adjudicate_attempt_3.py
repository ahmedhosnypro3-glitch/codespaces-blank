#!/usr/bin/env python3
"""Adjudicate the two pre-check findings against the original frame, PIL-first.

Findings under test:
  F1  test-line wrapping: render splits "Test1: x1=30,x2=15,y=60" into 2 lines
      where the original holds it on one.
  F2  missing table gridlines: original has persistent vertical/horizontal rules;
      the render draws none.

Outputs per-region ink-band measurements (row bands + x extents + dominant
colors) and vertical-stroke column profiles for BOTH images, so each finding is
either confirmed with numbers or dismissed with numbers.
"""
import sys
import numpy as np
from PIL import Image

VID = "videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = f"{VID}/unique_slides/slide_019.jpg"
RENDER = f"{VID}/recreated_pptx/qa/slide019/render_3.png"
SCALE = 2001 / 960.0  # render px per frame px

orig = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
rend = np.asarray(Image.open(RENDER).convert("RGB")).astype(int)
print(f"orig {orig.shape}  render {rend.shape}  scale {SCALE:.6f}")


def lum(a):
    return 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]


def ink_mask(a, bg=233, tol=22):
    """True where pixel is clearly not background (panel E9E9E7 -> lum 233)."""
    return np.abs(lum(a) - bg) > tol


def bands(mask, y0, y1, x0, x1, min_rows=2, gap=1):
    """Contiguous row bands with ink inside the box; returns [(y0,y1,xmin,xmax,count)]."""
    rows = mask[y0:y1, x0:x1]
    rowsum = rows.sum(axis=1)
    on = rowsum > 0
    out = []
    y = 0
    while y < len(on):
        if on[y]:
            j = y
            gaprun = 0
            while j < len(on):
                if on[j]:
                    gaprun = 0
                    j += 1
                else:
                    gaprun += 1
                    if gaprun > gap:
                        break
                    j += 1
            j -= gaprun
            if j - y >= min_rows:
                sub = rows[y:j]
                cols = np.where(sub.any(axis=0))[0]
                out.append((y0 + y, y0 + j, x0 + cols.min(), x0 + cols.max(), int(sub.sum())))
            y = j + 1
        else:
            y += 1
    return out


def dominant_colors(a, x0, y0, x1, y1, m, top=4):
    """Dominant RGB among inked px in a box (quantized to 32)."""
    sub = a[y0:y1, x0:x1].reshape(-1, 3)[m[y0:y1, x0:x1].reshape(-1)]
    if len(sub) == 0:
        return []
    q = (sub // 32) * 32
    keys, counts = np.unique(q, axis=0, return_counts=True)
    order = np.argsort(-counts)[:top]
    return [(tuple(int(v) for v in keys[i]), int(counts[i])) for i in order]


def report_bands(title, a, m, region):
    x0, y0, x1, y1 = region
    bs = bands(m, y0, y1, x0, x1)
    print(f"\n--- {title}: box x{x0}..{x1} y{y0}..{y1} ---")
    for b in bs:
        col = dominant_colors(a, b[2], b[0], b[3] + 1, b[1] + 1, m)
        cs = " ".join(f"{c}:{n}" for c, n in col)
        print(f"  y {b[0]:4d}..{b[1]:4d} (h={b[1]-b[0]:3d})  x {b[2]:4d}..{b[3]:4d}  px={b[4]:6d}  {cs}")
    return bs


def strokes(m, y0, y1, x0, x1, min_count, label):
    """Columns with >= min_count inked rows inside the box (persistent vertical rules)."""
    rows = m[y0:y1, x0:x1]
    colsum = rows.sum(axis=0)
    hits = np.where(colsum >= min_count)[0]
    # merge adjacent
    groups = []
    for h in hits:
        if groups and h - groups[-1][-1] <= 2:
            groups[-1].append(h)
        else:
            groups.append([h])
    print(f"\n--- {label}: vertical columns with >= {min_count} inked rows in y{y0}..{y1} ---")
    for g in groups:
        print(f"  x {x0+g[0]:4d}..{x0+g[-1]:4d}  rows={int(colsum[g].max())}")
    return groups


om = ink_mask(orig)
rm = ink_mask(rend)

# ── F2: gridlines over the whole table area ────────────────────────────────────
# Table region in frame px: y169..524, x54..903 (panel). Render: scale x2.084.
ox0, ox1, oy0, oy1 = 54, 903, 165, 530
rx0, rx1, ry0, ry1 = [int(round(v * SCALE)) for v in (ox0, ox1, oy0, oy1)]
strokes(om, oy0, oy1, ox0, ox1, 200, "ORIGINAL gridlines (frame px)")
strokes(rm, ry0, ry1, rx0, rx1, int(200 * SCALE), "RENDER gridlines (render px)")

# horizontal rules: rows with >= 300 inked cols across table width
def hrules(m, y0, y1, x0, x1, min_cols, label):
    rows = m[y0:y1, x0:x1]
    rowsum = rows.sum(axis=1)
    hits = np.where(rowsum >= min_cols)[0]
    groups = []
    for h in hits:
        if groups and h - groups[-1][-1] <= 2:
            groups[-1].append(h)
        else:
            groups.append([h])
    print(f"\n--- {label}: horizontal rows with >= {min_cols} inked cols ---")
    for g in groups:
        print(f"  y {y0+g[0]:4d}..{y0+g[-1]:4d}  cols={int(rowsum[g].max())}")

hrules(om, oy0, oy1, ox0, ox1, 400, "ORIGINAL hrules")
hrules(rm, ry0, ry1, rx0, rx1, int(400 * SCALE), "RENDER hrules")

# ── F1: test-line layout in the NO REG column ─────────────────────────────────
# Column NO REG: frame x124..380. First row group area y199..275.
report_bands("ORIGINAL NO REG first group", orig, om, (124, 199, 380, 275))
report_bands("RENDER  NO REG first group", rend, rm,
             (int(124 * SCALE), int(199 * SCALE), int(380 * SCALE), int(275 * SCALE)))
# Also the RIDGE 10 first group (640..904 crop region)
report_bands("ORIGINAL RIDGE10 first group", orig, om, (644, 399, 900, 460))
report_bands("RENDER  RIDGE10 first group", rend, rm,
             (int(644 * SCALE), int(399 * SCALE), int(900 * SCALE), int(460 * SCALE)))

# ── Control: outlier column + headers in both (should be 1 band each) ─────────
report_bands("ORIGINAL outlier col", orig, om, (58, 165, 124, 530))
report_bands("RENDER  outlier col", rend, rm,
             (int(58 * SCALE), int(165 * SCALE), int(124 * SCALE), int(530 * SCALE)))
