#!/usr/bin/env python3
"""Unbiased glyph-size calibration at MATCHED effective scale.

Original upscaled by H_render/540 (2.0833) so both images have the same
px-per-frame-px: render strokes and JPEG halos then contribute equally.
"""
import numpy as np
from PIL import Image

B = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
     "03_ridger_regression_gradient_descent")
o = Image.open(B + "/unique_slides/slide_003.jpg").convert("RGB")
r = Image.open(B + "/recreated_pptx/qa/slide003/render_9.png").convert("RGB")
S = r.height / 540.0
print(f"render {r.size}, orig {o.size}, matched scale {S:.4f}")
o2 = o.resize((int(round(o.width * S)), int(round(o.height * S))),
              Image.LANCZOS)
O = np.asarray(o2).astype(int)
R = np.asarray(r).astype(int)


def glyph(a, x0, x1, y0, y1, th=560):
    """Ink bbox in frame px (divide by S)."""
    xs, ys = [], []
    for y in range(int(y0 * S), int(y1 * S)):
        for x in range(int(x0 * S), int(x1 * S)):
            if a[y, x].sum() < th:
                xs.append(x); ys.append(y)
    if not xs:
        return None
    h = (max(ys) - min(ys) + 1) / S
    w = (max(xs) - min(xs) + 1) / S
    return dict(x0=min(xs) / S, x1=max(xs) / S, y0=min(ys) / S, y1=max(ys) / S,
                h=round(h, 1), w=round(w, 1))


TESTS = {
    "title 'M' cap":      (87, 108, 60, 96),
    "title full line":    (87, 833, 60, 100),
    "X_1 header":         (312, 340, 115, 142),
    "X_2 header":         (389, 415, 115, 142),
    "X_n header":         (532, 558, 115, 142),
    "red y_1":            (312, 340, 274, 296),
    "red y_n":            (534, 560, 274, 296),
    "Remember word":      (654, 702, 152, 182),
    "remember eq":        (695, 872, 180, 224),
    "In General text":    (655, 855, 262, 300),
    "bl y_1":             (108, 136, 360, 396),
    "bl matrix row1":     (198, 396, 362, 396),
    "bl dim 'N x 1'":     (80, 150, 466, 520),
    "w-vector b":         (460, 492, 352, 386),
    "br 'Y=X W'":         (584, 752, 348, 380),
    "br where line1":     (584, 752, 382, 412),
    "badge numeral":      (858, 898, 58, 90),
}
print(f"\n{'test':20s} {'ORIG h/w':>18s} {'RENDER h/w':>18s}   size_ratio")
for nm, (x0, x1, y0, y1) in TESTS.items():
    go, gr = glyph(O, x0, x1, y0, y1), glyph(R, x0, x1, y0, y1)
    so = f"h={go['h']} w={go['w']}" if go else "EMPTY"
    sr = f"h={gr['h']} w={gr['w']}" if gr else "EMPTY"
    rat = f"{go['h']/gr['h']:.2f}x" if go and gr and gr['h'] else ""
    print(f"{nm:20s} {so:>18s} {sr:>18s}   {rat}")
