#!/usr/bin/env python3
"""Independent PIL adjudication of attempt_6's MINOR findings against BOTH
images (960x540 frame, 1px=1pt), slide 019 attempt-8 lane.

Phantom-trap law: reject ink columns/rows with < 3 ink px before reasoning
about any measurement.
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
print(f"scaleX={SX:.6f} scaleY={SY:.6f}  render={R.shape[1]}x{R.shape[0]}")
print()

# NOTE: masks are DELIBERATELY inclusive of saturated primaries.
# An earlier revision used `b < 235`, which silently excludes pure #0000FF
# (b=255) and made the render look blue-free.


def blue_mask(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    # clearly blue: blue channel dominates both others
    return (b > r + 20) & (b > g + 20) & (b > 60)


def yellow_mask(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    # warm/yellow highlight: high r and g, visibly lower blue
    return (r > 150) & (g > 150) & (r > b + 30) & (g > b + 30)


def green_mask(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return (g > r + 15) & (g > b + 15) & (g > 60) & (g < 230)


def phantom(mask, axis):
    """Row/col index array keeping only >=3px lines (phantom-trap law)."""
    return np.nonzero(mask.sum(axis=axis) >= 3)[0]


def frame_rect(arr_i0, arr_i1, arr_j0, arr_j1, sx, sy):
    return (arr_j0 / sx, arr_j1 / sx, arr_i0 / sy, arr_i1 / sy)


print("=" * 72)
print("MINOR #5 — 'added title frame'")
print("  Judge claim: the original has PLAIN header text; the RECREATION adds a")
print("  blue box. Adjudication asks which image actually carries the blue box.")
print("=" * 72)
# JSON recreation_brief step 2: blue-bordered rect top-left, x=2%-32%, y=0%-8%.
# In frame px of the 960x540 original: x ~19..307, y ~0..43. The banked ledger
# instead located text/ink lower (y67..). Scan the whole upper frame to be safe.
for label, arr, scale in (("original", O, (1.0, 1.0)), ("render_8", R, (SX, SY))):
    bm = blue_mask(arr)
    rows = phantom(bm, axis=1)
    cols = phantom(bm, axis=0)
    if len(rows) == 0:
        print(f"  {label}: no blue ink at all")
        continue
    fx0, fx1, fy0, fy1 = frame_rect(rows.min(), rows.max() + 1,
                                    cols.min(), cols.max() + 1, *scale)
    print(f"  {label}: total blue px={int(bm.sum()):6d}  "
          f"rows(>=3px)={len(rows):3d}  cols(>=3px)={len(cols):4d}")
    print(f"           bbox frame x{fx0:.0f}..{fx1:.0f} y{fy0:.0f}..{fy1:.0f}")
    # is the blue ink a RECTANGLE? -> check the extreme rows and cols carry ink
    # while the centre is comparatively empty (a box outline), vs. dense text.
    top_rows = bm[:rows.min() + 4].sum()
    bot_rows = bm[max(0, rows.max() - 3):].sum()
    left_cols = bm[:, :cols.min() + 4].sum()
    right_cols = bm[:, max(0, cols.max() - 3):].sum()
    interior = bm[rows.min() + 8:rows.max() - 7,
                  cols.min() + 8:cols.max() - 7].sum()
    print(f"           outline-ink px: top={int(top_rows)} bottom={int(bot_rows)} "
          f"left={int(left_cols)} right={int(right_cols)} "
          f"interior={int(interior)} "
          f"(ratio {(interior / max(1, bm.sum())):.2f})")

print()
print("=" * 72)
print("MINOR #6 — highlight bands: judge says the original highlights ONLY the")
print("y-value cells; the banked ledger says the original's bands are FULL-WIDTH.")
print("=" * 72)
for label, arr, scale in (("original", O, (1.0, 1.0)), ("render_8", R, (SX, SY))):
    ym = yellow_mask(arr)
    rows = phantom(ym, axis=1)
    print(f"  {label}: total yellow-ish px={int(ym.sum()):6d}  "
          f"yellow rows(>=3px)={len(rows)}")
    if len(rows) == 0:
        continue
    gaps = np.nonzero(np.diff(rows) > 4)[0]
    starts = np.concatenate(([rows[0]], rows[gaps + 1]))
    ends = np.concatenate((rows[gaps], [rows[-1]]))
    for s, e in zip(starts, ends):
        band = ym[s:e + 1]
        cols = phantom(band, axis=0)
        if len(cols) == 0:
            continue
        fx0, fx1 = cols.min() / scale[0], cols.max() / scale[0]
        print(f"     band y{s/scale[1]:.0f}..{e/scale[1]:.0f}  "
              f"frame-x width {fx0:.0f}..{fx1:.0f} ({fx1-fx0:.0f} px)  "
              f"px={int(band.sum())}")
        # per-band column histogram: is ink spread full width or clustered?
        colhist = band.sum(axis=0)
        thirds = (len(colhist) // 3) or 1
        print(f"       ink by thirds: L={int(colhist[:thirds].sum())} "
              f"M={int(colhist[thirds:2*thirds].sum())} "
              f"R={int(colhist[2*thirds:].sum())}")

print()
print("=" * 72)
print("MINOR #3 — 'small green per-component figures flanking the W labels'")
print("=" * 72)
for label, arr, scale in (("original", O, (1.0, 1.0)), ("render_8", R, (SX, SY))):
    gm = green_mask(arr)
    cols = phantom(gm, axis=0)
    if len(cols) == 0:
        print(f"  {label}: no green ink (>=3px cols)")
        continue
    rows = phantom(gm, axis=1)
    fx0, fx1, fy0, fy1 = frame_rect(rows.min(), rows.max() + 1,
                                    cols.min(), cols.max() + 1, *scale)
    print(f"  {label}: green px={int(gm.sum()):6d}  rows(>=3px)={len(rows):3d} "
          f"cols(>=3px)={len(cols):4d}  bbox frame x{fx0:.0f}..{fx1:.0f} "
          f"y{fy0:.0f}..{fy1:.0f}")
    if len(rows):
        ys = phantom(gm, axis=1)
        print(f"           green row extent frame y{ys.min()/scale[1]:.0f}"
              f"..{ys.max()/scale[1]:.0f}")

print()
print("=" * 72)
print("MINOR #4 / #7 — number formatting + grid restructure (content, not pixels)")
print("=" * 72)
print("  #4: analysis/slide_019_final.json renders the reference line and the")
print("      outlier rows LINEALLY, and so does the original slide; the build")
print("      matches the original's own notation. Not a fix trigger.")
print("  #7: same 3x3 test values per row group in the same order; only the")
print("      internal cell-border geometry differs. Content-equivalent.")
