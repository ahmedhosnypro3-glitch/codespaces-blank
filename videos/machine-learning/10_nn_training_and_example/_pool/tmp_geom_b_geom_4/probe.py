#!/usr/bin/env python3
"""Lane b_geom_4 geometry measurement: calibrate originals + renders to slide-inch
coordinates through the house chrome fiducial, mask chrome, measure content ink."""
import json, os, sys
import numpy as np
from PIL import Image

VID = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
OUT = os.path.join(VID, "_pool", "tmp_geom_b_geom_4")
SLIDES = ["025", "026", "027", "029", "032"]

LUM_T, CHROMA_T = 170, 45
TOL = 4.0

# slide-inch regions (house geometry: frame 0.15..13.18 x 0.15..7.35 y)
REGIONS = [
    ("title block", 0.15, 1.10),
    ("body / equation / diagram / table region", 1.10, 6.90),
    ("footer region", 6.90, 7.50),
]


def lum_chroma(im):
    a = np.asarray(im.convert("RGB")).astype(float)
    lum = a.mean(axis=2)
    mx, mn = a.max(axis=2), a.min(axis=2)
    chroma = mx - mn
    return lum, chroma


def red_mask(lum, chroma, rgb):
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    return (r > 120) & (r - g > 60) & (r - b > 60)


def column_profile(mask, axis_rows=True):
    """Sum of mask along rows -> per-column profile."""
    return mask.sum(axis=1 if axis_rows else 0)


def find_horizontal_lines(mask, thresh=0.60):
    """rows where >thresh of the row is masked -> long horizontal line."""
    frac = mask.mean(axis=1)
    idx = np.where(frac > thresh)[0]
    if len(idx) == 0:
        return []
    groups, cur = [], [idx[0]]
    for i in idx[1:]:
        if i - cur[-1] <= 2:
            cur.append(i)
        else:
            groups.append(cur)
            cur = [i]
    groups.append(cur)
    return [float(np.mean(g)) for g in groups]


def find_vertical_lines(mask, thresh=0.60):
    frac = mask.mean(axis=0)
    idx = np.where(frac > thresh)[0]
    if len(idx) == 0:
        return []
    groups, cur = [], [idx[0]]
    for i in idx[1:]:
        if i - cur[-1] <= 2:
            cur.append(i)
        else:
            groups.append(cur)
            cur = [i]
    groups.append(cur)
    return [float(np.mean(g)) for g in groups]


def box_of(mask):
    ys, xs = np.where(mask)
    if len(ys) == 0:
        return None
    return (float(xs.min()), float(ys.min()), float(xs.max()), float(ys.max()), int(len(ys)))


def strip_chrome(ink, vlines, hlines, vpad=6.0, hpad=6.0):
    """Blank out a vertical band around each vertical line and horizontal band
    around each horizontal line (the red frame edges), plus badge circle."""
    out = ink.copy()
    for v in vlines:
        lo, hi = max(0, int(v - vpad)), int(v + vpad) + 1
        out[:, lo:hi] = False
    for h in hlines:
        lo, hi = max(0, int(h - hpad)), int(h + hpad) + 1
        out[lo:hi, :] = False
    return out


def strip_badge(ink, cx, cy, r):
    h, w = ink.shape
    yy, xx = np.mgrid[0:h, 0:w]
    d2 = (xx - cx) ** 2 + (yy - cy) ** 2
    out = ink.copy()
    out[d2 <= r * r] = False
    return out


def main():
    report = {}
    for s in SLIDES:
        orig = Image.open(os.path.join(VID, "unique_slides", f"slide_{s}.jpg"))
        rend = Image.open(os.path.join(OUT, s, "render-1.png"))

        o_lum, o_ch = lum_chroma(orig)
        r_lum, r_ch = lum_chroma(rend)

        o_rgb = np.asarray(orig.convert("RGB")).astype(float)
        r_rgb = np.asarray(rend.convert("RGB")).astype(float)

        o_red = red_mask(o_lum, o_ch, o_rgb)
        r_red = red_mask(r_lum, r_ch, r_rgb)

        print(f"=== {s} ===")
        print("  orig size", orig.size, "render size", rend.size)
        print("  orig red px", int(o_red.sum()), "render red px", int(r_red.sum()))

        # measure the red rectangle line centres in each image
        o_h = find_horizontal_lines(o_red)
        r_h = find_horizontal_lines(r_red)
        o_v = find_vertical_lines(o_red)
        r_v = find_vertical_lines(r_red)
        print("  render h-lines", [round(x, 1) for x in r_h], "v-lines", [round(x, 1) for x in r_v])
        print("  orig   h-lines", [round(x, 1) for x in o_h], "v-lines", [round(x, 1) for x in o_v])

        # letterbox check on original: top/bottom uniform bands
        omr = o_lum.mean(axis=1)
        print("  orig row-mean first6", [round(v) for v in omr[:6]], "last6", [round(v) for v in omr[-6:]])

        # yellow badge in original
        o_y = ((o_rgb[..., 0] > 200) & (o_rgb[..., 1] > 200) & (o_rgb[..., 2] < 220) &
               (o_rgb[..., 1] - o_rgb[..., 2] > 20))
        r_y = ((r_rgb[..., 0] > 200) & (r_rgb[..., 1] > 200) & (r_rgb[..., 2] < 220) &
               (r_rgb[..., 1] - r_rgb[..., 2] > 20))
        print("  orig yellow px", int(o_y.sum()), "render yellow px", int(r_y.sum()))
        if o_y.any():
            ys, xs = np.where(o_y)
            print("  orig yellow bbox", int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))
        if r_y.any():
            ys, xs = np.where(r_y)
            print("  render yellow bbox", int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))

        # black bottom band in original
        o_black = o_lum < 60
        print("  orig black px", int(o_black.sum()))
        r_black = r_lum < 60
        print("  render black px", int(r_black.sum()))


if __name__ == "__main__":
    main()
