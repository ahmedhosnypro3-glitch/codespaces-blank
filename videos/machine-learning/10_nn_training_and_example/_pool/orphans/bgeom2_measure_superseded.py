#!/usr/bin/env python3
"""Lane G geometry closed-loop PIL measurement for scope b_geom_2.

Compares ink edges of slide-specific content in the canonical deliverable render
(LO headless -> 150dpi PNG) against the original lecture frame, both mapped into
slide-inch coordinates via the red house frame fiducial.

House chrome (outer red frame, yellow badge, title box) is excluded from the
content mask and is never reported as a finding.
"""
import json
import sys

import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
SLIDE_W, SLIDE_H = 13.3333, 7.5
TOL_150PX = 4.0          # tolerance in px at 150dpi  (~0.0267 in)
TOL_IN = TOL_150PX / 150.0

# house chrome in slide inches (excluded from content measurement)
BADGE = (12.42, 0.26, 13.02, 0.84)     # x0, y0, x1, y1
REGIONS = {
    "title":  (0.15, 1.00),
    "body":   (1.00, 6.80),
    "footer": (6.80, 7.35),
}


def content_mask(arr):
    """Dark ink or strongly chromatic content."""
    a = arr.astype(int)
    mx, mn = a.max(axis=2), a.min(axis=2)
    lum = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]
    return (lum < 170) | ((mx - mn) > 45)


def strip_chrome_lines(mask, arr, axis):
    """Remove the long red house-frame lines (chrome)."""
    a = arr.astype(int)
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    red = (r - g > 22) & (r - b > 22) & (r > 90)
    if axis == "row":
        cnt = red.sum(axis=1)
        hits = np.nonzero(cnt > 0.5 * a.shape[1])[0]
        m = mask.copy()
        for y in hits:
            m[y, :] = False
        return m
    cnt = red.sum(axis=0)
    hits = np.nonzero(cnt > 0.5 * a.shape[0])[0]
    m = mask.copy()
    for x in hits:
        m[:, x] = False
    return m


def open_mask(mask, iters=1):
    """Morphological opening to kill JPEG speckle without moving real edges much."""
    from scipy import ndimage
    m = mask
    for _ in range(iters):
        m = ndimage.binary_opening(m, structure=np.ones((3, 3)))
    return m


def badge_and_slide_mask(mask, to_slide):
    """Zero out badge chrome and anything outside the calibrated slide area."""
    h, w = mask.shape
    yy, xx = np.mgrid[0:h, 0:w]
    sx = to_slide["x"](xx.ravel()).reshape(h, w)
    sy = to_slide["y"](yy.ravel()).reshape(h, w)
    keep = (sx >= 0.0) & (sx <= SLIDE_W) & (sy >= 0.0) & (sy <= SLIDE_H)
    badge = ((sx >= BADGE[0]) & (sx <= BADGE[2]) &
             (sy >= BADGE[1]) & (sy <= BADGE[3]))
    return mask & keep & ~badge


def build(img_path, kind):
    arr = np.asarray(Image.open(img_path).convert("RGB"))
    h, w = arr.shape[:2]
    if kind == "rend":
        # red frame line centers measured at x=22/1976, y=22/1102 => 150.0 px/in
        ppx = (1976 - 22) / 13.03
        ppy = (1102 - 22) / 7.2
        to_slide = {"x": lambda p: (p - 22) / ppx + 0.15,
                    "y": lambda p: (p - 22) / ppy + 0.15}
    else:
        # original frame: red frame line centers x=58.5/901.5, y=43.5/516.5
        ppx = (901.5 - 58.5) / 13.03
        ppy = (516.5 - 43.5) / 7.2
        to_slide = {"x": lambda p: (p - 58.5) / ppx + 0.15,
                    "y": lambda p: (p - 43.5) / ppy + 0.15}
    m = content_mask(arr)
    m = strip_chrome_lines(m, arr, "row")
    m = strip_chrome_lines(m, arr, "col")
    m = open_mask(m)
    m = badge_and_slide_mask(m, to_slide)
    return arr, m, to_slide, (w, h)


def bbox_slide(mask, to_slide, y0, y1, x0=0.0, x1=SLIDE_W):
    h, w = mask.shape
    yy, xx = np.mgrid[0:h, 0:w]
    sx = to_slide["x"](xx.ravel()).reshape(h, w)
    sy = to_slide["y"](yy.ravel()).reshape(h, w)
    sel = (sy >= y0) & (sy < y1) & (sx >= x0) & (sx < x1)
    if not sel.any():
        return None
    sub = mask & sel
    ys, xs = np.nonzero(sub)
    if not len(xs):
        return None
    return {
        "left": float(to_slide["x"](xs.min())),
        "top": float(to_slide["y"](ys.min())),
        "right": float(to_slide["x"](xs.max())),
        "bottom": float(to_slide["y"](ys.max())),
        "ink_px": int(sub.sum()),
    }


def edges(bb):
    if bb is None:
        return None
    return [bb["left"], bb["top"], bb["right"], bb["bottom"]]


def compare(slide):
    rp = f"{NS}/_pool/tmp_geom_b_geom_2/{slide}/render-1.png"
    op = f"{NS}/unique_slides/slide_{slide}.jpg"
    rarr, rm, rts, rsize = build(rp, "rend")
    oarr, om, ots, osize = build(op, "orig")
    mean_r = float(rarr.mean())
    out = {
        "slide": slide,
        "render_size": list(rsize),
        "orig_size": list(osize),
        "render_mean": round(mean_r, 1),
        "render_blank_ok": bool(20 <= mean_r <= 245),
        "render_dim_ok": bool(abs(rsize[0] - 2000) <= 8 and abs(rsize[1] - 1125) <= 8),
        "regions": {},
    }
    for name, (y0, y1) in REGIONS.items():
        rb = bbox_slide(rm, rts, y0, y1)
        ob = bbox_slide(om, ots, y0, y1)
        rec = {"render_box": rb, "orig_box": ob}
        if rb is None and ob is None:
            rec["status"] = "PASS"
            rec["note"] = "no content ink in either image"
            rec["deltas_px150"] = None
        elif rb is None or ob is None:
            rec["status"] = "EXCEEDS-TOLERANCE"
            rec["note"] = ("render region empty, original has ink"
                           if rb is None else "original region empty, render has ink")
            rec["deltas_px150"] = None
        else:
            d = [(rb[k] - ob[k]) * 150.0 for k in ("left", "top", "right", "bottom")]
            rec["deltas_px150"] = {k: round(v, 1) for k, v in
                                   zip(("left", "top", "right", "bottom"), d)}
            rec["max_abs_delta_px150"] = round(max(abs(v) for v in d), 1)
            rec["status"] = ("PASS" if max(abs(v) for v in d) <= TOL_150PX
                             else "EXCEEDS-TOLERANCE")
            rec["note"] = ""
        out["regions"][name] = rec
    # whole-slide content bbox for context
    rb = bbox_slide(rm, rts, 0.0, SLIDE_H)
    ob = bbox_slide(om, ots, 0.0, SLIDE_H)
    out["all_content"] = {"render_box": rb, "orig_box": ob}
    return out


if __name__ == "__main__":
    res = [compare(s) for s in sys.argv[1:]]
    print(json.dumps(res, indent=1))
