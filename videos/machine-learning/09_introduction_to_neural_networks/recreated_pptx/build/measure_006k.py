#!/usr/bin/env python3
"""Full inventory of colored elements in the diagram panel of the original."""
from PIL import Image
import numpy as np
from scipy import ndimage
from pathlib import Path

V = Path("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks")
a = np.array(Image.open(V / "unique_slides/slide_006.jpg").convert("RGB")).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

REG = (slice(140, 500), slice(420, 900))


def inv(name, m, min_area=10):
    mm = np.zeros_like(m)
    mm[REG] = m[REG]
    lab, n = ndimage.label(mm, structure=np.ones((3, 3)))
    got = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < min_area:
            continue
        got.append((xs.min(), ys.min(), xs.max(), ys.max(), len(ys)))
    got.sort(key=lambda t: (t[1], t[0]))
    print(f"\n== {name}: {len(got)} components (area>={min_area}) ==")
    for g in got:
        print(f"   x {g[0]:4d}-{g[2]:4d} y {g[1]:4d}-{g[3]:4d} w{g[2]-g[0]+1:3d} h{g[3]-g[1]+1:3d} area{g[4]:4d}")
    return got


inv("RED (chroma R-G>16, R-B>16)", (R - G > 16) & (R - B > 16) & (R > 120))
inv("BLUE (chroma B-R>18)", (B - R > 18) & (B - G > 14) & (B > 120))
inv("GREEN (chroma G-R>14, G-B>14)", (G - R > 14) & (G - B > 14) & (G > 110))
