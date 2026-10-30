#!/usr/bin/env python3
"""Zoomed ASCII dumps of specific regions of slide_023.jpg to read glyphs."""
import numpy as np
from PIL import Image
import sys

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_023.jpg')
a = np.array(im).astype(int)

def classify(r, g, b):
    if r > 120 and r - g > 80 and r - b > 80: return 'R'      # red core
    if r > 150 and r - g > 55 and r - b > 55: return 'r'      # red-ish blend
    if r < 110 and g < 110 and b < 110: return '#'            # dark core
    if r < 160 and g < 160 and b < 160: return 'o'            # dark blend
    if r > 235 and g > 200 and g - b > 25 and r - b > 40: return 'Y'
    return ' '

def dump(y0, y1, x0, x1, label):
    print(f"\n#### {label} y{y0}..{y1} x{x0}..{x1}")
    w = x1 - x0 + 1
    # header: tens digit row and units digit row
    print('     ' + ''.join(str((x//10) % 10) for x in range(x0, x1+1)))
    print('     ' + ''.join(str(x % 10) for x in range(x0, x1+1)))
    for y in range(y0, y1 + 1):
        print(f"{y:4d} " + ''.join(classify(*a[y, x]) for x in range(x0, x1+1)))

dump(194, 216, 395, 470, "between labels: the mystery glyph at x439-453")
dump(194, 216, 655, 760, "d+1 x d+1 region")
dump(146, 192, 100, 240, "equation: W = (X^T part")
dump(146, 192, 240, 440, "equation: X + lambdaI)^(-1 part")
dump(146, 192, 440, 480, "equation: X^T Y part")
