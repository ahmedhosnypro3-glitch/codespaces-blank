#!/usr/bin/env python3
"""Lane G geometry closed-loop measurement, scope b_geom_2.

Both images are mapped into slide-inch coordinates through the house chrome
fiducial (the outer red rectangle at x=0.15,y=0.15,w=13.03,h=7.2):

  render  red rect line-centres x=22.0/1976.0, y=22.0/1102.0 -> 150.00 px/in
  original red rect line-centres x=58.45/901.07, y=42.95/516.66 -> 64.67/65.79 px/in

The original 960x540 video frame letterboxes the slide (white band above the
rect, black band below) and is anisotropic, so a naive proportional
normalisation is wrong; the fiducial mapping absorbs both.

Content ink = luminance < 170 OR chroma > 45. The red rectangle, the yellow
badge and everything outside the slide area are masked out of BOTH images, so
house chrome can never appear as a finding.
"""
import numpy as np
from PIL import Image
from scipy import ndimage

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
SLIDE_W, SLIDE_H = 13.3333, 7.5
TOL_PX150 = 4.0                      # tolerance: px at 150dpi
TOL_IN = TOL_PX150 / 150.0
BADGE = (12.35, 0.15, 13.20, 0.95)    # generous house-badge mask (chrome)
REGIONS = {"title": (0.15, 1.10), "body": (1.10, 6.90), "footer": (6.90, 7.50)}

# fiducial line-centres per image type
FID = {
    "rend": {"x": (22.0, 1976.0), "y": (22.0, 1102.0)},
    "orig": {"x": (58.45, 901.07), "y": (42.95, 516.66)},
}
REF = {"x": (0.15, 13.18), "y": (0.15, 7.35)}   # house chrome rect, slide inches


def make_map(kind):
    x0, x1 = FID[kind]["x"]
    y0, y1 = FID[kind]["y"]
    sx = (REF["x"][1] - REF["x"][0]) / (x1 - x0)
    sy = (REF["y"][1] - REF["y"][0]) / (y1 - y0)
    return {"x": lambda p: (p - x0) * sx + REF["x"][0],
            "y": lambda p: (p - y0) * sy + REF["y"][0],
            "sx": sx, "sy": sy, "x0": x0, "y0": y0}


def content_mask(arr):
    a = arr.astype(int)
    mx, mn = a.max(axis=2), a.min(axis=2)
    lum = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]
    return (lum < 170) | ((mx - mn) > 45)


def strip_frame_lines(mask, arr):
    """Drop the outer red rectangle rows/cols that span the image (chrome)."""
    a = arr.astype(int)
    red = (a[:, :, 0] - np.maximum(a[:, :, 1], a[:, :, 2]) > 22) & (a[:, :, 0] > 90)
    m = mask.copy()
    for y in np.nonzero(red.sum(axis=1) > 0.5 * a.shape[1])[0]:
        m[y, :] = False
    for x in np.nonzero(red.sum(axis=0) > 0.5 * a.shape[0])[0]:
        m[:, x] = False
    return m


def chrome_free_mask(path, kind):
    """Content mask in slide-inch coordinates, chrome and letterbox removed."""
    arr = np.asarray(Image.open(path).convert("RGB"))
    h, w = arr.shape[:2]
    mp = make_map(kind)
    m = content_mask(arr)
    m = strip_frame_lines(m, arr)
    m = ndimage.binary_opening(m, structure=np.ones((3, 3)))
    yy, xx = np.mgrid[0:h, 0:w]
    sx = mp["x"](xx); sy = mp["y"](yy)
    inside = (sx >= 0.0) & (sx <= SLIDE_W) & (sy >= 0.0) & (sy <= SLIDE_H)
    badge = ((sx >= BADGE[0]) & (sx <= BADGE[2]) &
             (sy >= BADGE[1]) & (sy <= BADGE[3]))
    return m & inside & ~badge, mp, (w, h)


def region_box(mask, mp, y0, y1):
    """Ink bounding box inside a slide-inch horizontal band."""
    h, w = mask.shape
    yy, xx = np.mgrid[0:h, 0:w]
    sy = mp["y"](yy)
    sel = (sy >= y0) & (sy < y1)
    sub = mask & sel
    ys, xs = np.nonzero(sub)
    if not len(xs):
        return None
    return {"left": float(mp["x"](xs.min())), "top": float(mp["y"](ys.min())),
            "right": float(mp["x"](xs.max())), "bottom": float(mp["y"](ys.max())),
            "ink_px": int(sub.sum())}


def deltas_px150(rb, ob):
    return {k: round((rb[k] - ob[k]) * 150.0, 1)
            for k in ("left", "top", "right", "bottom")}


def measure(slide, tmp_root=None, orig_name=None):
    """Measure one slide; returns dict, or None when a deliverable is missing."""
    import os
    d = tmp_root or f"{NS}/_pool/tmp_geom_b_geom_2/{slide}"
    op = orig_name or f"{NS}/unique_slides/slide_{slide}.jpg"
    rp = f"{d}/render-1.png"
    if not (os.path.exists(rp) and os.path.exists(op)):
        return None
    from PIL import Image
    rmean = float(np.asarray(Image.open(rp).convert("RGB")).mean())
    rm, rmap, rsize = chrome_free_mask(rp, "rend")
    om, omap, osize = chrome_free_mask(op, "orig")
    res = {"slide": slide, "render_mean": round(rmean, 1),
           "render_dim": list(rsize), "orig_dim": list(osize),
           "dim_ok": abs(rsize[0] - 2000) <= 8 and abs(rsize[1] - 1125) <= 8,
           "blank_ok": 20.0 <= rmean <= 245.0,
           "calib": {"rend_ppin": 150.0,
                     "orig_ppin_x": round(1 / omap["sx"], 2),
                     "orig_ppin_y": round(1 / omap["sy"], 2)},
           "regions": {}}
    for name, (y0, y1) in REGIONS.items():
        rb, ob = region_box(rm, rmap, y0, y1), region_box(om, omap, y0, y1)
        rec = {"render": rb, "orig": ob}
        if rb is None and ob is None:
            rec.update(status="PASS", note="no slide content ink in either image",
                       deltas=None)
        elif rb is None or ob is None:
            rec.update(status="EXCEEDS-TOLERANCE",
                       note="region empty on one side only", deltas=None)
        else:
            dl = deltas_px150(rb, ob)
            worst = max(abs(v) for v in dl.values())
            rec.update(deltas=dl, worst_px150=round(worst, 1),
                       status="PASS" if worst <= TOL_PX150 else "EXCEEDS-TOLERANCE",
                       note="")
        res["regions"][name] = rec
    return res
