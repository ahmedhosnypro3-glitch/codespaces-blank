#!/usr/bin/env python3
"""Probe the four pink formula boxes on slide_021: pink/red bounds and ink bands."""
from PIL import Image
import numpy as np

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_021.jpg"
im = Image.open(SRC).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
print("size", W, H)

R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

pink = (R > 235) & (G > 215) & (G < 243) & (B > 195) & (B < 228)
red = (R > 120) & (R - G > 45) & (R - B > 45)
blue = (B - R > 45) & (B - G > 35)
black = (R < 90) & (G < 90) & (B < 90)

BOXES = {
    "TL": (110, 48, 418, 108),
    "TR": (545, 48, 855, 108),
    "BL": (90, 278, 435, 344),
    "BR": (580, 278, 818, 344),
}

for name, (x0, y0, x1, y1) in BOXES.items():
    sub_p = pink[y0:y1, x0:x1]
    sub_r = red[y0:y1, x0:x1]
    sub_k = black[y0:y1, x0:x1]
    def bbox(m):
        ys, xs = np.nonzero(m)
        if len(xs) == 0:
            return None
        return (x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max())
    print(f"\n=== {name} ===")
    print(" pink bbox", bbox(sub_p), " count", int(sub_p.sum()))
    print(" red  bbox", bbox(sub_r), " count", int(sub_r.sum()))
    print(" dark bbox", bbox(sub_k), " count", int(sub_k.sum()))
    print(" red row profile (y: count):")
    for y in range(y0, y1):
        c = int(red[y, x0:x1].sum())
        k = int(black[y, x0:x1].sum())
        if c or k:
            print(f"   y={y} red={c} dark={k}")
