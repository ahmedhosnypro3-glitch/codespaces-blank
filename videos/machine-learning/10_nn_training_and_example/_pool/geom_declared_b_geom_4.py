#!/usr/bin/env python3
"""Lane G (b_geom_4): declare->measure geometry check.

Reads each build script's declared px(x)/px(y)/px(w)/px(h) boxes (source-frame
px), and measures the ORIGINAL frame's ink bounding box inside the SAME box.
This tests whether the recreation landed on the original's actual content.

Source px map linearly onto 13.33x7.5in (PX = 13.33/960), and the render is the
pptx at 150dpi, so render_px * 960/2001 == source px. Both sides are compared in
SOURCE-FRAME px.
"""
import re
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
TMP = f"{NS}/_pool/tmp_geom_b_geom_4"
BUILD = f"{NS}/recreated_pptx/build"
SCOPE = "b_geom_4"
SLIDES = ["025", "026", "027", "029", "032"]

O_BOX = (38, 43, 922, 539)
O_RING = [(38, 43, 41, 539), (919, 43, 922, 539), (38, 43, 922, 46), (38, 536, 922, 539)]
R_CHROME_IN, R_CHROME_OUT = 26, 1975
R_BADGE = (1872, 45, 1947, 120)
R_TITLE = (90, 42, 1910, 130)
CHROME_Y = 70   # rows above this (orig) are title/badge chrome


def fast_bg(a, box):
    x0, y0, x1, y1 = box
    sub = a[y0:y1, x0:x1].reshape(-1, 3)
    key = (sub[:, 0].astype(np.int32) << 16) | (sub[:, 1].astype(np.int32) << 8) | sub[:, 2]
    vals, counts = np.unique(key, return_counts=True)
    k = vals[counts.argmax()]
    return np.array([(k >> 16) & 255, (k >> 8) & 255, k & 255])


def load_images(n):
    o = np.asarray(Image.open(f"{NS}/unique_slides/slide_{n}.jpg").convert("RGB")).astype(int)
    r = np.asarray(Image.open(f"{TMP}/png_{n}/render-1.png").convert("RGB")).astype(int)
    return o, r


def orig_ink(o):
    m = np.abs(o - fast_bg(o, O_BOX)).sum(axis=2) > 45
    m[: O_BOX[1], :] = m[O_BOX[3]:, :] = False
    m[:, : O_BOX[0]] = m[:, O_BOX[2]:] = False
    for x0, y0, x1, y1 in O_RING:
        m[y0:y1, x0:x1] = False
    return m


def render_ink(r):
    m = np.abs(r - fast_bg(r, (30, 30, r.shape[1] - 30, r.shape[0] - 30))).sum(axis=2) > 45
    m[:R_CHROME_IN, :] = m[1099:, :] = False
    m[:, :R_CHROME_IN] = m[:, R_CHROME_OUT:] = False
    m[R_BADGE[1]:R_BADGE[3], R_BADGE[0]:R_BADGE[2]] = False
    m[R_TITLE[1]:R_TITLE[3], R_TITLE[0]:R_TITLE[2]] = False
    return m


def bbox(m, ox=0, oy=0):
    rr = np.where(m.any(axis=1))[0]
    cc = np.where(m.any(axis=0))[0]
    if len(rr) == 0:
        return None
    return int(cc[0]) + ox, int(rr[0]) + oy, int(cc[-1]) + ox, int(rr[-1]) + oy


def main():
    for n in SLIDES:
        o, r = load_images(n)
        om, rm = orig_ink(o), render_ink(r)
        fx, fy = 960.0 / r.shape[1], 540.0 / r.shape[0]
        print(f"########## slide {n}: render {r.shape[1]}x{r.shape[0]} "
              f"scale(fx={fx:.5f}, fy={fy:.5f})")
        # empirical content bands from the original
        print("  ORIG content row bands (y, x-extent):")
        cnt = om.sum(axis=1)
        idx = np.where(cnt >= 2)[0]
        for (y0, y1) in runs(idx, 6):
            cc = np.where(om[y0:y1 + 1, :].any(axis=0))[0]
            rry = (int(round(y0 / fy)), int(round((y1 + 1) / fy)))
            rb = bbox(rm[rry[0]:rry[1], :], 0, rry[0])
            rf = None if rb is None else (round(rb[0] * fx), round(rb[1] * fy),
                                          round(rb[2] * fx), round(rb[3] * fy))
            print(f"    y{y0}-{y1}: ORIG x{int(cc[0])}-{int(cc[-1])}  REND(frame) {rf}")


def runs(idx, gap):
    if len(idx) == 0:
        return []
    out, s, p = [], idx[0], idx[0]
    for i in idx[1:]:
        if i - p > gap:
            out.append((int(s), int(p)))
            s = i
        p = i
    out.append((int(s), int(p)))
    return out


if __name__ == "__main__":
    main()
