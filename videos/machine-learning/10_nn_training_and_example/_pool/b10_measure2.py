import sys
import numpy as np
from PIL import Image

def load(path):
    return np.array(Image.open(path).convert("RGB")).astype(int)

def mask_close(a, hexv, tol=12):
    c = np.array([int(hexv[i:i+2], 16) for i in (0, 2, 4)])
    return (np.abs(a - c).max(axis=2) <= tol)

def bbox(m):
    ys, xs = np.where(m)
    if len(xs) == 0:
        return None
    return xs.min(), ys.min(), xs.max(), ys.max()

def report(path, label, specs, size_div=None):
    a = load(path)
    h, w = a.shape[:2]
    print(f"--- {label} {path} size=({w},{h})")
    for name, hexv, tol in specs:
        m = mask_close(a, hexv, tol)
        bb = bbox(m)
        n = int(m.sum())
        if bb is None:
            print(f"  {name:22s} {hexv}: none")
        else:
            x0, y0, x1, y1 = bb
            print(f"  {name:22s} {hexv}: n={n:7d} frac=({x0/w:.3f},{y0/h:.3f})-({x1/w:.3f},{y1/h:.3f})")

if __name__ == "__main__":
    path, label = sys.argv[1], sys.argv[2]
    specs = [
        ("cyan_fill", "D9F2F2", 10),
        ("tan_fill", "D8CEC0", 10),
        ("magenta", "CC00CC", 40),
        ("darkblue", "1F4E79", 25),
        ("red_C00000", "C00000", 30),
        ("orange_ED7D31", "ED7D31", 25),
        ("green_008000", "008000", 30),
        ("green_70AD47", "70AD47", 25),
        ("blue_4472C4", "4472C4", 25),
        ("yellow_FFC000", "FFC000", 25),
        ("badge_FFF9C4", "FFF9C4", 10),
        ("frame_C00000_hi", "C00000", 30),
    ]
    report(path, label, specs)
