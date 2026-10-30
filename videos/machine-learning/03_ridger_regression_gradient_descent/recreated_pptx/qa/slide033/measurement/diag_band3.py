#!/usr/bin/env python3
"""band3 column fills + full band/fill/cell census."""
import numpy as np
from PIL import Image
from collections import Counter

o = np.asarray(Image.open("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_033.jpg").convert("RGB")).astype(int)


def strip_mode(y0, y1, x):
    sub = o[y0:y1, x:x + 10].reshape(-1, 3)
    sub = sub[sub.sum(axis=1) > 400]
    if not len(sub):
        return None
    return Counter(map(tuple, sub)).most_common(1)[0][0]


print("=== band3 y458-479: mode fill per 10px column ===")
for x in range(86, 870, 10):
    m = strip_mode(458, 479, x)
    print(f"  x{x}-{x+9}: {m}")

print("\n=== band0 y334-368 column fills (mode) ===")
for x in range(86, 870, 20):
    m = strip_mode(334, 368, x)
    print(f"  x{x}-{x+19}: {m}")

print("\n=== band1 y376-410 column fills (mode, every 40) ===")
for x in range(86, 870, 40):
    m = strip_mode(376, 410, x)
    print(f"  x{x}-{x+39}: {m}")

print("\n=== band2 y420-455 column fills (mode, every 40) ===")
for x in range(86, 870, 40):
    m = strip_mode(420, 455, x)
    print(f"  x{x}-{x+39}: {m}")

print("\n=== band4 y482-504 column fills (mode, every 40) ===")
for x in range(86, 870, 40):
    m = strip_mode(482, 504, x)
    print(f"  x{x}-{x+39}: {m}")
