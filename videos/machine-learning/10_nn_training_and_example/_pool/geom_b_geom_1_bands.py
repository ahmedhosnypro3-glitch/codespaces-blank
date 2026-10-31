#!/usr/bin/env python3
"""Lane G (b_geom_1) — canonical structure bands per image (chrome masked)."""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
TMP = f"{NS}/_pool/tmp_geom_b_geom_1"
SLIDES = ["001", "004", "005", "006", "007"]


def load(n):
    o = np.asarray(Image.open(f"{NS}/unique_slides/slide_{n}.jpg").convert("RGB")).astype(np.int16)
    r = np.asarray(Image.open(f"{TMP}/frame_{n}.png").convert("RGB")).astype(np.int16)
    return o, r


def red_rect(a):
    h, w = a.shape[:2]
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    red = (r > 110) & (r - g > 35) & (r - b > 35)
    rows = np.nonzero(red.sum(axis=1) > 0.50 * w)[0]
    cols = np.nonzero(red.sum(axis=0) > 0.50 * h)[0]
    return int(cols.min()), int(rows.min()), int(cols.max()), int(rows.max())


def badge(a, rect):
    h, w = a.shape[:2]
    bx0, by0, bx1, by1 = rect
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    yel = (r > 185) & (g > 170) & (b > 110) & (b < 220)
    win = np.zeros_like(yel)
    win[by0:by1, bx0:bx1] = True
    win[:, :int(0.78 * w)] = False
    win[int(0.22 * h):, :] = False
    yel &= win
    lab, n = ndimage.label(yel, structure=np.ones((3, 3)))
    best, bestn = None, 0
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(ys) > bestn:
            best, bestn = (xs, ys), len(ys)
    if best is None or bestn < 30:
        return None
    xs, ys = best
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def structure(a, rect, bg, badge_box, strip_y, k=7, thr=26):
    """Local-median edge mask: catches text strokes AND drawn box borders."""
    lum = a.astype(np.float32).mean(axis=2)
    med = ndimage.median_filter(lum, size=k)
    m = np.abs(lum - med) > thr
    x0, y0, x1, y1 = rect
    m[max(0, y0 - 4):y0 + 6, :] = False
    m[max(0, y1 - 5):y1 + 5, :] = False
    m[:, max(0, x0 - 4):x0 + 6] = False
    m[:, max(0, x1 - 5):x1 + 5] = False
    m[strip_y:, :] = False
    if badge_box:
        px0, py0, px1, py1 = badge_box
        m[max(0, py0 - 5):py1 + 6, max(0, px0 - 5):px1 + 6] = False
    return m


def runs(idx, gap):
    if len(idx) == 0:
        return []
    out, s, p = [], int(idx[0]), int(idx[0])
    for i in idx[1:]:
        i = int(i)
        if i - p > gap:
            out.append((s, p + 1))
            s = i
        p = i
    out.append((s, p + 1))
    return out


def canon_bands(m, rect, minpx=3, gap=5):
    x0, y0, x1, y1 = rect
    sx = 960.0 / (x1 - x0)
    sy = 540.0 / (y1 - y0)
    out = []
    for a, b in runs(np.nonzero(m.sum(axis=1) >= minpx)[0], gap):
        sub = m[a:b]
        ys, xs = np.nonzero(sub)
        if xs.size < 8:
            continue
        out.append({"x0": round((int(xs.min()) - x0) * sx, 1),
                    "x1": round((int(xs.max()) + 1 - x0) * sx, 1),
                    "y0": round((a - y0) * sy, 1),
                    "y1": round((b - y0) * sy, 1),
                    "px": int(xs.size)})
    return out


def fmt(b):
    return "x %6.1f..%6.1f (w=%6.1f) y %6.1f..%6.1f (h=%6.1f) px=%d" % (
        b["x0"], b["x1"], b["x1"] - b["x0"], b["y0"], b["y1"], b["y1"] - b["y0"], b["px"])


for n in (sys.argv[1:] or SLIDES):
    o, r = load(n)
    obr, rbr = red_rect(o), red_rect(r)
    ob, rb = badge(o, obr), badge(r, rbr)
    om = structure(o, obr, None, ob, 517)
    rm = structure(r, rbr, None, rb, 529)
    print("=== slide_%s  orig_rect=%s badge=%s | rend_rect=%s badge=%s" %
          (n, obr, ob, rbr, rb))
    for i, b in enumerate(canon_bands(om, obr), 1):
        print("   O%-2d %s" % (i, fmt(b)))
    for i, b in enumerate(canon_bands(rm, rbr), 1):
        print("   R%-2d %s" % (i, fmt(b)))
