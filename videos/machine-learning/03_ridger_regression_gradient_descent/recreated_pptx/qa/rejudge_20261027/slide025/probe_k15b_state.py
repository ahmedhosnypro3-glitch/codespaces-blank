#!/usr/bin/env python3
"""Focused state probe: render_k15.png (or argv[1]) vs original slide_025.jpg.
Measures the four post-k14 MAJORs directly:
  A. BR bottom margin: per-row colored% y455..539 in BR cols x615..880
  B. BR band x672..816 y472..517: structural diff (colored-vs-white) + raw diff
  C. BR ruggedness: jet-t hist bins>8%, main-diag jet-t mean/std; black path comps
  D. BL bottom labels: ink in left window (x130..210) vs right window (x270..350)
     at y435..475 -> longer/darker string = "Global Minima"
  E. BL red marker-like comps count
  F. TR red residual comps (red minus long horizontal runs) slopes
"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = "/home/codespace/ai_llm_slides"
NS = ROOT + "/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = NS + "/recreated_pptx/qa/rejudge_20261027"
RENDER = sys.argv[1] if len(sys.argv) > 1 else RJ + "/slide025/render_k15.png"

orig = np.array(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)
ren_img = Image.open(RENDER).convert("RGB")
SX, SY = ren_img.size[0] / 960.0, ren_img.size[1] / 540.0
print("render=%s size=%s scale=%.4fx%.4f" % (RENDER, ren_img.size, SX, SY))

def ren_box(x0, y0, x1, y1):
    c = ren_img.crop((int(x0 * SX), int(y0 * SY), int(np.ceil(x1 * SX)), int(np.ceil(y1 * SY))))
    return np.array(c.resize((x1 - x0, y1 - y0), Image.BILINEAR)).astype(np.int32)

ren = ren_box(0, 0, 960, 540)

def colored(a, thr=50):
    return (a.max(2) - a.min(2)) > thr

def redmask(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 110) & (r - g > 50) & (r - b > 50)

def darkmask(a, thr=145, sat=80):
    return (a.max(2) < thr) & ((a.max(2) - a.min(2)) < sat)

def comps(mask, min_area=5):
    lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
    out = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) >= min_area:
            out.append((len(xs), int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())))
    return out

BR = (615, 344, 881, 532)
BL = (83, 290, 377, 528)
TR = (616, 115, 880, 318)

print("\n== A. BR per-row colored%% y455..539 (cols x615..880) ==")
for name, a in (("orig", orig), ("render", ren)):
    x0, y0, x1, y1 = BR
    p = a[y0:y1, x0:x1]
    rows = []
    for yy in range(455, 540):
        band = a[yy, x0:x1]
        rows.append("%d:%d" % (yy, round(100.0 * colored(band[None, :]).mean())))
    print(name + ": " + " ".join(rows))

print("\n== B. BR band x672..816 y472..517 structural diff ==")
bx0, by0, bx1, by1 = 672, 472, 816, 517
ob, rb = orig[by0:by1, bx0:bx1], ren[by0:by1, bx0:bx1]
oc, rc = colored(ob), colored(rb)
raw = (np.abs(ob - rb).sum(2) > 60)
print("orig colored%%=%.1f render colored%%=%.1f raw diff=%.1f%%" % (
    100 * oc.mean(), 100 * rc.mean(), 100 * raw.mean()))
print("orig-colored & render-white: %d px | render-colored & orig-white: %d px" % (
    int((oc & ~rc).sum()), int((rc & ~oc).sum())))

print("\n== C. BR surface stats ==")
JETLUT = (plt.get_cmap("jet")(np.linspace(0, 1, 256))[:, :3] * 255)
def jet_t(a, cm):
    px = a[cm].astype(np.float32)
    d2 = ((px[:, None, :] - JETLUT[None, :, :]) ** 2).sum(2)
    return d2.argmin(1) / 255.0
for name, a in (("orig", orig), ("render", ren)):
    x0, y0, x1, y1 = BR
    p = a[y0:y1, x0:x1]
    cm = colored(p)
    cm[:8] = False; cm[-8:] = False; cm[:, :8] = False; cm[:, -8:] = False
    ys, xs = np.nonzero(cm)
    t = jet_t(p, cm)
    hist = np.histogram(t, bins=16, range=(0, 1))[0] / max(len(t), 1)
    # main diagonal of the surface bbox
    yy, xx = np.mgrid[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    sel = (yy - ys.min()) == (xx - xs.min()) * (ys.max() - ys.min()) / max(xs.max() - xs.min(), 1)
    td = jet_t(p, cm & sel[ys.min():ys.max()+1 if False else slice(None)]) if False else None
    # simpler: sample jet-t along bbox diagonal
    n = min(ys.max() - ys.min(), xs.max() - xs.min()) + 1
    diag = [float(jet_t(p, colored(p))[ (ys.min()+i)*p.shape[1] + (xs.min()+i) ]) for i in range(n)]
    print("%s: bbox local x%d..%d y%d..%d colored%%=%.1f jet-bins>8%%=%d diag mean=%.2f std=%.3f min=%.2f max=%.2f" % (
        name, xs.min(), xs.max(), ys.min(), ys.max(), 100*cm.mean(),
        int((hist > 0.08).sum()), np.mean(diag), np.std(diag), min(diag), max(diag)))
# black path comps inside BR (exclude frame 8px)
print("-- BR dark comps (path) --")
for name, a in (("orig", orig), ("render", ren)):
    x0, y0, x1, y1 = BR
    p = a[y0:y1, x0:x1]
    dm = darkmask(p)
    dm[:8] = False; dm[-8:] = False; dm[:, :8] = False; dm[:, -8:] = False
    cs = sorted(comps(dm, 8), reverse=True)[:6]
    for area, cx0, cy0, cx1, cy1 in cs:
        w, h = cx1 - cx0 + 1, cy1 - cy0 + 1
        print("  %s: area=%d slide-x %d..%d slide-y %d..%d (w%d h%d)" % (name, area, x0+cx0, x0+cx1, y0+cy0, y0+cy1, w, h))

print("\n== D. BL bottom labels ink (y435..478) ==")
LW = (128, 435, 215, 478)   # left window
RW = (268, 435, 352, 478)   # right window
for name, a in (("orig", orig), ("render", ren)):
    for wname, w in (("left", LW), ("right", RW)):
        x0, y0, x1, y1 = w
        p = a[y0:y1, x0:x1]
        dm = darkmask(p)
        ys, xs = np.nonzero(dm)
        if len(xs):
            print("  %s %s: ink=%d xrange=%d..%d yrange=%d..%d" % (
                name, wname, len(xs), x0+xs.min(), x0+xs.max(), y0+ys.min(), y0+ys.max()))
        else:
            print("  %s %s: ink=0" % (name, wname))

print("\n== E. BL red marker-like comps ==")
for name, a in (("orig", orig), ("render", ren)):
    x0, y0, x1, y1 = BL
    p = a[y0:y1, x0:x1]
    rm = redmask(p)
    rm[:8] = False; rm[-8:] = False; rm[:, :8] = False; rm[:, -8:] = False
    rm[413 - y0:423 - y0] = False
    out = []
    for area, rx0, ry0, rx1, ry1 in comps(rm, 8):
        w, h = rx1 - rx0 + 1, ry1 - ry0 + 1
        if 12 <= area <= 200 and 4 <= w <= 16 and 4 <= h <= 16 and area / (w * h) > 0.3:
            out.append((area, x0 + (rx0 + rx1) // 2, y0 + (ry0 + ry1) // 2))
    print("  %s: %s" % (name, out))

print("\n== F. TR red residual comps (red minus horizontal runs>=20px) ==")
def resid(a, box):
    x0, y0, x1, y1 = box
    p = a[y0:y1, x0:x1]
    rm = redmask(p)
    rm[:6] = False; rm[-6:] = False; rm[:, :6] = False; rm[:, -6:] = False
    horiz = ndimage.binary_dilation(rm, structure=np.ones((1, 21)))
    r = rm & ~horiz
    out = []
    for area, rx0, ry0, rx1, ry1 in comps(r, 12):
        w, h = rx1 - rx0 + 1, ry1 - ry0 + 1
        slope = (ry1 - ry0) / max(w - 1, 1)
        out.append((area, x0 + rx0, y0 + ry0, x0 + rx1, y0 + ry1, round(slope, 3)))
    return sorted(out, reverse=True)[:8], int(rm.sum())
for name, a in (("orig", orig), ("render", ren)):
    rs, tot = resid(a, TR)
    print("  %s: red total=%d resid comps (area,x0,y0,x1,y1,slope): %s" % (name, tot, rs))

print("\nPROBE_DONE")
