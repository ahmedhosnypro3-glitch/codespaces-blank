import sys
import numpy as np
from PIL import Image

def find_panel(path, xr, yr, target="FFFFFF", tol=10):
    a = np.array(Image.open(path).convert("RGB")).astype(int)
    h, w = a.shape[:2]
    x0, x1 = int(xr[0] * w), int(xr[1] * w)
    y0, y1 = int(yr[0] * h), int(yr[1] * h)
    sub = a[y0:y1, x0:x1]
    t = np.array([int(target[i:i+2], 16) for i in (0, 2, 4)])
    m = (np.abs(sub - t).max(axis=2) <= tol)
    ys, xs = np.where(m)
    if len(xs) == 0:
        print("no white found"); return
    print(f"white bbox in window: x {x0+xs.min()}-{x0+xs.max()} y {y0+ys.min()}-{y0+ys.max()}"
          f" frac x {(x0+xs.min())/w:.3f}-{(x0+xs.max())/w:.3f} y {(y0+ys.min())/h:.3f}-{(y0+ys.max())/h:.3f}")

if __name__ == "__main__":
    p = sys.argv[1]
    find_panel(p, (float(sys.argv[2]), float(sys.argv[3])), (float(sys.argv[4]), float(sys.argv[5])),
               sys.argv[6] if len(sys.argv) > 6 else "FFFFFF")
