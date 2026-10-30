# Full-range ink profile of the two top boxes + Remember box on the ORIGINAL frame.
import numpy as np
from PIL import Image

O = np.asarray(Image.open("unique_slides/slide_004.jpg").convert("RGB")).astype(int)

def ranges(idx, counts, minc=2):
    out, start, prev = [], None, None
    for a, c in zip(idx, counts):
        if c >= minc:
            if start is None:
                start = a
            prev = a
        else:
            if start is not None:
                out.append((start, prev))
                start = None
    if start is not None:
        out.append((start, prev))
    return out

def scan(box, name):
    x0, y0, x1, y1 = box
    reg = O[y0:y1, x0:x1]
    masks = {
        "red": (reg[:, :, 0] > 150) & (reg[:, :, 1] < 110) & (reg[:, :, 2] < 110),
        "dark": reg.sum(axis=2) < 250,
        "blue": (reg[:, :, 2] > 130) & (reg[:, :, 0] < 120),
    }
    print("\n=== " + name + "  " + str(box) + " ===")
    for k, m in masks.items():
        rsum = m.sum(axis=1); csum = m.sum(axis=0)
        R = ranges(np.arange(y0, y1), rsum)
        C = ranges(np.arange(x0, x1), csum)
        if R:
            print("  %s ROWS: %s" % (k, [(int(a), int(b), int(rsum[a - y0:b - y0 + 1].sum())) for a, b in R]))
        if C:
            print("  %s COLS: %s" % (k, [(int(a), int(b), int(csum[a - x0:b - x0 + 1].sum())) for a, b in C]))

scan((80, 99, 395, 222), "LEFT Original Labels")
scan((427, 99, 745, 222), "RIGHT Predicted Labels")
scan((784, 100, 880, 152), "REMEMBER")
