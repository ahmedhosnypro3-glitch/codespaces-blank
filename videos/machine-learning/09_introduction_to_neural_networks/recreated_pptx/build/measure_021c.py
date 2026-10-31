#!/usr/bin/env python3
"""Per-graph internal measurement for slide_021.jpg: gridlines, axes, red curve,
tick label positions, and sampled colors."""
import numpy as np
from PIL import Image

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_021.jpg"
im = Image.open(SRC).convert("RGB")
a = np.asarray(im).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

GRAPHS = {
    "TL_relu": (122, 110, 399, 271),
    "TR_prelu": (564, 110, 841, 274),
    "BL_elu": (122, 347, 399, 508),
    "BR_softplus": (564, 347, 841, 508),
}


def runs(vals, cond, minlen=1):
    out, start = [], None
    for i, v in enumerate(vals):
        if cond(v) and start is None:
            start = i
        elif not cond(v) and start is not None:
            if i - start >= minlen:
                out.append((start, i - 1))
            start = None
    if start is not None:
        out.append((start, len(vals) - 1))
    return out


print("== sampled colors ==")
for label, (x, y) in [("bg between panels", (450, 200)), ("bg corner", (10, 10)),
                      ("pink fill TL", (200, 95)), ("pink fill BL", (200, 330)),
                      ("plot white TL", (140, 250)), ("red frame", (58, 300)),
                      ("blue frame TL", (122, 200)), ("badge fill", (865, 60))]:
    print(f"  {label} @({x},{y}) = {tuple(a[y, x])}")

for name, (x0, y0, x1, y1) in GRAPHS.items():
    print(f"\n=== {name} box x{x0}..{x1} y{y0}..{y1} ===")
    sub = a[y0:y1 + 1, x0:x1 + 1]
    sr, sg, sb = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    red = (sr > 130) & (sr - sg > 50) & (sr - sb > 50)
    blackish = (sr < 120) & (sg < 120) & (sb < 120)
    # light gray gridlines: fairly bright, channels close, below 245
    gray = (abs(sr - sg) < 12) & (abs(sg - sb) < 12) & (sr > 170) & (sr < 246)
    white = (sr > 246) & (sg > 246) & (sb > 246)

    print("  grid rows:", [(y0 + s, y0 + e) for s, e in runs(gray.sum(axis=1), lambda v: v > (x1 - x0) * 0.45)])
    print("  grid cols:", [(x0 + s, x0 + e) for s, e in runs(gray.sum(axis=0), lambda v: v > (y1 - y0) * 0.45)])
    print("  black long rows:", [(y0 + s, y0 + e) for s, e in runs(blackish.sum(axis=1), lambda v: v > (x1 - x0) * 0.35)])
    print("  black long cols:", [(x0 + s, x0 + e) for s, e in runs(blackish.sum(axis=0), lambda v: v > (y1 - y0) * 0.35)])
    ys, xs = np.nonzero(red)
    if len(xs):
        print(f"  red ink n={len(xs)} x {x0+xs.min()}..{x0+xs.max()} y {y0+ys.min()}..{y0+ys.max()}")
        # sample red extent per row every 8 rows
        for yy in range(y0, y1 + 1, 8):
            sel = np.nonzero(red[yy - y0])[0]
            if len(sel):
                print(f"    row {yy}: red x {x0+sel.min()}..{x0+sel.max()} (n={len(sel)})")
    else:
        print("  red ink: NONE")
