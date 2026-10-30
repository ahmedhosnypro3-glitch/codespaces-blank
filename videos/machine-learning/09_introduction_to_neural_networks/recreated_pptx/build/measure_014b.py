#!/usr/bin/env python3
"""Measure slide_014 original frame: main diagram label positions, threshold box,
and equation-panel line geometry. Text-free ink analysis (no image bytes loaded)."""
import numpy as np
from PIL import Image

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_014.jpg"
im = Image.open(SRC).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
print(f"image {W}x{H}  scale = {W/13.33:.2f} px/in (72 dpi nominal)")

# --- color masks -------------------------------------------------------
def mask(pred):
    return np.where(pred(a), 1, 0)

R, G, B = a[..., 0], a[..., 1], a[..., 2]
dark = (R + G + B) < 330
red = (R > 120) & (G < 90) & (B < 90)
green = (R < 120) & (G > 80) & (B < 120)
blue = (B > 120) & (R < 90) & (G < 90)
purple = (R > 170) & (B > 170) & (G > 130) & (G < 200)

def bands(m, x0, y0, x1, y1, label, minpx=1, gap=2):
    prof = m[y0:y1, x0:x1].sum(axis=1)
    runs, inrun = [], False
    for i, v in enumerate(prof):
        if v >= minpx and not inrun:
            inrun, st = True, i
        elif v < minpx and inrun:
            inrun = False
            if i - st >= gap or True:
                runs.append((st + y0, i - 1 + y0, int(prof[st:i].max())))
    if inrun:
        runs.append((st + y0, y1 - 1, int(prof[st:].max())))
    print(f"\n== {label}: bands x[{x0}..{x1}] y[{y0}..{y1}] ==")
    for r in runs:
        print(f"   y[{r[0]}..{r[1]}] h={r[1]-r[0]+1} maxpx={r[2]}")

def cols(m, x0, y0, x1, y1, label, minpx=1):
    prof = m[y0:y1, x0:x1].sum(axis=0)
    runs, inrun = [], False
    for i, v in enumerate(prof):
        if v >= minpx and not inrun:
            inrun, st = True, i
        elif v < minpx and inrun:
            inrun = False
            runs.append((st + x0, i - 1 + x0, int(prof[st:i].max())))
    if inrun:
        runs.append((st + x0, x1 - 1, int(prof[st:].max())))
    print(f"== {label}: cols y[{y0}..{y1}] x[{x0}..{x1}] ==")
    for r in runs:
        print(f"   x[{r[0]}..{r[1]}] w={r[1]-r[0]+1} maxpx={r[2]}")

def bbox(m, x0, y0, x1, y1):
    sub = m[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if not len(ys):
        return None
    return (xs.min() + x0, ys.min() + y0, xs.max() + x0, ys.max() + y0)

# --- 1. Equation panel outer box --------------------------------------
print("\n\n########## EQUATION PANEL ##########")
bands(dark, 82, 300, 596, 500, "panel vertical ink", gap=3)

# --- 2. Equation text line structure (tight) ---------------------------
print("\n\n########## EQUATION LINE TEXT (dark ink) ##########")
for (y0, y1, name) in [(320, 350, "L1 Sum1/Sum2"), (378, 406, "L2 Sum3"),
                        (408, 434, "L3 expand"), (444, 472, "L4 linear"), ]:
    sub = dark[y0:y1, 82:596]
    rows = sub.any(axis=1)
    ys = np.where(rows)[0]
    ytop, ybot = (ys.min() + y0, ys.max() + y0) if len(ys) else (None, None)
    colink = sub.any(axis=0)
    runs, inrun = [], False
    for i, v in enumerate(colink):
        if v and not inrun:
            inrun, st = True, i
        elif not v and inrun:
            inrun = False
            runs.append((st + 82, i - 1 + 82))
    if inrun:
        runs.append((st + 82, 595))
    merged = []
    for r in runs:
        if merged and r[0] - merged[-1][1] <= 7:
            merged[-1] = (merged[-1][0], r[1])
        else:
            merged.append(list(r))
    print(f"\n{name}: ink y[{ytop}..{ybot}] (h={ybot-ytop+1 if ytop else '?'})")
    for m in merged:
        print(f"    x[{m[0]}..{m[1]}] w={m[1]-m[0]+1}")

# --- 3. Main diagram ---------------------------------------------------
print("\n\n########## MAIN DIAGRAM (top-left) ##########")
print("panel dark border:")
bands(dark, 70, 90, 570, 330, "diagram box", gap=3)
cols(dark, 70, 90, 570, 330, "diagram box", minpx=50)

print("\n== w11/w12/w21/w22 label x-extent (dark, hidden-column zone) ==")
cols(dark, 150, 130, 330, 330, "hidden zone", minpx=1)

print("\n== RED pixels (neuron number circles) in diagram ==")
cols(red, 70, 90, 570, 330, "red cols", minpx=3)
bands(red, 70, 90, 570, 330, "red rows", minpx=3)

print("\n== GREEN pixels (w31/w32) in diagram ==")
cols(green, 70, 90, 570, 330, "green cols", minpx=2)
bands(green, 70, 90, 570, 330, "green rows", minpx=2)

# --- 4. Threshold box + O/P -------------------------------------------
print("\n\n########## THRESHOLD BOX / O/P ##########")
pb = bbox(purple, 70, 90, 570, 330)
print(f"purple bbox in diagram region: {pb}")
# search wider for purple
allpb = bbox(purple, 0, 0, W, H)
print(f"purple bbox whole image: {allpb}")
