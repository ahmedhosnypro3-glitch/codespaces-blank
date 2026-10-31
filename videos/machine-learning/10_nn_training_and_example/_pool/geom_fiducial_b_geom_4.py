#!/usr/bin/env python3
"""Lane G (b_geom_4): detect the ORIGINAL slide's own red rectangle (the
fiducial used by sibling lane b_geom_2 for calibration)."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
TMP = f"{NS}/_pool/tmp_geom_b_geom_4"
SLIDES = ["025", "026", "027", "029", "032"]


def runs(idx, gap=2):
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


def reddish(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 110) & (r < 215) & (r > g + 35) & (r > b + 35)


for n in SLIDES:
    o = np.asarray(Image.open(f"{NS}/unique_slides/slide_{n}.jpg").convert("RGB")).astype(int)
    m = reddish(o)
    rs, cs = m.sum(axis=1), m.sum(axis=0)
    hr = np.where(rs > 500)[0]
    vc = np.where(cs > 300)[0]
    print(f"##### slide {n}")
    print(f"  red h-rows (span>500): {runs(hr)}")
    print(f"  red v-cols (span>300): {runs(vc)}")
    # looser: rows/cols whose redish count is high
    print(f"  top red rows: {sorted(np.argsort(rs)[-6:].tolist())} counts "
          f"{sorted(rs[np.argsort(rs)[-6:]].tolist())}")
    print(f"  top red cols: {sorted(np.argsort(cs)[-6:].tolist())} counts "
          f"{sorted(cs[np.argsort(cs)[-6:]].tolist())}")
    # candidate border colour along the slide edge
    for (x, y) in [(37, 250), (921, 250), (480, 43), (480, 537), (40, 45)]:
        print(f"    px({x},{y}) = {o[y, x].tolist()}")
