#!/usr/bin/env python3
"""Lane G diag: calibrate original-frame vs render slide mapping via the red chrome frame."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"


def redmask(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 120) & (r < 230) & (g < 90) & (b < 90)


def bbox(m):
    ys, xs = np.nonzero(m)
    if not len(xs):
        return None
    return (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()), int(m.sum()))


for s in ("008", "009", "010", "012", "013"):
    print("=" * 66)
    print("SLIDE", s)
    for tag, p in (("orig", f"{NS}/unique_slides/slide_{s}.jpg"),
                   ("rend", f"{NS}/_pool/tmp_geom_b_geom_2/{s}/render-1.png")):
        a = np.asarray(Image.open(p).convert("RGB")).astype(int)
        h, w = a.shape[:2]
        rm = redmask(a)
        bb = bbox(rm)
        print(f"  {tag} {w}x{h} redbbox={bb}")
        if bb:
            x0, y0, x1, y1, n = bb
            # red pixel count per row/col to see frame thickness lines
            rows = rm.sum(axis=1)
            cols = rm.sum(axis=0)
            top_rows = [(y, int(rows[y])) for y in range(h) if rows[y] > w * 0.4][:6]
            bot_rows = [(y, int(rows[y])) for y in range(h - 1, -1, -1) if rows[y] > w * 0.4][:6]
            left_cols = [(x, int(cols[x])) for x in range(w) if cols[x] > h * 0.4][:6]
            right_cols = [(x, int(cols[x])) for x in range(w - 1, -1, -1) if cols[x] > h * 0.4][:6]
            print(f"    hlines top={top_rows} bot={bot_rows}")
            print(f"    vlines left={left_cols} right={right_cols}")
