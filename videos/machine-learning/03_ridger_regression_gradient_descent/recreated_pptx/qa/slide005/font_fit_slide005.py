#!/usr/bin/env python3
"""Glyph-level font/size identification for slide_005.jpg text bands.

For each (text, target ink bbox) band, render the string in every candidate font
at a range of sizes, rasterize with PIL, and score against the original ink mask
with an IoU-like overlap over the band. The winner is the (font, size) whose ink
bitmap best reproduces the original's, which also fixes the baseline offset.

Output: recreated_pptx/qa/slide005/font_fit_slide005.json
"""
import json
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

SRC = ("videos/machine-learning/03_ridger_regression_gradient_descent/"
       "unique_slides/slide_005.jpg")
OUT = ("videos/machine-learning/03_ridger_regression_gradient_descent/"
       "recreated_pptx/qa/slide005/font_fit_slide005.json")

FONTS = {
    "DejaVuSans-Bold": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "DejaVuSans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "DejaVuSansCondensed-Bold": "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf",
    "DejaVuSansCondensed": "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf",
    "LiberationSans-Bold": "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "LiberationSans": "/usr/share/fonts/truetype/liberation/LiberationSans.ttf",
    "LiberationSansNarrow-Bold": "/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf",
    "LiberationSansNarrow": "/usr/share/fonts/truetype/liberation/LiberationSansNarrow.ttf",
}
FONTS = {k: v for k, v in FONTS.items() if os.path.exists(v)}

img = np.asarray(Image.open(SRC).convert("L")).astype(int)

# (label, text, y_lo, y_hi, x_lo, x_hi)  -- band around the ink (frame px)
BANDS = [
    ("title", "Minimization of Loss function to obtain BEST model parameters", 64, 94, 156, 815),
    ("remember1", "Remember", 133, 153, 680, 760),
    ("l1", "X is a matrix, W is a vector,", 155, 173, 680, 880),
    ("l2", "XW is a vector", 176, 194, 680, 792),
    ("pinkright", "Get Best W that minimizes the loss", 303, 324, 192, 508),
    ("l3", "Remember", 373, 390, 680, 740),
]


def orig_mask(y0, y1, x0, x1):
    return img[y0:y1, x0:x1] < 150


def score(text, fpath, size, y0, y1, x0, x1):
    """Render text at size in a band-sized canvas, slide it to best overlap."""
    om = orig_mask(y0, y1, x0, x1)
    H, W = om.shape
    f = ImageFont.truetype(fpath, int(round(size)))
    bbox = f.getbbox(text)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    if tw <= 0 or th <= 0:
        return None
    # place the text on a canvas the size of the band, trying all integer offsets
    best = (-1.0, None)
    canvas = Image.new("L", (max(W, tw + 4), max(H, th + 4)), 0)
    d = ImageDraw.Draw(canvas)
    # vertical anchor by the text's top metric
    for dy in range(0, max(1, H - th + 1)):
        for dx in range(0, max(1, W - tw + 1)):
            c2 = Image.new("L", (max(W, tw + 4), max(H, th + 4)), 0)
            d2 = ImageDraw.Draw(c2)
            d2.text((dx, dy), text, font=f, fill=255)
            m = np.asarray(c2)[0:H, 0:W] > 100
            if m.sum() == 0:
                continue
            inter = (m & om).sum()
            union = (m | om).sum()
            iou = inter / union if union else 0.0
            if iou > best[0]:
                best = (iou, (dx, dy))
    return best


res = {}
for label, text, y0, y1, x0, x1 in BANDS:
    om = orig_mask(y0, y1, x0, x1)
    rows = []
    for fname, fpath in FONTS.items():
        for size in range(8, 27):
            r = score(text, fpath, size, y0, y1, x0, x1)
            if r:
                rows.append((round(r[0], 4), fname, size, r[1]))
    rows.sort(reverse=True)
    res[label] = {
        "text": text,
        "band": [x0, x1, y0, y1],
        "obs_ink_n": int(om.sum()),
        "best": rows[:5],
    }
    print(f"{label}: {text[:34]!r}")
    for s, fn, sz, off in rows[:3]:
        print(f"    IoU={s:.3f} {fn:32s} {sz}pt offset={off}")

with open(OUT, "w") as f:
    json.dump(res, f, indent=1)
print("wrote", OUT)
