#!/usr/bin/env python3
"""b09 s018: closed-loop check of the fixed render vs original (960x540 space)."""
import sys
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/"
RND = sys.argv[1] if len(sys.argv) > 1 else "qa/slide018/attempt4/render-1.png"

def load(p):
    im = Image.open(NS + p).convert("RGB")
    if im.size != (960, 540):
        im = im.resize((960, 540), Image.LANCZOS)
    a = np.asarray(im).astype(np.int16)
    return a, a.sum(2)

o, oe = load("unique_slides/slide_018.jpg")
r, re_ = load(RND)

def bbox(img, reg, thr):
    x0, y0, x1, y1 = reg
    m = img[y0:y1, x0:x1] < thr
    if not m.any():
        return None
    ys, xs = np.nonzero(m)
    return (int(x0 + xs.min()), int(y0 + ys.min()), int(x0 + xs.max()), int(y0 + ys.max()))

CHECKS = [
    ("black equation", (822, 100, 871, 158), 520),
    ("red question", (871, 100, 905, 158), 520),
    ("class column", (790, 50, 846, 215), 560),
    ("error bar red", (750, 50, 778, 215), 520),
    ("output labels", (700, 50, 745, 215), 560),
    ("bottom magenta", (360, 180, 620, 212), 560),
    ("input label", (355, 183, 412, 205), 560),
    ("diagram band", (360, 50, 750, 215), 560),
]

print(f"render = {RND}")
print(f"{'region':16s} {'orig bbox':26s} {'render bbox':26s} {'dx0':>4s} {'dx1':>4s} {'dy0':>4s} {'dy1':>4s}")
worst = 0
for name, reg, thr in CHECKS:
    bo, br = bbox(oe, reg, thr), bbox(re_, reg, thr)
    if not bo or not br:
        print(f"{name:16s} orig={bo} render={br} (empty side)")
        continue
    d = (bo[0] - br[0], bo[2] - br[2], bo[1] - br[1], bo[3] - br[3])
    worst = max(worst, max(abs(v) for v in d))
    flag = "" if max(abs(v) for v in d) <= 4 else "  <-- OVER 4px"
    print(f"{name:16s} {str(bo):26s} {str(br):26s} {d[0]:4d} {d[1]:4d} {d[2]:4d} {d[3]:4d}{flag}")
print(f"\nworst edge delta = {worst} px (960-space; 150dpi 4px tolerance)")

print("\n== eq symbol check on the fixed render ==")
for y in range(100, 155, 2):
    print(f"{y:4d} " + "".join("#" if re_[y, x] < 430 else ("+" if re_[y, x] < 620 else ".")
                               for x in range(828, 892, 1)))
