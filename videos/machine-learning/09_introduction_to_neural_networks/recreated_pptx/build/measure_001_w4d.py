#!/usr/bin/env python3
"""slide_001 w4: column-gap profile of the original subtitle + left-stack edges."""
import numpy as np
from PIL import Image

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"


def col_profile(path, sx, sy, y0, y1, x0, x1, label):
    a = np.asarray(Image.open(path).convert("RGB")).astype(float)
    reg = a[int(y0 * sy):int(y1 * sy), int(x0 * sx):int(x1 * sx)]
    L = 0.299 * reg[:, :, 0] + 0.587 * reg[:, :, 1] + 0.114 * reg[:, :, 2]
    ink = L < 175
    col = ink.sum(axis=0)
    runs, inb = [], False
    for i in range(len(col)):
        if col[i] > 0 and not inb:
            st, inb = i, True
        elif col[i] == 0 and inb:
            runs.append((st, i - 1))
            inb = False
    if inb:
        runs.append((st, len(col) - 1))
    print("### %s   x window %.2f-%.2f in" % (label, x0, x1))
    print("    ink runs (in): " + " ".join("%.2f-%.2f" % ((x0 + s) / sx, (x0 + e + 1) / sx) for s, e in runs))
    gaps = [(runs[i + 1][0] - runs[i][1] - 1) / sx for i in range(len(runs) - 1)]
    print("    gaps (in):     " + " ".join("%.3f" % g for g in gaps))
    # left ink edge per row-band
    print()


ORIG = f"{V}/unique_slides/slide_001.jpg"
REND = f"{V}/recreated_pptx/build/slide_001_rendered-1.png"
col_profile(ORIG, 72.0, 518 / 7.5, 3.95, 4.35, 4.0, 9.2, "ORIGINAL subtitle 'CSAI 253 - Spring 2024'")
col_profile(REND, 150.0, 150.0, 1.60, 2.00, 4.0, 9.2, "RENDER subtitle")
col_profile(ORIG, 72.0, 518 / 7.5, 5.84, 6.10, 0.5, 3.2, "ORIGINAL 'Instructors:'")
col_profile(ORIG, 72.0, 518 / 7.5, 6.22, 6.54, 0.5, 5.5, "ORIGINAL list name1")
col_profile(REND, 150.0, 150.0, 4.10, 4.35, 0.5, 3.2, "RENDER 'Instructors:'")
col_profile(REND, 150.0, 150.0, 4.50, 4.82, 0.5, 5.5, "RENDER list name1")
