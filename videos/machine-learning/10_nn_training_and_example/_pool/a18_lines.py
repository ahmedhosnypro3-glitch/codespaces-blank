#!/usr/bin/env python3
"""Per-line, per-color text run extraction for slide 31 (and any slide).

For every detected text line, reports the x-extent of each color's ink, so
text boxes can be placed at measured positions with the original's color coding.
"""
import sys
from PIL import Image
import numpy as np

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides"
PPI = 13.33 / 960


def groups(idx, gap=4):
    idx = sorted(idx)
    out, start, prev = [], None, None
    for v in idx:
        if start is None:
            start = prev = v
        elif v - prev <= gap:
            prev = v
        else:
            out.append((start, prev)); start = prev = v
    if start is not None:
        out.append((start, prev))
    return out


def mask_of(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return {
        "R": (r > 140) & (r - g > 55) & (r - b > 55),
        "B": (b > 130) & (b - r > 45) & (b - g > 25),
        "K": (r < 100) & (g < 100) & (b < 100),
        "G": (g > 105) & (g - r > 30) & (g - b > 30),
    }


def analyze(n, y_lo=0, y_hi=540):
    a = np.asarray(Image.open(f"{BASE}/slide_{n:03d}.jpg").convert("RGB")).astype(int)
    H, W = a.shape[:2]
    masks = mask_of(a)
    ink = np.zeros((H, W), bool)
    for m in masks.values():
        ink |= m
    prof = ink.sum(axis=1)
    print(f"===== SLIDE {n} lines (y {y_lo}..{y_hi}) =====")
    for y0, y1 in groups([y for y in range(int(y_lo), int(y_hi)) if prof[y] >= 2]):
        if y1 - y0 < 3:
            continue
        sub_ink = ink[y0:y1 + 1]
        cc = np.where(sub_ink.any(axis=0))[0]
        # split into word clusters by gap > 10px
        words = []
        ws = None
        for c in range(cc.min(), cc.max() + 2):
            on = c < W and sub_ink[:, c].any() if c < W else False
            if on and ws is None:
                ws = c
            elif not on and ws is not None:
                words.append((ws, c - 1)); ws = None
        parts = []
        for (wx0, wx1) in words:
            cols = [k for k, m in masks.items() if m[y0:y1 + 1, wx0:wx1 + 1].any()]
            parts.append(f"{wx0}-{wx1}{'/' + ''.join(cols) if cols else ''}")
        print(f"y {y0}..{y1} ({y0*PPI:.2f}..{y1*PPI:.2f}in): " + "  ".join(parts))


for a_ in sys.argv[1:]:
    if a_.isdigit():
        analyze(int(a_))
        print()
