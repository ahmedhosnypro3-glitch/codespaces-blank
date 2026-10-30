#!/usr/bin/env python3
"""PIL-first measurement for slide014: ink census + band geometry + fill colors,
measured against BOTH images (original 960x540 and 150dpi render 2001x1125).

Scale: 1 frame-px = 1125/540 render-px (2001/960 would be the per-axis value; the
150dpi pipeline yields 2001x1125, i.e. 2.0833 render-px per frame-px on Y).
"""
import json
import sys

import numpy as np
from PIL import Image

DECK = "videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = f"{DECK}/unique_slides/slide_014.jpg"
REND = f"{DECK}/recreated_pptx/qa/slide014/render_2.png"

o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
r = np.asarray(Image.open(REND).convert("RGB")).astype(int)
OH, OW = o.shape[:2]
RH, RW = r.shape[:2]
SC = RH / OH  # render px per frame px


def ink(im, thresh=400):
    """Count of 'ink' pixels: any channel far from white."""
    mx = im.max(axis=2)
    mn = im.min(axis=2)
    return int(((mx < 240) | ((mx - mn) > 40)).sum())


def ink_in(im, x0, y0, x1, y1, scale=SC):
    sub = im[int(y0 * scale):int(y1 * scale), int(x0 * scale):int(x1 * scale)]
    if sub.size == 0:
        return 0
    mx = sub.max(axis=2)
    mn = sub.min(axis=2)
    return int(((mx < 240) | ((mx - mn) > 40)).sum())


def ink_in_orig(im, x0, y0, x1, y1):
    sub = im[y0:y1, x0:x1]
    if sub.size == 0:
        return 0
    mx = sub.max(axis=2)
    mn = sub.min(axis=2)
    return int(((mx < 240) | ((mx - mn) > 40)).sum())


def mode_color(im, x0, y0, x1, y1, scale=SC, exclude_ink=True):
    """Dominant (non-ink) color in a region, for fill bands."""
    sub = im[int(y0 * scale):int(y1 * scale), int(x0 * scale):int(x1 * scale)]
    if sub.size == 0:
        return None
    flat = sub.reshape(-1, 3)
    if exclude_ink:
        mx = flat.max(axis=1)
        mn = flat.min(axis=1)
        keep = (mx >= 240) & ((mx - mn) <= 40)
        if keep.sum() < 10:
            keep = np.ones(len(flat), bool)
        flat = flat[keep]
    if len(flat) == 0:
        return None
    vals, counts = np.unique(flat, axis=0, return_counts=True)
    return tuple(int(v) for v in vals[counts.argmax()])


def extents(im, x0, y0, x1, y1, scale=SC):
    """Bounding box of ink inside a frame-px region, in frame-px units."""
    sub = im[int(y0 * scale):int(y1 * scale), int(x0 * scale):int(x1 * scale)]
    if sub.size == 0:
        return None
    mx = sub.max(axis=2)
    mn = sub.min(axis=2)
    m = (mx < 240) | ((mx - mn) > 40)
    if not m.any():
        return None
    rows = np.where(m.any(axis=1))[0]
    cols = np.where(m.any(axis=0))[0]
    return {
        "x0": round(float(x0 + cols.min() / scale), 1),
        "x1": round(float(x0 + cols.max() / scale), 1),
        "y0": round(float(y0 + rows.min() / scale), 1),
        "y1": round(float(y0 + rows.max() / scale), 1),
    }


def extents_orig(im, x0, y0, x1, y1):
    sub = im[y0:y1, x0:x1]
    if sub.size == 0:
        return None
    mx = sub.max(axis=2)
    mn = sub.min(axis=2)
    m = (mx < 240) | ((mx - mn) > 40)
    if not m.any():
        return None
    rows = np.where(m.any(axis=1))[0]
    cols = np.where(m.any(axis=0))[0]
    return {
        "x0": round(float(x0 + cols.min()), 1),
        "x1": round(float(x0 + cols.max()), 1),
        "y0": round(float(y0 + rows.min()), 1),
        "y1": round(float(y0 + rows.max()), 1),
    }


out = {}
out["sizes"] = {"orig": [OW, OH], "render": [RW, RH], "scale": round(SC, 4)}
out["ink_total"] = {"orig": ink(o), "render": ink(r)}

# --- regions (frame-px), from the build script's measured geometry ---
REGIONS = {
    "title": (40, 55, 700, 105),
    "badge": (850, 50, 905, 100),
    "left_box": (54, 104, 450, 232),
    "right_box": (500, 104, 880, 232),
    "ridge_band": (54, 250, 903, 278),
    "objective_band": (54, 310, 903, 334),
    "define_loss_band": (54, 398, 903, 422),
    "loss_term_box": (54, 468, 450, 520),
    "reg_term_box": (500, 468, 903, 520),
    "final_band": (54, 505, 903, 528),
}

ink_cmp = {}
for name, (x0, y0, x1, y1) in REGIONS.items():
    ink_cmp[name] = {
        "orig": ink_in_orig(o, x0, y0, x1, y1),
        "render": ink_in(r, x0, y0, x1, y1),
        "extents_orig": extents_orig(o, x0, y0, x1, y1),
        "extents_rend": extents(r, x0, y0, x1, y1),
    }
out["regions"] = ink_cmp

# --- fill colors of the bands (dominant non-ink color in a text-free strip) ---
FILLS = {
    "ridge_band": (120, 262, 860, 274),
    "objective_band": (120, 320, 860, 330),
    "define_loss_band": (120, 402, 860, 418),
    "loss_term_box": (80, 512, 440, 517),
    "reg_term_box": (520, 512, 860, 517),
    "final_band": (120, 507, 860, 521),
}
fills = {}
for name, (x0, y0, x1, y1) in FILLS.items():
    co = mode_color(o, x0, y0, x1, y1) if False else None
    # original: exact px coords
    sub = o[y0:y1, x0:x1].reshape(-1, 3)
    mx = sub.max(axis=1)
    mn = sub.min(axis=1)
    keep = (mx >= 240) & ((mx - mn) <= 40)
    if keep.sum() < 10:
        keep = np.ones(len(sub), bool)
    vals, counts = np.unique(sub[keep], axis=0, return_counts=True)
    co = tuple(int(v) for v in vals[counts.argmax()]) if len(sub) else None
    # render: scale coords
    rsub = r[int(y0 * SC):int(y1 * SC), int(x0 * SC):int(x1 * SC)].reshape(-1, 3)
    rmx = rsub.max(axis=1)
    rmn = rsub.min(axis=1)
    rkeep = (rmx >= 240) & ((rmx - rmn) <= 40)
    if rkeep.sum() < 10:
        rkeep = np.ones(len(rsub), bool)
    rvals, rcounts = np.unique(rsub[rkeep], axis=0, return_counts=True)
    cr = tuple(int(v) for v in rvals[rcounts.argmax()]) if len(rsub) else None
    fills[name] = {"orig": co, "render": cr}
out["fills"] = fills

# --- horizontal extent of every band (both images), to check containment ---
BANDS = {
    "ridge_band": (250, 270),
    "objective_band": (315, 332),
    "define_loss_band": (400, 420),
    "final_band": (506, 524),
}
band_ext = {}
for name, (y0, y1) in BANDS.items():
    band_ext[name] = {
        "orig": extents_orig(o, 0, y0, OW, y1),
        "rend": extents(r, 0, y0, OW, y1),
    }
out["band_h_extents"] = band_ext

# --- unique colors census (top 12) for palette comparison ---
def top_colors(im, n=12):
    flat = im.reshape(-1, 3)
    vals, counts = np.unique(flat, axis=0, return_counts=True)
    idx = counts.argsort()[::-1][:n]
    return [(tuple(int(v) for v in vals[i]), int(counts[i])) for i in idx]

out["top_colors_orig"] = top_colors(o)
out["top_colors_rend"] = top_colors(r)

# --- red stroke geometry on both (deck law) ---
def stroke_probe(im, scale, tag):
    rr, gg, bb = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    red = (rr > 90) & ((rr - gg) > 40) & ((rr - bb) > 10)
    res = {}
    # top band must be bare
    res["top_red"] = int(red[int(44 * scale):int(52 * scale), int(80 * scale):int(880 * scale)].sum())
    mid = slice(int(270 * scale) - 20, int(270 * scale) + 20)
    lr = np.where(red[mid, :].any(axis=0))[0]
    rr2 = np.where(red[mid, :].any(axis=0))[0]
    if len(lr):
        res["mid_left_x"] = round(float(lr.min() / scale), 1)
    if len(rr2):
        res["mid_right_x"] = round(float(rr2.max() / scale), 1)
    bot = red[int(533 * scale):, :]
    bc = np.where(bot.any(axis=0))[0]
    if len(bc):
        res["bottom_x"] = (round(float(bc.min() / scale), 1), round(float(bc.max() / scale), 1))
    babr = np.where(bot.any(axis=1))[0]
    if len(babr):
        res["bottom_y"] = (round(float((533 * scale + babr.min()) / scale), 1),
                           round(float((533 * scale + babr.max()) / scale), 1))
    return res

out["strokes"] = {
    "orig": stroke_probe(o, 1.0, "orig"),
    "rend": stroke_probe(r, SC, "rend"),
}

with open(f"{DECK}/recreated_pptx/qa/slide014/pil_measure_attempt2.json", "w") as f:
    json.dump(out, f, indent=1)

print(json.dumps(out, indent=1))
