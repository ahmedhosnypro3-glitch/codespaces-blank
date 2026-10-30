#!/usr/bin/env python3
"""Crop the differing regions between twin slides so a vision call can read them."""
import sys
from PIL import Image
import numpy as np

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides"
OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/_pool/a18_crops"
import os
os.makedirs(OUT, exist_ok=True)


def diff_regions(a_n, b_n, tag, thresh=60):
    a = np.asarray(Image.open(f"{BASE}/slide_{a_n:03d}.jpg").convert("RGB")).astype(int)
    b = np.asarray(Image.open(f"{BASE}/slide_{b_n:03d}.jpg").convert("RGB")).astype(int)
    d = np.abs(a - b).sum(axis=2)
    mask = d > thresh
    ys, xs = np.where(mask)
    if not len(xs):
        print(tag, "no diff")
        return
    print(f"{tag}: diff bbox x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} ({mask.sum()} px)")
    # cluster by connected-ish regions using a grid
    from scipy import ndimage
    lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
    sizes = ndimage.sum(mask, lab, range(1, n + 1))
    order = np.argsort(sizes)[::-1][:8]
    for i in order:
        if sizes[i] < 8:
            continue
        ys2, xs2 = np.where(lab == i + 1)
        x0, x1, y0, y1 = xs2.min(), xs2.max(), ys2.min(), ys2.max()
        pad = 12
        x0 = max(0, x0 - pad); y0 = max(0, y0 - pad)
        x1 = min(a.shape[1] - 1, x1 + pad); y1 = min(a.shape[0] - 1, y1 + pad)
        name = f"{OUT}/{tag}_r{i+1}_x{x0}-{x1}_y{y0}-{y1}.png"
        ia = Image.open(f"{BASE}/slide_{a_n:03d}.jpg").convert("RGB").crop((x0, y0, x1 + 1, y1 + 1))
        ib = Image.open(f"{BASE}/slide_{b_n:03d}.jpg").convert("RGB").crop((x0, y0, x1 + 1, y1 + 1))
        canvas = Image.new("RGB", (ia.width, ia.height * 2 + 8), "white")
        canvas.paste(ia, (0, 0)); canvas.paste(ib, (0, ia.height + 8))
        canvas = canvas.resize((canvas.width * 2, canvas.height * 2), Image.LANCZOS)
        canvas.save(name)
        print(f"   region {i+1}: x {x0}..{x1} y {y0}..{y1} ({int(sizes[i])} px) -> {name}")


diff_regions(30, 31, "d30_31")
print()
diff_regions(32, 33, "d32_33")
