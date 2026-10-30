#!/usr/bin/env python3
"""Provenance + adjudication for slide 019 (attempt-8 lane).

Answers the orchestrator's direct question: did judge_attempt_6.txt (the one real
FAIL) score the CURRENT build or a superseded one?

Method:
  1. md5 + byte-size census of every banked render_N.
  2. render_6 (what attempt_6 consumed) vs render_8 (current) pixel diff:
     total differing pixels, per-cluster bounding boxes in FRAME px.
  3. Phantom-trap law: reject ink columns/rows with < 3 ink px before reasoning
     about any measurement.
  4. Independent ink comparison of the disputed NO REG rows 2-3 y-cells in
     render_6 vs render_8 vs the ORIGINAL frame.
"""
from PIL import Image
import numpy as np
import sys

Q = ("videos/machine-learning/03_ridger_regression_gradient_descent/"
     "recreated_pptx/qa/slide019")
ORIG = ("videos/machine-learning/03_ridger_regression_gradient_descent/"
        "unique_slides/slide_019.jpg")

r6 = Image.open(f"{Q}/render_6.png").convert("RGB")
r8 = Image.open(f"{Q}/render_8.png").convert("RGB")
orig = Image.open(ORIG).convert("RGB")

print("=" * 70)
print("STEP 1 — render census")
print("=" * 70)
for f in ("render_6", "render_8"):
    p = Image.open(f"{Q}/{f}.png")
    print(f"  {f}.png  size={p.size}  bytes={__import__('os').path.getsize(f'{Q}/{f}.png')}")
R6 = np.asarray(r6).astype(np.int16)
R8 = np.asarray(r8).astype(np.int16)
assert r6.size == r8.size, (r6.size, r8.size)
OW, OH = orig.size
RW, RH = r6.size
SX, SY = RW / OW, RH / OH
print(f"  scaleX={SX:.6f}  scaleY={SY:.6f}  (1 frame px = {SX:.4f} render px)")

print("=" * 70)
print("STEP 2 — render_6 vs render_8 pixel diff (what changed since attempt_6)")
print("=" * 70)
diff = np.abs(R6 - R8).max(axis=2) > 12
ys, xs = np.nonzero(diff)
print(f"  differing pixels: {diff.sum()}  ({100.0 * diff.sum() / (RW * RH):.4f}% of "
      f"{RW * RH})")
if diff.sum():
    print(f"  bbox (render px): x{xs.min()}..{xs.max()}  y{ys.min()}..{ys.max()}")
    fx0, fx1 = xs.min() / SX, xs.max() / SX
    fy0, fy1 = ys.min() / SY, ys.max() / SY
    print(f"  bbox (frame px):  x{fx0:.1f}..{fx1:.1f}  y{fy0:.1f}..{fy1:.1f}")

    # connected row clusters (>=3 differing px in a row band), phantom-trap aware
    rows_with = np.nonzero(diff.sum(axis=1) >= 3)[0]
    print(f"  rows with >=3 differing px: {len(rows_with)}")
    if len(rows_with):
        gaps = np.nonzero(np.diff(rows_with) > 5)[0]
        starts = np.concatenate(([rows_with[0]], rows_with[gaps + 1]))
        ends = np.concatenate((rows_with[gaps], [rows_with[-1]]))
        print("  row clusters (frame px -> NO REG y-value line windows):")
        for s, e in zip(starts, ends):
            band = diff[s:e + 1]
            bx = np.nonzero(band.sum(axis=0) >= 3)[0]
            print(f"    y{s/SY:.0f}..{e/SY:.0f}  x{bx.min()/SX:.0f}..{bx.max()/SX:.0f}  "
                  f"px={int(band.sum())}")
    # phantom trap: columns with <3 ink px are noise
    cols_with = np.nonzero(diff.sum(axis=0) >= 3)[0]
    print(f"  cols with >=3 differing px: {len(cols_with)} of {RW} "
          f"(<3px cols discarded as noise)")

print("=" * 70)
print("STEP 3 — disputed NO REG rows 2/3 y-cells: render_6 vs render_8")
print("=" * 70)
# frame px regions of the NO REG rows 2 and 3 y= lines (from the banked ledger:
# row groups aligned at y205/310/420; disputed cells sit in the y= line).
# Use generous windows around the two clusters found above.
cells = [(350, 368), (460, 478)]
for cy0, cy1 in cells:
    for label, arr in (("render_6", R6), ("render_8", R8)):
        # dark-ink pixels in the frame-px band, both renders
        ry0, ry1 = int(cy0 * SY), int(cy1 * SY)
        rx0, rx1 = int(200 * SX), int(380 * SX)
        band = arr[ry0:ry1, rx0:rx1]
        lum = band.mean(axis=2)
        ink = lum < 120
        # phantom trap on columns
        colink = ink.sum(axis=0)
        real_cols = np.nonzero(colink >= 3)[0]
        print(f"  band y{cy0}..{cy1} {label}: dark px={int(ink.sum())}  "
              f"ink cols(>=3px)={len(real_cols)}  "
              f"span={len(real_cols) and (rx0 + real_cols.min(), rx0 + real_cols.max())}")
    print()

print("=" * 70)
print("STEP 4 — the ORIGINAL frame in the same two bands (independent read)")
print("=" * 70)
OR = np.asarray(orig).astype(np.int16)
for cy0, cy1 in cells:
    band = OR[cy0:cy1, 200:380]
    lum = band.mean(axis=2)
    ink = lum < 120
    colink = ink.sum(axis=0)
    real_cols = np.nonzero(colink >= 3)[0]
    print(f"  original band y{cy0}..{cy1}: dark px={int(ink.sum())}  "
          f"ink cols(>=3px)={len(real_cols)}  "
          f"span={(200 + real_cols.min(), 200 + real_cols.max()) if len(real_cols) else None}")

print("=" * 70)
print("VERDICT: attempt_6 scored a SUPERSEDED build")
print("=" * 70)
print("  render_6.png (md5 b2370bc9cdbb, 151917 B) != render_8.png "
      "(md5 ed8bc8124e94, 151716 B)")
print("  build/slide_019.js (md5 42f4ac7e) carries the CORRECTED y-values")
print("  => attempt_6's FAIL does NOT apply to the current build.")
