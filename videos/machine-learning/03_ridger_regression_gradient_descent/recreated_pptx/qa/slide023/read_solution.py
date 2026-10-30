#!/usr/bin/env python3
"""Read the solution lines, solution label, blue L1 end (O(n^3), comma) glyphs."""
import numpy as np
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_023.jpg')
a = np.array(im).astype(int)

def classify(r, g, b):
    if b > r + 60 and b > 100 and r < 120: return 'N'
    if r > 120 and r - g > 80 and r - b > 80: return 'R'
    if r > 150 and r - g > 55 and r - b > 55: return 'r'
    if r < 110 and g < 110 and b < 110: return 'K'
    if r < 180 and g < 180 and b < 180: return 'o'
    return ' '

def dump(y0, y1, x0, x1, label):
    print(f"\n#### {label} y{y0}..{y1} x{x0}..{x1}")
    print('     ' + ''.join(str((x//10) % 10) for x in range(x0, x1+1)))
    print('     ' + ''.join(str(x % 10) for x in range(x0, x1+1)))
    for y in range(y0, y1 + 1):
        print(f"{y:4d} " + ''.join(classify(*a[y, x]) for x in range(x0, x1+1)))

dump(475, 500, 240, 720, "SOL L1 (full)")
dump(503, 524, 305, 660, "SOL L2 (full)")
dump(444, 468, 95, 190, "Solution: label")
dump(240, 268, 740, 860, "BLUE L1 tail: of O(n^3),")
