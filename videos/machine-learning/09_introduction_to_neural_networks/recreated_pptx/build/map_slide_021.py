#!/usr/bin/env python3
"""ASCII structure map of slide_021.jpg: classify each grid cell by dominant color class."""
from PIL import Image
import numpy as np

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_021.jpg"
im = Image.open(SRC).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
GY, GX = 45, 80   # grid cells
ch, cw = H // GY, W // GX

def classify(block):
    r, g, b = block[:, :, 0], block[:, :, 1], block[:, :, 2]
    n = block.shape[0] * block.shape[1]
    white = ((r > 245) & (g > 245) & (b > 245)).sum()
    gray = ((np.abs(r - 232) < 12) & (np.abs(g - 232) < 12) & (np.abs(b - 232) < 12)).sum()
    lightbg = ((np.abs(r - 231) < 12) & (np.abs(g - 233) < 12) & (np.abs(b - 230) < 12)).sum()
    pink = ((r > 235) & (g > 205) & (g < 252) & (b > 185) & (b < 245) & (r - b > 12)).sum()
    red = ((r > 130) & (g < 120) & (b < 120)).sum()
    blue = ((b > 110) & (b - r > 35) & (b - g > 35)).sum()
    black = ((r < 60) & (g < 60) & (b < 60)).sum()
    green = ((g > 90) & (g - r > 25) & (g - b > 25)).sum()
    counts = {"W": white, ".": gray + lightbg, "p": pink, "R": red, "B": blue, "#": black, "G": green}
    best = max(counts, key=counts.get)
    frac = counts[best] / n
    if frac < 0.25:
        return " "
    if best == "R" and frac < 0.5:
        return "r"   # some red ink (text/line)
    if best == "B" and frac < 0.5:
        return "b"
    if best == "#" and frac < 0.5:
        return "x"
    return best

print("Legend: W=white .=graybg p=pinkfill r/B/x=red/blue/black-ink R/B/#=solid color")
for gy in range(GY):
    line = ""
    for gx in range(GX):
        block = a[gy*ch:(gy+1)*ch, gx*cw:(gx+1)*cw]
        line += classify(block)
    print(f"{gy*ch:3d} {line}")
