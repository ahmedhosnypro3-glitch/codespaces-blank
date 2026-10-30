#!/usr/bin/env python3
"""Row-profile the equation panel text in original vs render to determine
line structure (are Sum 1 and Sum 2 on one line or two?)."""
import numpy as np
from PIL import Image

ORIG = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_014.jpg"
REND = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_014_rendered-1.png"

def profile(path, x0, y0, x1, y1, label, ink_thr=200):
    a = np.asarray(Image.open(path).convert("L")).astype(int)
    sub = a[y0:y1, x0:x1]
    rows = (sub < ink_thr).sum(axis=1)
    print(f"\n########## {label}  x[{x0}..{x1}] y[{y0}..{y1}] ##########")
    bands, inb = [], False
    for i, v in enumerate(rows):
        if v > 0 and not inb:
            inb, st = True, i
        elif v == 0 and inb:
            inb = False
            bands.append((st + y0, i - 1 + y0))
    if inb:
        bands.append((st + y0, y1 - 1))
    for st, en in bands:
        seg = sub[st - y0:en - y0 + 1]
        cols = (seg < ink_thr).sum(axis=0)
        nz = np.where(cols > 0)[0]
        if len(nz):
            print(f"  text band y[{st}..{en}] h={en-st+1}  x[{nz.min()+x0}..{nz.max()+x0}] inkcols={nz.max()-nz.min()+1}")
    # column profile of the whole panel to find horizontal split
    cols = (sub < ink_thr).sum(axis=0)
    print("  column ink density (every 20px):")
    print("   " + " ".join(f"{i+x0}:{c}" for i, c in enumerate(cols[::10]) if c > 0))

# Original equation panel: x[84..300] and x[380..592] from compare_014.py; full panel approx x[60..620] y[316..479]
profile(ORIG, 60, 316, 620, 479, "ORIGINAL equation panel")
profile(REND, 125, 660, 1290, 1000, "RENDER equation panel (scaled x2.0865)")
