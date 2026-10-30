#!/usr/bin/env python3
"""Run-length scan at exact node-row centres of the slide-019 diagram (a11)."""
import sys
import numpy as np
from PIL import Image

img = Image.open(sys.argv[1]).convert("RGB")
a = np.asarray(img).astype(int)
H, W, _ = a.shape
sc = W / 13.333
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
istam = (r > 170) & (g > 155) & (b < r) & ((r - b) < 95)
iswh = (r > 228) & (g > 228) & (b > 218)
ink = ~(istam | iswh)

for yin in [1.42, 2.02, 2.68, 2.99, 3.05]:
    print(f"-- y={yin}")
    for dy in (-0.03, 0.0, 0.03):
        y = int((yin + dy) * sc)
        row = ink[y, int(5.3 * sc):int(12.9 * sc)]
        runs = []
        i = 0
        while i < len(row):
            if row[i]:
                j = i
                while j < len(row) and row[j]:
                    j += 1
                runs.append((5.3 + i / sc, 5.3 + j / sc))
                i = j
            else:
                i += 1
        print(f"   dy={dy:+.2f}: " + " ".join(f"[{p:.2f},{q:.2f}]" for p, q in runs))
