# b09: per-row ink runs of the slide_018 network band.
# usage: python3 b09_rows.py [x0 x1] [y0 y1]
import sys
from PIL import Image
import numpy as np

A = np.asarray(Image.open('/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides/slide_018.jpg').convert('RGB')).astype(int)

x0, x1, y0, y1 = (int(v) for v in (sys.argv[1:5] if len(sys.argv) > 4 else (360, 760, 56, 208)))

def cls(c):
    r, g, b = c
    if r > 120 and g < 130 and b < 130: return 'R'
    if g > 150 and r < 220 and g - r > 15 and b < 210: return 'G'
    if r > 120 and g < 120 and b > 100: return 'M'
    if b > 100 and r < 130 and g < 130: return 'B'
    if r > 195 and g > 160 and b < 165: return 'y'
    if r < 120 and g < 120 and b < 120: return '#'
    return '.'

for y in range(y0, y1):
    runs = []
    cur = None
    for x in range(x0, x1):
        k = cls(A[y, x])
        if k == '.': k = ' '
        if k != ' ':
            if cur and cur[0] == k and x == cur[2] + 1: cur[2] = x
            else:
                if cur: runs.append(cur)
                cur = [k, x, x]
        else:
            if cur: runs.append(cur); cur = None
    if cur: runs.append(cur)
    if runs:
        print(f"{y:3d} " + ' '.join(f"{a}{s}-{e}" for a, s, e in runs))
