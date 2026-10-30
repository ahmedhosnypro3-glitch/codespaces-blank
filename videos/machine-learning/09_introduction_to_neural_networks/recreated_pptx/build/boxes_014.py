#!/usr/bin/env python3
"""Locate the three panel boxes in slide_014 original (960x540) + render (2001x1125)."""
import sys
import numpy as np
from PIL import Image

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"


def boxes(path, label, px_per_in):
    a = np.asarray(Image.open(path).convert("RGB")).astype(int)
    H, W = a.shape[:2]
    mx = a.max(axis=2)
    mn = a.min(axis=2)
    dark = mx < 215
    red = (a[..., 0] > a[..., 1] + 45) & (a[..., 0] > a[..., 2] + 45) & (a[..., 0] > 100) & dark
    print(f"\n########## {label}  {W}x{H}  {px_per_in:.2f} px/in ##########")

    def hlines(mask, minlen_frac=0.10):
        rows = mask.sum(axis=1)
        out = []
        inr = False
        thr = W * minlen_frac
        for i, v in enumerate(rows):
            if v >= thr and not inr:
                inr, st = True, i
            elif v < thr and inr:
                inr = False
                out.append((st, i - 1, int(rows[st:i].max())))
        if inr:
            out.append((st, H - 1, int(rows[st:].max())))
        return out

    def vlines(mask, minlen_frac=0.06):
        cols = mask.sum(axis=0)
        out = []
        inr = False
        thr = H * minlen_frac
        for i, v in enumerate(cols):
            if v >= thr and not inr:
                inr, st = True, i
            elif v < thr and inr:
                inr = False
                out.append((st, i - 1, int(cols[st:i].max())))
        if inr:
            out.append((st, W - 1, int(cols[st:].max())))
        return out

    print("DARK horizontal runs (>=10% width):")
    for r in hlines(dark, 0.10):
        print(f"   y[{r[0]}..{r[1]}] maxlen={r[2]}")
    print("DARK vertical runs (>=6% height):")
    for c in vlines(dark, 0.06):
        print(f"   x[{c[0]}..{c[1]}] maxlen={c[2]}")
    print("RED horizontal runs (>=10% width):")
    for r in hlines(red, 0.10):
        print(f"   y[{r[0]}..{r[1]}] maxlen={r[2]}")
    print("RED vertical runs (>=6% height):")
    for c in vlines(red, 0.06):
        print(f"   x[{c[0]}..{c[1]}] maxlen={c[2]}")

    # white-panel interiors: find large rectangles of near-white
    white = (mn > 235)
    print("WHITE fill horizontal runs (>=15% width):")
    for r in hlines(white, 0.15):
        print(f"   y[{r[0]}..{r[1]}] maxlen={r[2]}")
    return a


if __name__ == "__main__":
    boxes(f"{BASE}/unique_slides/slide_014.jpg", "ORIGINAL", 72.017)
    boxes(f"{BASE}/recreated_pptx/build/slide_014_rendered-1.png", "RENDER", 150.075)
