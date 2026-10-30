#!/usr/bin/env python3
"""Band-region fill probe: locate each colored band's true horizontal/vertical
extent by segmenting the band's own fill hue, not by an ink mask (an ink mask
falsely joins a pale band to white panel beyond the band's real right edge).

Prints per-band: fill color, x-extent, y-extent for BOTH the original frame and
the 150dpi render, in frame-px units.
"""
import numpy as np
from PIL import Image

DECK = "videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = f"{DECK}/unique_slides/slide_014.jpg"
REND = f"{DECK}/recreated_pptx/qa/slide014/render_2.png"
SC = 1125 / 540.0

o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
r = np.asarray(Image.open(REND).convert("RGB")).astype(int)

# frame-px search strip per band (label, y_center)
BANDS = [
    ("ridge_band", 262),
    ("objective_band", 322),
    ("define_loss_band", 410),
    ("loss_term_box", 500),
    ("reg_term_box", 500),
    ("final_band", 514),
]


def mask_within(im, rr, scale, target, tol):
    return (np.abs(im[:, :, 0] - target[0]) <= tol) & \
           (np.abs(im[:, :, 1] - target[1]) <= tol) & \
           (np.abs(im[:, :, 2] - target[2]) <= tol)


def probe(im, yc, scale, name):
    row = int(yc * scale)
    line = im[row]
    # find the most common color on this scanline (the band fill, or panel gray)
    vals, counts = np.unique(line, axis=0, return_counts=True)
    base = vals[counts.argmax()]
    tol = 12
    # count how many distinct "fill" colors there really are by clustering runs
    prev = None
    runs = []
    for i, c in enumerate(line):
        c = tuple(int(v) for v in c)
        if prev is None or (abs(c[0]-prev[0]) + abs(c[1]-prev[1]) + abs(c[2]-prev[2])) > tol:
            runs.append([i, i, c])
            prev = c
        else:
            runs[-1][1] = i
    # merge tiny runs (<= 8 render px) into the previous run
    merged = []
    for a, b, c in runs:
        if merged and (b - a) < 8 * scale:
            merged[-1][1] = b
            # keep the merged run's colour = previous run's colour
        else:
            merged.append([a, b, c])
    long_runs = [(a, b, c) for a, b, c in merged if (b - a) > 30 * scale]

    def to_frame(a, b):
        return round(a / scale, 1), round(b / scale, 1)

    print(f"  {name}: scanline frame-y={yc}")
    for a, b, c in long_runs:
        fa, fb = to_frame(a, b)
        print(f"    x {fa}..{fb} (w {(fb-fa):.1f})  RGB{c}")

    # vertical extent of the band fill: take the widest non-white/gray run's color
    if long_runs:
        widest = max(long_runs, key=lambda t: t[1] - t[0])
        c = widest[2]
        if c not in [(255, 255, 255)] and not (abs(c[0]-c[1]) < 4 and abs(c[1]-c[2]) < 4 and c[0] > 180):
            t = 14
            m = mask_within(im, None, scale, c, t)
            rows = np.where(m.sum(axis=1) > 0.6 * m.shape[1])[0]
            if len(rows):
                print(f"    -> full-fill rows frame-y {rows.min()/scale:.1f}..{rows.max()/scale:.1f}")


print("=== ORIGINAL (960x540, scale 1.0) ===")
for name, yc in BANDS:
    probe(o, yc, 1.0, name)
print()
print("=== RENDER (2001x1125, scale %.4f) ===" % SC)
for name, yc in BANDS:
    probe(r, yc, SC, name)
