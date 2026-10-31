# b09: 1px-resolution colour-classified ASCII of an arbitrary region of slide_018.
# usage: python3 b09_zoom.py x0 y0 x1 y1 [mask]
# mask: any of R G M B y # or "red|green|..." to isolate one colour class.
import sys
from PIL import Image
import numpy as np

A = np.asarray(Image.open('/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides/slide_018.jpg').convert('RGB')).astype(int)

x0, y0, x1, y1 = (int(v) for v in sys.argv[1:5])
mask = sys.argv[5] if len(sys.argv) > 5 else None

CLASS = {'R': lambda c: c[0] > 150 and c[1] < 130 and c[2] < 130,
         'G': lambda c: c[1] > 160 and c[0] < 220 and c[1] - c[0] > 20 and c[2] < 200,
         'M': lambda c: c[0] > 130 and c[1] < 120 and c[2] > 110,
         'B': lambda c: c[2] > 120 and c[0] < 120 and c[1] < 120,
         'y': lambda c: c[0] > 200 and c[1] > 170 and c[2] < 170,
         '#': lambda c: c[0] < 110 and c[1] < 110 and c[2] < 110}

def cls(c):
    for k, f in CLASS.items():
        if f(c): return k
    return '.'

print(f"x{x0}..{x1} y{y0}..{y1} mask={mask}")
print('     ' + ''.join(str(x // 10 % 10) for x in range(x0, x1)))
print('     ' + ''.join(str(x % 10) for x in range(x0, x1)))
for y in range(y0, y1):
    row = ''
    for x in range(x0, x1):
        k = cls(A[y, x])
        row += k if (mask is None or k == mask) else (' ' if k in CLASS else '.')
    print(f"{y:4d} {row}")
