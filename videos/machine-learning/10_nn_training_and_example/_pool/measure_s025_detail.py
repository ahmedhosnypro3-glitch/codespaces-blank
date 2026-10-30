#!/usr/bin/env python3
"""Fine detail: error-bar text, bias icon, left box fills/borders, headers."""
import numpy as np
from PIL import Image

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides"
img = Image.open(f"{BASE}/slide_025.jpg").convert("RGB")
a = np.asarray(img).astype(int)

print("=== error bar interior (x 838..862, y 130..285) ===")
for y in range(130, 286, 8):
    s = " ".join(f"{tuple(a[y,x])}" for x in (844, 848, 852))
    print(f"  y={y}: {s}")

print("\n=== 'Error' text rows: non-red pixels inside bar x842-857 ===")
for y in range(130, 284):
    row = a[y, 842:858]
    nonred = [(x + 842, tuple(row[x])) for x in range(16)
              if not (row[x][0] > 140 and row[x][0] - row[x][1] > 45 and row[x][0] - row[x][2] > 45)]
    if len(nonred) >= 3:
        print(f"  y={y}: {nonred[:5]}")

print("\n=== left boxes: dominant color per row (x 70..280) ===")
for y in range(160, 312, 4):
    seg = a[y, 70:280]
    mean = seg.mean(axis=0).astype(int)
    print(f"  y={y}: mean {tuple(mean)}")

print("\n=== box borders: vertical scan at x=60,100,280 ===")
for x in (60, 100, 280):
    print(f"  --x={x}")
    for y in range(165, 306, 6):
        print(f"     y={y}: {tuple(a[y,x])}")
