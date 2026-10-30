#!/usr/bin/env python3
"""Forensic read of slide_014 original: ASCII-art crops so text/lines can be read
without loading image bytes into the model context."""
import numpy as np
from PIL import Image

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_014.jpg"
im = Image.open(SRC).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]


def ascii_region(x0, y0, x1, y1, cols=150, label=""):
    crop = im.crop((x0, y0, x1, y1)).convert("L")
    w, h = crop.size
    step = max(1, w // cols)
    cw, ch = w // step, h // max(1, step // 2)
    small = crop.resize((cols, max(1, h // max(1, step // 2))), Image.LANCZOS)
    arr = np.asarray(small)
    chars = " .:-=+*#%@"
    print(f"\n--- {label}  src x[{x0}..{x1}] y[{y0}..{y1}] ({(x1-x0)}x{(y1-y0)}px) ---")
    for row in arr:
        print("".join(chars[min(int(v) * len(chars) // 256, len(chars) - 1)] for v in row))


def ink_profile(x0, y0, x1, y1, label, thr=330, minpx=2):
    band = (a[y0:y1, x0:x1].sum(axis=2) < thr)
    prof = band.sum(axis=1)
    runs = []
    inrun = False
    for i, v in enumerate(prof):
        if v >= minpx and not inrun:
            inrun, st = True, i
        elif v < minpx and inrun:
            inrun = False
            runs.append((st + y0, i - 1 + y0, int(prof[st:i].max())))
    if inrun:
        runs.append((st + y0, y1 - 1, int(prof[st:].max())))
    print(f"\n== ink bands {label} (x{x0}..{x1}) ==")
    for r in runs:
        print(f"   y[{r[0]}..{r[1]}] h={r[1]-r[0]+1} maxpx={r[2]}")


def col_profile(x0, y0, x1, y1, label, thr=330, minpx=2):
    band = (a[y0:y1, x0:x1].sum(axis=2) < thr)
    prof = band.sum(axis=0)
    runs = []
    inrun = False
    for i, v in enumerate(prof):
        if v >= minpx and not inrun:
            inrun, st = True, i
        elif v < minpx and inrun:
            inrun = False
            runs.append((st + x0, i - 1 + x0, int(prof[st:i].max())))
    if inrun:
        runs.append((st + x0, x1 - 1, int(prof[st:].max())))
    print(f"\n== ink columns {label} (y{y0}..{y1}) ==")
    for r in runs:
        print(f"   x[{r[0]}..{r[1]}] w={r[1]-r[0]+1} maxpx={r[2]}")


print("=== EQUATION PANEL region x[82..595] y[316..479] ===")
ascii_region(82, 316, 596, 480, cols=150, label="equation panel full")
ink_profile(82, 316, 596, 480, "equation panel")
ink_profile(82, 316, 340, 480, "equation panel LEFT HALF")
ink_profile(340, 316, 596, 480, "equation panel RIGHT HALF")

print("\n\n=== MAIN DIAGRAM region x[85..551] y[102..302] ===")
ascii_region(85, 102, 552, 303, cols=150, label="main diagram full")
