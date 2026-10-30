#!/usr/bin/env python3
"""Closed-loop measurement for slide 037 attempt 3: compare the 150dpi render
against the original frame line-by-line / glyph-by-glyph (960x540 frame px)."""
import numpy as np
from PIL import Image

QA = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide037"
R = np.asarray(Image.open(f"{QA}/render_3.png").convert("RGB")).astype(int)
O = np.asarray(Image.open("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_037.jpg").convert("RGB")).astype(int)

s = R.shape[0] / 540.0
print(f"render {R.shape[1]}x{R.shape[0]}  scale {s:.4f} render-px per frame-px")


def ink(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r < 190) & (g < 190) & (b < 190)


def redish(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 110) & (r > g + 45) & (r > b + 35)


def bbox(mask, y0, y1, x0, x1, scale=1.0):
    sub = mask[int(y0 * scale):int(y1 * scale), int(x0 * scale):int(x1 * scale)]
    rows = np.where(sub.any(axis=1))[0]
    cols = np.where(sub.any(axis=0))[0]
    if not len(rows):
        return None
    return (
        round((rows.min() + int(y0 * scale)) / scale, 1),
        round((rows.max() + int(y0 * scale)) / scale, 1),
        round((cols.min() + int(x0 * scale)) / scale, 1),
        round((cols.max() + int(x0 * scale)) / scale, 1),
    )


IR, IO = ink(R), ink(O)
RR, RO = redish(R), redish(O)

LINES = {
    "title": (56, 90, 300, 700),
    "p1 heading": (106, 140, 70, 880),
    "implication 1": (140, 172, 70, 880),
    "implication 2": (170, 194, 70, 880),
    "p2 heading": (238, 262, 70, 880),
    "error equation": (258, 292, 70, 890),
    "error eq subscript": (288, 308, 140, 290),
    "summation line": (304, 332, 70, 700),
    "p3 heading": (356, 388, 70, 600),
    "update eq 1": (400, 442, 70, 890),
    "update eq 1 subscript": (438, 458, 590, 700),
    "update eq 2": (466, 504, 70, 500),
    "update eq 2 subscript": (502, 520, 250, 440),
}

print("\n%-24s %-30s %-30s" % ("region", "RENDER (r0,r1,c0,c1)", "ORIGINAL"))
for name, (y0, y1, x0, x1) in LINES.items():
    rb = bbox(IR, y0, y1, x0, x1, s)
    ob = bbox(IO, y0, y1, x0, x1, 1.0)
    print("%-24s %-30s %-30s" % (name, rb, ob))

print("\n--- red subscript extents (render vs original) ---")
for name, box in {
    "error eq subscript": (288, 308, 140, 290),
    "update eq 1 subscript": (438, 458, 590, 700),
    "update eq 2 subscript": (502, 520, 250, 440),
}.items():
    print("%-24s %-30s %-30s" % (
        name, bbox(RR, *box, s), bbox(RO, *box, 1.0)))

print("\n--- fill colours (render median vs original mode) ---")
from collections import Counter


def med(a, y0, y1, x0, x1, scale=1.0):
    sub = a[int(y0 * scale):int(y1 * scale), int(x0 * scale):int(x1 * scale)]
    return tuple(np.median(sub.reshape(-1, 3), axis=0).astype(int))


for label, (y0, y1, x0, x1) in {
    "P1 fill": (150, 200, 300, 600),
    "P2 fill": (250, 335, 300, 600),
    "P3 fill": (370, 440, 300, 600),
    "green box": (470, 500, 100, 250),
    "house gray": (215, 225, 200, 700),
}.items():
    print(f"  {label:12s} render {med(R, y0, y1, x0, x1, s)}   original {med(O, y0, y1, x0, x1, 1.0)}")

print("\n--- panel borders (redish long runs) ---")


def hruns(y0, y1):
    rr = (O[y0:y1, :, 0] > 80) & (O[y0:y1, :, 1] < 110) & (O[y0:y1, :, 2] < 110) & ((O[y0:y1, :, 0] - O[y0:y1, :, 1]) > 40)
    rows = [y0 + i for i in range(rr.shape[0]) if rr[i].sum() > 200]
    return rows


print("  original horizontal red rows:", hruns(100, 545))
rr2 = (R[:, :, 0] > 80) & (R[:, :, 1] < 110) & (R[:, :, 2] < 110) & ((R[:, :, 0] - R[:, :, 1]) > 40)
runs2 = [int(round(i / s)) for i in range(rr2.shape[0]) if rr2[i].sum() > 200 * s]
print("  render   horizontal red rows:", runs2)

print("\n--- frame containment: ink outside each panel? ---")
for label, (py0, py1, px0, px1) in {
    "P1": (108, 210, 68, 870),
    "P2": (229, 341, 66, 891),
    "P3": (348, 531, 66, 891),
    "green box": (462, 520, 80, 485),
}.items():
    # look for content ink in the 4px band just outside the panel, excluding
    # the panel's own border stroke itself
    lo = int((py0 - 6) * s)
    band_top = IR[lo:int(py0 * s), int(px0 * s):int(px1 * s)]
    lo2 = int((py1 + 1) * s)
    band_bot = IR[lo2:int((py1 + 7) * s), int(px0 * s):int(px1 * s)]
    print(f"  {label:10s} ink in 6px band above={int(band_top.sum())} below={int(band_bot.sum())}")

print("\n--- equations have ink (never empty) ---")
for label, box in {
    "error equation": (258, 292, 70, 890),
    "update eq 1": (400, 442, 70, 890),
    "update eq 2": (466, 504, 70, 500),
}.items():
    print(f"  {label:16s} render ink px = {int(IR[int(box[0]*s):int(box[1]*s), int(box[2]*s):int(box[3]*s)].sum())}")
