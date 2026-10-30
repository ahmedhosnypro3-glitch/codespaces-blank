import sys
import numpy as np
from PIL import Image

def grid(path, xs, ys, label):
    a = np.array(Image.open(path).convert("RGB"))
    h, w = a.shape[:2]
    print(f"# {label} {path} {w}x{h}")
    for fy in ys:
        row = []
        for fx in xs:
            x = min(w - 1, int(fx * w)); y = min(h - 1, int(fy * h))
            r, g, b = a[y, x]
            row.append(f"{r:02X}{g:02X}{b:02X}")
        print(f"  y={fy:.3f} " + " ".join(row))

if __name__ == "__main__":
    path, label = sys.argv[1], sys.argv[2]
    xs = [0.005, 0.012, 0.02, 0.03, 0.04, 0.045, 0.05, 0.055, 0.06, 0.40, 0.41, 0.42,
          0.55, 0.70, 0.80, 0.84, 0.88, 0.92, 0.94, 0.96, 0.985, 0.995]
    ys = [0.005, 0.02, 0.06, 0.07, 0.08, 0.09, 0.10, 0.13, 0.14, 0.15, 0.40,
          0.42, 0.44, 0.50, 0.70, 0.85, 0.92, 0.96, 0.98, 0.995]
    grid(path, xs, ys, label)
