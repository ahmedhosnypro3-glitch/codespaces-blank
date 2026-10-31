#!/usr/bin/env python3
"""Lane G (b_geom_4): colour-class band decomposition on BOTH sides.

Prints, per slide and per colour class, the row bands and the x-extent of the
largest blob inside each band — for the original frame and for the render
(normalised to the same 960x540 source grid). This is the evidence used to pick
the final per-region windows.
"""
import numpy as np
from PIL import Image
from scipy import ndimage

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
TMP = f"{NS}/_pool/tmp_geom_b_geom_4"
SLIDES = ["025", "026", "027", "029", "032"]
O_BOX = (38, 43, 922, 539)
O_RING = [(38, 43, 41, 539), (919, 43, 922, 539), (38, 43, 922, 46), (38, 536, 922, 539)]
O_BADGE = (866, 46, 922, 98)
R_IN, R_OUT, R_OUT_Y = 26, 1975, 1099
R_BADGE = (1872, 45, 1947, 120)
R_TITLE = (90, 42, 1910, 130)


def fast_bg(a, box):
    x0, y0, x1, y1 = box
    sub = a[y0:y1, x0:x1].reshape(-1, 3)
    key = (sub[:, 0].astype(np.int32) << 16) | (sub[:, 1].astype(np.int32) << 8) | sub[:, 2]
    vals, counts = np.unique(key, return_counts=True)
    k = vals[counts.argmax()]
    return np.array([(k >> 16) & 255, (k >> 8) & 255, k & 255])


def ink(a, bg, thr=45):
    return np.abs(a - bg).sum(axis=2) > thr


def cls(a, kind):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    if kind == "red":
        return (r > 100) & (r > g + 25) & (r > b + 25)
    if kind == "blue":
        return (b > 80) & (b > r + 20) & (b > g + 15)
    if kind == "green":
        return (g > 100) & (g > r + 20) & (g > b + 20)
    if kind == "dark":
        return a.mean(axis=2) < 115
    if kind == "purple":
        return (r > 90) & (b > 90) & (g < r - 25) & (g < b - 25)
    raise ValueError(kind)


def bands(cnt, gap=3, minpx=4):
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


def prep(n):
    o = np.asarray(Image.open(f"{NS}/unique_slides/slide_{n}.jpg").convert("RGB")).astype(int)
    r = np.asarray(Image.open(f"{TMP}/png_{n}/render-1.png").convert("RGB")).astype(int)
    om = ink(o, fast_bg(o, O_BOX))
    om[: O_BOX[1], :] = om[O_BOX[3]:, :] = False
    om[:, : O_BOX[0]] = om[:, O_BOX[2]:] = False
    for x0, y0, x1, y1 in O_RING + [O_BADGE]:
        om[y0:y1, x0:x1] = False
    rm = ink(r, fast_bg(r, (30, 30, r.shape[1] - 30, r.shape[0] - 30)))
    rm[:R_IN, :] = rm[R_OUT_Y:, :] = False
    rm[:, :R_IN] = rm[:, R_OUT:] = False
    rm[R_BADGE[1]:R_BADGE[3], R_BADGE[0]:R_BADGE[2]] = False
    rm[R_TITLE[1]:R_TITLE[3], R_TITLE[0]:R_TITLE[2]] = False
    return o, om, r, rm


def main():
    for n in SLIDES:
        o, om, r, rm = prep(n)
        fx, fy = 960.0 / r.shape[1], 540.0 / r.shape[0]
        for kind in ("red", "blue", "green", "dark", "purple"):
            print(f"##### slide {n} class={kind}")
            for tag, img, m, is_o in (("ORIG", o, om, True), ("REND", r, rm, False)):
                cm = cls(img, kind) & m
                for (y0, y1) in bands(cm.sum(axis=1)):
                    sub = cm[y0:y1 + 1, :]
                    cc = np.where(sub.any(axis=0))[0]
                    if is_o:
                        print(f"   {tag} y{y0}-{y1} x{cc[0]}-{cc[-1]}")
                    else:
                        print(f"   {tag} y{round(y0*fy,1)}-{round(y1*fy,1)} "
                              f"x{round(cc[0]*fx,1)}-{round(cc[-1]*fx,1)}")


if __name__ == "__main__":
    main()
