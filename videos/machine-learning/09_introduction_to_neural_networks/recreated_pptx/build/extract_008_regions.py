#!/usr/bin/env python3
"""Extract the measured class-region tint lattice inside the slide_008 panel.

Centroids measured by sampling the original frame. Outputs a label array the
graph generator renders from, so the recreated shading matches the original
region-for-region instead of being re-derived from an assumed classifier.
"""
import numpy as np
from PIL import Image

P = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_008.jpg"
OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_008_regions.npy"

a = np.asarray(Image.open(P).convert("RGB")).astype(float)
PX0, PX1, PY0, PY1 = 167, 798, 120, 505

# measured tint centroids (from sample_008_tints.py)
C = np.array([
    [255, 255, 255],   # 0 white
    [220, 248, 213],   # 1 pale green
    [196, 194, 240],   # 2 pale lavender
    [251, 219, 225],   # 3 pale pink
    [231, 231, 231],   # 4 grey
])
NAMES = ["white", "green", "lavend", "pink", "grey"]

panel = a[PY0:PY1 + 1, PX0:PX1 + 1, :]
d = ((panel[:, :, None, :] - C[None, None, :, :]) ** 2).sum(axis=3)
lab = d.argmin(axis=2).astype(np.uint8)

# drop the border ring so only the interior is classified
lab[0:3, :] = 255; lab[-3:, :] = 255
lab[:, 0:3] = 255; lab[:, -3:] = 255

np.save(OUT, lab)
print("saved", OUT, lab.shape, lab.dtype)
for i, n in enumerate(NAMES):
    print(f"  {n:7s} {(lab == i).sum()} px")

print()
print("=== x-intervals of each tint family, every 12 rows ===")
for y in range(12, panel.shape[0], 12):
    row = lab[y]
    parts = []
    for i, n in enumerate(NAMES):
        xs = np.where(row == i)[0]
        if len(xs) == 0:
            continue
        # contiguous runs
        runs = []
        s = p = xs[0]
        for v in xs[1:]:
            if v == p + 1:
                p = v
            else:
                runs.append((s, p)); s = p = v
        runs.append((s, p))
        rr = " ".join(f"{r[0]}-{r[1]}" for r in runs if r[1] - r[0] > 8)
        if rr:
            parts.append(f"{n[:1].upper()}:{rr}")
    print(f" y={y:3d}  " + "  ".join(parts))
