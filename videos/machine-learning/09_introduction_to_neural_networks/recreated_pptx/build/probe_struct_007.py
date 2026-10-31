"""ASCII structure map of the original slide 007 panel (hue-classified, 6px cells)."""
from PIL import Image
import numpy as np

SRC = '/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_007.jpg'
a = np.asarray(Image.open(SRC).convert('RGB')).astype(int)
F = a.reshape(a.shape[0], a.shape[1], 3)


def cls(y, x):
    r, g, b = int(F[y, x, 0]), int(F[y, x, 1]), int(F[y, x, 2])
    m = max(r, g, b)
    c = m - min(r, g, b)
    L = (r + g + b) / 3.0
    if c < 30:
        if L < 90:
            return 'K'
        return '.' if L > 245 else ':'
    if r > 200 and g > 200 and b < 160:
        return 'Y'
    if r == m and g > 0.6 * r and b > 0.6 * r:
        return 'y'
    if r == m and b > 0.55 * r:
        return 'm'
    if r == m:
        return 'R' if L < 200 else 'r'
    if g == m:
        return 'G' if L < 200 else 'g'
    if b == m:
        return 'B' if L < 200 else 'b'
    return '?'


for y in range(112, 484, 6):
    print(f'{y:3d} ' + ''.join(cls(y, x) for x in range(152, 762, 6)))
