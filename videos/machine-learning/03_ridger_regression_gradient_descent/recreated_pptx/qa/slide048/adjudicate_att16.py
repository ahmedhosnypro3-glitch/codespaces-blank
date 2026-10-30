#!/usr/bin/env python3
"""PIL-first adjudication of slide 048 judge attempt 16 (render_16 vs original frame).

Measures, in matched slide space:
  A  header initial-W zone  -> column ink segments (is the vector left or right of the label?)
  A2 header bars             -> are the two delimiter bars present, at the measured x?
  B  row-2 action text       -> ink row bands (one line or wrapped?)
  C  row-1 update equation   -> semicolon ink present?
  D  row-1 d(x) equation     -> dot ink present?
  E  header "-2" digit color -> RGB sample
  F  legend italic words     -> glyph geometry (slant proxy)
  G  rows 2-6 right side     -> vertical bar ink (stray rules claim)
"""
import numpy as np
from PIL import Image

NS = "videos/machine-learning/03_ridger_regression_gradient_descent"
R = Image.open(f"{NS}/recreated_pptx/qa/slide048/render_16.png").convert("RGB")
O = Image.open(f"{NS}/unique_slides/slide_048.jpg").convert("RGB")
SC = R.size[1] / 540.0
print(f"render {R.size} scale {SC:.4f}   orig {O.size}")


def pair(x0, y0, x1, y1):
    """Return (render_crop, orig_crop) at the render's effective scale."""
    rc = R.crop((int(x0 * SC), int(y0 * SC), int(np.ceil(x1 * SC)), int(np.ceil(y1 * SC))))
    oc = O.crop((x0, y0, x1, y1)).resize(rc.size, Image.LANCZOS)
    return rc, oc


def dark(a, thr=140):
    return (a.astype(np.int16).mean(axis=2) < thr)


def segments(mask1d, minrun=1):
    segs, start = [], None
    for i, v in enumerate(mask1d):
        if v and start is None:
            start = i
        elif not v and start is not None:
            if i - start >= minrun:
                segs.append((start, i - 1))
            start = None
    if start is not None:
        segs.append((start, len(mask1d) - 1))
    return segs


def col_profile(rc, oc, x0, label):
    mr = dark(np.asarray(rc))
    mo = dark(np.asarray(oc))
    # both crops share the same pixel width (render scale), so columns align
    pr = mr.sum(axis=0)
    po = mo.sum(axis=0)
    sr = segments(pr > 0)
    so = segments(po > 0)
    print(f"\n[{label}] frame x {x0}..{x0 + (rc.size[0] / SC):.0f}")
    print(f"  render ink cols: {[(int(a / SC + x0), int(b / SC + x0)) for a, b in sr]}")
    print(f"  orig   ink cols: {[(int(a / SC + x0), int(b / SC + x0)) for a, b in so]}")


def row_bands(rc, oc, x0, y0, label):
    mr = dark(np.asarray(rc))
    mo = dark(np.asarray(oc))
    br = segments(mr.sum(axis=1) > 0)
    bo = segments(mo.sum(axis=1) > 0)
    print(f"\n[{label}] frame y {y0}..{y0 + (rc.size[1] / SC):.0f}")
    print(f"  render ink rows: {[(round(a / SC + y0, 1), round(b / SC + y0, 1)) for a, b in br]}")
    print(f"  orig   ink rows: {[(round(a / SC + y0, 1), round(b / SC + y0, 1)) for a, b in bo]}")
    print(f"  render lines={len(br)}  orig lines={len(bo)}")


def ink_count(rc, oc, x0, y0, x1, y1, thr=150):
    """Ink pixels inside a frame-space sub-rectangle of both images."""
    a = rc.crop((int((x0) * SC - 0), 0, 0, 0)) if False else None
    rr = R.crop((int(x0 * SC), int(y0 * SC), int(x1 * SC), int(y1 * SC)))
    oo = O.crop((x0, y0, x1, y1)).resize(rr.size, Image.LANCZOS)
    nr, no = int(dark(np.asarray(rr), thr).sum()), int(dark(np.asarray(oo), thr).sum())
    return nr, no


# A: header initial-W zone (label + vector + bars), frame x320..545 y50..110
rc, oc = pair(320, 50, 545, 110)
col_profile(rc, oc, 320, "A header initial-W (cols)")

# A2: are the two header delimiter bars drawn? (spec dbar at 330.28 and 351.72, y57..106)
for bx in (330.28, 351.72):
    n_r, n_o = ink_count(rc, oc, bx - 1.0, 57, bx + 1.0, 106, thr=190)
    print(f"[A2] bar x={bx}: render ink px={n_r}  orig ink px={n_o}")

# B: row-2 action text ("Keep same Weight") frame x505..600 y210..265
rc, oc = pair(505, 210, 600, 265)
row_bands(rc, oc, 505, 210, "B row2 action text (rows)")

# B2: rows 3-6 action text bands (frame x505..600)
for ry0, ry1 in ((275, 330), (340, 395), (405, 460), (470, 528)):
    rc2, oc2 = pair(505, ry0, 600, ry1)
    row_bands(rc2, oc2, 505, ry0, f"B2 action rows {ry0}-{ry1}")

# C: semicolons in row-1 update equation (right of the vec1 digits) frame x656..668 y164..180
n_r, n_o = ink_count(rc, oc, 0, 0, 0, 0) if False else ink_count(*pair(300, 150, 800, 200), 656, 164, 668, 180, thr=170)
print(f"[C] semicolon zone (656..668,164..180): render ink={n_r} orig ink={n_o}")

# D: dot between the row-1 vectors: frame x700..714 y162..176
n_r, n_o = ink_count(*pair(300, 150, 800, 200), 700, 162, 714, 176, thr=170)
print(f"[D] dot zone (700..714,162..176): render ink={n_r} orig ink={n_o}")

# E: color of header '-2' digits (frame x336..352 y76..101)
rr = R.crop((int(336 * SC), int(76 * SC), int(352 * SC), int(101 * SC)))
oo = O.crop((336, 76, 352, 101)).resize(rr.size, Image.LANCZOS)
arr = np.asarray(rr).reshape(-1, 3)
dk = arr[arr.mean(axis=1) < 170]
print(f"[E] header -2 color render median RGB={np.median(dk, axis=0).astype(int) if len(dk) else None}")
arr = np.asarray(oo).reshape(-1, 3)
dk = arr[arr.mean(axis=1) < 170]
print(f"[E] header -2 color orig   median RGB={np.median(dk, axis=0).astype(int) if len(dk) else None}")

# F: legend words italic? frame x239..540 y108..126
rc3, oc3 = pair(239, 106, 540, 128)
row_bands(rc3, oc3, 239, 106, "F legend (rows)")

# G: rows 2-6 right side — vertical bar ink around the W vector columns (frame x720..770)
for gy0, gy1 in ((216, 260), (280, 322), (348, 392), (410, 455), (476, 522)):
    n_r, n_o = ink_count(*pair(600, gy0, 800, gy1), 720, gy0, 770, gy1, thr=190)
    print(f"[G] rows band {gy0}-{gy1} x720..770: render ink={n_r} orig ink={n_o}")
