import sys
import numpy as np
from PIL import Image

def load(path):
    im = Image.open(path).convert("RGB")
    return np.array(im), im.size

def mask_close(a, hexv, tol=28):
    c = np.array([int(hexv[i:i+2], 16) for i in (0, 2, 4)])
    d = np.abs(a.astype(int) - c).sum(axis=2)
    return d < tol * 3

def bbox(m):
    ys, xs = np.where(m)
    if len(xs) == 0:
        return None
    return xs.min(), ys.min(), xs.max(), ys.max()

def report(path, label, specs):
    a, size = load(path)
    print(f"--- {label} {path} size={size}")
    for name, hexv, tol in specs:
        m = mask_close(a, hexv, tol)
        bb = bbox(m)
        n = int(m.sum())
        if bb is None:
            print(f"  {name:22s} {hexv}: none")
        else:
            x0, y0, x1, y1 = bb
            print(f"  {name:22s} {hexv}: n={n:7d} px bbox=({x0},{y0})-({x1},{y1}) "
                  f"frac=({x0/size[0]:.3f},{y0/size[1]:.3f})-({x1/size[0]:.3f},{y1/size[1]:.3f})")

if __name__ == "__main__":
    path, label = sys.argv[1], sys.argv[2]
    specs = [
        ("cyan_fill", "D9F2F2", 30),
        ("cyan_border", "2E5C8A", 30),
        ("tan_fill", "D8CEC0", 30),
        ("magenta", "CC00CC", 45),
        ("darkblue", "1F4E79", 35),
        ("red_bar", "C00000", 35),
        ("orange", "ED7D31", 30),
        ("green", "008000", 35),
    ]
    report(path, label, specs)
