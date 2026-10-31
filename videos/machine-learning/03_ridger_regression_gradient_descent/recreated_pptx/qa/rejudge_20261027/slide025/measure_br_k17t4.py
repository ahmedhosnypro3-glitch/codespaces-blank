#!/usr/bin/env python3
"""k17t4 BR metrics: measure jet hist / surf bbox / red path / bottom-band taper.

Usage: measure_br_k17t4.py <image> [--slide] 
  default: treat <image> as a slide-space asset (1103x779) composited at
  (615,344,265x187) onto a 960x540 white canvas; --slide = image already 960x540.
All metrics computed on the crop x470..901 y346..530 (431x184) in slide space.
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = NS + "/unique_slides/slide_025.jpg"

# slide-space crop of the BR region
CX0, CY0, CX1, CY1 = 470, 346, 901, 530
# asset placement in slide space
BX0, BY0, BW, BH = 615, 344, 265, 187

# 16 jet bin centers (matplotlib jet at bin midpoints)
_JET = plt.get_cmap("jet")
JET16 = (np.array([_JET((i + 0.5) / 16.0)[:3] for i in range(16)]) * 255)


def colored_mask(a):
    mx, mn = a.max(2), a.min(2)
    m = ((mx - mn) > 60) & (mx > 90)
    red = red_mask(a)
    return m & ~red, red


def red_mask(a):
    return (a[:, :, 0] > 150) & (a[:, :, 1] < 100) & (a[:, :, 2] < 100) & \
           ((a[:, :, 0] - a[:, :, 1]) > 60) & ((a[:, :, 0] - a[:, :, 2]) > 60)


def dark_mask(a):
    mx = a.max(2)
    return (mx < 90) & (a.max(2) - a.min(2) < 40)


def jet_hist(a, m):
    px = a[m].astype(np.float32)
    if len(px) == 0:
        return np.zeros(16, dtype=np.int64)
    d = ((px[:, None, :] - JET16[None, :, :]) ** 2).sum(2)
    idx = d.argmin(1)
    return np.bincount(idx, minlength=16).astype(np.int64)


def to_slide(img_path, as_slide):
    im = Image.open(img_path).convert("RGB")
    if as_slide:
        return np.array(im).astype(np.int32)
    canvas = np.full((540, 960, 3), 255, np.int32)
    a = np.array(im.resize((BW, BH), Image.LANCZOS)).astype(np.int32)
    canvas[BY0:BY0 + BH, BX0:BX0 + BW] = a
    return canvas


def metrics(arr, label):
    crop = arr[CY0:CY1, CX0:CX1]
    cm, red = colored_mask(crop)
    dark = dark_mask(crop)
    hist = jet_hist(crop, cm)
    ys, xs = np.nonzero(cm)
    if len(ys):
        surf = (CX0 + xs.min(), CY0 + ys.min(), CX0 + xs.max(), CY0 + ys.max())
    else:
        surf = None
    rys, rxs = np.nonzero(red)
    redbb = (CX0 + rxs.min(), CY0 + rys.min(), CX0 + rxs.max(), CY0 + rys.max()) if len(rxs) else None
    dys, dxs = np.nonzero(dark & ~cm)
    darkbb = (CX0 + dxs.min(), CY0 + dys.min(), CX0 + dxs.max(), CY0 + dys.max()) if len(dxs) else None
    # bottom-band taper: per-row colored fraction for slide rows 460..529
    band_rows = np.arange(460, 530)
    prof = []
    for y in band_rows:
        row = cm[y - CY0]
        prof.append(100.0 * row.mean())
    prof = np.array(prof)
    # bottom strip = rows 515..529 (bottom 15 rows of crop)
    strip = cm[515 - CY0:530 - CY0]
    print("== %s" % label)
    print("crop %dx%d colored=%d (%.1f%%) red=%d dark=%d" % (
        CX1 - CX0, CY1 - CY0, cm.sum(), 100.0 * cm.mean(), red.sum(), (dark & ~cm).sum()))
    print("jet16 hist: %s  sum=%d" % (list(hist), hist.sum()))
    h = hist.astype(np.float64)
    if h.sum():
        print("jet16 norm: %s" % np.round(h / h.sum(), 4).tolist())
    print("surf bbox (slide px): %s" % (surf,))
    print("red  bbox (slide px): %s count=%d" % (redbb, red.sum()))
    print("dark bbox (slide px): %s count=%d" % (darkbb, (dark & ~cm).sum()))
    print("band taper rows460..529: first=%.1f last=%.1f  profile=%s" % (
        prof[0], prof[-1], np.round(prof[::6], 1).tolist()))
    print("bottom strip rows515..529 colored frac=%.3f  meanRGB=%s" % (
        strip.mean(), np.round(crop[515 - CY0:530 - CY0].reshape(-1, 3).mean(0), 1).tolist()))
    return dict(hist=hist, surf=surf, red=redbb, redn=int(red.sum()),
                prof=prof, cm=cm)


def l1(h1, h2):
    a = h1.astype(np.float64); b = h2.astype(np.float64)
    a = a / max(a.sum(), 1); b = b / max(b.sum(), 1)
    return float(np.abs(a - b).sum())


if __name__ == "__main__":
    as_slide = "--slide" in sys.argv
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    orig = np.array(Image.open(ORIG).convert("RGB")).astype(np.int32)
    mo = metrics(orig, "ORIG slide_025.jpg")
    if args:
        mr = metrics(to_slide(args[0], as_slide), "RENDER %s" % args[0])
        print("== L1 jet hist (norm, 16 bins): %.4f" % l1(mo["hist"], mr["hist"]))
        po, pr = mo["prof"], mr["prof"]
        print("== band profile L1 (rows460..529): %.2f" % float(np.abs(po - pr).mean()))
        print("orig surf %s vs render surf %s" % (mo["surf"], mr["surf"]))
        print("orig red  %s n=%d vs render red %s n=%d" % (mo["red"], mo["redn"], mr["red"], mr["redn"]))
