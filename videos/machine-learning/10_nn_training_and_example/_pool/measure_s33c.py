#!/usr/bin/env python3
"""Fine class map of slide 33 top box (A) and bottom box (B)."""
from PIL import Image
import collections

img = Image.open('/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides/slide_033.jpg').convert('RGB')
W, H = img.size
px = img.load()
IN = W / 13.33


def classify(p):
    r, g, b = p
    mx, mn = max(p), min(p)
    sat = mx - mn
    if sat < 20:
        return '.' if mx > 190 else ('-' if mx > 110 else '#')
    if r > g and r > b:
        return 'R' if sat > 60 else 'p'
    if r > 185 and g > 185 and b < g - 12:
        return 'Y'
    if b > r + 12:
        return 'B'
    if g > r + 12:
        return 'G'
    return '?'


def mapregion(x0, y0, x1, y1, cols, rows, label):
    print(f"\n=== {label}  x=[{x0},{x1}] ({x0/IN:.2f}-{x1/IN:.2f}in)  y=[{y0},{y1}] ({y0/IN:.2f}-{y1/IN:.2f}in) ===")
    print("   col_x_in: " + " ".join(f"{x0 + c*(x1-x0)/cols:6.2f}" for c in range(0, cols, 8)))
    for r in range(rows):
        ry0 = y0 + r * (y1 - y0) // rows
        ry1 = y0 + (r + 1) * (y1 - y0) // rows
        line = ''
        for c in range(cols):
            rx0 = x0 + c * (x1 - x0) // cols
            rx1 = x0 + (c + 1) * (x1 - x0) // cols
            cnt = collections.Counter()
            for y in range(ry0, ry1):
                for x in range(rx0, rx1):
                    cnt[classify(px[x, y])] += 1
            dom, n = cnt.most_common(1)[0]
            # prefer ink over background
            for k in ('R', 'Y', 'B', 'G', '#', 'p', '-', '?'):
                if cnt.get(k, 0) > n * 0.30:
                    dom = k
                    break
            line += dom
        print(f"  y={ry0/IN:5.2f} {line}")


mapregion(95, 90, 830, 290, 92, 26, "TOP BOX A")
mapregion(95, 330, 830, 530, 92, 26, "BOTTOM BOX B")
