#!/usr/bin/env python3
"""Per-column vertical runs for the 050 augmented-table paren strokes."""
import numpy as np
from PIL import Image

NS = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
o = np.asarray(Image.open(NS + "/unique_slides/slide_050.jpg").convert("RGB")).astype(int)
lum = o.mean(axis=2)
ink = lum < 190

COLS = [93, 107, 115, 128, 137, 150, 151, 159, 173, 182, 196, 205, 218]
for c in COLS:
    for cc in (c,):
        col = ink[170:235, cc]
        ys = np.where(col)[0]
        if len(ys) == 0:
            print("x%d: none" % cc); continue
        runs, s, p = [], ys[0], ys[0]
        for y in ys[1:]:
            if y - p > 2:
                runs.append((s+170, p+170)); s = y
            p = y
        runs.append((s+170, p+170))
        runs = [(a, b) for a, b in runs if b - a >= 5]
        print("x%d: runs>=5px: %s" % (cc, runs))
