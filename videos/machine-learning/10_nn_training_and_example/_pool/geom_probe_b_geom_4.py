#!/usr/bin/env python3
"""Lane G (b_geom_4) probe: exact slide-area and original-border geometry."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
SLIDES = ["025", "026", "027", "029", "032"]
WHITE = np.array([254, 255, 253])
GRAY = np.array([231, 233, 230])


def near(a, c, tol=12):
    return np.abs(a - c).sum(axis=2) <= tol


def runs(idx, gap=3):
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


for n in SLIDES:
    o = np.asarray(Image.open(f"{NS}/unique_slides/slide_{n}.jpg").convert("RGB")).astype(int)
    w = near(o, WHITE)
    g = near(o, GRAY)
    red = (o[:, :, 0] > 120) & (o[:, :, 0] < 210) & (o[:, :, 1] < 70) & (o[:, :, 2] < 70)
    print(f"##### slide {n}")
    print(f"  white rows : {runs(np.where(w.all(axis=1))[0])}")
    print(f"  white cols : {runs(np.where(w.all(axis=0))[0])}")
    print(f"  gray  rows : {runs(np.where(g.sum(axis=1) > 700)[0])[:6]}")
    print(f"  gray  cols : {runs(np.where(g.sum(axis=0) > 400)[0])[:6]}")
    rs, cs = red.sum(axis=1), red.sum(axis=0)
    print(f"  red rows>400: {runs(np.where(rs > 400)[0])}")
    print(f"  red cols>200: {runs(np.where(cs > 200)[0])}")
