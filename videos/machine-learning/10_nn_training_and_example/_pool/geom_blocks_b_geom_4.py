#!/usr/bin/env python3
"""Lane G (b_geom_4): ink-structure census in ORIGINAL FRAME coords (960x540).

Both images are reduced to frame coordinates:
  - original: already 960x540 (video capture, slide area x37..922 y42..539)
  - render:   2001x1125 LO PNG, BOX-resampled to 960x540
The recreation maps source frame px linearly onto 13.33x7.5in, so frame coords
are directly comparable. Verified on slide 029: red box top edge orig y202-203
vs render y201-202.
"""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
TMP = f"{NS}/_pool/tmp_geom_b_geom_4"
SLIDES = ["025", "026", "027", "029", "032"]
AREA = (37, 42, 923, 540)  # slide pixels inside the original frame


def fast_bg(a, box):
    x0, y0, x1, y1 = box
    sub = a[y0:y1, x0:x1].reshape(-1, 3)
    key = (sub[:, 0].astype(np.int32) << 16) | (sub[:, 1].astype(np.int32) << 8) | sub[:, 2]
    vals, counts = np.unique(key, return_counts=True)
    k = vals[counts.argmax()]
    return np.array([(k >> 16) & 255, (k >> 8) & 255, k & 255])


def ink(a, bg, thr=45):
    return np.abs(a - bg).sum(axis=2) > thr


def runs_of(idx, gap=3, minlen=1):
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


def row_runs(mask, minpx=4, gap=3):
    """Row bands (y ranges) with >= minpx ink in each row."""
    cnt = mask.sum(axis=1)
    return runs_of(np.where(cnt >= minpx)[0], gap)


def col_runs(mask, minpx=4, gap=3):
    cnt = mask.sum(axis=0)
    return runs_of(np.where(cnt >= minpx)[0], gap)


def load(n):
    o = np.asarray(Image.open(f"{NS}/unique_slides/slide_{n}.jpg").convert("RGB")).astype(int)
    r = np.asarray(Image.open(f"{TMP}/png_{n}/render-1.png").convert("RGB")).astype(int)
    return o, r


def render_frame(r):
    rs = np.asarray(Image.fromarray(r.astype("uint8")).resize((960, 540), Image.BOX)).astype(int)
    return rs


def main():
    for n in SLIDES:
        o, r = load(n)
        of = render_frame(r)
        obg = fast_bg(o, AREA)
        rbg = fast_bg(r, (30, 30, r.shape[1] - 30, r.shape[0] - 30))
        om = ink(o, obg)
        rm = ink(of, rbg)
        # original: blank the letterbox outside the slide area
        om[:, :AREA[0]] = False
        om[:, AREA[2]:] = False
        om[:AREA[1], :] = False
        print(f"===== slide {n}  obg={obg.tolist()} rbg={rbg.tolist()}")
        print(f"  ORIG rowbands: {row_runs(om)}")
        print(f"  REND rowbands: {row_runs(rm)}")
        print(f"  ORIG colbands: {col_runs(om)}")
        print(f"  REND colbands: {col_runs(rm)}")


if __name__ == "__main__":
    main()
