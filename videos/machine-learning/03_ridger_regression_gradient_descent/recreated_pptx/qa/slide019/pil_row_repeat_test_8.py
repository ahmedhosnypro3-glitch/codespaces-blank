#!/usr/bin/env python3
"""Decisive PIL test: did the original's NO REG rows 2/3 repeat row 1's digits?

For each row group of a column, extract the ink bitmap of each of its three
test lines (the y-value line), normalise it, and cross-correlate across row
groups. If row 2 and row 3 really repeated row 1's "60 / 80 / 100", their
bitmaps would correlate strongly with row 1's; if they carry different values
(32.4 / 42.3 / 52.3 and 24.4 / 31.2 / 38), they will not.

The same measurement is run on the build renders as a control:
render_6 repeats 60/80/100 in rows 2/3 (the judged defect), render_8 does not.
"""
from PIL import Image
import numpy as np

DECK = "videos/machine-learning/03_ridger_regression_gradient_descent"
QA = f"{DECK}/recreated_pptx/qa/slide019"
ORIG = f"{DECK}/unique_slides/slide_019.jpg"

# Original frame: NO REG column digit lines (frame coords), measured from the
# pale-blue/dark ink maps.
ORIG_LINES = {
    "rg1": [(229, 244), (253, 268), (279, 290)],
    "rg2": [(316, 329), (337, 352), (361, 376)],
    "rg3": [(446, 460), (470, 484), (496, 507)],
}
ORIG_X = (306, 338)

SCALE = 150 / 72.0
REND_LINES = {
    "rg1": [(246, 262), (246, 262), (246, 262)],
    "rg2": [(351, 367), (351, 367), (351, 367)],
    "rg3": [(461, 477), (461, 477), (461, 477)],
}


def orig_ink_crop(path, fx0, fx1, fy0, fy1):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(float)
    crop = a[fy0:fy1, fx0:fx1]
    r, g, b = crop[:, :, 0], crop[:, :, 1], crop[:, :, 2]
    # ink = blue-dominant OR dark; weight by ink strength
    blue = np.clip((b - r) - 10, 0, None)
    dark = np.clip(150 - (r + g + b) / 3.0, 0, None)
    return np.maximum(blue, dark)


def rend_green_crop(path, fx0, fx1, fy0, fy1):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(float)
    crop = a[int(fy0 * SCALE):int(fy1 * SCALE),
             int(fx0 * SCALE):int(fx1 * SCALE)]
    r, g, b = crop[:, :, 0], crop[:, :, 1], crop[:, :, 2]
    return np.clip((g - r) - 10, 0, None)


def norm(bm):
    ys, xs = np.nonzero(bm > 20)
    if len(ys) == 0:
        return None
    sub = bm[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    out = np.asarray(Image.fromarray(np.clip(sub, 0, 255).astype(np.uint8))
                     .resize((24, 12), Image.BILINEAR)).astype(float)
    out = out - out.min()
    if out.max() == 0:
        return None
    return out / out.max()


def corr(a, b):
    if a is None or b is None:
        return float("nan")
    a = a - a.mean()
    b = b - b.mean()
    d = np.sqrt((a * a).sum() * (b * b).sum())
    return float((a * b).sum() / d) if d else float("nan")


def report(title, lines, cropfn, path, xwin):
    print(f"===== {title} =====")
    mats = {}
    for rg, specs in lines.items():
        mats[rg] = []
        for (y0, y1) in specs:
            mats[rg].append(norm(cropfn(path, xwin[0], xwin[1], y0, y1)))
    for rg in lines:
        for i in range(3):
            vals = [round(corr(mats[rg][i], mats[other][i]), 3)
                    for other in lines]
            print(f"  {rg} line{i+1} vs rg1/rg2/rg3 same-line: {vals}")
    print()


report("ORIGINAL frame (pale blue/dark ink), NO REG column",
       ORIG_LINES, orig_ink_crop, ORIG, ORIG_X)
