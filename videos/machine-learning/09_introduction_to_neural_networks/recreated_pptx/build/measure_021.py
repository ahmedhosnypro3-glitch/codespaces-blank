#!/usr/bin/env python3
"""Measure slide_021.jpg geometry with PIL: red frames, pink formula boxes,
blue graph frames, badge, black bar, and per-panel ink structure."""
import numpy as np
from PIL import Image

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_021.jpg"
im = Image.open(SRC).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
print("size", W, H)

R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]


def bbox(mask, label, minpix=20):
    ys, xs = np.nonzero(mask)
    if len(xs) < minpix:
        print(f"{label}: none ({len(xs)} px)")
        return None
    print(f"{label}: n={len(xs)} bbox x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()}")
    return (xs.min(), ys.min(), xs.max(), ys.max())


red = (R > 140) & (R - G > 55) & (R - B > 55)
blue = (B > 120) & (B - R > 50) & (B - G > 50)
pink = (R > 235) & (G > 195) & (G < 235) & (B > 195) & (B < 235) & (R - B > 15)
black = (R < 60) & (G < 60) & (B < 60)

print("\n--- global masks ---")
bbox(red, "red")
bbox(blue, "blue")
bbox(pink, "pink")
bbox(black, "black")

# row profile of red ink to find horizontal frame lines
rows_red = red.sum(axis=1)
print("\nred row peaks (count>20):", [(i, int(c)) for i, c in enumerate(rows_red) if c > 20])
cols_red = red.sum(axis=0)
print("red col peaks (count>20):", [(i, int(c)) for i, c in enumerate(cols_red) if c > 20])

rows_blue = blue.sum(axis=1)
print("\nblue row peaks (count>10):", [(i, int(c)) for i, c in enumerate(rows_blue) if c > 10])
cols_blue = blue.sum(axis=0)
print("blue col peaks (count>10):", [(i, int(c)) for i, c in enumerate(cols_blue) if c > 10])

rows_black = black.sum(axis=1)
print("\nblack row peaks (count>50):", [(i, int(c)) for i, c in enumerate(rows_black) if c > 50])

# pink connected-ish: column/row histogram
print("\npink row bands:", [(i, int(c)) for i, c in enumerate(pink.sum(axis=1)) if c > 5])
