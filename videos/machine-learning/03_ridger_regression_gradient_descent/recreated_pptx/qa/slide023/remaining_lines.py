#!/usr/bin/env python3
"""ASCII dumps of remaining text lines: blue box x3, example x2, solution x3.
N=navy-blue, K=black, R=red, o=blend."""
import numpy as np
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_023.jpg')
a = np.array(im).astype(int)

def classify(r, g, b):
    if b > r + 60 and b > 100 and r < 120: return 'N'   # navy
    if r > 120 and r - g > 80 and r - b > 80: return 'R'
    if r < 110 and g < 110 and b < 110: return 'K'
    if r < 180 and g < 180 and b < 180: return 'o'
    return ' '

def dump(y0, y1, x0, x1, label, every=1):
    print(f"\n#### {label} y{y0}..{y1} x{x0}..{x1}")
    print('     ' + ''.join(str((x//100) % 10) for x in range(x0, x1+1)))
    print('     ' + ''.join(str((x//10) % 10) for x in range(x0, x1+1)))
    print('     ' + ''.join(str(x % 10) for x in range(x0, x1+1)))
    for y in range(y0, y1 + 1):
        print(f"{y:4d} " + ''.join(classify(*a[y, x]) for x in range(x0, x1+1)))

# word-level runs: navy/black/red runs per line
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]
navy = (B > R + 40) & (B > 90) & (G < 120)
blk = (R < 110) & (G < 110) & (B < 110)
red = (R > 120) & (R - G > 80) & (R - B > 80)

def wruns(y0, y1, label, gap=4):
    m = navy | blk | red
    ch = m[y0:y1+1].any(axis=0)
    xs = []
    x = 0
    while x < len(ch):
        if ch[x]:
            s = x
            while x < len(ch) and (ch[x] or ch[max(0,x-gap):x+gap].any() if x+gap<len(ch) else ch[x]):
                x += 1
            xs.append((s, x-1))
        else:
            x += 1
    out = []
    for s, e in xs:
        seg = slice(s, e+1)
        nn = int((navy[y0:y1+1, seg]).sum()); nk = int((blk[y0:y1+1, seg]).sum()); nr = int((red[y0:y1+1, seg]).sum())
        ys = np.where(m[y0:y1+1, seg].any(axis=1))[0]
        out.append(f"x[{s}..{e}]y[{ys[0]+y0}..{ys[-1]+y0}] N{nn}/K{nk}/R{nr}")
    print(f"\n== {label}: " + " | ".join(out))

wruns(240, 266, "BLUE L1")
wruns(272, 298, "BLUE L2")
wruns(304, 332, "BLUE L3")
wruns(360, 392, "EX L1")
wruns(394, 422, "EX L2")
wruns(444, 470, "SOLUTION label")
wruns(474, 500, "SOL L1")
wruns(502, 528, "SOL L2")
