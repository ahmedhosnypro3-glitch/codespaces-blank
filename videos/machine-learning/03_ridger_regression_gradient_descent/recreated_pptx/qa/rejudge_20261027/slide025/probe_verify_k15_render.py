#!/usr/bin/env python3
"""Robust render-level verification of promoted k15 (render.png 05:21) vs orig:
BL red x-marker positions, TR red horizontal rows + diagonal segments (band-sampled)."""
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = "/home/codespace/ai_llm_slides"
NS = ROOT + "/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = NS + "/recreated_pptx/qa/rejudge_20261027/slide025"

orig = np.array(Image.open(NS + "/unique_slides/slide_025.jpg").convert("RGB")).astype(np.int32)
rend = np.array(Image.open(RJ + "/render.png").convert("RGB")).astype(np.int32)
SX, SY = 2001 / 960.0, 1125 / 540.0


def red_mask(a):
    return (a[:, :, 0] > 170) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90)


def to_slide(x, y):
    return x / SX, y / SY


def red_comps_slide(mask, box, min_area=8, max_bbox=30):
    """box in slide px (x0,y0,x1,y1); returns comps mapped to slide coords."""
    x0, y0, x1, y1 = box
    sub = np.zeros_like(mask)
    sub[y0:y1, x0:x1] = mask[y0:y1, x0:x1]
    lab, n = ndimage.label(sub, structure=np.ones((3, 3)))
    out = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        area = len(xs)
        if area < min_area:
            continue
        bw, bh = xs.max() - xs.min() + 1, ys.max() - ys.min() + 1
        if bw > max_bbox or bh > max_bbox:
            continue
        out.append((area, bw, bh, area / (bw * bh),
                    (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2))
    return out


print("== BL red x-marker-like comps (slide px) ==")
for tag, img, sc in (("orig", orig, 1.0), ("render", rend, 1.0)):
    m = red_mask(img)
    if tag == "render":
        box = (int(83 * SX), int(290 * SY), int(377 * SX), int(528 * SY))
    else:
        box = (83, 290, 377, 528)
    comps = red_comps_slide(m, box)
    print(" %s:" % tag)
    for (area, bw, bh, fill, cx, cy) in comps:
        sx, sy = cx / SX if tag == "render" else cx, cy / SY if tag == "render" else cy
        print("   area=%4d bbox=%2dx%2d fill=%.2f slide=(%.0f,%.0f)" % (area, bw, bh, fill, sx, sy))

print("== TR red horizontal rows (x616..880) ==")
for tag, img in (("orig", orig), ("render", rend)):
    m = red_mask(img)
    if tag == "render":
        x0, x1 = int(616 * SX), int(880 * SX)
        rows = [(y, 100.0 * m[y, x0:x1].mean()) for y in range(int(160 * SY), int(320 * SY))]
        rows.sort(key=lambda t: -t[1])
        print(" %s top rows (slide y, cov%%):" % tag)
        for y, c in rows[:6]:
            print("   y=%.1f cov=%.1f%%" % (y / SY, c))
    else:
        rows = [(y, 100.0 * m[y, 616:880].mean()) for y in range(160, 320)]
        rows.sort(key=lambda t: -t[1])
        print(" %s top rows:" % tag)
        for y, c in rows[:6]:
            print("   y=%d cov=%.1f%%" % (y, c))


def seg_band_cov(img, x0, y0, x1, y1, band=2):
    n = 80
    ts = np.linspace(0, 1, n)
    cx = x0 + (x1 - x0) * ts
    cy = y0 + (y1 - y0) * ts
    nx, ny = -(y1 - y0), (x1 - x0)
    L = max(np.hypot(nx, ny), 1e-6)
    nx, ny = nx / L, ny / L
    m = red_mask(img)
    hit = 0
    for t in range(n):
        found = False
        for d in range(-band, band + 1):
            x = int(round(cx[t] + nx * d)); y = int(round(cy[t] + ny * d))
            if 0 <= y < m.shape[0] and 0 <= x < m.shape[1] and m[y, x]:
                found = True
                break
        hit += found
    return 100.0 * hit / n


print("== TR diagonal segments (band +-2px) ==")
segs = {"A_long (655,189)->(860,209)": (655, 189, 860, 209),
        "B (737,210)->(755,225)": (737, 210, 755, 225),
        "steep (652,165)->(667,189)": (652, 165, 667, 189),
        "steep2 (660,158)->(672,186)": (660, 158, 672, 186)}
for name, (x0, y0, x1, y1) in segs.items():
    co = seg_band_cov(orig, x0, y0, x1, y1)
    cr = seg_band_cov(rend, x0 * SX, y0 * SY, x1 * SX, y1 * SY)
    print("  %-30s orig=%5.1f%% render=%5.1f%%" % (name, co, cr))
