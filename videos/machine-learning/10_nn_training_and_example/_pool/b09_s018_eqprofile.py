#!/usr/bin/env python3
"""b09 s018: row/col ink profiles in the equation zone, both sides."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/"

def load(p):
    im = Image.open(NS + p).convert("RGB")
    if im.size != (960, 540):
        im = im.resize((960, 540), Image.LANCZOS)
    return np.asarray(im).astype(np.int16).sum(2)

oe, re = load("unique_slides/slide_018.jpg"), load("qa/slide018/rejudge/attempt2/render-1.png")
REG = (820, 80, 912, 182)

def profile(img, name):
    x0, y0, x1, y1 = REG
    print(f"\n== {name}: region {REG} ==")
    print("row  ink(<=520)  ink(<=700)")
    for y in range(y0, y1, 2):
        sub = img[y, x0:x1]
        print(f"{y:4d} {int((sub<=520).sum()):5d} {int((sub<=700).sum()):5d}")
    print("col  ink(<=520)")
    cols = {}
    for x in range(x0, x1, 2):
        c = img[y0:y1, x]
        cols[x] = int((c <= 520).sum())
    print("  ".join(f"{x}:{n}" for x, n in cols.items() if n > 2))

profile(oe, "ORIGINAL")
profile(re, "RENDER")

print("\n== render eq ASCII (x826..900 y100..140, step1, thr 650) ==")
for y in range(100, 140, 1):
    print(f"{y:4d} " + "".join("#" if re[y, x] < 400 else ("+" if re[y, x] < 650 else ".")
                               for x in range(826, 900, 2)))
