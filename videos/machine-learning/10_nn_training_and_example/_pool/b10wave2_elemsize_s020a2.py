#!/usr/bin/env python3
"""Slide 020 per-element size comparison, orig vs render.
Threshold 200 (video frames are anti-aliased; threshold 128 misses light strokes)."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
S = 960 / 13.3333
IN = 2001 / 13.3333

O = np.array(Image.open(f"{NS}/unique_slides/slide_020.jpg").convert("L")).astype(int)
R = np.array(Image.open(f"{NS}/qa/slide020/b10wave2/a2/render-1.png").convert("L")).astype(int)


def bbox(a, sc, x0, y0, x1, y1, thr):
    X0, Y0, X1, Y1 = (int(v * sc) for v in (x0, y0, x1, y1))
    sub = a[Y0:Y1, X0:X1] < thr
    if not sub.any():
        return None
    ys, xs = np.where(sub)
    return dict(
        x0=(xs.min() + X0) / sc, x1=(xs.max() + X0) / sc,
        y0=(ys.min() + Y0) / sc, y1=(ys.max() + Y0) / sc,
        w=(xs.max() - xs.min()) / sc, h=(ys.max() - ys.min()) / sc,
        n=int(sub.sum()))


ELEMS = {
    "cyan box text":   (0.75, 0.90, 5.30, 3.20),
    "mid row 1":       (0.67, 3.42, 7.34, 3.86),
    "mid row 2":       (0.67, 4.32, 7.48, 5.00),
    "cream deriv all": (9.15, 3.40, 12.60, 6.45),
    "cream line 1":    (9.15, 3.40, 12.60, 3.85),
    "cream line 2":    (9.15, 4.20, 12.60, 4.80),
    "cream line 3":    (9.15, 5.00, 12.60, 5.60),
    "cream line 4":    (9.15, 5.85, 12.60, 6.45),
    "delta box text":  (0.90, 5.90, 6.05, 6.75),
    "where strip":     (0.75, 6.72, 8.90, 7.40),
    "diagram canvas":  (5.58, 0.66, 11.20, 3.26),
    "class labels":    (11.50, 0.90, 12.45, 2.80),
    "node mode":       (5.65, 2.85, 7.10, 3.20),
}

for thr in (128, 200):
    print(f"\n########## threshold {thr} ##########")
    print(f"{'element':<17} {'ORIG x0-x1 (w)':<30} {'REND x0-x1 (w)':<30} dw_in")
    for nm, (x0, y0, x1, y1) in ELEMS.items():
        o = bbox(O, S, x0, y0, x1, y1, thr)
        r = bbox(R, IN, x0, y0, x1, y1, thr)
        if not o or not r:
            print(f"{nm:<17} {'n/a' if not o else 'ok':<30} {'n/a' if not r else 'ok'}")
            continue
        dw = r["w"] - o["w"]
        flag = "  <<< SIZE MISMATCH" if abs(dw) > 0.25 else ""
        print(f"{nm:<17} {o['x0']:.2f}-{o['x1']:.2f} (w{o['w']:.2f})       "
              f"{r['x0']:.2f}-{r['x1']:.2f} (w{r['w']:.2f})       {dw:+.2f}{flag}")
