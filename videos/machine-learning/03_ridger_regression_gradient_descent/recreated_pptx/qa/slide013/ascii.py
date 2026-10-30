import numpy as np
from PIL import Image

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = np.asarray(Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

RED = (r > g + 40) & (r > b + 40)
BLUE = (b > r + 60) & (b > 100) & (g < r + 30)
BLK = (r < 120) & (g < 120) & (b < 120)
YEL = (r > 240) & (g > 235) & (b < 150) & (abs(r - g) < 12)


def ascii_map(y0, y1, x0, x1, step=1, chars=None):
    if chars is None:
        chars = (RED, BLUE, BLK, YEL)
    syms = ['R', 'B', 'K', 'Y']
    print(f"=== y{y0}..{y1} x{x0}..{x1} step={step} (R=red B=blue K=black Y=yellow) ===")
    for y in range(y0, y1, step):
        line = ''
        for x in range(x0, x1, step):
            c = ' '
            got = False
            for m, s in zip(chars, syms):
                if m[y, x]:
                    if not got:
                        c = s
                        got = True
            line += c
        print(f"{y:4d}|{line}")


import sys
which = sys.argv[1] if len(sys.argv) > 1 else 'all'
if which in ('all', 'tbl1'):
    ascii_map(126, 256, 96, 470, step=2)
if which in ('all', 'hdr1'):
    ascii_map(130, 155, 128, 470, step=1)
if which in ('all', 'w1'):
    ascii_map(155, 220, 458, 690, step=1)
if which in ('all', 'test1'):
    ascii_map(126, 256, 712, 884, step=2)
