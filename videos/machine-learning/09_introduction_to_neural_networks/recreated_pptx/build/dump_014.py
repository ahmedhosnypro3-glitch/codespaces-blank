#!/usr/bin/env python3
"""1:1 pixel ASCII dumps of slide_014 regions (no image bytes into context)."""
import sys
import numpy as np
from PIL import Image

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_014.jpg"
im = Image.open(SRC).convert("L")

def dump(x0, y0, x1, y1, thr=190, label=""):
    crop = np.asarray(im.crop((x0, y0, x1, y1))).astype(int)
    h, w = crop.shape
    print(f"\n--- {label}  x[{x0}..{x1}] y[{y0}..{y1}]  {w}x{h} thr={thr} ---")
    print("     " + "".join(str((x0 + i) // 100 % 10) for i in range(w)))
    print("     " + "".join(str((x0 + i) // 10 % 10) for i in range(w)))
    print("     " + "".join(str((x0 + i) % 10) for i in range(w)))
    for j, r in enumerate(crop):
        print(f"{y0+j:4d} " + "".join("#" if v < thr else ("+" if v < 235 else ".") for v in r))

def runs_x(x0, y0, x1, y1, thr=200, gap=5, label=""):
    crop = np.asarray(im.crop((x0, y0, x1, y1))).astype(int)
    ink = crop < thr
    colink = ink.any(axis=0)
    out, inr = [], False
    for i, v in enumerate(colink):
        if v and not inr:
            inr, st = True, i
        elif not v and inr:
            inr = False
            out.append((st + x0, i - 1 + x0))
    if inr:
        out.append((st + x0, x1 - 1))
    merged = []
    for r in out:
        if merged and r[0] - merged[-1][1] <= gap:
            merged[-1] = (merged[-1][0], r[1])
        else:
            merged.append(list(r))
    ys = np.where(ink.any(axis=1))[0]
    print(f"\n== {label}: y[{y0}..{y1}] ink y[{ys.min()+y0}..{ys.max()+y0}] (h={ys.max()-ys.min()+1})")
    for m in merged:
        print(f"    x[{m[0]}..{m[1]}] w={m[1]-m[0]+1}")

if __name__ == "__main__":
    what = sys.argv[1]
    if what == "thr":
        dump(410, 160, 545, 245, thr=190, label="threshold box + O/P (1:1)")
    elif what == "w":
        dump(150, 120, 290, 215, thr=190, label="w11/w12 zone (1:1)")
    elif what == "w2":
        dump(150, 200, 290, 300, thr=190, label="w21/w22 zone (1:1)")
