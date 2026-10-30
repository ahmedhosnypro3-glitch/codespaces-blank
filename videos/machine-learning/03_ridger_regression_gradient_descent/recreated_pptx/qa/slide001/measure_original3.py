#!/usr/bin/env python3
"""Component-level analysis of slide_001.jpg: per text-line ink bbox + core colors.
Settle: title color (dark red vs pink), line structure, subtitle, Prepared-By block,
Instructors block, logo panels, exact geometry for the build."""
import numpy as np
from PIL import Image
from collections import Counter

IM = np.asarray(Image.open(
    "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_001.jpg"
).convert("RGB")).astype(int)
H, W = IM.shape[:2]
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]

print("=== horizontal slices (color runs) ===")
for (label, y) in [("title L1 mid", 149), ("title L2 mid", 198), ("title L3 mid", 252),
                   ("subtitle mid", 324), ("preparedby mid", 363), ("name mid", 389),
                   ("email mid", 410), ("red@429 mid", 429), ("instr hdr mid", 458)]:
    row = IM[y]
    # find runs of non-background
    bgdist = np.minimum(np.abs(row - np.array([231, 233, 230])).sum(axis=1),
                        np.abs(row - np.array([254, 255, 253])).sum(axis=1))
    on = bgdist > 90
    runs = []
    if on.any():
        idx = np.where(on)[0]
        s = p = idx[0]
        for x in idx[1:]:
            if x - p > 6:
                runs.append((s, p)); s = x
            p = x
        runs.append((s, p))
    desc = []
    for (x0, x1) in runs[:40]:
        seg = row[x0:x1 + 1]
        core = seg[bgdist[x0:x1 + 1].argmax()]
        desc.append(f"[{x0}-{x1} core={tuple(int(v) for v in core)}]")
    print(f"{label} (y={y}): {' '.join(desc) if desc else 'clean'}")

print("\n=== per-band core color census ===")
def band_census(y0, y1, x0=None, x1=None, label=""):
    seg = IM[y0:y1 + 1, (x0 or 0):(x1 or W)]
    bgd = np.minimum(np.abs(seg - np.array([231, 233, 230])).sum(axis=2),
                     np.abs(seg - np.array([254, 255, 253])).sum(axis=2))
    m = bgd > 90
    if not m.any():
        print(f"{label}: no ink")
        return
    pxs = seg[m]
    # core = saturated, far from bg
    q = (pxs // 24 * 24)
    cnt = Counter(map(tuple, q))
    print(f"{label} y{y0}..{y1} x{(x0 or 0)}..{(x1 or W)}: inkpx={m.sum()} top: {cnt.most_common(5)}")

band_census(127, 171, label="RED band 1 (title L1)")
band_census(178, 219, label="RED band 2 (title L2)")
band_census(231, 274, label="RED band 3 (title L3)")
band_census(314, 335, label="SUBTITLE band (blue+dark)")
band_census(354, 373, label="PREPARED BY band")
band_census(378, 400, label="NAME band (center)")
band_census(404, 417, label="EMAIL band (center)")
band_census(422, 437, 80, 260, label="RED band @422..437 LEFT (x80..260)")
band_census(440, 470, 80, 600, label="INSTRUCTORS hdr band (x80..600)")
band_census(473, 535, 80, 400, label="INSTRUCTORS body band (x80..400)")
band_census(440, 535, 580, 960, label="LOGO region (x580..960)")

print("\n=== logo structure (y440..535, x580..960) ===")
seg = IM[440:536, 580:960]
sr, sg, sb = seg[:, :, 0], seg[:, :, 1], seg[:, :, 2]
teal = (sg > 120) & (sb > 120) & (sr < 110)
ys, xs = np.where(teal)
if len(ys):
    print(f"teal panel: x {580+xs.min()}..{580+xs.max()}, y {440+ys.min()}..{440+ys.max()}")
    # column profile to find panel edges precisely
    colcount = teal.sum(axis=0)
    on = np.where(colcount > 2)[0]
    print(f"teal col extent: {580+on.min()}..{580+on.max()} (w={on.max()-on.min()+1})")
    rowcount = teal.sum(axis=1)
    onr = np.where(rowcount > 2)[0]
    print(f"teal row extent: {440+onr.min()}..{440+onr.max()} (h={onr.max()-onr.min()+1})")
# right panel: what's between teal right edge and ~x881? probe fills
for (name, x, y) in [("rp1", 700, 470), ("rp2", 720, 500), ("rp3", 800, 475), ("rp4", 850, 500), ("rp5", 880, 490)]:
    print(f"logo px ({x},{y}): {tuple(int(v) for v in IM[y, x])}")

print("\n=== badge numeral check ===")
band_census(55, 92, 855, 898, label="badge window")

print("\n=== Instructors block line-by-line (x80..560) ===")
# text lines in the left-lower quadrant: all ink rows
sub = IM[440:536, 80:560]
bgd = np.minimum(np.abs(sub - np.array([231, 233, 230])).sum(axis=2),
                 np.abs(sub - np.array([254, 255, 253])).sum(axis=2))
m = bgd > 90
rows = np.where(m.any(axis=1))[0]
if len(rows):
    bands = []
    s = p = rows[0]
    for yy in rows[1:]:
        if yy - p > 3:
            bands.append((s, p)); s = yy
        p = yy
    bands.append((s, p))
    for (ry0, ry1) in bands:
        xs2 = np.where(m[ry0:ry1 + 1].any(axis=0))[0]
        pxs = sub[ry0:ry1 + 1][m[ry0:ry1 + 1]]
        cnt = Counter(map(tuple, (pxs // 24 * 24)))
        print(f"line y {440+ry0}..{440+ry1} x {80+xs2.min()}..{80+xs2.max()}: {cnt.most_common(3)}")
