#!/usr/bin/env python3
"""PIL colour-map dump of slide 044's calc bands (fresh lane, attempt 1).

Prints a character map per pixel (R=red ink, G=green ink, B=blue ink,
K=dark ink, .=background) for the measured regions of the ORIGINAL frame
(unique_slides/slide_044.jpg, 960x540, 1px=1pt).  Coordinates are frame px.
"""
import sys
from PIL import Image

V = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = Image.open(f"{V}/unique_slides/slide_044.jpg").convert("RGB")

def cls(p):
    r, g, b = p
    if r > 150 and g < 110 and b < 110:
        return "R"
    if g > 110 and r < 150 and b < 140 and g - r > 25 and g - b > 25:
        return "G"
    if b > 120 and r < 140 and b - r > 45 and b - g > 45:
        return "B"
    if r < 140 and g < 140 and b < 140:
        return "K"
    return "."

def dump(name, x0, y0, x1, y1):
    print(f"=== {name}: frame x{x0}..{x1} y{y0}..{y1}")
    print("     " + "".join(str((x // 10) % 10) for x in range(x0, x1)))
    print("     " + "".join(str(x % 10) for x in range(x0, x1)))
    for y in range(y0, y1):
        row = "".join(cls(ORIG.getpixel((x, y))) for x in range(x0, x1))
        print(f"{y:4d} {row}")

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "b2left"):
        dump("box2 left equation", 280, 208, 460, 262)
    if which in ("all", "b2w"):
        dump("box2 W group", 630, 208, 845, 262)
    if which in ("all", "b6left"):
        dump("box6 left equation", 280, 472, 460, 528)
