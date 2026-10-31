import sys
import numpy as np
from PIL import Image

path = sys.argv[1]
cols = int(sys.argv[2]) if len(sys.argv) > 2 else 110
im = Image.open(path).convert("RGBA")
a = np.asarray(im)
alpha = a[:, :, 3]
h, w = alpha.shape
rows = max(1, int(cols * h / w * 0.5))
small = np.asarray(Image.fromarray(alpha).resize((cols, rows)))
chars = " .:-=+*#%@"
for r in small:
    print("".join(chars[min(9, int(v / 256 * 10))] for v in r))
print(f"{path}: {w}x{h}px")
