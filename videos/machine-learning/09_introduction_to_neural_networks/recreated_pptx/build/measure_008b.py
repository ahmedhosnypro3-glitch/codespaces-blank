#!/usr/bin/env python3
"""Palette-based structural comparison of original vs render for slide 008."""
import sys
from collections import Counter
from PIL import Image
import numpy as np

ORIG = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_008.jpg"
REND = sys.argv[1] if len(sys.argv) > 1 else "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_008_rendered_resized.png"

orig = Image.open(ORIG).convert("RGB")
pal = orig.quantize(colors=16, method=Image.MEDIANCUT).convert("RGB")
counts = Counter(pal.getdata())
print("ORIGINAL palette (top 16):")
for c, n in counts.most_common():
    print(f"  {c} {n:7d}  {n/ (960*540)*100:5.1f}%")


def classify(path):
    im = Image.open(path).convert("RGB").resize((960, 540), Image.LANCZOS)
    a = np.asarray(im).astype(int)
    palarr = np.array([c for c, _ in counts.most_common()]).astype(int)
    d = np.abs(a[:, :, None, :] - palarr[None, None, :, :]).sum(axis=3)
    idx = d.argmin(axis=2)
    return a, palarr, idx


def report(label, a, palarr, idx):
    print(f"\n=== {label} ===")
    for i, c in enumerate(palarr):
        m = idx == i
        n = int(m.sum())
        if n < 40:
            continue
        ys, xs = np.nonzero(m)
        # count distinct 20px-grid blobs
        b = Counter((int(x // 20), int(y // 20)) for x, y in zip(xs, ys))
        nb = len(b)
        top = sorted(b.values(), reverse=True)[:5]
        print(f"  {tuple(c)} n={n:7d} blobs20={nb:4d} biggest={top} bbox x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}]")


ao, palarr, idxo = classify(ORIG)
ar, palarr2, idxr = classify(REND)
report("ORIGINAL classified", ao, palarr, idxo)
report("RENDER classified", ar, palarr2, idxr)

# cross-tab: fraction of each original color matched in render
print("\n=== cross-tab (orig color -> render color agreement) ===")
for i, c in enumerate(palarr):
    m = idxo == i
    n = int(m.sum())
    if n < 200:
        continue
    rs = Counter(idxr[m].tolist())
    top = rs.most_common(3)
    s = "  ".join(f"{tuple(palarr2[j])}={v*100//n}%" for j, v in top)
    print(f"  {tuple(c)}: {s}")
