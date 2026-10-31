#!/usr/bin/env python3
"""Lane G (b_geom_4): element decomposition of the ORIGINAL frame.

For each slide: row bands (gap 2, minpx 5) and, inside each row band, the
column bands. This decomposes the original into individual content elements so
the final per-region spec is derived from measurement, not guesswork.
"""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
SLIDES = ["025", "026", "027", "029", "032"]
O_BOX = (38, 43, 922, 539)
O_RING = [(38, 43, 41, 539), (919, 43, 922, 539), (38, 43, 922, 46), (38, 536, 922, 539)]
O_BADGE = (866, 46, 922, 98)      # original's own yellow badge


def fast_bg(a, box):
    x0, y0, x1, y1 = box
    sub = a[y0:y1, x0:x1].reshape(-1, 3)
    key = (sub[:, 0].astype(np.int32) << 16) | (sub[:, 1].astype(np.int32) << 8) | sub[:, 2]
    vals, counts = np.unique(key, return_counts=True)
    k = vals[counts.argmax()]
    return np.array([(k >> 16) & 255, (k >> 8) & 255, k & 255])


def bands(cnt, gap=2, minpx=5):
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


def main():
    for n in SLIDES:
        o = np.asarray(Image.open(f"{NS}/unique_slides/slide_{n}.jpg").convert("RGB")).astype(int)
        m = np.abs(o - fast_bg(o, O_BOX)).sum(axis=2) > 45
        m[: O_BOX[1], :] = m[O_BOX[3]:, :] = False
        m[:, : O_BOX[0]] = m[:, O_BOX[2]:] = False
        for x0, y0, x1, y1 in O_RING + [O_BADGE]:
            m[y0:y1, x0:x1] = False
        print(f"##### slide {n}")
        for (y0, y1) in bands(m.sum(axis=1)):
            sub = m[y0:y1 + 1, :]
            cols = bands(sub.sum(axis=0))
            ext = " ".join(f"x{c[0]}-{c[1]}" for c in cols[:8])
            print(f"  y{y0:3d}-{y1:3d}  {ext}")


if __name__ == "__main__":
    main()
