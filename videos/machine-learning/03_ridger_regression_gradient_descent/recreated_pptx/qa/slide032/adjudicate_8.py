#!/usr/bin/env python3
"""Adjudicate the 4 residual render_6 selfcheck items PIL-first against BOTH images.

Every gate below is a RELATIVE / local-contrast test with the ORIGINAL measured in
the SAME window, so probe artifacts (window overlap with legitimately-inked regions,
absolute-threshold blindness on 0.5pt antialiased lines) cannot masquerade as defects.
"""
import numpy as np
from collections import Counter
from PIL import Image

V = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = V + "/unique_slides/slide_032.jpg"
REND = V + "/recreated_pptx/qa/slide032/render_6.png"

o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
r = np.asarray(Image.open(REND).convert("RGB")).astype(int)
S = r.shape[0] / 540.0
print(f"render {r.shape[1]}x{r.shape[0]}  scale={S:.4f}\n")

fails = []


def sub(im, x0, y0, x1, y1):
    sc = im.shape[0] / 540.0
    return im[int(y0 * sc):int(y1 * sc), int(x0 * sc):int(x1 * sc)]


def lum(a):
    return 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]


# ---------------------------------------------------------------- 1. tick labels
# The old window x556..826 y274..295 overlapped (a) the extended plot area on the
# right and (b) the right end of box3's pink band. Census the whole band per-column
# so each ink cluster is attributed to a feature instead of one aggregate count.
print("=== 1. TICK-LABEL ZONE — column census, render vs original ===")
for tag, im in (("ORIG", o), ("REND", r)):
    band = sub(im, 540, 270, 840, 300)
    sat = band.max(axis=2) - band.min(axis=2)
    ink = (sat > 45) | (band.max(axis=2) < 110)
    cols = ink.sum(axis=0)
    nz = np.nonzero(cols)[0]
    if len(nz):
        print(f"  {tag}: ink cols {len(nz)} (of {band.shape[1]}), "
              f"col ink min/max/median = {cols[nz].min()}/{cols[nz].max()}/{int(np.median(cols[nz]))}")
        # cluster contiguous runs
        runs, start = [], nz[0]
        for a, b in zip(nz, nz[1:]):
            if b - a > 3:
                runs.append((start, a)); start = b
        runs.append((start, nz[-1]))
        print(f"       clusters: {[(int(s)/S + 540, int(e)/S + 540) for s, e in runs]}")
    else:
        print(f"  {tag}: NO ink at all")

print("\n  per-column ORIG vs REND side by side (frame x -> ink px):")
o_band = sub(o, 540, 270, 840, 300); r_band = sub(r, 540, 270, 840, 300)
def colink(b):
    s = b.max(axis=2) - b.min(axis=2)
    return ((s > 45) | (b.max(axis=2) < 110)).sum(axis=0)
ci_o, ci_r = colink(o_band), colink(r_band)
for i in range(0, r_band.shape[1], 10):
    xa = int(i / S) + 540
    print(f"    x{xa:>4}: ORIG {ci_o[i]:>3}   REND {ci_r[i]:>3}")
rows_same = int((np.abs(ci_o.astype(float) - ci_r.astype(float)) < 40).sum())
print(f"  columns within +-40 ink px of the ORIGINAL: {rows_same}/{r_band.shape[1]}")

# ---------------------------------------------------------------- 2. gridlines
# 0.5pt D9D9D9 lines antialias to ~1px and are NOT below an absolute 240 threshold.
# Local test: a column/row is a gridline if it is darker than its horizontal
# neighbourhood median, applied identically to both images.
print("\n=== 2. GRIDLINES below the x-axis — local-contrast test ===")
print("  measured frame y: -1 -> 277.5, -2 -> 289.5, -3 -> 301.5 (SY=12)")
for y_exp in (277.5, 289.5, 301.5):
    print(f"\n  gridline y={y_exp}:")
    for tag, im in (("ORIG", o), ("REND", r)):
        y0, y1 = y_exp - 3, y_exp + 4
        band = sub(im, 600, y0, 800, y1)
        L = lum(band)
        med = np.median(L, axis=1, keepdims=True)
        # a row is a gridline if its mean luminance sits >6 below the band median
        dev = med - L.mean(axis=1)
        rows = [int(i / S) + int(y0 * S) // int(S) for i in np.nonzero(dev > 6)[0]]
        best = int(np.argmax(dev))
        print(f"    {tag}: max dev {dev.max():5.1f} at frame y={y0 + best/S:6.2f}"
              f"   rows>6dev={len(rows)}  bandLmin={L.min():.0f} bandLmax={L.max():.0f}")

# white interior below the axis — relative check
print("\n  white interior continuity below the x-axis (y267..306, x610..790):")
for tag, im in (("ORIG", o), ("REND", r)):
    band = sub(im, 610, 267, 790, 306)
    L = lum(band)
    near = (L > 235).sum()
    print(f"    {tag}: near-white px {near}/{L.size} ({100*near/L.size:.1f}%)")

# ---------------------------------------------------------------- 3. box2 borders
# Measured: box2 green 1pt borders at y234 and y279, x370..540 (frame px).
print("\n=== 3. BOX2 GREEN 1PT BORDERS ===")
for tag, im in (("ORIG", o), ("REND", r)):
    band = sub(im, 360, 228, 550, 240)
    g = band[:, :, 1] - band[:, :, 0]
    g2 = band[:, :, 1] - band[:, :, 2]
    m = (g > 18) & (g2 > 18)
    print(f"  {tag} y228..240 x360..550: green px {m.sum()} ; rows with green>50: "
          f"{[int(i/S)+228 for i in np.nonzero(m.sum(axis=1) > 50)[0]]}")
for tag, im in (("ORIG", o), ("REND", r)):
    band = sub(im, 360, 273, 550, 285)
    g = band[:, :, 1] - band[:, :, 0]
    g2 = band[:, :, 1] - band[:, :, 2]
    m = (g > 18) & (g2 > 18)
    print(f"  {tag} y273..285 x360..550: green px {m.sum()} ; rows with green>50: "
          f"{[int(i/S)+273 for i in np.nonzero(m.sum(axis=1) > 50)[0]]}")

# ---------------------------------------------------------------- 4. box3 band
print("\n=== 4. BOX3 PINK BAND (measured x~330..600 y291..320) ===")
for tag, im in (("ORIG", o), ("REND", r)):
    band = sub(im, 300, 291, 620, 320)
    pk = ((band[:, :, 0] > 210) & (band[:, :, 1] > 140) & (band[:, :, 2] > 175)
          & (band[:, :, 0] - band[:, :, 1] > 25))
    rows = pk.sum(axis=1)
    cols = pk.sum(axis=0)
    rnz = np.nonzero(rows > 20)[0]
    cnz = np.nonzero(cols > 20)[0]
    if len(rnz) and len(cnz):
        print(f"  {tag}: pink bbox frame x{300 + cnz[0]/S:.0f}..{300 + cnz[-1]/S:.0f} "
              f"y{291 + rnz[0]/S:.0f}..{291 + rnz[-1]/S:.0f}  px={pk.sum()}")
    else:
        print(f"  {tag}: pink px={pk.sum()} rows>20={len(rnz)} cols>20={len(cnz)}")

# 800080 text inside box3
print("  box3 purple text (800080-ish):")
for tag, im in (("ORIG", o), ("REND", r)):
    band = sub(im, 300, 291, 620, 320)
    p = (np.abs(band[:, :, 0] - 128) < 70) & (band[:, :, 2] > 110) & (band[:, :, 1] < 90)
    print(f"    {tag}: {p.sum()} px")

# ---------------------------------------------------------------- summary
print("\n" + "=" * 60)
print("RESIDUAL ADJUDICATION: %d hard failure(s)" % len(fails))
for f in fails:
    print("  - " + f)
print("=" * 60)
