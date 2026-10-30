#!/usr/bin/env python3
"""Sibling-frame bottom-bar check + precise slide_023 box extents."""
import numpy as np
from PIL import Image

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/"

print("== bottom-bar comparison across sibling frames ==")
for n in [1, 5, 9, 13, 17, 21, 22, 23, 24, 26, 30, 32]:
    p = f"{BASE}slide_{n:03d}.jpg"
    a = np.asarray(Image.open(p).convert("RGB")).astype(int)
    H, W, _ = a.shape
    # find first row (from bottom) where mean < 40
    firstdark = None
    for y in range(H - 1, 0, -1):
        if a[y].mean() < 40:
            firstdark = y
        elif firstdark is not None:
            break
    # width of dark region at row H-5
    darkfrac = (a[H - 5].mean(axis=1) < 40).mean()
    print(f"  slide_{n:03d}: H={H} black bar starts y={firstdark} "
          f"(height {H-firstdark if firstdark else 0}), dark width frac at bottom={darkfrac:.2f}")
