#!/usr/bin/env python3
"""Binary-ink ASCII dumps of slide_014 regions so text/lines are readable
without loading image bytes into the model context."""
import numpy as np
from PIL import Image

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_014.jpg"
im = Image.open(SRC).convert("RGB")

def dump(x0, y0, x1, y1, cols=120, thr=190, sx=2, sy=2, label=""):
    crop = im.crop((x0, y0, x1, y1)).convert("L")
    w, h = crop.size
    nx = cols
    ny = max(1, int(h * (cols / w) * (sx / sy) * 0.5))
    small = crop.resize((nx, ny), Image.LANCZOS)
    arr = np.asarray(small).astype(int)
    print(f"\n--- {label}  src x[{x0}..{x1}] y[{y0}..{y1}]  {nx}x{ny} thr={thr} ---")
    print("    " + "".join(str((x0 + int(i * (x1 - x0) / nx)) // 100 % 10) for i in range(nx)))
    print("    " + "".join(str((x0 + int(i * (x1 - x0) / nx)) // 10 % 10) for i in range(nx)))
    for r in arr:
        print("    " + "".join("#" if v < thr else ("+" if v < 230 else ".") for v in r))

def ink_runs_x(x0, y0, x1, y1, thr=200, gap=8, label=""):
    crop = np.asarray(im.crop((x0, y0, x1, y1)).convert("L")).astype(int)
    ink = crop < thr
    colink = ink.any(axis=0)
    runs, inrun = [], False
    for i, v in enumerate(colink):
        if v and not inrun:
            inrun, st = True, i
        elif not v and inrun:
            inrun = False
            runs.append((st + x0, i - 1 + x0))
    if inrun:
        runs.append((st + x0, x1 - 1))
    merged = []
    for r in runs:
        if merged and r[0] - merged[-1][1] <= gap:
            merged[-1] = (merged[-1][0], r[1])
        else:
            merged.append(list(r))
    rows = ink.any(axis=1)
    ys = np.where(rows)[0]
    print(f"\n== {label}: x[{x0}..{x1}] y[{y0}..{y1}] ink y[{ys.min()+y0}..{ys.max()+y0}]")
    for m in merged:
        print(f"    x[{m[0]}..{m[1]}] w={m[1]-m[0]+1}")

# ---- 1. Threshold box + O/P region (main diagram, right side) ----
dump(400, 170, 570, 260, cols=130, thr=190, label="threshold box + O/P (main diagram)")
ink_runs_x(400, 170, 570, 260, thr=200, gap=6, label="threshold+OP rows split")
for (y0,y1,nm) in [(178,196,"row A"),(196,214,"row B"),(214,232,"row C")]:
    ink_runs_x(400, y0, 570, y1, thr=200, gap=5, label=f"threshold {nm}")

# ---- 2. full main diagram ----
dump(85, 100, 555, 305, cols=150, thr=190, label="main diagram full")
