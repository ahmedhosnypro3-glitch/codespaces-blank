#!/usr/bin/env python3
"""att27 frame measure 3 — pins the remaining 034 table/plot geometry.

Settles (PIL, on unique_slides/slide_034.jpg 960x540):
  A. table box rules: top/bottom rule x-extents, left/right border cols
  B. band edges: vertical strip samples at x300 (y315..378, y405..422, y450..485)
     + band right/left edge fill samples (x876 / x72)
  C. column grid: LSQ fit of slope-strip centers + next-x red verticals +
     band1 white separator columns
  D. next-x row red verticals (full grid vs band-only)
  E. slope row: text-only ink center + inset-box border rows at x210
  F. plot gridline modal color (vgrid x775/x668, hgrid y190)
  G. plot border dark-red bbox
  H. label-column ink right edge per band
"""
import numpy as np
from PIL import Image
from collections import Counter

im = np.asarray(Image.open("unique_slides/slide_034.jpg").convert("RGB")).astype(int)
out = []
def w(s=""): out.append(s)

# ---------- A. table rules ----------
def dark_cols(y0, y1, x0=60, x1=900, thr=140):
    seg = im[y0:y1, x0:x1]
    m = seg.mean(axis=2)
    n = (m < thr).sum(axis=0)
    return [(x0 + i, int(n[i])) for i in np.nonzero(n > (y1 - y0) * 0.5)[0]]

def dark_rows(x0, x1, y0=310, y1=525, thr=140):
    seg = im[y0:y1, x0:x1]
    m = seg.mean(axis=2)
    n = (m < thr).sum(axis=1)
    return [(y0 + i, int(n[i])) for i in np.nonzero(n > (x1 - x0) * 0.5)[0]]

w("### A. table rules")
w("top rule rows y316..325 dark(x150..850): %s" % dark_rows(150, 850, 316, 326))
w("bottom rule rows y512..521 dark(x150..850): %s" % dark_rows(150, 850, 512, 522))
w("left border cols x62..76 dark(y325..510): %s" % dark_cols(325, 510, 62, 77))
w("right border cols x872..892 dark(y325..510): %s" % dark_cols(325, 510, 872, 893))
for yy in (320, 321):
    row = im[yy, 60:900].mean(axis=1)
    dk = np.nonzero(row < 170)[0]
    if len(dk):
        w("  y%d dark x-extent: %d..%d n=%d" % (yy, 60 + dk.min(), 60 + dk.max(), len(dk)))
for yy in (516, 517):
    row = im[yy, 60:900].mean(axis=1)
    dk = np.nonzero(row < 170)[0]
    if len(dk):
        w("  y%d dark x-extent: %d..%d n=%d" % (yy, 60 + dk.min(), 60 + dk.max(), len(dk)))

# ---------- B. band edges ----------
w("### B. band edge strips (x=300)")
for y0, y1 in ((314, 380), (404, 422), (448, 486)):
    w(" x300 y%d..%d:" % (y0, y1 - 1))
    for yy in range(y0, y1):
        px = im[yy, 300]
        w("   y%d %s" % (yy, tuple(int(v) for v in px)))
w(" fill samples x876: y340 %s y390 %s y425 %s y470 %s y493 %s" % (
    tuple(int(v) for v in im[340, 876]), tuple(int(v) for v in im[390, 876]),
    tuple(int(v) for v in im[425, 876]), tuple(int(v) for v in im[470, 876]),
    tuple(int(v) for v in im[493, 876])))
w(" fill samples x72:  y340 %s y390 %s y425 %s y470 %s y493 %s" % (
    tuple(int(v) for v in im[340, 72]), tuple(int(v) for v in im[390, 72]),
    tuple(int(v) for v in im[425, 72]), tuple(int(v) for v in im[470, 72]),
    tuple(int(v) for v in im[493, 72])))
w(" fill samples x860: y340 %s y470 %s" % (
    tuple(int(v) for v in im[340, 860]), tuple(int(v) for v in im[470, 860])))

# ---------- C. column grid ----------
w("### C. column grid")
# slope-row dark strip centers (from att27_frame_measure.txt pass, yellowish gaps)
strips = [179, 219.5, 260.5, 301.5, 341.5, 423, 463.5, 504, 545.5, 585.5, 625.5,
          666.5, 707.5, 747.5, 789, 829.5]
# next-x red verticals
seg = im[486:500, 70:880]
r, g, b = seg[..., 0], seg[..., 1], seg[..., 2]
red = (r > 150) & (r - g > 45) & (r - b > 40)
coln = red.sum(axis=0)
cand = [70 + i for i in np.nonzero(coln >= 9)[0]]
clusters = []
for x in cand:
    if clusters and x - clusters[-1][-1] <= 2:
        clusters[-1].append(x)
    else:
        clusters.append([x])
nx_centers = [sum(c) / len(c) for c in clusters]
w(" next-x red col clusters: %s" % [f"({c[0]},{c[-1]})" for c in clusters])
# band1 white separator columns (light px, y333..367, outside insert zone)
seg = im[333:368, 145:660]
light = (seg[..., 2] > 190) & (seg[..., 0] > 225) & (seg[..., 1] > 225)
coln = light.sum(axis=0)
cand = [145 + i for i in np.nonzero(coln >= 12)[0]]
clusters = []
for x in cand:
    if clusters and x - clusters[-1][-1] <= 2:
        clusters[-1].append(x)
    else:
        clusters.append([x])
b1_centers = [sum(c) / len(c) for c in clusters]
w(" band1 white sep col clusters: %s" % [f"({c[0]},{c[-1]})" for c in clusters])
# band2 + band3 white separators
for nm, (ya, yb) in (("band2", (377, 408)), ("band3", (420, 452))):
    seg = im[ya:yb, 145:860]
    light = (seg[..., 2] > 200) & (seg[..., 0] > 225) & (seg[..., 1] > 210)
    coln = light.sum(axis=0)
    cand = [145 + i for i in np.nonzero(coln >= (yb - ya) * 0.6)[0]]
    clusters = []
    for x in cand:
        if clusters and x - clusters[-1][-1] <= 2:
            clusters[-1].append(x)
        else:
            clusters.append([x])
    w(" %s white sep col clusters: %s" % (nm, [f"({c[0]},{c[-1]})" for c in clusters]))
# LSQ fit x = a + p*k over all candidates
allc = [(x, None) for x in nx_centers] + [(x, None) for x in b1_centers] + [(x, None) for x in strips]
a0, p0 = 138.3, 40.7
ks, xs = [], []
for (x, _) in allc:
    k = round((x - a0) / p0)
    if 0 <= k <= 18:
        ks.append(k); xs.append(x)
ks = np.array(ks); xs = np.array(xs)
A = np.vstack([np.ones_like(ks), ks]).T
(a_fit, p_fit), res, _, _ = np.linalg.lstsq(A, xs, rcond=None)
pred = a_fit + p_fit * ks
w(" LSQ: a=%.2f p=%.3f  n=%d  max|r|=%.2f" % (a_fit, p_fit, len(ks), np.abs(pred - xs).max()))
w(" per-k residuals: %s" % {int(k): round(float(v), 2) for k, v in sorted(zip(ks, pred - xs))})
XSEP = [a_fit + p_fit * k for k in range(19)]
w(" XSEP: %s" % [round(v, 1) for v in XSEP])
w(" checks: insert L %.1f (meas 666-668) R %.1f (788-791); yellow1 %.1f..%.1f (711,744); yellow2 %.1f..%.1f (792,827)"
  % (XSEP[13], XSEP[16], XSEP[14], XSEP[15], XSEP[16], XSEP[17]))

# ---------- D. next-x red verticals summary ----------
w("### D. next-x: %d red col clusters -> %s" % (len(clusters), [round(c, 1) for c in nx_centers]))
# next-x red rows at x=700 (clean of text)
seg = im[478:508, 700]
for i, px in enumerate(seg):
    rr, gg, bb = int(px[0]), int(px[1]), int(px[2])
    if rr > 150 and rr - gg > 45:
        w("  x700 y%d %s REDDISH" % (478 + i, (rr, gg, bb)))

# ---------- E. slope row ----------
w("### E. slope row")
seg = im[459:479, 145:870]
m = seg.mean(axis=2)
dark = m < 110
rown = dark.sum(axis=1)
w(" text-only dark rows: %s" % {459 + i: int(rown[i]) for i in np.nonzero(rown > 3)[0]})
w(" x210 y455..482: %s" % [tuple(int(v) for v in im[yy, 210]) for yy in range(455, 483)])
# slope edge rule color: rows 459..461 & 476..478 over x150..860, greenish px
for nm, (ya, yb) in (("top", (458, 462)), ("bot", (475, 479))):
    seg = im[ya:yb, 150:860]
    r, g, b = seg[..., 0], seg[..., 1], seg[..., 2]
    grn = (g > r + 20) & (g > b + 40) & (g < 200)
    if grn.sum():
        mean = seg[grn].mean(axis=0)
        w(" slope %s edge green mean RGB: %s n=%d" % (nm, tuple(round(float(v), 1) for v in mean), int(grn.sum())))

# ---------- F. gridline color ----------
w("### F. gridline modal colors")
for nm, (x, y0, y1) in (("vgrid x775", (775, 62, 310)), ("vgrid x668", (668, 62, 310)),
                        ("vgrid x704", (704, 62, 310))):
    seg = im[y0:y1, x - 1:x + 2].reshape(-1, 3)
    mx = seg.max(axis=1); mn = seg.min(axis=1); mean = seg.mean(axis=1)
    keep = seg[(mx - mn < 30) & (mean > 185) & (mean < 245)]
    if len(keep):
        cnt = Counter(tuple(v) for v in keep)
        w(" %s: n=%d modal %s" % (nm, len(keep), cnt.most_common(3)))
for nm, y in (("hgrid y190", 190), ("hgrid y278", 278)):
    seg = im[y - 1:y + 2, 615:840].reshape(-1, 3)
    mx = seg.max(axis=1); mn = seg.min(axis=1); mean = seg.mean(axis=1)
    keep = seg[(mx - mn < 30) & (mean > 185) & (mean < 245)]
    if len(keep):
        cnt = Counter(tuple(v) for v in keep)
        w(" %s: n=%d modal %s" % (nm, len(keep), cnt.most_common(3)))

# ---------- G. plot border ----------
w("### G. plot dark-red border")
seg = im[48:322, 590:860]
r, g, b = seg[..., 0], seg[..., 1], seg[..., 2]
dr = (r > 90) & (r < 210) & (g < 80) & (b < 80)
ys, xs = np.nonzero(dr)
if len(xs):
    w(" bbox x%d..%d y%d..%d n=%d" % (590 + xs.min(), 590 + xs.max(), 48 + ys.min(), 48 + ys.max(), len(dr)))
    coln = dr.sum(axis=0); rown = dr.sum(axis=1)
    w(" cols n>40: %s" % [590 + i for i in np.nonzero(coln > 40)[0]])
    w(" rows n>40: %s" % [48 + i for i in np.nonzero(rown > 40)[0]])
    mean = seg[dr].mean(axis=0)
    w(" mean RGB: %s" % (tuple(round(float(v), 1) for v in mean),))

# ---------- H. label ink ----------
w("### H. label ink per band (x70..137)")
for nm, (ya, yb) in (("band1", (333, 367)), ("band2", (376, 409)), ("band3", (419, 453)),
                     ("slope", (460, 477)), ("nextx", (485, 501))):
    seg = im[ya:yb, 70:138]
    m = seg.mean(axis=2)
    dk = m < 110
    ys, xs = np.nonzero(dk)
    if len(xs):
        w(" %s: ink x%d..%d y%d..%d n=%d" % (nm, 70 + xs.min(), 70 + xs.max(), ya + ys.min(), ya + ys.max(), len(xs)))
    else:
        w(" %s: no ink" % nm)

txt = "\n".join(out)
with open("recreated_pptx/qa/slide034/att27_frame_measure3.txt", "w") as f:
    f.write(txt + "\n")
print(txt)
