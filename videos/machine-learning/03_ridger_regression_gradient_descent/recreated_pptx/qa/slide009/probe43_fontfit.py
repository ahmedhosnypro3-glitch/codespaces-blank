#!/usr/bin/env python3
"""Probe 43: caption font fitting. For each measured caption run, find the
Liberation Serif (Times metrics) and Liberation Sans (Arial metrics) size whose
rendered ink width best matches the measured ink width, and report stem widths
for weight determination.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SRC = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def inkbox(text, fontpath, size):
    f = ImageFont.truetype(fontpath, size)
    im = Image.new("L", (2000, 300), 0)
    d = ImageDraw.Draw(im)
    d.text((100, 100), text, fill=255, font=f)
    arr = np.asarray(im)
    ys, xs = np.nonzero(arr > 128)
    if not len(xs):
        return None
    return xs.min()-100, xs.max()-100, ys.min()-100, ys.max()-100

RUNS = [
    ("LCAP1_RED",  "Overfit",                                    109, 160, 488, 501, "C00000"),
    ("LCAP1_BLK",  " (try to minimize the residuals ONLY)",      160, 419, 488, 504, "333333"),
    ("LCAP2",      "Fails to detect the Pattern",                179, 349, 507, 520, "333333"),
    ("RCAP1_RED",  "Generalized",                                523, 610, 488, 501, "C00000"),
    ("RCAP1_BLK",  " (Residuals are not minimized)",             605, 819, 488, 503, "333333"),
    ("RCAP2",      "Successes to detect the Pattern",            502, 774, 506, 526, "333333"),
]
FONTS = {
    "SerifReg":  "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    "SerifBold": "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    "SansReg":   "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "SansBold":  "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
}

print(f"{'run':12s} {'measW':>6s} {'measH':>6s} | " + " ".join(f"{k:>10s}" for k in FONTS))
fits = {}
for name, text, x0, x1, y0, y1, col in RUNS:
    mw = x1 - x0 + 1
    mh = y1 - y0 + 1
    row = {}
    for k, fp in FONTS.items():
        best = None
        for s10 in range(120, 260, 1):
            s = s10 / 10.0
            bb = inkbox(text, fp, int(round(s * 4)))   # render at 4x for precision
            if bb is None:
                continue
            w = (bb[1] - bb[0] + 1) / 4.0
            err = abs(w - mw)
            if best is None or err < best[1]:
                best = (s, err)
        row[k] = best
    fits[name] = row
    print(f"{name:12s} {mw:6d} {mh:6d} | " + " ".join(
        f"{row[k][0]:5.1f}pt({row[k][1]:4.1f})" for k in FONTS))

print("\n=== SerifReg fit at the consensus size, ink widths vs measured ===")
for nm in ("SerifReg", "SerifBold"):
    print(f"-- {nm}")
    for name, text, x0, x1, y0, y1, col in RUNS:
        mw = x1 - x0 + 1
        s = fits[name][nm][0]
        bb = inkbox(text, FONTS[nm], int(round(s * 4)))
        w = (bb[1] - bb[0] + 1) / 4.0
        print(f"   {name:12s} {s:5.1f}pt rendered_w={w:6.1f} measured={mw:4d}  err={w-mw:+5.1f}")

# stem widths from the frame for weight check
print("\n=== stem widths (measured, vertical runs) ===")
for name, x0, x1, y0, y1 in [("LCAP1_RED", 109, 160, 488, 501), ("LCAP2", 179, 349, 507, 520),
                             ("RCAP1_RED", 523, 610, 488, 501), ("RCAP2", 502, 774, 506, 526)]:
    sub = a[y0:y1+1, x0:x1+1].sum(axis=2)
    dark = sub <= 700
    widths = []
    for xx in range(dark.shape[1]):
        col = np.nonzero(dark[:, xx])[0]
        if len(col) >= (y1 - y0):
            widths.append(xx)
    # measure contiguous horizontal thickness of a stem
    print(f"  {name}: full-height cols {len(widths)}")
