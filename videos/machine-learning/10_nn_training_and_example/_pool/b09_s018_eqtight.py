#!/usr/bin/env python3
"""b09 s018: tight eq ink bbox at several thresholds, both sides."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/"

def load(p):
    im = Image.open(NS + p).convert("RGB")
    if im.size != (960, 540):
        im = im.resize((960, 540), Image.LANCZOS)
    return np.asarray(im).astype(np.int16).sum(2)

oe, re = load("unique_slides/slide_018.jpg"), load("qa/slide018/rejudge/attempt2/render-1.png")

def tight(img, reg, thr, minfrac=0.55):
    x0, y0, x1, y1 = reg
    sub = img[y0:y1, x0:x1]
    rows = (sub < thr).sum(1)
    cols = (sub < thr).sum(0)
    ry = [i for i, v in enumerate(rows) if v > 0]
    cx = [i for i, v in enumerate(cols) if v > 0]
    return (x0 + cx[0], y0 + ry[0], x0 + cx[-1], y0 + ry[-1]) if (ry and cx) else None

REG = (822, 100, 908, 155)
for thr in (520, 560, 620, 700):
    print(f"thr={thr}")
    print("  orig  ", tight(oe, REG, thr))
    print("  render", tight(re, REG, thr))

# per-side glyph extents excluding the '?' (x>=872)
for thr in (520, 560, 620):
    print(f"\n--- thr={thr}: eq-only region x822..870 ---")
    print("  orig  ", tight(oe, (822, 100, 872, 155), thr))
    print("  render", tight(re, (822, 100, 872, 155), thr))
    print(f"--- thr={thr}: question-mark region x872..905 ---")
    print("  orig  ", tight(oe, (872, 100, 905, 155), thr))
    print("  render", tight(re, (872, 100, 905, 155), thr))
