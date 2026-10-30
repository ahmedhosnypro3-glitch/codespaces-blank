#!/usr/bin/env python3
"""Clean band-geometry census for slide014: for each band, sample a wide
text-free horizontal strip INSIDE the band on both images and report
(dominant fill color, precise row extent, precise column extent).

Text-free strips chosen by sampling rows known to be between text lines.
"""
import numpy as np
from PIL import Image

DECK = "videos/machine-learning/03_ridger_regression_gradient_descent"
o = np.asarray(Image.open(f"{DECK}/unique_slides/slide_014.jpg").convert("RGB")).astype(int)
r = np.asarray(Image.open(f"{DECK}/recreated_pptx/qa/slide014/render_2.png").convert("RGB")).astype(int)
SC = r.shape[0] / 540.0


def census(im, x0, y0, x1, y1, scale, label):
    sub = im[int(y0*scale):int(y1*scale), int(x0*scale):int(x1*scale)]
    if sub.size == 0:
        return
    flat = sub.reshape(-1, 3)
    vals, counts = np.unique(flat, axis=0, return_counts=True)
    top = [(tuple(int(v) for v in vals[i]), int(counts[i])) for i in counts.argsort()[::-1][:4]]
    # the band fill = most common color that is NOT near-white/near-gray-panel
    fill = None
    for c, n in top:
        if not (c[0] > 245 and c[1] > 245 and c[2] > 245) and not (abs(c[0]-c[1]) < 6 and abs(c[1]-c[2]) < 6):
            fill = (c, n)
            break
    if fill is None:
        fill = top[0]
    c = fill[0]
    m = (np.abs(sub[:, :, 0]-c[0]) <= 10) & (np.abs(sub[:, :, 1]-c[1]) <= 10) & (np.abs(sub[:, :, 2]-c[2]) <= 10)
    rows = np.where(m.any(axis=1))[0]
    cols = np.where(m.any(axis=0))[0]
    print(f"{label}:")
    print(f"    dominant fill RGB {c} ({fill[1]} px)")
    if len(rows):
        print(f"    fill rows  frame-y {y0 + rows.min()/scale:.1f}..{y0 + rows.max()/scale:.1f}")
    if len(cols):
        print(f"    fill cols  frame-x {x0 + cols.min()/scale:.1f}..{x0 + cols.max()/scale:.1f}")
    print(f"    top colors: {top}")


# Band search windows (frame px), generous in y, full panel width in x
WINDOWS = {
    "ridge_band (yellow?)":        (60, 244, 900, 285),
    "objective_band (yellow?)":    (60, 305, 900, 340),
    "define_loss_band (pink?)":    (60, 395, 900, 428),
    "loss_term_box (blue?)":       (60, 466, 440, 524),
    "reg_term_box (blue?)":        (500, 466, 900, 524),
    "final_band (blue?)":          (60, 504, 900, 530),
}

for name, (x0, y0, x1, y1) in WINDOWS.items():
    print("=" * 60)
    print(name)
    census(o, x0, y0, x1, y1, 1.0, "  ORIGINAL")
    census(r, x0, y0, x1, y1, SC, "  RENDER")
    print()
