import sys
import numpy as np
from PIL import Image
from scipy import ndimage

def components(path, hexv, tol=18, min_area=400):
    a = np.array(Image.open(path).convert("RGB")).astype(int)
    c = np.array([int(hexv[i:i+2], 16) for i in (0, 2, 4)])
    m = (np.abs(a - c).max(axis=2) <= tol)
    lab, n = ndimage.label(m)
    out = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(xs) < min_area:
            continue
        out.append((len(xs), xs.min(), ys.min(), xs.max(), ys.max()))
    out.sort(reverse=True)
    h, w = a.shape[:2]
    print(f"# {path} {w}x{h} color={hexv} tol={tol} comps={len(out)}")
    for area, x0, y0, x1, y1 in out[:14]:
        print(f"   area={area:7d} bbox=({x0},{y0})-({x1},{y1}) "
              f"frac=({x0/w:.3f},{y0/h:.3f})-({x1/w:.3f},{y1/h:.3f})")

if __name__ == "__main__":
    components(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 18,
               int(sys.argv[4]) if len(sys.argv) > 4 else 400)
