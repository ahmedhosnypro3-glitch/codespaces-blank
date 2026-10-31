#!/usr/bin/env python3
"""Lane G (b_geom_4): define regions from the ORIGINAL's own ink density,
then measure both images on identical boxes."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
TMP = f"{NS}/_pool/tmp_geom_b_geom_4"
SLIDES = ["025", "026", "027", "029", "032"]
O_BOX = (38, 43, 922, 539)
O_RING = [(38, 43, 41, 539), (919, 43, 922, 539), (38, 43, 922, 46), (38, 536, 922, 539)]
TITLE_TOP = 70      # original title band (chrome analogue)


def fast_bg(a, box):
    x0, y0, x1, y1 = box
    sub = a[y0:y1, x0:x1].reshape(-1, 3)
    key = (sub[:, 0].astype(np.int32) << 16) | (sub[:, 1].astype(np.int32) << 8) | sub[:, 2]
    vals, counts = np.unique(key, return_counts=True)
    k = vals[counts.argmax()]
    return np.array([(k >> 16) & 255, (k >> 8) & 255, k & 255])


def orig_mask(n):
    o = np.asarray(Image.open(f"{NS}/unique_slides/slide_{n}.jpg").convert("RGB")).astype(int)
    om = np.abs(o - fast_bg(o, O_BOX)).sum(axis=2) > 45
    om[: O_BOX[1], :] = om[O_BOX[3]:, :] = False
    om[:, : O_BOX[0]] = om[:, O_BOX[2]:] = False
    for x0, y0, x1, y1 in O_RING:
        om[y0:y1, x0:x1] = False
    om[:TITLE_TOP, :] = False
    return o, om


def render_mask(n, r):
    rbg = fast_bg(r, (30, 30, r.shape[1] - 30, r.shape[0] - 30))
    rm = np.abs(r - rbg).sum(axis=2) > 45
    rm[:26, :] = False
    rm[1099:, :] = False
    rm[:, :26] = rm[:, 1975:] = False
    rm[45:120, 1872:1947] = False      # house badge
    rm[42:130, 90:1910] = False        # house title box
    return rm


def bands(cnt, minpx=2, gap=6, minlen=3):
    """Contiguous runs of indices whose count >= minpx."""
    idx = np.where(cnt >= minpx)[0]
    if len(idx) == 0:
        return []
    out, s, p = [], idx[0], idx[0]
    for i in idx[1:]:
        if i - p > gap:
            if p - s + 1 >= minlen:
                out.append((int(s), int(p)))
            s = i
        p = i
    if p - s + 1 >= minlen:
        out.append((int(s), int(p)))
    return out


def row_bands(m):
    return bands(m.sum(axis=1))


def col_bands(m):
    return bands(m.sum(axis=0))


def bbox(m, ox=0, oy=0):
    r = np.where(m.any(axis=1))[0]
    c = np.where(m.any(axis=0))[0]
    if len(r) == 0:
        return None
    return int(c[0]) + ox, int(r[0]) + oy, int(c[-1]) + ox, int(r[-1]) + oy


def main():
    for n in SLIDES:
        om = orig_mask(n)[1]
        r = np.asarray(Image.open(f"{TMP}/png_{n}/render-1.png").convert("RGB")).astype(int)
        rm = render_mask(n, r)
        fx = 960.0 / r.shape[1]
        fy = 540.0 / r.shape[0]
        print(f"##### slide {n}")
        for (y0, y1) in row_bands(om):
            sub = om[y0:y1 + 1, :]
            c = np.where(sub.any(axis=0))[0]
            # same band in the render, then to frame px
            ry0, ry1 = int(round(y0 / fy)), int(round((y1 + 1) / fy))
            rb = bbox(rm[ry0:ry1, :], 0, ry0)
            rf = None if rb is None else [round(rb[0] * fx), round(rb[1] * fy),
                                          round(rb[2] * fx), round(rb[3] * fy)]
            print(f"        y{y0}-{y1:4d}: ORIG x{int(c[0])}-{int(c[-1])} | "
                  f"REND(frame) {rf}")


if __name__ == "__main__":
    main()
