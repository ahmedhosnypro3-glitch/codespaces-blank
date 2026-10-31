#!/usr/bin/env python3
"""Lane G (b_geom_4): ASCII ink maps, original frame vs render, both in frame
coords (960x540). Render is BOX-resampled from 2001x1125."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
TMP = f"{NS}/_pool/tmp_geom_b_geom_4"
SLIDES = ["025", "026", "027", "029", "032"]
AREA = (37, 42, 923, 540)


def fast_bg(a, box):
    x0, y0, x1, y1 = box
    sub = a[y0:y1, x0:x1].reshape(-1, 3)
    key = (sub[:, 0].astype(np.int32) << 16) | (sub[:, 1].astype(np.int32) << 8) | sub[:, 2]
    vals, counts = np.unique(key, return_counts=True)
    k = vals[counts.argmax()]
    return np.array([(k >> 16) & 255, (k >> 8) & 255, k & 255])


def ink(a, bg, thr=45):
    return np.abs(a - bg).sum(axis=2) > thr


def amap(mask):
    rows = []
    for ry in range(27):
        line = ""
        for cx in range(48):
            blk = mask[ry * 20:(ry + 1) * 20, cx * 20:(cx + 1) * 20]
            f = blk.mean()
            line += " " if f < 0.02 else ("." if f < 0.08 else ("o" if f < 0.3 else "#"))
        rows.append(line)
    return rows


def main():
    for n in SLIDES:
        o = np.asarray(Image.open(f"{NS}/unique_slides/slide_{n}.jpg").convert("RGB")).astype(int)
        r = np.asarray(Image.open(f"{TMP}/png_{n}/render-1.png").convert("RGB")).astype(int)
        rf = np.asarray(Image.fromarray(r.astype("uint8")).resize((960, 540), Image.BOX)).astype(int)
        om = ink(o, fast_bg(o, AREA))
        rm = ink(rf, fast_bg(rf, (20, 20, 940, 520)))
        om[:, :AREA[0]] = False
        om[:, AREA[2]:] = False
        om[:AREA[1], :] = False
        # kill the original's own outer border lines (thin full-span runs)
        om[:3, :] = False
        om[-3:, :] = False
        om[:, :3] = False
        om[:, -3:] = False
        oa, ra = amap(om), amap(rm)
        print(f"##### slide {n}")
        print("  ORIGINAL (frame coords)  |  RENDER (frame coords)")
        for i in range(27):
            print(f"{i*20:4d} {oa[i]}  |  {ra[i]}")


if __name__ == "__main__":
    main()
