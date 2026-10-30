#!/usr/bin/env python3
"""Slide 003 resume measurement: render_9 vs original (frame px, 1px=1pt).

Element-by-element ink extent + colour, both images, so every judge finding can be
adjudicated PIL-first against the original frame.
"""
import numpy as np
from PIL import Image

B = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
     "03_ridger_regression_gradient_descent")
QA = B + "/recreated_pptx/qa/slide003"

orig = Image.open(B + "/unique_slides/slide_003.jpg").convert("RGB")
ren = Image.open(QA + "/render_9.png").convert("RGB").resize(
    (960, 540), Image.LANCZOS)
a = np.asarray(orig).astype(int)
r = np.asarray(ren).astype(int)


def blk(ao, win):
    x0, y0, x1, y1 = win
    return ao[y0:y1, x0:x1]


def ink_cols_rows(ao, win, sat_lo=0.0, val_lo=520):
    """Dark-ink bbox inside a window (pixel sum < val_lo, i.e. not near-white)."""
    m = ao.sum(axis=2) < val_lo
    b = blk(m, win)
    if b.sum() == 0:
        return None
    ys, xs = np.where(b)
    return (int(xs.min() + win[0]), int(ys.min() + win[1]),
            int(xs.max() + win[0]), int(ys.max() + win[1]), int(b.sum()))


def color_at(ao, x, y, rad=2):
    w = ao[y - rad:y + rad + 1, x - rad:x + rad + 1].reshape(-1, 3)
    return tuple(int(v) for v in w.mean(axis=0).round())


ZONES = {
    "title":            (70, 60, 840, 95),
    "badge_numeral":    (845, 55, 905, 92),
    "NTrainLabel":      (70, 165, 285, 210),
    "topbox_border_T":  (270, 105, 600, 115),
    "topbox_border_B":  (270, 295, 600, 308),
    "band_yellow":      (290, 138, 340, 300),
    "band_cyan":        (365, 138, 420, 300),
    "band_pink":        (510, 138, 562, 300),
    "ellip_col":        (412, 110, 482, 300),
    "red_ylabels":      (290, 270, 560, 300),
    "remember_box":     (645, 148, 878, 226),
    "ingenera_box":     (655, 262, 855, 300),
    "bl_box_T":         (75, 320, 540, 328),
    "bl_box_B":         (75, 512, 540, 522),
    "bl_bands_yellow":  (150, 363, 433, 393),
    "bl_bands_cyan":    (150, 393, 433, 428),
    "bl_bands_white":   (150, 428, 433, 452),
    "bl_bands_pink":    (150, 452, 433, 480),
    "w_vector":         (455, 325, 525, 480),
    "arrow":            (530, 380, 580, 405),
    "br_box_T":         (568, 320, 758, 328),
    "br_box_B":         (568, 512, 758, 522),
    "br_where_line1":   (578, 360, 750, 400),
    "br_where_line2":   (578, 410, 750, 455),
}

print(f"{'zone':20s} {'ORIG bbox (x0,y0,x1,y1)':34s} {'RENDER bbox':34s} d")
for name, win in ZONES.items():
    bo = ink_cols_rows(a, win)
    br = ink_cols_rows(r, win)
    so = f"{bo}" if bo else "EMPTY"
    sr = f"{br}" if br else "EMPTY"
    if bo and br:
        d = (br[0] - bo[0], br[1] - bo[1], br[2] - bo[2], br[3] - bo[3])
        sd = f"dx{d[0]:+d} dy{d[1]:+d}"
    else:
        sd = ""
    print(f"{name:20s} {so:34s} {sr:34s} {sd}")

print("\n=== COLOR SAMPLES ===")
PTS = [
    ("canvas_topL", (20, 20)), ("panel_gray", (80, 460)),
    ("topbox_fill", (300, 200)), ("topbox_border", (271, 200)),
    ("band_y", (315, 250)), ("band_c", (393, 250)), ("band_p", (535, 250)),
    ("remember_fill", (700, 160)), ("remember_border", (649, 185)),
    ("ingenera_fill", (700, 281)),
    ("bl_fill", (120, 400)), ("bl_border", (79, 400)),
    ("bl_band_y", (300, 378)), ("bl_band_c", (300, 408)), ("bl_band_p", (300, 468)),
    ("br_fill", (600, 400)), ("br_border", (572, 400)),
    ("badge_fill", (876, 65)),
]
for nm, (x, y) in PTS:
    co, cr = color_at(a, x, y), color_at(r, x, y)
    print(f"  {nm:18s} orig={co}  render={cr}")
