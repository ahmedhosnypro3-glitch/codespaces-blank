#!/usr/bin/env python3
"""Focused follow-up for MINOR #3 ('small green per-component figures flanking
the W labels'), slide 019 attempt-8 lane.

Two questions, both answered with phantom-trap census (>=3 px per line):
  Q1. What colour are the ORIGINAL's y-value glyphs in the disputed cells?
      (banked ledger says BLACK text; the build paints them GREEN per spec)
  Q2. Does the ORIGINAL carry green ink in the W-label zone (frame x124..206)
      that the render omits? If yes, how much, and is it glyph-like or noise?
"""
from PIL import Image
import numpy as np

Q = ("videos/machine-learning/03_ridger_regression_gradient_descent/"
     "recreated_pptx/qa/slide019")
ORIG = ("videos/machine-learning/03_ridger_regression_gradient_descent/"
        "unique_slides/slide_019.jpg")

O = np.asarray(Image.open(ORIG).convert("RGB")).astype(np.int16)
R = np.asarray(Image.open(f"{Q}/render_8.png").convert("RGB")).astype(np.int16)
SX, SY = R.shape[1] / 960.0, R.shape[0] / 540.0


def is_green(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return (g > r + 15) & (g > b + 15) & (g > 60) & (g < 230)


def is_dark(a):
    return a.mean(axis=2) < 120


print("=" * 72)
print("Q1 — colour of the y-value glyphs in the disputed NO REG cells")
print("=" * 72)
# disputed y= line bands, frame px (from the provenance diff: y356..362, y466..472)
for cy0, cy1 in ((350, 368), (460, 478)):
    ox, oy = int(210 * 1), int(cy0)
    ob = O[oy:cy1, 210:378]
    rb = R[int(cy0 * SY):int(cy1 * SY), int(210 * SX):int(378 * SX)]
    for label, band in (("original", ob), ("render_8", rb)):
        g = is_green(band)
        d = is_dark(band)
        gcols = np.nonzero(g.sum(axis=0) >= 3)[0]
        print(f"  band y{cy0}..{cy1} {label:9s}: green px={int(g.sum()):5d} "
              f"(cols>=3px: {len(gcols)})  dark px={int(d.sum()):5d}  "
              f"green/dark={g.sum() / max(1, d.sum()):.3f}")
    print()

print("=" * 72)
print("Q2 — green ink in the W-label zone (frame x124..206), per row group")
print("=" * 72)
# the three NO REG / Ridge row groups are aligned at frame y205/310/420
for gy0, gy1, name in ((200, 300, "group 1 (y205)"), (305, 405, "group 2 (y310)"),
                       (415, 515, "group 3 (y420)")):
    for label, arr, scale in (("original", O, (1.0, 1.0)),
                              ("render_8", R, (SX, SY))):
        x0, x1 = int(124 * scale[0]), int(206 * scale[0])
        y0, y1 = int(gy0 * scale[1]), int(gy1 * scale[1])
        band = arr[y0:y1, x0:x1]
        g = is_green(band)
        gcols = np.nonzero(g.sum(axis=0) >= 3)[0]
        grows = np.nonzero(g.sum(axis=1) >= 3)[0]
        print(f"  {name} {label:9s} W-zone: green px={int(g.sum()):5d} "
              f"cols>=3px={len(gcols):3d} rows>=3px={len(grows):3d}")
    print()

print("=" * 72)
print("Verdict on MINOR #3")
print("=" * 72)
print("  If the original's W-zone green is < a few dozen px per group and its")
print("  y-cells are dark (black) rather than green, the judge's 'green")
print("  per-component figures' reading is a chroma-mutated-JPEG artefact ->")
print("  INDETERMINATE at this frame quality (as the banked ledger recorded).")
print("  A build change would be drawing a defect the original lacks.")
