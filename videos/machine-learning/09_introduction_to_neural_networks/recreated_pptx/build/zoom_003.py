#!/usr/bin/env python3
"""1px ASCII zoom for arbitrary regions of slide_003.jpg."""
from PIL import Image
import sys

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_003.jpg"
im = Image.open(SRC).convert("RGB")
px = im.load()

def cls(c):
    r, g, b = c
    if abs(c[0]-254)+abs(c[1]-255)+abs(c[2]-253) <= 150: return " "
    if r > 105 and r-g > 40 and r-b > 30: return "R"
    if b > r+25 and b > g+20: return "B"
    if g-r > 22 and g-b > 18 and g > 60: return "G"
    if c[0]+c[1]+c[2] < 560: return "#"
    return "."

def zoom(x0, y0, x1, y1, label=""):
    print(f"\n===== {label}  x={x0}..{x1} y={y0}..{y1} =====")
    hdr = "     " + "".join(str((x//100)%10) if x%100==0 else (str((x//10)%10) if x%10==0 else " ") for x in range(x0, x1+1))
    print(hdr)
    for y in range(y0, y1+1):
        print(f"  {y:3d} " + "".join(cls(px[x,y]) for x in range(x0, x1+1)))

if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) == 5:
        zoom(int(a[0]), int(a[1]), int(a[2]), int(a[3]), a[4])
    else:
        zoom(80, 345, 400, 400, "EQ-LEFT (Error= ... sum ...)")
        zoom(400, 345, 800, 400, "EQ-RIGHT")
        zoom(150, 380, 310, 400, "CAPTION")
