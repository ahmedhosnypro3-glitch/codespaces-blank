#!/usr/bin/env python3
"""High-res class map of slide 33 panel A network region (left of target table)."""
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
    if sat < 22:
        return '.' if mx > 195 else ('-' if mx > 120 else '#')
    if r > g and r > b:
        return 'R' if sat > 60 else 'p'
    if r > 180 and g > 180 and b < g - 10:
        return 'Y'
    if b > r + 10:
        return 'B'
    if g > r + 10:
        return 'G'
    return '?'


def mapregion(x0, y0, x1, y1, cols, rows, label):
    print(f"\n=== {label} x=[{x0},{x1}] ({x0/IN:.2f}-{x1/IN:.2f}in) y=[{y0},{y1}] ({y0/IN:.2f}-{y1/IN:.2f}in) ===")
    hdr = "   "
    for c in range(0, cols, 10):
        hdr += f"{x0 + c*(x1-x0)/cols/IN:6.2f}"
    print(hdr + "   (col x_in)")
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
            for k in ('R', 'Y', 'B', 'G', '#', 'p', '-', '?'):
                if cnt.get(k, 0) > n * 0.35:
                    dom = k
                    break
            line += dom
        print(f"  y={ry0/IN:5.2f} {line}")


mapregion(100, 90, 640, 290, 108, 40, "PANEL A NETWORK")
