import sys
import numpy as np
from PIL import Image

def cellmap(path, cols=16, rows=9):
    a = np.array(Image.open(path).convert("RGB")).astype(int)
    h, w = a.shape[:2]
    print(f"# {path} {w}x{h} grid {cols}x{rows}")
    for r in range(rows):
        y0, y1 = int(r * h / rows), int((r + 1) * h / rows)
        line = []
        for c in range(cols):
            x0, x1 = int(c * w / cols), int((c + 1) * w / cols)
            blk = a[y0:y1, x0:x1].reshape(-1, 3)
            med = np.median(blk, axis=0).astype(int)
            line.append(f"{med[0]:02X}{med[1]:02X}{med[2]:02X}")
        print(f"  r{r} " + " ".join(line))

if __name__ == "__main__":
    cellmap(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 16,
            int(sys.argv[3]) if len(sys.argv) > 3 else 9)
