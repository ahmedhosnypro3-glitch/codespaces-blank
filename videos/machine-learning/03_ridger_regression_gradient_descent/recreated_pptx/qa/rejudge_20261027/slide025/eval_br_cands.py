#!/usr/bin/env python3
"""Score every available br candidate PNG for assembling a complete k17a 4-set.

Each candidate is pasted at the build/slide_025.js BR rect (615,344,265x187)
onto a 960x540 white canvas and measured vs unique_slides/slide_025.jpg:
  band_diff%  CHECK1 metric over x672..816 y472..517 (|sum d|>60), target <50
  band_col%   colored-pixel fraction in the same band (orig ~71.2) = band fill
  wind        winding ratio of largest dark comp in BR panel (target ~6.0)
usage: eval_br_cands.py   -> prints ranked table, best first
"""
import glob
import hashlib
import os

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = "/home/codespace/ai_llm_slides"
NS = ROOT + "/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = NS + "/recreated_pptx/qa/rejudge_20261027/slide025"
ORIG = np.asarray(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)

BX0, BY0, BW, BH = 615, 344, 265, 187
X0, Y0, X1, Y1 = 672, 472, 816, 517


def md5(p):
    with open(p, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def colmask(a):
    mx_, mn_ = a.max(2), a.min(2)
    red = (a[:, :, 0] > 170) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90)
    return ((mx_ - mn_) > 30) & (mx_ > 90) & ~red


def comps(mask, min_area=5):
    lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
    out = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) >= min_area:
            out.append((len(xs), int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())))
    return out


def wind_ratio(a):
    br = a[BY0 + 8:BY0 + BH - 8, BX0 + 8:BX0 + BW - 8]
    dm = (br.max(2) < 110) & ((br.max(2) - br.min(2)) < 70)
    best = None
    for area, x0, y0, x1, y1 in comps(dm, min_area=15):
        if best is None or area > best[0]:
            best = (area, x0, y0, x1, y1)
    if best is None:
        return None
    area, x0, y0, x1, y1 = best
    ys, xs = np.nonzero(dm[y0:y1 + 1, x0:x1 + 1])
    order = np.argsort(xs)
    px, py = xs[order].astype(float), ys[order].astype(float)
    seg = float(np.hypot(np.diff(px), np.diff(py)).sum())
    straight = float(np.hypot(px[-1] - px[0], py[-1] - py[0]))
    return seg / max(straight, 1.0)


ob = ORIG[Y0:Y1, X0:X1]
oc = 100.0 * colmask(ob).mean()
print("orig band colored%% = %.1f" % oc)

cands = []
for pat in ("assets_k17*/plot_025_br.png", "assets_k15*/plot_025_br.png",
            "assets_bank_0506_pre_my_k15/plot_025_br.png",
            "br_cand_best*.png", "probe_k16_br_best*.png",
            "../../build/assets/plot_025_br.png",
            "../../build/assets_k15b/plot_025_br.png",
            "../../build/assets_k16b/plot_025_br.png"):
    for p in sorted(glob.glob(os.path.join(RJ, pat))):
        cands.append(p)

rows = []
for p in cands:
    im = Image.open(p).convert("RGB")
    im = im.resize((BW, BH), Image.BILINEAR)
    canvas = np.full((540, 960, 3), 255, np.int32)
    canvas[BY0:BY0 + BH, BX0:BX0 + BW] = np.asarray(im).astype(np.int32)
    rb = canvas[Y0:Y1, X0:X1]
    diff = (np.abs(ob - rb).sum(2) > 60)
    band_pct = 100.0 * diff.mean()
    col_pct = 100.0 * colmask(rb).mean()
    wr = wind_ratio(canvas)
    rows.append((band_pct, col_pct, wr if wr else -1, md5(p)[:12], os.path.relpath(p, RJ)))

rows.sort(key=lambda r: r[0])
print("%-10s %-8s %-7s %-12s %s" % ("band_diff%", "band_col%", "wind", "md5", "path"))
for r in rows:
    print("%-10.2f %-8.1f %-7.2f %-12s %s" % r)
