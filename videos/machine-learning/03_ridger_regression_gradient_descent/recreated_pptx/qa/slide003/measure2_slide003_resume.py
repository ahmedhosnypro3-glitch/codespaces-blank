#!/usr/bin/env python3
"""Precise colour-band and ink-extent measurement, both images, per element."""
import numpy as np
from PIL import Image

B = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
     "03_ridger_regression_gradient_descent")
ORIG = B + "/unique_slides/slide_003.jpg"
REN = B + "/recreated_pptx/qa/slide003/render_9.png"

o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
r = np.asarray(Image.open(REN).convert("RGB").resize((960, 540),
         Image.LANCZOS)).astype(int)


def masks(a):
    R, G, Bc = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    m = {}
    # pastel band fills: high value, low-ish saturation, distinct hue
    m["Y"] = (R > 215) & (G > 215) & (Bc < 210) & (Bc > 100)
    m["C"] = (G > 215) & (Bc > 215) & (R < 215) & (R > 110)
    m["P"] = (R > 215) & (Bc > 190) & (G < 220) & (G > 120)
    m["red"] = (R > 140) & (G < 105) & (Bc < 105)
    m["blue"] = (Bc > 140) & (R < 105) & (G < 130)
    m["dark"] = (a.sum(axis=2) < 400)
    m["gray"] = (abs(R - G) < 26) & (abs(G - Bc) < 26) & (R > 80) & (R < 215)
    return m


def bbox(m, win):
    x0, y0, x1, y1 = win
    b = m[y0:y1, x0:x1]
    if b.sum() == 0:
        return None
    ys, xs = np.where(b)
    return (int(xs.min() + x0), int(ys.min() + y0), int(xs.max() + x0),
            int(ys.max() + y0), int(b.sum()))


mo, mr = masks(o), masks(r)
WINS = {
    "topbox_yellow_band":  (280, 130, 350, 305),
    "topbox_cyan_band":    (355, 130, 430, 305),
    "topbox_pink_band":    (500, 130, 570, 305),
    "topbox_ellip":        (405, 105, 490, 305),
    "bl_yellow_band":      (100, 350, 460, 400),
    "bl_cyan_band":        (100, 390, 460, 445),
    "bl_white_row":        (100, 425, 460, 455),
    "bl_pink_band":        (100, 448, 460, 490),
    "bl_yvec":             (75, 325, 130, 520),
    "bl_wvec":             (440, 325, 545, 520),
    "bl_leftbracket_zone": (150, 340, 210, 500),
    "bl_rightbracket_zone":(380, 340, 460, 500),
    "bl_dimlabels":        (75, 470, 545, 520),
    "br_where":            (570, 350, 760, 480),
    "bl_equals":           (120, 355, 200, 420),
}

print(f"{'zone':24s} {'mask':6s} {'ORIG bbox':30s} {'RENDER bbox':30s} delta")
for zn, win in WINS.items():
    for k in ("Y", "C", "P", "red", "blue", "dark", "gray"):
        bo, br = bbox(mo[k], win), bbox(mr[k], win)
        if bo is None and br is None:
            continue
        d = ""
        if bo and br:
            d = f"dx{br[0]-bo[0]:+d} dy{br[1]-bo[1]:+d} dw{br[2]-br[0]-(bo[2]-bo[0]):+d}"
        so = f"{bo}" if bo else "-"
        sr = f"{br}" if br else "-"
        print(f"{zn:24s} {k:6s} {so:30s} {sr:30s} {d}")
    print()
