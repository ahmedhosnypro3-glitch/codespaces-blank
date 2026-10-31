#!/usr/bin/env python3
"""Lane G (b_geom_1) - FINAL v5: reference (b_geom_2) method, slide-inch coords.

Both images are mapped to slide-inch coordinates through the house chrome
fiducial (outer red rectangle x=0.15,y=0.15,w=13.03,h=7.2 in). The original
960x540 frames letterbox the slide, so proportional normalisation is wrong by
~10%; the red rectangle is the shared reference.
"""
import glob
import json
import numpy as np
from PIL import Image
from scipy import ndimage

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
TMP = f"{NS}/_pool/tmp_geom_b_geom_1"
TOL = 4.0
DPI = 150.0

REGIONS = [
    ("title block", 0.15, 1.10),
    ("body / equation / diagram / table region", 1.10, 6.90),
    ("footer region", 6.90, 7.50),
]


def red_rect(a):
    h, w = a.shape[:2]
    r, g, b = (a[..., i] for i in range(3))
    red = (r > 110) & (r - g > 35) & (r - b > 35)
    rows = np.nonzero(red.sum(axis=1) > 0.50 * w)[0]
    cols = np.nonzero(red.sum(axis=0) > 0.50 * h)[0]
    return int(cols.min()), int(rows.min()), int(cols.max()), int(rows.max())


def badge_box(a):
    h, w = a.shape[:2]
    r, g, b = (a[..., i] for i in range(3))
    yel = (r > 185) & (g > 170) & (b > 110) & (b < 220)
    win = np.zeros_like(yel)
    win[:int(0.22 * h), int(0.78 * w):] = True
    yel &= win
    lab, n = ndimage.label(yel, structure=np.ones((3, 3)))
    best = None
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(ys) < 30 or xs.max() - xs.min() > 46 or ys.max() - ys.min() > 46:
            continue
        if best is None or len(ys) > best[0]:
            best = (len(ys), int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))
    return None if best is None else best[1:]


def ink_mask(a, lum_thr=170, chroma_thr=45):
    rgb = a.astype(np.float32)
    lum = 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    m = (lum < lum_thr) | (chroma > chroma_thr)
    m = ndimage.binary_opening(m, structure=np.ones((3, 3)))
    return m


def strip_chrome(m, rect, badge, letterbox_y=None):
    x0, y0, x1, y1 = rect
    m[max(0, y0 - 3):y0 + 5, :] = False
    m[max(0, y1 - 4):y1 + 4, :] = False
    m[:, max(0, x0 - 3):x0 + 5] = False
    m[:, max(0, x1 - 4):x1 + 4] = False
    if letterbox_y is not None:
        m[max(0, letterbox_y - 2):, :] = False
        m[:letterbox_y, :] = False
    if badge:
        bx0, by0, bx1, by1 = badge
        m[max(0, by0 - 6):by1 + 6, max(0, bx0 - 6):bx1 + 6] = False
    return m


def measure(m, sx, sy, ox, oy):
    """Return the ink box in slide inches over the region, or None."""
    ys, xs = np.nonzero(m)
    if xs.size < 8:
        return None
    return {"left": (xs.min() - ox) / sx, "right": (xs.max() + 1 - ox) / sx,
            "top": (ys.min() - oy) / sy, "bottom": (ys.max() + 1 - oy) / sy,
            "px": int(xs.size)}


def slide_image(n, which):
    path = (f"{NS}/unique_slides/slide_{n}.jpg" if which == "orig"
            else f"{TMP}/frame_{n}.png")
    return np.asarray(Image.open(path).convert("RGB")).astype(np.int16)


def letterbox_top(a):
    """Original frames carry a white letterbox band above the gray page."""
    h, w = a.shape[:2]
    white = (a[..., 0] > 238) & (a[..., 1] > 238) & (a[..., 2] > 238)
    frac = white.mean(axis=1)
    rows = np.nonzero(frac > 0.95)[0]
    if rows.size == 0:
        return None
    return int(rows.max()) + 1


def one(n):
    out = {"slide": n}
    imgs = {}
    for which in ("orig", "rend"):
        a = slide_image(n, which)
        rr = red_rect(a)
        bd = badge_box(a)
        lb = letterbox_top(a) if which == "orig" else None
        m = strip_chrome(ink_mask(a), rr, bd, lb)
        # red-rect line centres: left column centre and right column centre
        lx = (rr[0] + rr[2]) / 2.0
        ly = (rr[1] + rr[3]) / 2.0
        rx0, ry0, rx1, ry1 = rr
        # scale: the red rect spans 13.03 in wide, 7.2 in tall
        sx = (rx1 - rx0 + 1) / 13.03
        sy = (ry1 - ry0 + 1) / 7.2
        imgs[which] = (m, sx, sy, rx0, ry0, rr, bd, lb)
    om, osx, osy, oox, ooy, orr, obd, olb = imgs["orig"]
    rm, rsx, rsy, rox, roy, rrr, rbd, rlb = imgs["rend"]
    out["red_rect"] = {"orig": list(orr), "rend": list(rrr)}
    out["badge"] = {"orig": list(obd) if obd else None,
                    "rend": list(rbd) if rbd else None}
    out["scale"] = {"orig": [round(osx, 2), round(osy, 2)],
                    "rend": [round(rsx, 2), round(rsy, 2)]}
    # cross-check: badge centre maps to ~12.73/0.55 in under house rule
    if obd:
        bc = ((obd[0] + obd[2]) / 2.0 - oox) / osx
        br = ((obd[1] + obd[3]) / 2.0 - ooy) / osy
        out["badge_residual_in"] = [round(bc - 12.73, 3), round(br - 0.55, 3)]
    # region measurements: map to inches then take rows in the window
    out["regions"] = []
    for name, y0, y1 in REGIONS:
        ob, rb = None, None
        om_sub = om.copy()
        rm_sub = rm.copy()
        om_sub[:int(y0 * osy + ooy), :] = False
        om_sub[int(y1 * osy + ooy):, :] = False
        rm_sub[:int(y0 * rsy + roy), :] = False
        rm_sub[int(y1 * rsy + roy):, :] = False
        ob = measure(om_sub, osx, osy, oox, ooy)
        rb = measure(rm_sub, rsx, rsy, rox, roy)
        if ob is None or rb is None:
            out["regions"].append({"name": name, "orig": ob, "rend": rb,
                                   "delta": None, "worst": None,
                                   "verdict": "EXCEEDS-TOLERANCE",
                                   "note": "region empty on one side only"})
            continue
        d = {"left": (rb["left"] - ob["left"]) * DPI,
             "right": -(rb["right"] - ob["right"]) * DPI,
             "top": -(rb["top"] - ob["top"]) * DPI,
             "bottom": -(rb["bottom"] - ob["bottom"]) * DPI}
        worst = max(abs(v) for v in d.values())
        out["regions"].append({"name": name, "orig": ob, "rend": rb,
                               "delta": {k: round(v, 1) for k, v in d.items()},
                               "worst": round(worst, 1),
                               "verdict": "PASS" if worst <= TOL else "EXCEEDS-TOLERANCE",
                               "note": None})
    return out


def main():
    res = {}
    for n in ["001", "004", "005", "006", "007"]:
        res[n] = one(n)
        print(n, json.dumps(res[n]["red_rect"]), json.dumps(res[n]["scale"]),
              "badge_residual", res[n].get("badge_residual_in"))
        for r in res[n]["regions"]:
            print("   %-38s %s worst=%s" % (r["name"], r["verdict"], r["worst"]))
    with open(f"{NS}/_pool/v5_b_geom_1.json", "w") as fh:
        json.dump(res, fh, indent=2)


if __name__ == "__main__":
    main()
