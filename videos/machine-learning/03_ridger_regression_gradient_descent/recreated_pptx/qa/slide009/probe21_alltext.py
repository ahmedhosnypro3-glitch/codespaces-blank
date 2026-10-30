#!/usr/bin/env python3
"""Probe 21: measure EVERY remaining text element's ink bbox with the robust
'differs from local background by > 55' predicate (which rejects JPEG noise on
gray regions — the failure mode of a plain brightness threshold), then fit a
font+size to each.

Elements:
  LCAP1_RED  'Overfit'                                  (red keyword)
  LCAP1_BLK  '(try to minimize the residuals ONLY)'     (rest of line 1)
  LCAP2      'Fails to detect the Pattern'
  RCAP1_RED  'Generalized'
  RCAP1_BLK  '(Residuals are not minimized)'
  RCAP2      'Successes to detect the Pattern'
  LEQ / REQ  the annotation-box equations
  LMM / RMM  the 'mm' labels
  BADGE      the numeral '9'
"""
import numpy as np
from PIL import Image
from PIL import ImageFont, ImageDraw

SRC = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]


def bbox_diff(x0, x1, y0, y1, thr=55):
    """ink bbox under 'differs from per-row background mode by > thr'."""
    best = None
    for y in range(y0, y1 + 1):
        row = a[y, x0:x1 + 1]
        q = (row // 8) * 8
        keys, counts = np.unique(q.reshape(-1, 3), axis=0, return_counts=True)
        bg = keys[counts.argmax()]
        d = np.abs(row - bg).max(axis=1)
        xs = np.where(d > thr)[0]
        if not len(xs):
            continue
        lo, hi = x0 + xs.min(), x0 + xs.max()
        if best is None:
            best = [lo, hi, y, y]
        else:
            best[0] = min(best[0], lo)
            best[1] = max(best[1], hi)
            best[2] = min(best[2], y)
            best[3] = max(best[3], y)
    return best


def red_bbox(x0, x1, y0, y1):
    """ink bbox restricted to red-family pixels."""
    m = (r - g > 30) & (r - b > 30) & (r > 90)
    sub = m[y0:y1 + 1, x0:x1 + 1]
    ys, xs = np.where(sub)
    if not len(ys):
        return None
    return [x0 + xs.min(), x0 + xs.max(), y0 + ys.min(), y0 + ys.max()]


ELEMS = [
    ("LCAP1_RED", "Overfit", "red", 100, 170, 486, 506),
    ("LCAP1_BLK", "(try to minimize the residuals ONLY)", "blk", 160, 470, 486, 506),
    ("LCAP2", "Fails to detect the Pattern", "blk", 100, 470, 506, 526),
    ("RCAP1_RED", "Generalized", "red", 495, 615, 486, 506),
    ("RCAP1_BLK", "(Residuals are not minimized)", "blk", 605, 838, 486, 506),
    ("RCAP2", "Successes to detect the Pattern", "blk", 495, 838, 506, 526),
    ("LEQ", "50.85^2 = 2585", "blk", 140, 460, 140, 180),
    ("REQ", "63.64^2 = 4050", "blk", 510, 865, 140, 180),
    ("LMM", "50.85 mm", "blk", 96, 152, 140, 182),
    ("RMM", "63.64 mm", "blk", 492, 548, 140, 182),
    ("BADGE", "9", "blk", 860, 892, 58, 88),
]
print("name                text                                     x0    x1    y0    y1     w     h")
RES = {}
for nm, text, kind, x0, x1, y0, y1 in ELEMS:
    if kind == "red":
        bb = red_bbox(x0, x1, y0, y1)
    else:
        bb = bbox_diff(x0, x1, y0, y1)
    if bb is None:
        print(f"{nm:18s} {text!r:42s} <none>")
        continue
    RES[nm] = (text, bb[1] - bb[0] + 1, bb)
    print(f"{nm:18s} {text!r:42s} {bb[0]:5d} {bb[1]:5d} {bb[2]:5d} {bb[3]:5d} "
          f"{bb[1]-bb[0]+1:5d} {bb[3]-bb[2]+1:5d}")

# ---------------- font fit ----------------
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def fit(text, meas_w):
    rows = []
    for label, path in (("SerifReg", SERIF), ("SerifBold", SERIF_B),
                        ("SansReg", SANS), ("SansBold", SANS_B)):
        for size in [x / 4 for x in range(40, 100)]:
            f = ImageFont.truetype(path, int(round(size * 4)))
            im = Image.new("L", (10, 10), 255)
            d = ImageDraw.Draw(im)
            bb = d.textbbox((0, 0), text, font=f)
            w = (bb[2] - bb[0]) / 4.0
            hb = d.textbbox((0, 0), "H", font=f)
            rows.append((abs(w - meas_w), label, size, w, (hb[3] - hb[1]) / 4.0))
    rows.sort()
    return rows[:3]


print("\n================ FONT FIT (measured ink width) ================")
for nm, (text, w, bb) in RES.items():
    print(f"\n{nm} measured w={w} h={bb[3]-bb[2]+1}")
    for diff, label, size, fw, cap in fit(text, w):
        print(f"   {label:9s} {size:5.2f}pt -> w {fw:6.1f} ({100*(fw-w)/w:+5.2f}%) capH {cap:5.1f}")
