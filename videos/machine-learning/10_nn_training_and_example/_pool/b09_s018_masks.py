#!/usr/bin/env python3
"""b09 s018: masked-feature geometry, original vs render (960x540 space)."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/"

def load(p):
    im = Image.open(NS + p).convert("RGB")
    if im.size != (960, 540):
        im = im.resize((960, 540), Image.LANCZOS)
    return np.asarray(im).astype(np.int16)

o = load("unique_slides/slide_018.jpg")
r = load("qa/slide018/rejudge/attempt2/render-1.png")

def mask(a, lo, hi, reg):
    x0, y0, x1, y1 = reg
    sub = a[y0:y1, x0:x1]
    m = np.ones(sub.shape[:2], bool)
    for i, (l, h) in enumerate(zip(lo, hi)):
        m &= (sub[:, :, i] >= l) & (sub[:, :, i] <= h)
    return m, (x0, y0)

def comps(m, off, minsize=6):
    """coarse bbox via row/col projection (objects are separated here)."""
    x0, y0 = off
    if not m.any():
        return []
    ys, xs = np.nonzero(m)
    return [(x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max(), int(m.sum()))]

def report(name, lo, hi, reg):
    mo = comps(*mask(o, lo, hi, reg))
    mr = comps(*mask(r, lo, hi, reg))
    print(f"{name:22s} orig={mo}\n{'':22s} rnd ={mr}")

RED = ([140, 0, 0], [255, 100, 90])
BLUE = ([0, 0, 130], [90, 90, 255])
GREEN = ([140, 210, 140], [210, 255, 210])
ORANGE = ([240, 220, 150], [255, 255, 220])
PINK = ([200, 150, 200], [255, 210, 240])
MAROON = ([120, 20, 20], [190, 70, 70])
CREAM = ([230, 215, 200], [255, 245, 230])

print("== whole-slide bboxes by mask ==")
ALL = (0, 0, 960, 540)
report("red (all)", *RED, ALL)
report("blue text", *BLUE, ALL)
report("green sigma", *GREEN, ALL)
report("orange sigbox", *ORANGE, ALL)
report("pink box", *PINK, ALL)
report("maroon border", *MAROON, ALL)
report("cream panel fill", *CREAM, ALL)

print("\n== diagram band only (x360..750, y50..215) ==")
D = (360, 50, 750, 215)
report("red", *RED, D)
report("green sigma", *GREEN, D)
report("orange sigbox", *ORANGE, D)
report("pink box", *PINK, D)
report("maroon border", *MAROON, D)

print("\n== output-label column (x740..800, y50..215) ==")
report("dark ink", [0, 0, 0], [110, 110, 110], (740, 50, 800, 215))

print("\n== error bar (x745..800, y50..215) ==")
report("red", *RED, (745, 50, 800, 215))

print("\n== class column (x790..845, y50..215) ==")
report("dark ink", [0, 0, 0], [110, 110, 110], (790, 50, 845, 215))

print("\n== eq + q (x820..905, y95..160) ==")
EQ = (820, 95, 905, 160)
report("red q", *RED, EQ)
report("black eq", [0, 0, 0], [100, 100, 100], (822, 100, 870, 158))
