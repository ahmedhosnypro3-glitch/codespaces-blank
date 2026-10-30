#!/usr/bin/env python3
"""Slide 030 PIL adjudication baseline, CORRECTED SCALE (worker w030-finish-20261024c).

Why this file exists: measure_w030.py converts ORIG pixels with the RENDER's
scale factor (SX = render_width/960 = 2.0844), so every original-frame value in
that script is halved and windows starting past orig column 460 come back empty.
This copy converts each image with ITS OWN scale (orig is 960x540 = frame px,
scale 1.0; render is 2001x1125 = 2.0844/2.0833 render px per frame px).

Outputs frame-px bboxes for both images per colour mask, so a judge finding can
be refuted with a measurement instead of an opinion. Noisy rows/cols with
<3 ink px are rejected before measuring (phantom trap).
"""
import numpy as np
from PIL import Image

V = "videos/machine-learning/03_ridger_regression_gradient_descent"
Q = f"{V}/recreated_pptx/qa/slide030"
REND = f"{Q}/render_6.png"
ORIG = f"{V}/unique_slides/slide_030.jpg"

rend = Image.open(REND).convert("RGB")
orig = Image.open(ORIG).convert("RGB")
RW, RH = rend.size
OW, OH = orig.size
SXR, SYR = RW / 960.0, RH / 540.0
print(f"== slide 030 measurement (corrected scale) ==")
print(f"render {RW}x{RH}  SXR={SXR:.4f} SYR={SYR:.4f}   orig {OW}x{OH} (frame px, scale 1.0)")

rend_a = np.asarray(rend).astype(int)
orig_a = np.asarray(orig).astype(int)


def masks(im):
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    return {
        "dark": (r < 120) & (g < 120) & (b < 120),
        "red": (r - g > 60) & (r - b > 40) & (r > 110),
        "green": (g - r > 40) & (g - b > 40) & (g > 100),
        "blue": (b - r > 30) & (b - g > 15) & (b > 120),
        "purple": (r - g > 25) & (b - g > 25) & (b > 120),
        "navy": (b > 90) & (b - r > 50) & (b - g > 50) & (r < 130),
    }


mr, mo = masks(rend_a), masks(orig_a)


def clean(mask, min_ink=3):
    m = mask.copy()
    colsum, rowsum = m.sum(axis=0), m.sum(axis=1)
    m[:, colsum < min_ink] = False
    m[rowsum < min_ink, :] = False
    return m


def box_px(box, sx, sy, W, H):
    x0, y0, x1, y1 = box
    return (int(round(x0 * sx)), int(round(y0 * sy)),
            min(int(round(x1 * sx)), W), min(int(round(y1 * sy)), H))


def bbox(mask, box, sx, sy, W, H):
    """BBox of `mask` inside `box` (frame px), returned in FRAME px."""
    X0, Y0, X1, Y1 = box_px(box, sx, sy, W, H)
    sub = clean(mask[Y0:Y1, X0:X1])
    ys, xs = np.where(sub)
    if not len(xs):
        return None, 0
    return ((round((xs.min() + X0) / sx, 1), round((ys.min() + Y0) / sy, 1),
             round((xs.max() + X0) / sx, 1), round((ys.max() + Y0) / sy, 1)),
            int(len(xs) / (sx * sy)))


REGIONS = {
    "title":        ((55, 55, 600, 100), ("dark", "red", "green")),
    "param_table":  ((90, 185, 260, 300), ("dark", "navy")),
    "upper_eq_box": ((390, 175, 545, 220), ("red", "dark")),
    "green_box":    ((340, 225, 565, 292), ("green", "red", "blue", "dark")),
    "callout":      ((325, 282, 580, 335), ("purple", "dark")),
    "plot_frame":   ((560, 55, 825, 322), ("red",)),
    "arrow":        ((150, 285, 215, 355), ("red",)),
    "iter_table":   ((70, 315, 665, 540), ("navy", "dark")),
    "iter_left":    ((72, 318, 400, 538), ("navy", "dark")),
    "iter_right":   ((370, 318, 662, 538), ("navy", "dark")),
    "callout_band": ((320, 280, 585, 332), ("purple",)),
}

print("\n== per-region bbox, render vs orig (frame px) ==")
for name, (box, ms) in REGIONS.items():
    rm = np.zeros(rend_a.shape[:2], bool)
    om = np.zeros(orig_a.shape[:2], bool)
    for m in ms:
        rm |= mr[m]
        om |= mo[m]
    rb, rc_ = bbox(rm, box, SXR, SYR, RW, RH)
    ob, oc_ = bbox(om, box, 1.0, 1.0, OW, OH)
    if rb and ob:
        dx, dy = rb[0] - ob[0], rb[1] - ob[1]
        dw, dh = (rb[2] - rb[0]) - (ob[2] - ob[0]), (rb[3] - rb[1]) - (ob[3] - ob[1])
        print(f"  {name:14s} render={rb} ink={rc_:6d}  orig={ob} ink={oc_:6d}  "
              f"dpos=({dx:+.1f},{dy:+.1f}) dsize=({dw:+.1f},{dh:+.1f})")
    else:
        print(f"  {name:14s} render={rb} ink={rc_:6d}  orig={ob} ink={oc_:6d}  (one side empty)")

print("\n== per-colour bbox inside each judge crop region ==")
CROPS = {
    "param":    ((95, 190, 245, 292), ("navy", "dark", "red", "blue")),
    "formula":  ((340, 178, 562, 288), ("red", "green", "blue", "dark")),
    "plot":     ((565, 58, 818, 318), ("red", "blue", "green", "dark")),
    "iter_left":  ((72, 318, 400, 538), ("navy", "dark", "red", "blue")),
    "iter_right": ((370, 318, 662, 538), ("navy", "dark", "red", "blue")),
    "callout":  ((325, 282, 580, 330), ("purple", "dark", "red")),
    "arrow":    ((160, 294, 208, 348), ("red", "dark")),
}
for name, (box, ms) in CROPS.items():
    print(f"  -- {name}")
    for m in ms:
        rb, rc_ = bbox(mr[m], box, SXR, SYR, RW, RH)
        ob, oc_ = bbox(mo[m], box, 1.0, 1.0, OW, OH)
        print(f"     {m:7s} render={str(rb):28s} ink={rc_:6d} | orig={str(ob):28s} ink={oc_:6d}")

print("\n== grid-line structure (iteration table) ==")
for label, m, sx, sy, W, H, box in (
        ("render", np.zeros(rend_a.shape[:2], bool), SXR, SYR, RW, RH, (70, 315, 665, 540)),
        ("orig", np.zeros(orig_a.shape[:2], bool), 1.0, 1.0, OW, OH, (70, 315, 665, 540))):
    X0, Y0, X1, Y1 = box_px(box, sx, sy, W, H)
    sub = clean(m[Y0:Y1, X0:X1])
    colsum, rowsum = sub.sum(axis=0), sub.sum(axis=1)
    vlines = int((colsum > 0.35 * sub.shape[0]).sum())
    hlines = int((rowsum > 0.35 * sub.shape[1]).sum())
    print(f"  {label:6s} full-height cols>{0.35 * sub.shape[0]:.0f}px: {vlines}  "
          f"full-width rows>{0.35 * sub.shape[1]:.0f}px: {hlines}")

print("\n== callout band: purple fill extent + text ink ==")
box = (320, 280, 585, 332)
for label, m, sx, sy, W, H in (("render", mr["purple"], SXR, SYR, RW, RH),
                               ("orig", mo["purple"], 1.0, 1.0, OW, OH)):
    X0, Y0, X1, Y1 = box_px(box, sx, sy, W, H)
    sub = m[Y0:Y1, X0:X1]
    rows = sub.sum(axis=1)
    solid = np.where(rows > 0.5 * sub.shape[1])[0]
    print(f"  {label:6s} purple rows>50% width: {len(solid)}  "
          f"band frame px y={Y0/sy:.1f}..{Y1/sy:.1f}" +
          (f"  solid y={(solid.min()+Y0)/sy:.1f}..{(solid.max()+Y0)/sy:.1f}" if len(solid) else ""))

print("\nMEASUREMENT (corrected scale) DONE")
