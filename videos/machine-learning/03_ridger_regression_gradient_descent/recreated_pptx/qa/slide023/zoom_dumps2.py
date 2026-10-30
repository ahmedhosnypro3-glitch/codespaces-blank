#!/usr/bin/env python3
"""More zoomed dumps: (X^T X) superscript, Recall line, title, plus row profiles."""
import numpy as np
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_023.jpg')
a = np.array(im).astype(int)

def classify(r, g, b):
    if r > 120 and r - g > 80 and r - b > 80: return 'R'
    if r > 150 and r - g > 55 and r - b > 55: return 'r'
    if r < 110 and g < 110 and b < 110: return '#'
    if r < 170 and g < 170 and b < 170: return 'o'
    if r > 235 and g > 200 and g - b > 25 and r - b > 40: return 'Y'
    return ' '

def dump(y0, y1, x0, x1, label):
    print(f"\n#### {label} y{y0}..{y1} x{x0}..{x1}")
    print('     ' + ''.join(str((x//10) % 10) for x in range(x0, x1+1)))
    print('     ' + ''.join(str(x % 10) for x in range(x0, x1+1)))
    for y in range(y0, y1 + 1):
        print(f"{y:4d} " + ''.join(classify(*a[y, x]) for x in range(x0, x1+1)))

dump(193, 215, 500, 570, "(X^T X) in dim-note line")
dump(110, 145, 100, 185, "Recall: line")
dump(75, 108, 215, 660, "TITLE")

# title per-row red counts to measure cap height exactly
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]
red = (R > 120) & (R - G > 80) & (R - B > 80)
print("\nTitle red px per row (x200..680):")
for y in range(70, 110):
    n = int(red[y, 200:680].sum())
    if n: print(f"  y={y}: {n}")
