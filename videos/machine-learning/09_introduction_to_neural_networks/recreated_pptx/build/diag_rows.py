#!/usr/bin/env python3
"""Row color-run profiles at box centers for slide_023."""
import numpy as np
from PIL import Image

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_023.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
H, W, _ = a.shape


def hexc(c):
    return f"#{c[0]:02X}{c[1]:02X}{c[2]:02X}"


def profile(y, label):
    row = a[y]
    print(f"\n--- row y={y} ({label}) ---")
    runs = []
    start = 0
    for x in range(1, W):
        if not np.array_equal(row[x], row[x - 1]):
            if x - start >= 2:
                runs.append((start, x - 1, tuple(row[start])))
            start = x
    runs.append((start, W - 1, tuple(row[start])))
    # merge runs with near-identical color (tolerance 12)
    merged = []
    for r in runs:
        if merged and np.abs(np.array(r[2]) - np.array(merged[-1][2])).max() <= 12 and r[0] - merged[-1][1] <= 3:
            merged[-1] = (merged[-1][0], r[1], r[2])
        else:
            merged.append(list(r) if False else (r[0], r[1], r[2]))
    for x0, x1, c in merged:
        print(f"   x={x0}..{x1} (w={x1-x0+1}) {hexc(c)}")


for y, lab in [
    (118, "above inner frame top"),
    (160, "row1 mid-left (peach?)"),
    (168, "row1 mid center+right"),
    (180, "row1 lower"),
    (240, "row2 peach"),
    (255, "row2 right"),
    (320, "row3"),
    (400, "row4"),
    (475, "row5"),
    (500, "row5 lower / frame"),
    (510, "violet frame bottom?")
]:
    profile(y, lab)
