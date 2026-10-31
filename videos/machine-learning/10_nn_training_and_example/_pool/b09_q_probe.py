# b09: probe slide_018 original for open questions.
# usage: python3 b09_q_probe.py <mode>
#   label  - bottom-left magenta label (x360..405, y188..202) ASCII zoom
#   errdir - error-bar red glyphs (x750..790, y60..200) ASCII zoom
#   topo   - green/magenta/blue/dark ink column profile across the diagram band
#   rows   - per-row element scan (x360..900) for each of the 3 rows
import sys
from PIL import Image
import numpy as np

IM = Image.open('/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides/slide_018.jpg').convert('RGB')
A = np.asarray(IM).astype(int)

def key(rgb):
    r, g, b = rgb
    if r < 110 and g < 110 and b < 110: return '#'   # dark ink
    if r > 190 and g < 120 and b < 120: return 'R'   # red
    if g > 170 and r < 215 and b < 200 and g - r > 25: return 'G'  # green
    if r > 150 and g < 110 and b > 130: return 'M'   # magenta/purple
    if b > 140 and r < 110 and g < 110: return 'B'   # blue
    if r > 215 and g > 190 and b < 160: return 'y'   # yellow/gold
    if abs(r - 218) < 26 and abs(g - 206) < 26 and abs(b - 194) < 26: return '.'  # cream
    if r > 190: return ' '
    return '.'

def shown(x0, y0, x1, y1, sx=1, sy=2):
    print(f"region x{x0}..{x1} y{y0}..{y1}")
    hdr = '     ' + ''.join(str((x0 + i * sx) // 10 % 10) for i in range((x1 - x0) // sx))
    print(hdr)
    for y in range(y0, y1, sy):
        row = ''.join(key(A[y, x]) for x in range(x0, x1, sx))
        print(f"{y:4d} {row}")

m = sys.argv[1] if len(sys.argv) > 1 else 'label'
if m == 'label':
    shown(360, 188, 405, 203, 1, 2)
elif m == 'errdir':
    shown(750, 60, 790, 200, 1, 2)
elif m == 'topo':
    for name, pred in [('green', lambda c: c[1] > 170 and c[0] < 215 and c[1] - c[0] > 25),
                       ('magenta', lambda c: c[0] > 140 and c[1] < 110 and c[2] > 120),
                       ('blue', lambda c: c[2] > 140 and c[0] < 110 and c[1] < 110),
                       ('dark', lambda c: c[0] < 110 and c[1] < 110 and c[2] < 110)]:
        msk = np.zeros(A.shape[:2], bool)
        for y in range(58, 206):
            for x in range(360, 900):
                if pred(A[y, x]): msk[y, x] = True
        prof = [int(msk[58:206, x:x + 10].sum()) for x in range(360, 900, 10)]
        print(name, ' '.join(f"{360 + i * 10}:{v}" for i, v in enumerate(prof)))
elif m == 'rows':
    for y in range(58, 206, 1):
        cells = []
        for x in range(360, 900, 5):
            seg = A[y, x:x + 5]
            k = ''.join(key(c) for c in seg)
            if set(k) - {' ', '.'}: cells.append(f"{x}:{k.replace(' ', '')}")
        if cells: print(y, ' '.join(cells))
