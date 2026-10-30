"""ASCII color-class map of slide_021.jpg — lets me read the layout without a binary image read."""
import numpy as np
from PIL import Image

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/"
im = Image.open(V + "unique_slides/slide_021.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape

# class map at 8x8 px cells -> 120 x 67
CH, CW = 8, 8
print("Legend: .=bg  f=formula-fill(peach)  R=red  B=blue/indigo  G=green  O=orange  K=black  W=white  g=gray-grid")
print("        -=other")
rows = []
for gy in range(0, H, CH):
    line = ""
    for gx in range(0, W, CW):
        cell = a[gy:gy+CH, gx:gx+CW].reshape(-1, 3)
        med = np.median(cell, axis=0)
        rr, gg, bb = med
        if rr > 245 and gg > 245 and bb > 245: c = "."
        elif rr < 90 and gg < 90 and bb < 90: c = "K"
        elif rr - gg > 35 and rr - bb > 35 and rr > 140: c = "R"
        elif rr - gg > 6 and rr - bb > 6 and rr > 230 and gg > 205: c = "f"
        elif bb - rr > 40: c = "B"
        elif gg - rr > 25 and gg - bb > 25: c = "G"
        elif rr - bb > 60 and gg > 120 and gg < 220: c = "O"
        elif abs(rr - gg) < 8 and abs(gg - bb) < 8 and rr < 230: c = "g"
        else: c = "-"
        line += c
    rows.append(f"{gy:3d} " + line)
print("\n".join(rows))

# Print precise x-axis ruler
print("\nx ruler (each char = 8px): 0 at col 4")
print("y ruler: each row = 8px")
