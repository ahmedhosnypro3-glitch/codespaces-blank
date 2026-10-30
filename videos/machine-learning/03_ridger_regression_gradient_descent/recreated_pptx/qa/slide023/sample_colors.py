#!/usr/bin/env python3
"""Sample actual colors in the putative regions of slide_023.jpg + column checks."""
import numpy as np
from PIL import Image
from collections import Counter
import json

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_023.jpg')
a = np.array(im).astype(int)

def top_colors(y0, y1, x0, x1, n=8, label=""):
    reg = a[y0:y1+1, x0:x1+1]
    flat = [tuple(p) for p in reg.reshape(-1, 3)]
    c = Counter(flat).most_common(n)
    print(f"== {label} region y{y0}..{y1} x{x0}..{x1}")
    for col, cnt in c:
        print(f"   {col}  x{cnt}")

# interior samples (avoid text): sample strips and count dominant colors
top_colors(230, 235, 200, 800, 8, "between green box and example text (blue box?)")
top_colors(245, 250, 150, 700, 8, "blue box mid upper")
top_colors(275, 285, 150, 700, 8, "blue box mid lower")
top_colors(300, 310, 150, 700, 8, "below blue box / above example")
top_colors(390, 395, 200, 800, 8, "between example and solution")
top_colors(455, 465, 500, 860, 8, "solution box interior right (no text?)")
top_colors(445, 452, 90, 880, 8, "solution box top strip")
top_colors(522, 527, 500, 860, 8, "solution box bottom strip")
top_colors(485, 492, 90, 240, 8, "solution box left interior")
top_colors(108, 222, 60, 94, 8, "left of green box")
top_colors(100, 106, 200, 700, 8, "above green box")
top_colors(224, 230, 200, 700, 8, "below green box")
top_colors(60, 75, 200, 400, 8, "title band left of text")
top_colors(78, 104, 100, 215, 8, "title left margin")

# column profile: check for vertical borders of the yellow region x85..95 and x865..880, y437..528
for xc in range(85, 100):
    col = a[440:525, xc]
    print("col x=%d y440..524 unique colors:" % xc, Counter(tuple(p) for p in col).most_common(3))
for xc in range(860, 880):
    col = a[440:525, xc]
    print("col x=%d y440..524 unique colors:" % xc, Counter(tuple(p) for p in col).most_common(3))
