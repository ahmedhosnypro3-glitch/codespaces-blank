#!/usr/bin/env python3
"""Fast vectorized state probe: render (argv[1], default render_k15.png) vs orig."""
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
ren = np.array(ren_img.crop((0, 0, int(960 * SX), int(540 * SY))).resize((960, 540), Image.BILINEAR)).astype(np.int32)
print("render=%s size=%s" % (RENDER, ren_img.size))

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

print("\n== A. BR per-row colored%% y500..539 (cols x615..880) ==")
for name, a in (("orig", orig), ("render", ren)):
    x0, _, x1, _ = BR
    rows = []
    for yy in range(500, 540):
        rows.append("%d:%d" % (yy, round(100.0 * colored(a[yy:yy+1, x0:x1]).mean())))
    print(name + ": " + " ".join(rows))

print("\n== B. BR band x672..816 y472..517 ==")
bx0, by0, bx1, by1 = 672, 472, 816, 517
ob, rb = orig[by0:by1, bx0:bx1], ren[by0:by1, bx0:bx1]
oc, rc = colored(ob), colored(rb)
raw = (np.abs(ob - rb).sum(2) > 60)
print("orig colored%%=%.1f render colored%%=%.1f raw-diff=%.1f%% | orig-colored&render-white=%d render-colored&orig-white=%d" % (
    100*oc.mean(), 100*rc.mean(), 100*raw.mean(), int((oc & ~rc).sum()), int((rc & ~oc).sum())))

print("\n== C. BR surface stats ==")
JETLUT = (plt.get_cmap("jet")(np.linspace(0, 1, 256))[:, :3] * 255).astype(np.float32)
def jet_t_vec(a, cm):
    px = a[cm].astype(np.float32)
    d2 = ((px[:, None, :] - JETLUT[None, :, :]) ** 2).sum(2)
    return d2.argmin(1) / 255.0
for name, a in (("orig", orig), ("render", ren)):
    x0, y0, x1, y1 = BR
    p = a[y0:y1, x0:x1]
    cm = colored(p)
    cm[:8] = False; cm[-8:] = False; cm[:, :8] = False; cm[:, -8:] = False
    ys, xs = np.nonzero(cm)
    t = jet_t_vec(p, cm)
    h16 = np.histogram(t, bins=16, range=(0, 1))[0] / len(t)
    bx0, bx1, by0, by1 = xs.min(), xs.max(), ys.min(), ys.max()
    n = 120
    di = []
    for i in range(n):
        xx = int(bx0 + (bx1 - bx0) * i / (n - 1)); yy = int(by0 + (by1 - by0) * i / (n - 1))
        if cm[yy, xx]:
            px = p[yy, xx].astype(np.float32)
            di.append(float(((JETLUT - px) ** 2).sum(1).argmin()) / 255.0)
    di = np.array(di)
    ext = int(np.sum(np.diff(np.sign(np.diff(ndimage.uniform_filter1d(di, 5)))) != 0)) if len(di) > 10 else -1
    print("%s: bbox slide x%d..%d y%d..%d colored%%=%.1f bins>8%%=%d diag mean=%.2f std=%.3f extrema=%d" % (
        name, x0+xs.min(), x0+xs.max(), y0+ys.min(), y0+ys.max(), 100*cm.mean(),
        int((h16 > 0.08).sum()), di.mean() if len(di) else -1, di.std() if len(di) else -1, ext))
print("-- BR dark comps (winding path) --")
for name, a in (("orig", orig), ("render", ren)):
    x0, y0, x1, y1 = BR
    p = a[y0:y1, x0:x1]
    dm = darkmask(p)
    dm[:8] = False; dm[-8:] = False; dm[:, :8] = False; dm[:, -8:] = False
    for area, cx0, cy0, cx1, cy1 in sorted(comps(dm, 8), reverse=True)[:5]:
        w, h = cx1-cx0+1, cy1-cy0+1
        print("  %s: area=%d slide-x %d..%d slide-y %d..%d (w%d h%d)" % (name, area, x0+cx0, x0+cx1, y0+cy0, y0+cy1, w, h))

print("\n== D. BL bottom labels ink y435..478, left win x128..215, right win x268..352 ==")
for name, a in (("orig", orig), ("render", ren)):
    for wname, wx0, wx1 in (("left", 128, 215), ("right", 268, 352)):
        p = a[435:478, wx0:wx1]
        dm = darkmask(p)
        ys, xs = np.nonzero(dm)
        if len(xs):
            print("  %s %s: ink=%d xrange=%d..%d yrange=%d..%d" % (name, wname, len(xs), wx0+xs.min(), wx0+xs.max(), 435+ys.min(), 435+ys.max()))
        else:
            print("  %s %s: ink=0" % (name, wname))

print("\n== E. BL red marker-like comps ==")
for name, a in (("orig", orig), ("render", ren)):
    x0, y0, x1, y1 = BL
    p = a[y0:y1, x0:x1]
    rm = redmask(p)
    rm[:8] = False; rm[-8:] = False; rm[:, :8] = False; rm[:, -8:] = False
    rm[413-y0:423-y0] = False
    out = []
    for area, rx0, ry0, rx1, ry1 in comps(rm, 8):
        w, h = rx1-rx0+1, ry1-ry0+1
        if 12 <= area <= 200 and 4 <= w <= 16 and 4 <= h <= 16 and area/(w*h) > 0.3:
            out.append((area, x0+(rx0+rx1)//2, y0+(ry0+ry1)//2))
    print("  %s: %s" % (name, out))

print("\n== F. TR red residual comps (red minus horiz runs>=20px) ==")
for name, a in (("orig", orig), ("render", ren)):
    x0, y0, x1, y1 = TR
    p = a[y0:y1, x0:x1]
    rm = redmask(p)
    rm[:6] = False; rm[-6:] = False; rm[:, :6] = False; rm[:, -6:] = False
    horiz = ndimage.binary_dilation(rm, structure=np.ones((1, 21)))
    r = rm & ~horiz
    out = []
    for area, rx0, ry0, rx1, ry1 in comps(r, 12):
        w = rx1-rx0+1
        slope = (ry1-ry0)/max(w-1, 1)
        out.append((area, x0+rx0, y0+ry0, x0+rx1, y0+ry1, round(slope, 3)))
    print("  %s: redtot=%d resid=%s" % (name, int(rm.sum()), sorted(out, reverse=True)[:8]))

print("\nPROBE_DONE")
