#!/usr/bin/env python3
"""Classify panel pixels of slide_008.jpg into tint families and print a map.

Families (from measured sample colours):
  G  pale-green region   (~207-236, 244-255, 201-238)
  L  pale-lavender region(~183-208, 181-207, 230-249)
  P  pale-pink region    (~219-255, 174-224, 179-224)
  Y  bright yellow tag
  R/B/G strong ink
  w  white / near-white
  x  grey cross-hatch wedge / other
"""
import numpy as np
from PIL import Image

P = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_008.jpg"
a = np.asarray(Image.open(P).convert("RGB")).astype(int)
H, W, _ = a.shape
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

# hue-ish separation
mg = G - (R + B) / 2.0
mb = B - (R + G) / 2.0
mr = R - (G + B) / 2.0

fam = np.full((H, W), ".", dtype="<U1")
lum = (R + G + B) / 3.0

fam[(lum > 246)] = "w"
fam[(lum <= 246) & (lum > 200)] = "x"      # tinted light
# greenish
fam[(mg > 3.5) & (lum > 190)] = "G"
# lavender / blueish
fam[(mb > 3.0) & (lum > 190)] = "L"
# pink / reddish
fam[(mr > 3.0) & (lum > 190)] = "P"
# strong inks
fam[(R > 120) & (R - G > 45) & (R - B > 45)] = "R"
fam[(B > 140) & (B - R > 80) & (B - G > 60)] = "B"
fam[(G > 120) & (G - R > 40) & (G - B > 25)] = "G"
fam[(R > 190) & (G > 180) & (B < 150) & (R - B > 70)] = "Y"

step = 8
print("      " + "".join(str(((168 + i * step) // 100) % 10) for i in range(80)))
print("      " + "".join(str(((168 + i * step) // 10) % 10) for i in range(80)))
for y in range(120, 512, step):
    line = ""
    for i in range(80):
        x = 168 + i * step
        blk = fam[y:y + step, x:x + step].ravel()
        vals, cnts = np.unique(blk, return_counts=True)
        line += str(vals[np.argmax(cnts)])
    print(f"{y:4d}  {line}")

# Region coverage counts
print()
for c in "GLPYRBwx":
    n = ((fam[120:505, 168:795] == c)).sum()
    print(f"  {c}: {n} px")
