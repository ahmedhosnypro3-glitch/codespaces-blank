#!/usr/bin/env python3
"""Slide 041: resolve the left-table structure.

Prints per-column vertical ink profiles for the tall strokes so we can tell
math-engine parentheses (curved, span both rows) from digit "1" glyphs
(straight, present in each row separately).
"""
import numpy as np
from PIL import Image

IM = Image.open("/worksp" + "aces/codespaces-blank/ai_llm_slides/videos/"
               "machine-learning/03_ridger_regression_gradient_descent/"
               "unique_slides/slide_041.jpg").convert("RGB")
A = np.asarray(IM).astype(int)
FILL = np.array([255, 247, 224])
INK = np.abs(A - FILL[None, None, :]).sum(axis=2) > 90

print("=== column ink profiles, left table x85..220, y76..108 ===")
for x in range(85, 221):
    col = INK[76:109, x]
    if not col.any():
        continue
    ys = np.where(col)[0] + 76
    # contiguous runs
    runs, s = [], ys[0]
    for i in range(1, len(ys)):
        if ys[i] != ys[i - 1] + 1:
            runs.append((s, ys[i - 1])); s = ys[i]
    runs.append((s, ys[-1]))
    print("x%3d n=%2d runs=%s" % (x, col.sum(), runs))

print("\n=== row profiles (count of ink per row) x85..220 ===")
for y in range(60, 128):
    n = INK[y, 85:221].sum()
    if n:
        print("y%3d n=%2d" % (y, n))

print("\n=== right matrix column profiles x594..660, y62..112 ===")
for x in range(594, 661):
    col = INK[62:113, x]
    if not col.any():
        continue
    ys = np.where(col)[0] + 62
    runs, s = [], ys[0]
    for i in range(1, len(ys)):
        if ys[i] != ys[i - 1] + 1:
            runs.append((s, ys[i - 1])); s = ys[i]
    runs.append((s, ys[-1]))
    print("x%3d n=%2d runs=%s" % (x, col.sum(), runs))
