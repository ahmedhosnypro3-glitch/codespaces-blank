"""Targeted geometry of slide_028 elements."""
import numpy as np
from PIL import Image
from scipy import ndimage

o = np.asarray(Image.open("../../unique_slides/slide_028.jpg").convert("RGB")).astype(int)
X0, Y0 = 56, 42
SL = o[Y0:540, X0:907]
h, w, _ = SL.shape
r, g, b = SL[..., 0], SL[..., 1], SL[..., 2]
mx = SL.max(axis=2); mn = SL.min(axis=2); sat = mx - mn

def F(x0, x1, y0, y1):
    """content bbox -> frame bbox"""
    return (x0 + X0, x1 + X0, y0 + Y0, y1 + Y0)

def rep(name, mask, minpx=30, limit=40):
    lab, n = ndimage.label(mask)
    sizes = ndimage.sum(mask, lab, range(1, n + 1))
    out = []
    for i in range(1, n + 1):
        if sizes[i - 1] >= minpx:
            ys, xs = np.nonzero(lab == i)
            out.append((len(ys), int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())))
    out.sort(key=lambda t: (t[3], t[1]))
    print("=== %s (%d) ===" % (name, len(out)))
    for npx, x0, x1, y0, y1 in out[:limit]:
        fx0, fx1, fy0, fy1 = F(x0, x1, y0, y1)
        print("  n=%5d frame x %3d..%3d y %3d..%3d  (%dx%d)" % (npx, fx0, fx1, fy0, fy1, x1 - x0 + 1, y1 - y0 + 1))

# 1. TAN PANEL: beige, but exclude JPEG noise -> smooth with 5x5 mean
beige = ((np.abs(r - 216) < 22) & (np.abs(g - 206) < 22) & (np.abs(b - 194) < 24)).astype(float)
sm = ndimage.uniform_filter(beige, 13)
tp = sm > 0.55
lab, n = ndimage.label(tp)
sizes = ndimage.sum(tp, lab, range(1, n + 1))
big = [(i + 1, int(sizes[i])) for i in range(n) if sizes[i] > 2000]
print("=== TAN PANEL candidates ===")
for i, s in sorted(big, key=lambda t: -t[1]):
    ys, xs = np.nonzero(lab == i)
    print("  n=%6d frame x %3d..%3d y %3d..%3d" % (s, xs.min() + X0, xs.max() + X0, ys.min() + Y0, ys.max() + Y0))

# 2. Light boxes (annotation + class + legend): color != bg(231,233,230) and not black, not tan
boxish = (np.abs(SL - np.array([231, 233, 230])).max(axis=2) > 12) & (mx > 110) & (~beige.astype(bool))
print("\n=== LIGHT BOX comps (>=800px) ===")
lab, n = ndimage.label(boxish)
sizes = ndimage.sum(boxish, lab, range(1, n + 1))
out = []
for i in range(1, n + 1):
    if sizes[i - 1] >= 800:
        ys, xs = np.nonzero(lab == i)
        out.append((int(sizes[i - 1]), int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())))
out.sort(key=lambda t: (t[3], t[1]))
for s, x0, x1, y0, y1 in out:
    fx0, fx1, fy0, fy1 = F(x0, x1, y0, y1)
    mid = SL[(y0 + y1) // 2, (x0 + x1) // 2]
    print("  n=%6d frame x %3d..%3d y %3d..%3d (%3dx%3d) mid=%s" % (s, fx0, fx1, fy0, fy1, x1 - x0 + 1, y1 - y0 + 1, tuple(mid)))

# 3. vertical dark-red bar
vr = (r > 110) & (g < 60) & (b < 60)
print("\n=== VERTICAL RED BAR ===")
lab, n = ndimage.label(vr)
sizes = ndimage.sum(vr, lab, range(1, n + 1))
out = [(int(sizes[i]), i) for i in range(n) if sizes[i] > 500]
for s, i in sorted(out, key=lambda t: -t[0]):
    ys, xs = np.nonzero(lab == i)
    print("  n=%6d frame x %3d..%3d y %3d..%3d" % (s, xs.min() + X0, xs.max() + X0, ys.min() + Y0, ys.max() + Y0))
print("  sample colour:", tuple(SL[200, 745]), tuple(SL[250, 755]))

# 4. row profile of ink to find text bands
ink = (np.abs(SL - np.array([231, 233, 230])).max(axis=2) > 18) | (np.abs(SL - np.array([254, 255, 253])).max(axis=2) > 18)
rows = ink.sum(axis=1)
print("\n=== INK ROW BANDS (frame y) ===")
st = None
for y in range(h):
    if rows[y] > 3 and st is None: st = y
    elif rows[y] <= 3 and st is not None:
        print("  frame y %3d..%3d  maxink %d" % (st + Y0, y - 1 + Y0, rows[st:y].max()))
        st = None
if st is not None:
    print("  frame y %3d..%3d" % (st + Y0, h - 1 + Y0))

# 5. column profile
cols = ink.sum(axis=0)
print("\n=== INK COL BANDS (frame x) ===")
st = None
for x in range(w):
    if cols[x] > 3 and st is None: st = x
    elif cols[x] <= 3 and st is not None:
        print("  frame x %3d..%3d  maxink %d" % (st + X0, x - 1 + X0, cols[st:x].max()))
        st = None
if st is not None:
    print("  frame x %3d..%3d" % (st + X0, w - 1 + X0))
