#!/usr/bin/env python3
"""Slide 045 PIL-first adjudication harness.

Compares render_1.png (150dpi, 2001x1125) against unique_slides/slide_045.jpg
(960x540) in FRAME space (render downsampled by H_render/540 = 2.0833) so any
judge finding can be measured against both images at 1px = 1pt before a build
change is proposed.

Usage:
  python3 measure_adjudicate_045.py            # full report
  python3 measure_adjudicate_045.py box X0 Y0 X1 Y1   # per-region ink/diff detail
"""
import sys
from PIL import Image
import numpy as np

NS = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = NS + "/recreated_pptx/qa/slide045"
RENDER = QA + "/render_1.png"
ORIG = NS + "/unique_slides/slide_045.jpg"

FW, FH = 960, 540

rim = Image.open(RENDER).convert("RGB")
RW, RH = rim.size
S = RH / float(FH)

# render -> frame space (box average = pixel-accurate resample to 1px/pt)
rframe = rim.resize((FW, FH), Image.BOX).convert("L")
oim = Image.open(ORIG).convert("RGB")
oframe = oim.convert("L")

r = np.asarray(rframe, dtype=np.int16)
o = np.asarray(oframe, dtype=np.int16)
och = np.asarray(oim)
rch = np.asarray(rim.resize((FW, FH), Image.BOX).convert("RGB"))


def ink(a, thr=128):
    return a < thr


d = np.abs(r - o)
print("render %dx%d scale=%.4f  frame %dx%d" % (RW, RH, S, FW, FH))
print("mean|diff|=%.2f  px>32: %d  px>64: %d  px>128: %d" %
      (d.mean(), (d > 32).sum(), (d > 64).sum(), (d > 128).sum()))

# ink confusion, in frame px
oi, ri = ink(o), ink(r)
print("original ink px=%d  render ink px=%d  (ink=luma<128)" % (oi.sum(), ri.sum()))
print("ink only in ORIGINAL (present in orig, absent in render) = %d" % ((oi & ~ri).sum()))
print("ink only in RENDER  (absent in orig, present in render) = %d" % ((ri & ~oi).sum()))

# coarse grid: 24 cols x 14 rows (40x40pt cells)
print("\ncoarse grid (40pt cells): / = original-only ink, # = both ink, + = render-only ink, . = blank")
for gy in range(14):
    row = []
    for gx in range(24):
        y0, y1 = gy * 40, (gy + 1) * 40
        x0, x1 = gx * 40, (gx + 1) * 40
        oi_c = oi[y0:y1, x0:x1].sum()
        ri_c = ri[y0:y1, x0:x1].sum()
        if oi_c == 0 and ri_c == 0:
            row.append(".")
        elif oi_c > 0 and ri_c > 0:
            row.append("#")
        elif oi_c > 0:
            row.append("/")
        else:
            row.append("+")
    print("y%3d-%3d  %s" % (gy * 40, (gy + 1) * 40, "".join(row)))
print("        " + "".join("|" if i % 6 == 0 else " " for i in range(24)))

# house chrome re-measure in frame px on BOTH images
def chrome(name, ch):
    a = np.asarray(ch, dtype=np.int16).sum(axis=2)
    r_red = (ch[:, :, 0] > 150) & (ch[:, :, 1] < 90) & (ch[:, :, 2] < 90)
    print("\n[%s] red px total=%d" % (name, r_red.sum()))
    # left stroke column scan: count red per column in x 50..70
    for cand in range(50, 72):
        n = r_red[:, cand].sum()
        if n > 200:
            print("   col x=%d red=%d" % (cand, n))
    for cand in range(890, 910):
        n = r_red[:, cand].sum()
        if n > 200:
            print("   col x=%d red=%d" % (cand, n))
    for cand in range(525, 540):
        n = r_red[cand, :].sum()
        if n > 200:
            print("   row y=%d red=%d" % (cand, n))
    topband = r_red[40:60, :].sum()
    # exclude the vertical strokes' own columns (x56..62, x897..904): their
    # topmost pixels (rows 46..59) are mandated, NOT a top stroke.
    tbm = r_red.copy()
    tbm[40:60, 56:63] = False
    tbm[40:60, 897:905] = False
    print("   top band y40..60 red px=%d (of which vertical-stroke tops=%d); after excluding x56..62+897..904 => %d (must be 0 on this deck)" %
          (topband, topband - tbm[40:60, :].sum(), tbm[40:60, :].sum()))
    # an actual top stroke = a horizontal run: count red in rows 40..59 per row
    # outside the two vertical columns
    for rr in range(40, 60):
        n = tbm[rr, :].sum()
        if n > 20:
            print("   !! possible top stroke row y=%d red px=%d" % (rr, n))


chrome("ORIGINAL", och)
chrome("RENDER  ", rch)


def badge(name, ch):
    r_, g_, b_ = ch[:, :, 0], ch[:, :, 1], ch[:, :, 2]
    yel = (r_ > 220) & (g_ > 220) & (b_ < 190) & ((r_ - b_) > 40)
    sub = yel[45:105, 840:915]
    ys, xs = np.nonzero(sub)
    if len(xs) == 0:
        print("\n[%s] no yellow badge pixels in x840..915 y45..105" % name)
        return
    print("\n[%s] yellow badge bbox in x840..915/y45..105: x%d..%d y%d..%d  n=%d  centroid=(%.1f,%.1f)" %
          (name, xs.min() + 840, xs.max() + 840, ys.min() + 45, ys.max() + 45, len(xs),
           xs.mean() + 840, ys.mean() + 45))
    # horizontal diameter at the centroid row, and vertical extent -> estimate d
    cy = int(round(ys.mean())) + 45
    cx = int(round(xs.mean())) + 840
    rowx = np.nonzero(yel[cy, 820:930])[0]
    coly = np.nonzero(yel[40:110, cx])[0]
    if len(rowx):
        print("   badge row y=%d: x%d..%d  (w=%d)" % (cy, rowx.min() + 820, rowx.max() + 820, rowx.max() - rowx.min() + 1))
    if len(coly):
        print("   badge col x=%d: y%d..%d  (h=%d)" % (cx, coly.min() + 40, coly.max() + 40, coly.max() - coly.min() + 1))
    # purple ring scan: for each column in the bbox, find purple (6A5ACD) pixels
    purp = (np.abs(r_.astype(int) - 106) < 60) & (np.abs(g_.astype(int) - 90) < 60) & (np.abs(b_.astype(int) - 205) < 60) & ((b_ - r_) > 40)
    ps = purp[45:105, 840:915]
    pys, pxs = np.nonzero(ps)
    if len(pxs):
        print("   purple ring px=%d bbox x%d..%d y%d..%d" % (len(pxs), pxs.min() + 840, pxs.max() + 840, pys.min() + 45, pys.max() + 45))


def topred(name, r_red):
    ys, xs = np.nonzero(r_red[0:60, :])
    print("\n[%s] red-ish px in y0..59: %d" % (name, len(xs)))
    if len(xs):
        byrow = {}
        for y_, x_ in zip(ys.tolist(), xs.tolist()):
            byrow.setdefault(y_, []).append(x_)
        for rr in sorted(byrow):
            xx = sorted(byrow[rr])
            show = xx if len(xx) <= 30 else str(xx[:15]) + "...(%d total)" % len(xx)
            print("   y=%d: %d px  x=%s" % (rr, len(xx), show))


def _redmask(ch):
    return (ch[:, :, 0] > 150) & (ch[:, :, 1] < 90) & (ch[:, :, 2] < 90)


topred("ORIGINAL", _redmask(och))
topred("RENDER  ", _redmask(rch))

badge("ORIGINAL", och)
badge("RENDER  ", rch)

if len(sys.argv) > 5:
    X0, Y0, X1, Y1 = [int(v) for v in sys.argv[2:6]]
    sl = (slice(Y0, Y1), slice(X0, X1))
    print("\n=== REGION x%d..%d y%d..%d ===" % (X0, Y0, X1, Y1))
    print("orig ink=%d render ink=%d orig-only=%d render-only=%d mean|d|=%.2f" %
          (oi[sl].sum(), ri[sl].sum(), (oi & ~ri)[sl].sum(), (ri & ~oi)[sl].sum(), d[sl].mean()))
    # per-row ink profile (original only rows that have ink)
    print("row profiles (y: orig/render ink):")
    for y in range(Y0, Y1):
        a, b2 = oi[y, X0:X1].sum(), ri[y, X0:X1].sum()
        if a or b2:
            print("  y=%4d  orig=%5d render=%5d" % (y, a, b2))
