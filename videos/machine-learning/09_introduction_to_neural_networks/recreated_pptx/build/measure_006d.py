#!/usr/bin/env python3
"""Blob finder for slide 006 original: every saturated-color component + bbox."""
from PIL import Image
import numpy as np
from scipy import ndimage
from pathlib import Path

V = Path("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks")
a = np.array(Image.open(V / "unique_slides/slide_006.jpg").convert("RGB")).astype(int)


def blobs(pred, region, label, min_area=10, max_n=40):
    x0, y0, x1, y1 = region
    sub = pred[y0:y1, x0:x1]
    lab, n = ndimage.label(sub, structure=np.ones((3, 3)))
    out = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < min_area:
            continue
        col = a[y0:y1, x0:x1][lab == i].mean(axis=0).round().astype(int)
        out.append((x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max(), len(ys), tuple(col)))
    out.sort(key=lambda t: (t[1], t[0]))
    print(f"\n== {label} ({len(out)} blobs, area>={min_area}) ==")
    for b in out[:max_n]:
        print(f"   x {b[0]:4d}-{b[2]:4d} y {b[1]:4d}-{b[3]:4d} w{b[2]-b[0]+1:3d} h{b[3]-b[1]+1:3d} area{b[4]:5d} rgb{b[5]}")
    return out


def close(rgb, tol):
    return np.abs(a - np.array(rgb)).sum(axis=2) <= tol


red = close((204, 0, 0), 190) & (a[:, :, 0] > 120) & (a[:, :, 1] < 110) & (a[:, :, 2] < 110)
blue = close((26, 52, 200), 150) & (a[:, :, 2] > 120) & (a[:, :, 0] < 130)
green = close((0, 166, 0), 170) & (a[:, :, 1] > 90) & (a[:, :, 0] < 110) & (a[:, :, 2] < 110)
pink = close((255, 204, 255), 60)
cyan = close((204, 255, 255), 60) & (a[:, :, 0] < 245)
yellow = close((255, 255, 204), 40)

EQ = (60, 90, 500, 240)
PANEL = (380, 130, 910, 510)

blobs(red, EQ, "RED in equation box", 8)
blobs(red, PANEL, "RED in diagram panel", 8)
blobs(blue, PANEL, "BLUE in diagram panel", 8)
blobs(green, PANEL, "GREEN in diagram panel", 8)
blobs(pink, PANEL, "PINK activation fill", 20)
blobs(cyan, PANEL, "CYAN sigma fill", 40)
blobs(yellow, (100, 340, 360, 420), "YELLOW callout", 60)

# black ink clusters (text) in diagram panel
dark = a.sum(axis=2) < 330
dark[487:, :] = False
blobs(dark, PANEL, "DARK ink in diagram panel", 8, 80)
blobs(dark, (100, 340, 360, 420), "DARK ink in callout", 8, 20)
blobs(dark, EQ, "DARK ink in equation box", 8, 60)
