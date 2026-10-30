"""Comprehensive geometry measurement of slide_028 original content."""
import numpy as np
from PIL import Image
from scipy import ndimage

o = np.asarray(Image.open("../../unique_slides/slide_028.jpg").convert("RGB")).astype(int)
X0, X1, Y0, Y1 = 56, 907, 42, 540
SL = o[Y0:Y1, X0:X1]
h, w, _ = SL.shape
r, g, b = SL[..., 0], SL[..., 1], SL[..., 2]
mx = SL.max(axis=2); mn = SL.min(axis=2); sat = mx - mn

def show(name, mask, minpx=40):
    lab, n = ndimage.label(mask)
    sizes = ndimage.sum(mask, lab, range(1, n + 1))
    rows = []
    for i in range(1, n + 1):
        if sizes[i - 1] >= minpx:
            ys, xs = np.nonzero(lab == i)
            cy, cx = int(ys.mean()), int(xs.mean())
            rows.append((len(ys), xs.min(), xs.max(), ys.min(), ys.max(), cx, cy))
    rows.sort(key=lambda t: (t[5], t[6]))
    print("=== %s (%d comps >= %d px) ===" % (name, len(rows), minpx))
    for npx, x0, x1, y0, y1, cx, cy in rows:
        print("  n=%5d x %3d..%3d y %3d..%3d  c(%3d,%3d)" % (npx, x0, x1, y0, y1, cx, cy))
    return rows

# --- purple: input dots + input/target boxes
show("PURPLE", (r > 100) & (b > 100) & (g < 120) & (sat > 40), 40)

# --- tan/beige panel
beige = (np.abs(r - 216) < 20) & (np.abs(g - 206) < 20) & (np.abs(b - 194) < 22)
ys, xs = np.nonzero(beige)
print("BEIGE n=%d bbox x %d..%d y %d..%d" % (len(ys), xs.min(), xs.max(), ys.min(), ys.max()))
rows = beige.sum(axis=1); cols = beige.sum(axis=0)
print("  rows>100:", [(y, int(rows[y])) for y in range(h) if rows[y] > 100][:6], "...", [(y, int(rows[y])) for y in range(h) if rows[y] > 100][-6:])
print("  cols>100:", [(x, int(cols[x])) for x in range(w) if cols[x] > 100][:6], "...", [(x, int(cols[x])) for x in range(w) if cols[x] > 100][-6:])

# --- black bars (bottom)
show("BLACK<60", mx < 60, 200)

# --- light-colored boxes: sample bands at specific y rows
print("\n=== colour samples at probe points ===")
pts = {
  "InputSample box": (120, 100), "InputSample text": (120, 95),
  "neuron col1 circle": (360, 210), "neuron col2 circle": (590, 210),
  "neuron col3?": (660, 210),
  "class1 text": (800, 212), "class2 text": (800, 283), "class3 text": (800, 365),
  "error bar": (744, 250),
  "prev layer box": (60, 450), "current box": (250, 450), "next box": (430, 450),
  "ip bar": (60, 490), "hidden bar": (300, 490), "op bar": (790, 490),
  "output1 txt": (700, 212), "output2 txt": (700, 283), "output3 txt": (700, 365),
  "beige mid": (300, 330), "bg top": (300, 70),
}
for k, (x, y) in pts.items():
    print("  %-18s @(%3d,%3d) = %s" % (k, x, y, tuple(SL[y, x])))
