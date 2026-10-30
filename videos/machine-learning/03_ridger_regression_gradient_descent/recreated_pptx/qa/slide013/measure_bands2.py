import numpy as np
from PIL import Image

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = np.asarray(Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

BLUE = (b > r + 60) & (b > 100) & (g < r + 30)
RED = (r > g + 40) & (r > b + 40)
YELLOW = (r > 150) & (g > 130) & (b < 130) & (abs(r - g) < 70)


def bands(idx):
    if not len(idx):
        return []
    out = []
    s = p = int(idx[0])
    for v in idx[1:]:
        v = int(v)
        if v == p + 1:
            p = v
        else:
            out.append((s, p))
            s = p = v
    out.append((s, p))
    return out


print("RED row bands:", bands(np.where(RED.any(axis=1))[0]))
print("BLUE row bands:", bands(np.where(BLUE.any(axis=1))[0]))
print("YELLOW row bands:", bands(np.where(YELLOW.any(axis=1))[0]))
print()
print("RED col bands:", bands(np.where(RED.any(axis=0))[0]))
print("BLUE col bands:", bands(np.where(BLUE.any(axis=0))[0]))
print("YELLOW col bands:", bands(np.where(YELLOW.any(axis=0))[0]))

# column profiles per band, 1px resolution for the big row bands
print("\n=== per-column RED/ink counts for each YELLOW band ===")
for (y0, y1) in bands(np.where(YELLOW.any(axis=1))[0]):
    seg = slice(y0, y1 + 1)
    rr = RED[seg].sum(axis=0)
    bb = BLUE[seg].sum(axis=0)
    cols = np.where((rr > 0) | (bb > 0))[0]
    if not len(cols):
        continue
    print(f"  y{y0}..{y1}: ink cols x{cols.min()}..{cols.max()}")
