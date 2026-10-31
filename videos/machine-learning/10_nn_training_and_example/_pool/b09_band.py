# b09: whole-band ASCII map of slide_018 at 2px subsampling.
import sys
from PIL import Image
import numpy as np

A = np.asarray(Image.open('/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides/slide_018.jpg').convert('RGB')).astype(int)

def cls(c):
    r, g, b = c
    if abs(r-218) < 24 and abs(g-206) < 24 and abs(b-194) < 24: return '.'   # cream
    if abs(r-231) < 12 and abs(g-233) < 12 and abs(b-230) < 14: return ' '    # house grey
    if r > 245 and g > 245 and b > 245: return ' '                            # white
    if g > 150 and r < 225 and g - r > 12 and b < 215: return 'G'             # green
    if r > 200 and g > 160 and b < 150: return 'Y'                            # gold/tan
    if r > 190 and g < 150 and b < 150: return 'R'                            # red
    if r > 130 and g < 120 and b > 100: return 'M'                            # magenta/purple
    if b > 100 and r < 140 and g < 140: return 'B'                            # blue
    if r < 130 and g < 130 and b < 130: return '#'                            # dark
    return ':'

x0, x1, y0, y1 = (int(v) for v in (sys.argv[1:5] if len(sys.argv) > 4 else (360, 770, 55, 210)))
sx, sy = 2, 2
print('     ' + ''.join(str(x // 10 % 10) for x in range(x0, x1, sx)))
for y in range(y0, y1, sy):
    row = ''
    for x in range(x0, x1, sx):
        blk = A[y:y + sy, x:x + sx].reshape(-1, 3).mean(axis=0)
        row += cls(blk)
    print(f"{y:4d} {row}")
