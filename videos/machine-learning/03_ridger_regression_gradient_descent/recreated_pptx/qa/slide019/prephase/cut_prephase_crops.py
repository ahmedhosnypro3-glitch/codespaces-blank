#!/usr/bin/env python3
"""Cut zoomed crops of the ORIGINAL frames 019/025 for S20b prephase vision reads.

Crops are cut from the 960x540 originals at x3 Lanczos upscale (recreation reads
need the 4-8px table glyphs legible). Slide-space coords are encoded in the
filename: slideNNN_<name>__x<X0>-<X1>_y<Y0>-<Y1>_x3.png
"""
from PIL import Image
import os

VID = "videos/machine-learning/03_ridger_regression_gradient_descent"
QA = f"{VID}/recreated_pptx/qa"

SPEC = {
    19: [
        ("titlevec",  58, 470,  50, 165),
        ("outlier",   55, 140, 160, 535),
        ("noreg",    115, 390, 160, 535),
        ("ridge3",   378, 650, 160, 535),
        ("ridge10",  640, 905, 160, 535),
    ],
    25: [
        ("title",   240, 620,  50, 100),
        ("tl",       55, 470, 105, 295),
        ("tr",      465, 905, 105, 325),
        ("bl",       55, 530, 285, 535),
        ("br",      465, 905, 335, 535),
    ],
}

for n, crops in SPEC.items():
    pre = f"{QA}/slide{n:03d}/prephase/orig_judges/crops" if n != 25 else f"{QA}/slide_025/prephase/orig_judges/crops"
    os.makedirs(pre, exist_ok=True)
    im = Image.open(f"{VID}/unique_slides/slide_{n:03d}.jpg").convert("RGB")
    assert im.size == (960, 540), im.size
    for name, x0, x1, y0, y1 in crops:
        c = im.crop((x0, y0, x1, y1))
        c3 = c.resize((c.width * 3, c.height * 3), Image.LANCZOS)
        out = f"{pre}/slide{n:03d}_{name}__x{x0}-{x1}_y{y0}-{y1}_x3.png"
        c3.save(out)
        print(out, c3.size)
print("done")
