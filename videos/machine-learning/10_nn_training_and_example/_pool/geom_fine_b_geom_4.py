#!/usr/bin/env python3
"""Lane G (b_geom_4) diagnostic: fine ink bands with x-extents, both sides,
source-frame px. Used to finalise per-region boxes."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
TMP = f"{NS}/_pool/tmp_geom_b_geom_4"
SLIDES = ["025", "026", "027", "029", "032"]
O_BOX = (38, 43, 922, 539)
O_RING = [(38, 43, 41, 539), (919, 43, 922, 539), (38, 43, 922, 46), (38, 536, 922, 539)]


def fast_bg(a, box):
    x0, y0, x1, y1 = box
    sub = a[y0:y1, x0:x1].reshape(-1, 3)
    key = (sub[:, 0].astype(np.int32) << 16) | (sub[:, 1].astype(np.int32) << 8) | sub[:, 2]
    vals, counts = np.unique(key, return_counts=True)
    k = vals[counts.argmax()]
    return np.array([(k >> 16) & 255, (k >> 8) & 255, k & 255])


def bands(cnt, gap=3, minpx=2):
    idx = np.where(cnt >= minpx)[0]
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


def orig_m(n):
    o = np.asarray(Image.open(f"{NS}/unique_slides/slide_{n}.jpg").convert("RGB")).astype(int)
    m = np.abs(o - fast_bg(o, O_BOX)).sum(axis=2) > 45
    m[: O_BOX[1], :] = m[O_BOX[3]:, :] = False
    m[:, : O_BOX[0]] = m[:, O_BOX[2]:] = False
    for x0, y0, x1, y1 in O_RING:
        m[y0:y1, x0:x1] = False
    return m, 1.0


def rend_m(n):
    r = np.asarray(Image.open(f"{TMP}/png_{n}/render-1.png").convert("RGB")).astype(int)
    m = np.abs(r - fast_bg(r, (30, 30, r.shape[1] - 30, r.shape[0] - 30))).sum(axis=2) > 45
    m[:26, :] = m[1099:, :] = False
    m[:, :26] = m[:, 1975:] = False
    m[45:120, 1872:1947] = False      # badge
    return m, 540.0 / r.shape[0]


def main():
    for n in SLIDES:
        print(f"##### slide {n}")
        for tag, fn in (("ORIG", orig_m), ("REND", rend_m)):
            m, sc = fn(n)
            for (y0, y1) in bands(m.sum(axis=1), 3):
                sub = m[y0:y1 + 1, :]
                cc = np.where(sub.any(axis=0))[0]
                print(f"  {tag} y{round(y0*sc,1):>6}-{round(y1*sc,1):<6} "
                      f"x{int(cc[0])}-{int(cc[-1])}")


if __name__ == "__main__":
    main()
