#!/usr/bin/env python3
"""ASCII ink map at 1px resolution for the dimension-note line and equation line
of the green box in slide_023.jpg. R=red, Y=yellow, #=dark, ' '=fill/bg."""
import numpy as np
from PIL import Image
import sys

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_023.jpg')
a = np.array(im).astype(int)
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]

def classify(r, g, b):
    if r > 130 and r - g > 70 and r - b > 70: return 'R'
    if r > 235 and g > 200 and g > b + 20 and b < 230: return 'Y'
    if r < 150 and g < 150 and b < 150: return '#'
    # dark-olive / yellow-dark ink (JPEG blend of yellow on green?)
    if r < 200 and g < 200: return 'o'
    return ' '

def dump(y0, y1, x0, x1, label, seg=118):
    print(f"\n#### {label} y{y0}..{y1}")
    for xs in range(x0, x1, seg):
        xe = min(xs + seg, x1)
        print(f"--- x{xs}..{xe}")
        hdr = '     ' + ''.join(str((x // 10) % 10) for x in range(xs, xe))
        print(hdr)
        for y in range(y0, y1 + 1):
            line = ''.join(classify(*a[y, x]) for x in range(xs, xe))
            print(f"{y:4d} {line}")

# dimension note line
dump(193, 216, 100, 470, "DIM NOTE part 1 (x100-470)")
dump(193, 216, 470, 770, "DIM NOTE part 2 (x470-770)")
