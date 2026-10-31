#!/usr/bin/env python3
"""Verify assets_k17j composited vs orig slide_025.jpg -> pil_k17j_out.txt.

Composite: white canvas + gray panel E9E9E7 (x54..903 y45..539) + the four
plot PNGs resized to their slide-px boxes at their addImage positions.
Checks: CHECK1 BR band x672..816 y472..517 diff%, CHECK2 BL label anchors,
CHECK3 red marker-like comps, BR winding wind-ratio, BR colored%/jet-hist/diag,
md5 comparison vs assets_k15.
"""
import os, sys, hashlib, json
import numpy as np
from PIL import Image
from scipy import ndimage

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = NS + "/recreated_pptx/qa/rejudge_20261027/slide025"
AJ = os.path.join(RJ, "assets_k17j")
K15 = os.path.join(RJ, "assets_k15")
OUT = os.path.join(RJ, "pil_k17j_out.txt")

orig = np.array(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)

PANELS = {"tl": (85, 115, 180, 173), "tr": (616, 115, 263, 202),
          "bl": (83, 290, 293, 237), "br": (615, 344, 265, 187)}

canvas = np.full((540, 960, 3), 255, np.int32)
canvas[45:540, 54:904] = np.array([233, 233, 231], np.int32)
for name, (x, y, w, h) in PANELS.items():
    im = Image.open(os.path.join(AJ, "plot_025_%s.png" % name)).convert("RGB")
    im = im.resize((w, h), Image.BILINEAR)
    canvas[y:y + h, x:x + w] = np.array(im).astype(np.int32)

L = []
def log(s=""):
    print(s)
    L.append(s)


def colmask(a):
    mx, mn = a.max(2), a.min(2)
    red = (a[:, :, 0] > 170) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90)
    return ((mx - mn) > 60) & (mx > 90) & ~red


def redmask(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 110) & (r - g > 50) & (r - b > 50)


def jet_t(px, lut):
    d = ((lut[None, :, :] - px[:, None, :].astype(np.float64)) ** 2).sum(2)
    return d.argmin(1) / 255.0


import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
JET_LUT = (plt.get_cmap("jet")(np.linspace(0, 1, 256))[:, :3] * 255.0)

log("== pil_k17j_out.txt — assets_k17j composited vs orig slide_025.jpg ==")
log("")
# md5 check
log("== md5 assets_k17j vs assets_k15 (all must differ) ==")
alldiff = True
for n in ("tl", "tr", "bl", "br"):
    f = "plot_025_%s.png" % n
    m1 = hashlib.md5(open(os.path.join(AJ, f), "rb").read()).hexdigest()
    m2 = hashlib.md5(open(os.path.join(K15, f), "rb").read()).hexdigest()
    diff = m1 != m2
    alldiff &= diff
    log("  %-18s k17j=%s k15=%s differ=%s" % (f, m1, m2, diff))
log("  md5_all_diff=%s" % alldiff)
log("")

# BR metrics (panel x615..880 y344..531, pad 8)
P = 8
Bx0, By0, Bx1, By1 = 615, 344, 880, 531


def br_stats(img):
    p = img[By0:By1, Bx0:Bx1]
    m = colmask(p)
    m[:P] = False; m[-P:] = False; m[:, :P] = False; m[:, -P:] = False
    ys, xs = np.nonzero(m)
    t = jet_t(p[ys, xs], JET_LUT)
    h = np.histogram(t, bins=16, range=(0, 1))[0]
    bx0, bx1, by0, by1 = xs.min(), xs.max(), ys.min(), ys.max()
    dgm = np.abs((xs - bx0) - (ys - by0)) <= 2
    td = t[dgm] if dgm.sum() > 10 else t
    iL, iR, iT, iB = xs.argmin(), xs.argmax(), ys.argmin(), ys.argmax()
    return dict(bbox=(int(bx0), int(bx1), int(by0), int(by1)),
                L=(int(xs[iL]), int(ys[iL])), R=(int(xs[iR]), int(ys[iR])),
                T=(int(xs[iT]), int(ys[iT])), B=(int(xs[iB]), int(ys[iB])),
                colored=float(m.mean()), hist=h.tolist(),
                diag=(float(td.mean()), float(td.std()), float(td.min()), float(td.max())))


so = br_stats(orig)
sr = br_stats(canvas)
log("== BR surface stats (panel pad-8 crop; slide bbox = +615/+344) ==")
log("  orig: bbox slide x%d..%d y%d..%d colored=%.1f%% diag mean=%.3f std=%.3f min=%.2f max=%.2f" % (
    so["bbox"][0] + Bx0, so["bbox"][1] + Bx0, so["bbox"][2] + By0, so["bbox"][3] + By0,
    100 * so["colored"], *so["diag"]))
log("  orig: jet-t hist/16: %s" % so["hist"])
log("  rend: bbox slide x%d..%d y%d..%d colored=%.1f%% diag mean=%.3f std=%.3f min=%.2f max=%.2f" % (
    sr["bbox"][0] + Bx0, sr["bbox"][1] + Bx0, sr["bbox"][2] + By0, sr["bbox"][3] + By0,
    100 * sr["colored"], *sr["diag"]))
log("  rend: jet-t hist/16: %s" % sr["hist"])
ho = np.array(so["hist"], float); ho /= ho.sum()
hr = np.array(sr["hist"], float); hr /= hr.sum() if hr.sum() else 1
log("  hist L1/2 dist = %.3f" % (0.5 * np.abs(ho - hr).sum()))
log("")

# CHECK1: BR band x672..816 y472..517
bx0, by0, bx1, by1 = 672, 472, 816, 517
ob = orig[by0:by1, bx0:bx1]
rb = canvas[by0:by1, bx0:bx1]
raw = (np.abs(ob - rb).sum(2) > 60)


def classify(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    mx, mn = a.max(2), a.min(2)
    out = np.zeros(a.shape[:2], np.int32)
    sat = (mx - mn) > 60
    out[sat & (b >= r) & (b >= g)] = 1
    out[sat & (g > r) & (g >= b)] = 2
    out[sat & (r > 200) & (g > 120) & (b < 100)] = 3
    out[sat & (r > 150) & (g <= 120)] = 4
    out[sat & ~((b >= r) & (b >= g)) & ~((g > r) & (g >= b))
        & ~((r > 200) & (g > 120) & (b < 100)) & ~((r > 150) & (g <= 120))] = 5
    return out


oc, rc = classify(ob), classify(rb)
cdiff = (oc != rc)
H, W = cdiff.shape
gx, gy = 12, 5
mx = max(cdiff[iy * H // gy:(iy + 1) * H // gy, ix * W // gx:(ix + 1) * W // gx].sum()
         for iy in range(gy) for ix in range(gx))
ca = (H // gy) * (W // gx)
log("== CHECK1 BR bottom band x672..816 y472..517 ==")
log("  raw diff=%.1f%%  class diff=%.1f%%  max cell=%d/%d (%.0f%%)" % (
    100 * raw.mean(), 100 * cdiff.mean(), mx, ca, 100.0 * mx / ca))
log("  CHECK1 band%%=%.1f (raw) — target well below k15's 93-98%%" % (100 * raw.mean()))
log("")

# CHECK2: BL label anchors
log("== CHECK2 BL label anchors (dark ink in slide windows) ==")
for (x0, y0, x1, y1, tag) in [
        (236, 302, 278, 322, "UL expect Global Minima"),
        (325, 388, 350, 401, "UR expect Local Minima"),
        (138, 438, 205, 470, "LL expect Local Minima"),
        (300, 448, 346, 470, "LR expect Global Minima")]:
    wo = orig[y0:y1, x0:x1]
    wr = canvas[y0:y1, x0:x1]

    def dk(a):
        lum = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]
        m = lum < 100
        ys, xs = np.nonzero(m)
        return m, (x0 + xs.min(), x0 + xs.max(), y0 + ys.min(), y0 + ys.max()) if len(xs) else None
    mo, bo = dk(wo)
    mr, br_ = dk(wr)
    log("  %-26s orig dark%%=%.1f bbox=%s | rend dark%%=%.1f bbox=%s" % (
        tag, 100 * mo.mean(), bo, 100 * mr.mean(), br_))
log("")

# CHECK3 + markers: red marker-like comps in BL
def markers(a):
    BL = (83, 290, 377, 528)
    bl = a[BL[1]:BL[3], BL[0]:BL[2]]
    rm = redmask(bl)
    rm[:8] = False; rm[-8:] = False; rm[:, :8] = False; rm[:, -8:] = False
    lab, n = ndimage.label(rm, structure=np.ones((3, 3)))
    out = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < 8:
            continue
        w = xs.max() - xs.min() + 1; h = ys.max() - ys.min() + 1
        if 12 <= len(xs) <= 200 and 4 <= w <= 16 and 4 <= h <= 16 and len(xs) / (w * h) > 0.3:
            out.append((len(xs), (xs.min() + xs.max()) // 2 + BL[0], (ys.min() + ys.max()) // 2 + BL[1]))
    return out


om = markers(orig)
rmk = markers(canvas)
log("== CHECK3 red marker-like comps in BL ==")
log("  orig markers: %s" % (om,))
log("  rend markers: %s" % (rmk,))
log("  CHECK3 (rend count <= orig count): %s" % ("PASS" if len(rmk) <= len(om) else "FAIL"))
log("  orig markers at (199,445),(270,482): %s" % (om,))
log("")

# winding: BR largest dark comp wind-ratio
br = canvas[By0 + P:By1 - P, Bx0 + P:Bx1 - P]
lum = 0.299 * br[:, :, 0] + 0.587 * br[:, :, 1] + 0.114 * br[:, :, 2]
dm = (lum < 100) & ((br.max(2) - br.min(2)) < 80)
lab, n = ndimage.label(dm, structure=np.ones((3, 3)))
best = None
for i in range(1, n + 1):
    ys, xs = np.nonzero(lab == i)
    if len(xs) < 15:
        continue
    if best is None or len(xs) > best[0]:
        best = (len(xs), xs, ys)
if best:
    a, xs, ys = best
    order = np.argsort(xs)
    px, py = xs[order], ys[order]
    seg = float(np.hypot(np.diff(px), np.diff(py)).sum())
    straight = float(np.hypot(px[-1] - px[0], py[-1] - py[0]))
    ratio = seg / max(straight, 1.0)
    log("== BR winding path ==")
    log("  largest dark comp area=%d spanx=%d len=%.1f straight=%.1f wind-ratio=%.3f (target ~6.02)" % (
        a, xs.max() - xs.min() + 1, seg, straight, ratio))
    log("  winding=%.3f" % ratio)
else:
    log("== BR winding path ==  no dark comp found wind-ratio=N/A")
log("")

# BR row taper comparison
log("== BR per-row colored%% y455..528 (x615..880) orig vs rend ==")
omf = colmask(orig[By0:By1, Bx0:Bx1]).mean(1)
rmf = colmask(canvas[By0:By1, Bx0:Bx1]).mean(1)
for y in range(455, 529):
    log("  y%d orig=%.0f%% rend=%.0f%%" % (y, 100 * omf[y - By0], 100 * rmf[y - By0]))
a, b = 455 - By0, 529 - By0
log("  row-profile MAE y455..528 = %.2f  corr=%.3f" % (
    np.abs(omf[a:b] - rmf[a:b]).mean(),
    float(np.corrcoef(omf[:187], rmf[:187])[0, 1])))

with open(OUT, "w") as f:
    f.write("\n".join(L) + "\n")
print("wrote", OUT)
