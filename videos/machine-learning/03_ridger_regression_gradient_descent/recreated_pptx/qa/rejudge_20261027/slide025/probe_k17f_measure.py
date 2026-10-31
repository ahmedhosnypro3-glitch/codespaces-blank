#!/usr/bin/env python3
"""Measure original slide_025.jpg panel structure to drive k17f regeneration.
Panels (from build/slide_025.js addImage calls, slide px, 960x540):
  TL x85..265 y115..288 (180x173) | TR x616..879 y115..317 (263x202)
  BL x83..376  y290..527 (293x237) | BR x615..880 y344..531 (265x187)
For each: colored-surface bbox, jet-t histogram (16 bins), row/col profiles,
extrema count of the jet-t field, red comps census. BR gets the bottom-band
taper profile y472..528. TR gets the diagonal red segment census around
(652,189)->(667,165).
"""
import numpy as np
from PIL import Image
from scipy import ndimage

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
orig = np.array(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)
print("orig size", orig.shape)

PANELS = {
    "tl": (85, 115, 266, 289),
    "tr": (616, 115, 880, 318),
    "bl": (83, 290, 377, 528),
    "br": (615, 344, 881, 532),
}

# jet colormap lookup: t in [0,1] -> RGB (matplotlib jet, 256 entries)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
JET = (plt.get_cmap("jet")(np.linspace(0, 1, 256))[:, :3] * 255).astype(np.int32)


def colmask(a):
    mx, mn = a.max(2), a.min(2)
    m = ((mx - mn) > 60) & (mx > 90)
    pr = (a[:, :, 0] > 170) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90)
    return m & ~pr


def redmask(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 110) & (r - g > 50) & (r - b > 50)


def jet_t(a):
    """per colored pixel, nearest jet t"""
    m = colmask(a)
    px = a[m]
    if len(px) == 0:
        return m, np.array([])
    d = ((px[:, None, :] - JET[None, :, :]) ** 2).sum(2)
    t = d.argmin(1) / 255.0
    return m, t


for name, (x0, y0, x1, y1) in PANELS.items():
    p = orig[y0:y1, x0:x1]
    m, t = jet_t(p)
    ys, xs = np.nonzero(m)
    print("\n== %s panel x%d..%d y%d..%d ==" % (name, x0, x1 - 1, y0, y1 - 1))
    if len(xs):
        print("  surf bbox local x%d..%d y%d..%d (slide x%d..%d y%d..%d) colored%%=%.1f" % (
            xs.min(), xs.max(), ys.min(), ys.max(),
            x0 + xs.min(), x0 + xs.max(), y0 + ys.min(), y0 + ys.max(), 100 * m.mean()))
        h16, _ = np.histogram(t, bins=16, range=(0, 1))
        print("  jet-t hist/16: %s  bins>8%%=%d  t mean=%.2f std=%.2f" % (
            list(h16), (h16 > 0.08 * len(t)).sum(), t.mean(), t.std()))
        # row profile of colored% (8px rows)
        H = m.shape[0]
        prof = [100 * m[i * H // 8:(i + 1) * H // 8].mean() for i in range(8)]
        print("  row colored%% (8 bands top->bottom): %s" % ["%.0f" % v for v in prof])
        # extrema of jet-t field: smooth and count local max/min on coarse grid
        T = np.full(m.shape, np.nan)
        T[m] = t
        g = 8
        gh, gw = H // g, m.shape[1] // g
        small = np.zeros((gh, gw))
        for i in range(gh):
            for j in range(gw):
                blk = T[i * g:(i + 1) * g, j * g:(j + 1) * g]
                v = blk[~np.isnan(blk)]
                small[i, j] = v.mean() if len(v) else np.nan
        sm = ndimage.uniform_filter(np.nan_to_num(small, nan=np.nanmean(small)), 2)
        mx = ndimage.maximum_filter(sm, 3)
        mn = ndimage.minimum_filter(sm, 3)
        nmax = int(((sm == mx) & ~np.isnan(sm)).sum())
        nmin = int(((sm == mn) & ~np.isnan(sm)).sum())
        print("  coarse t-field extrema: maxima=%d minima=%d (grid %dx%d)" % (nmax, nmin, gh, gw))
        print("  coarse t-field map (x10, nan=.):")
        for i in range(gh):
            print("   " + "".join("." if np.isnan(small[i, j]) else "%X" % int(max(0, min(15, small[i, j] * 16))) for j in range(gw)))
    # red comps
    rm = redmask(p)
    rm[:6] = False; rm[-6:] = False; rm[:, :6] = False; rm[:, -6:] = False
    lab, n = ndimage.label(rm, structure=np.ones((3, 3)))
    comps = []
    for i in range(1, n + 1):
        ys2, xs2 = np.nonzero(lab == i)
        if len(xs2) < 5:
            continue
        w = xs2.max() - xs2.min() + 1; h = ys2.max() - ys2.min() + 1
        comps.append((len(xs2), x0 + xs2.min(), y0 + ys2.min(), x0 + xs2.max(), y0 + ys2.max(), w, h))
    print("  red comps (area>=5):")
    for c in sorted(comps, key=lambda c: -c[0])[:14]:
        print("    area=%d x%d..%d y%d..%d (w%d h%d)" % c)

# BR bottom band taper: per-row colored% for slide y460..531 inside BR x615..880
print("\n== BR bottom band taper (per slide row y455..531, x620..875) ==")
for y in range(455, 532, 2):
    row = orig[y, 620:876]
    m = colmask(row[None, :, :])[0]
    rm = redmask(row[None, :, :])[0]
    print("  y%d colored=%.1f%% red=%.1f%%" % (y, 100 * m.mean(), 100 * rm.mean()))

# TR diagonal red segment: window around (652,189)->(667,165), measure red-hit fraction
# along the segment and its angle
print("\n== TR diagonal red segment window x640..680 y155..200 ==")
p = orig[155:200, 640:680]
rm = redmask(p)
ys3, xs3 = np.nonzero(rm)
if len(xs3):
    print("  red px count=%d bbox local x%d..%d y%d..%d -> slide x%d..%d y%d..%d" % (
        len(xs3), xs3.min(), xs3.max(), ys3.min(), ys3.max(),
        640 + xs3.min(), 640 + xs3.max(), 155 + ys3.min(), 155 + ys3.max()))
    # fit line: slope dy/dx
    A = np.polyfit(xs3, ys3, 1)
    print("  fit slope=%.3f intercept=%.1f -> slide-space line through (652,189)-(667,165): slope=%.3f" % (
        A[0], A[1], (165 - 189) / (667 - 652)))
    # red-hit along the segment (652,189)->(667,165): sample points, fraction red within 2px
    hits = 0; tot = 0
    for f in np.linspace(0, 1, 60):
        sx = 652 + 15 * f; sy = 189 - 24 * f
        x0w = int(sx) - 2; x1w = int(sx) + 3; y0w = int(sy) - 2; y1w = int(sy) + 3
        w = redmask(orig[y0w:y1w, x0w:x1w])
        tot += 1
        if w.any():
            hits += 1
    print("  red-hit along (652,189)->(667,165): %d/%d = %.1f%%" % (hits, tot, 100 * hits / tot))
else:
    print("  no red in window")

# BL label anchor windows: dark-text presence
print("\n== BL label anchor windows (dark ink %) ==")
for (lx0, ly0, lx1, ly1, tag) in [
    (138, 438, 205, 470, "Local Minima LL"),
    (300, 448, 346, 470, "Global Minima LR"),
    (325, 388, 350, 401, "Local Minima UR"),
    (236, 302, 278, 322, "Global Minima UL"),
]:
    w = orig[ly0:ly1, lx0:lx1]
    lum = 0.299 * w[:, :, 0] + 0.587 * w[:, :, 1] + 0.114 * w[:, :, 2]
    dk = (lum < 100)
    ys4, xs4 = np.nonzero(dk)
    if len(xs4):
        print("  %-18s x%d..%d y%d..%d dark%%=%.1f ink bbox slide x%d..%d y%d..%d" % (
            tag, lx0, lx1 - 1, ly0, ly1 - 1, 100 * dk.mean(),
            lx0 + xs4.min(), lx0 + xs4.max(), ly0 + ys4.min(), ly0 + ys4.max()))
    else:
        print("  %-18s no dark ink" % tag)

# BL red x markers at (199,445),(270,482): confirm and measure size
print("\n== BL red marker windows ==")
for (mx, my) in [(199, 445), (270, 482)]:
    w = orig[my - 10:my + 11, mx - 10:mx + 11]
    rm = redmask(w)
    ys5, xs5 = np.nonzero(rm)
    if len(xs5):
        print("  (%d,%d): area=%d bbox slide x%d..%d y%d..%d" % (
            mx, my, len(xs5), mx - 10 + xs5.min(), mx - 10 + xs5.max(),
            my - 10 + ys5.min(), my - 10 + ys5.max()))
    else:
        print("  (%d,%d): none" % (mx, my))
