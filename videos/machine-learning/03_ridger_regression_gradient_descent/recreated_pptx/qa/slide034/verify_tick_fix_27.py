#!/usr/bin/env python3
"""PIL verification of the attempt-27 plot tick-label fix for slide 034.

Frame-derived label positions (from gen_plot_27.py: X0=721.825 SX=8.9296
Y0=172.336 SY=8.8443; labels drawn at data x=-0.60 for Y ticks, data y=-0.95
for X ticks):
    y-tick "6":  data (-0.60, 6)     -> frame (716.47, 119.27)
    x-tick "8":  data (8, -0.95)     -> frame (793.26, 180.74)
Prints a dark-pixel census + ASCII art for both the original frame and the
render, so the glyph presence can be judged without a vision call.
"""
from PIL import Image

D = "videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = Image.open(f"{D}/unique_slides/slide_034.jpg").convert("RGB")
REND = Image.open(f"{D}/recreated_pptx/qa/slide034/render_27.png").convert("RGB")
SX, SY = REND.width / 960.0, REND.height / 540.0

CHECKS = {
    "y-tick '6'  (frame ~716,119)": (709, 112, 724, 127),
    "y-tick '4'  (control ~716,137)": (709, 130, 724, 145),
    "x-tick '8'  (frame ~793,181)": (786, 174, 801, 190),
    "x-tick '6'  (control ~775,181)": (768, 174, 783, 190),
}


def census(im, box):
    x0, y0, x1, y1 = box
    sx = im.width / 960.0
    sy = im.height / 540.0
    px = im.load()
    dark = 0
    cells = []
    for y in range(int(y0 * sy), int(y1 * sy)):
        row = ""
        for x in range(int(x0 * sx), int(x1 * sx)):
            r, g, b = px[x, y]
            lum = (r + g + b) / 3
            if lum < 110:
                row += "#"
                dark += 1
            elif lum < 175:
                row += "+"
                dark += 1
            else:
                row += "."
        cells.append(row)
    return dark, cells


for name, box in CHECKS.items():
    do, co = census(ORIG, box)
    dr, cr = census(REND, box)
    print(f"\n### {name}")
    print(f"dark-ish px: original={do}  render={dr}")
    print("ORIGINAL:")
    for r in co:
        print("   ", r)
    print("RENDER:")
    for r in cr:
        print("   ", r)
